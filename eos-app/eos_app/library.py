"""The shared library: the Author's pools, read by the components that draw on them (requirements v0.13, FR-LIB, D20).

Built to the Author's own vault structure (Obsidian Vault\\Writing EOS):
- Character Pool: one card per character (`CHAR-### Name.md`), a few fields in the frontmatter and the rest as
  `**field:** value` lines in sections A to K; status follows the vault's Controlled Vocabulary.
- Pen Names Pool: subgenre rows, each naming a pen name with its literary style, tones, themes, cinematic, trailer
  and cover style and palette; a pen name is the set of rows that name it, plus its own short note.
- Narrative Genres Pool: one note per minor subgenre with its definition and concepts.
- Story Pitch Pool: writing topics, each classified by the pitch type it serves; doctrine topics feed the Story Bible.
- Content Levels: spice, violence and swearing (0 to 5) for each subgenre; they set the book's ceiling and decide
  which scenes go to the mature tier.
- Conflict and Structure Map: for each conflict core and modifier value, the plot structures that fit best or
  situationally.
- Character Arc and Theme: one entry per character (theme, basics, relationships, arc), written by the app at the
  arc gate and kept by the Author.

The library lives beside the projects (`<projects root>/library/`) and stays Obsidian Markdown. Import copies notes
byte for byte and never changes the vault; older copies in Archive folders are skipped. Code enforces the rules:
pool before creation (P4), only offerable statuses are offered, entries are written only with the Author's approval,
private fields never reach a model, and models get a style's description rather than the people it names.
"""

from __future__ import annotations

import copy
import csv
import fnmatch
import hashlib
import io
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import office

MAP_PATH = Path(__file__).resolve().parent.parent / "config" / "library_map.yaml"
_FM = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)
_BOLD = re.compile(r"^\*\*([^*\n]{1,60}?):\*\*[ \t]*(.*?)\s*$", re.M)


class LibraryError(ValueError):
    """A library note, folder or write is not usable."""


class PoolFirstError(RuntimeError):
    """A character was about to be created before the Character Pool was searched (P4)."""


@dataclass(frozen=True)
class LibraryMap:
    version: str
    root: str
    exclude: list
    send_named_influences: bool
    pools: dict


@dataclass(frozen=True)
class Approval:
    gate: str
    by: str


def load_map(path=MAP_PATH) -> LibraryMap:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return LibraryMap(raw["version"], raw["root"], raw.get("exclude", []), bool(raw.get("send_named_influences")),
                      raw["pools"])


def _pool(lmap: LibraryMap, pool: str) -> dict:
    if pool not in lmap.pools:
        raise LibraryError(f"unknown pool {pool!r}; the library has {', '.join(lmap.pools)}")
    return lmap.pools[pool]


def _key(name) -> str:
    return re.sub(r"[\s_\-]+", "", str(name)).lower()


def _snake(name) -> str:
    return re.sub(r"[\s\-]+", "_", str(name).strip()).lower()


def _slug(text) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def parse_note(text: str):
    """Split a note into (frontmatter dict, body). A note with no frontmatter has an empty dict."""
    m = _FM.match(text)
    if not m:
        return {}, text.strip()
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise LibraryError(f"the frontmatter is not valid YAML: {str(e).splitlines()[0]}") from None
    if not isinstance(fm, dict):
        raise LibraryError("the frontmatter is not a list of fields")
    return fm, text[m.end():].strip()


def body_fields(body: str) -> dict:
    """The card's `**field:** value` lines. The first occurrence of a field wins."""
    out = {}
    for k, v in _BOLD.findall(body):
        out.setdefault(k.strip(), v.strip())
    return out


def _blank(v) -> bool:
    """Missing or empty; a level of 0 is a value."""
    return v is None or v == [] or (isinstance(v, str) and not v.strip())


def _sections(body: str) -> dict:
    out, cur, buf = {}, None, []
    for line in body.splitlines():
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = h.group(1), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def _heading(body: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    return m.group(1) if m else fallback


def _map_keys(raw: dict, cfg: dict) -> dict:
    """Translate field names: aliases first, otherwise the field's own name in snake_case."""
    aliases = {_key(a): t for a, t in (cfg.get("aliases") or {}).items()}
    out = {}
    for k, v in raw.items():
        name = aliases.get(_key(k), _snake(k))
        out.setdefault(name, v.strip() if isinstance(v, str) else v)
    return out


def _skip_dir(part: str, lmap: LibraryMap) -> bool:
    return part.startswith(".") or any(fnmatch.fnmatch(part, pat) for pat in lmap.exclude)


def _notes(folder: Path, lmap: LibraryMap):
    for f in sorted(folder.rglob("*.md")) if folder.is_dir() else []:
        if not any(_skip_dir(p, lmap) for p in f.relative_to(folder).parts[:-1]):
            yield f


# ---------- import ----------

@dataclass
class ImportReport:
    imported: list = field(default_factory=list)      # new to the library
    updated: list = field(default_factory=list)       # changed in the vault only, so the library copy was refreshed
    unchanged: list = field(default_factory=list)
    conflicts: list = field(default_factory=list)     # the library copy was edited too: left for the Author
    skipped: list = field(default_factory=list)
    problems: list = field(default_factory=list)
    missing_in_vault: list = field(default_factory=list)   # in the library but no longer in the vault: never deleted


BASELINE = ".import-baseline.json"     # per pool folder: the fingerprint of each note as last copied from the vault


def _fingerprint(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_path(vault_root, cfg: dict):
    """Where a pool lives in the vault: its folder, or for a spreadsheet pool, its files (in its folder, if it has one)."""
    if cfg.get("tables"):
        return [Path(vault_root) / cfg.get("source_folder", "") / name for name in cfg["tables"]]
    return Path(vault_root) / cfg["source_folder"]


def import_folder(src, pool: str, library_root, lmap: LibraryMap, overwrite=False) -> ImportReport:
    """Copy a vault folder's notes (or a pool's spreadsheet) into the library, byte for byte. The vault is never
    changed. When a folder is walked, hidden folders (Obsidian's settings) and Archive copies are skipped; a file the
    map names is read wherever it is, a plugin's hidden data folder included. The library remembers each file as it
    was last copied, so a file changed only in the vault is refreshed, while one whose library copy was edited too is
    a conflict, left alone unless overwrite is set. A library file gone from the vault is reported, never deleted."""
    cfg = _pool(lmap, pool)
    dest = Path(library_root) / cfg["folder"]
    if isinstance(src, (list, tuple)):                           # a spreadsheet pool: its files, side by side
        missing = [str(p) for p in map(Path, src) if not p.is_file()]
        if missing:
            raise LibraryError(f"no file at {', '.join(missing)}")
        src = [Path(p) for p in src]
        root, found = None, src
    elif (src := Path(src)).is_file():
        root, found = src.parent, [src]
    elif src.is_dir():
        root, found = src, sorted(p for p in src.rglob("*") if p.is_file())
    else:
        raise LibraryError(f"no folder or file at {src}")
    types = [t.lower() for t in cfg.get("file_types", [".md"])]
    base_path = dest / BASELINE
    base = json.loads(base_path.read_text(encoding="utf-8")) if base_path.exists() else {}
    seen, rep = set(), ImportReport()
    for f in found:
        parts = (f.name,) if root is None else f.relative_to(root).parts      # named files land flat in the pool folder
        if root is not None and (any(_skip_dir(p, lmap) for p in parts[:-1]) or parts[-1].startswith(".")):
            continue
        rel = "/".join(parts)
        if f.suffix.lower() not in types:
            rep.skipped.append(rel)
            continue
        data = f.read_bytes()
        try:
            if f.suffix.lower() in (".md", ".csv", ".txt"):          # spreadsheets and Word files are binary
                text = data.decode("utf-8-sig")
                if f.suffix.lower() == ".md":
                    parse_note(text)
        except (LibraryError, UnicodeDecodeError) as e:
            rep.problems.append(f"{rel}: {e}")
        target, seen = dest / rel, seen | {rel}
        if target.exists():
            held = target.read_bytes()
            if held == data:
                base[rel] = _fingerprint(data)
                rep.unchanged.append(rel)
                continue
            if base.get(rel) != _fingerprint(held) and not overwrite:
                rep.conflicts.append(rel)                        # edited in the library since the last copy
                continue
            rep.updated.append(rel)
        else:
            rep.imported.append(rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        base[rel] = _fingerprint(data)
    new = cfg.get("new_folder")
    for f in sorted(p for p in dest.rglob("*") if p.suffix.lower() in types) if dest.is_dir() else []:
        rel = f.relative_to(dest).as_posix()
        if rel not in seen and not (new and rel.startswith(new + "/")):
            rep.missing_in_vault.append(rel)
    if base:
        dest.mkdir(parents=True, exist_ok=True)
        base_path.write_text(json.dumps(base, indent=0, sort_keys=True, ensure_ascii=False), encoding="utf-8")
    return rep


# ---------- reading ----------

@dataclass
class Entry:
    pool: str
    id: str
    title: str
    fields: dict
    private: dict
    body: str
    sections: dict
    path: Path
    missing: list
    config: dict = field(repr=False, default_factory=dict)

    @property
    def status(self):
        return self.fields.get("status")

    def offered_to(self, project: str) -> bool:
        """Whether a component may offer this entry to a project (Controlled Vocabulary statuses)."""
        if self.missing:
            return False
        cfg = self.config
        if "offer_statuses" not in cfg:
            return True
        if self.status in cfg["offer_statuses"]:
            return True
        if self.status in cfg.get("project_statuses", []):
            used = str(self.fields.get(cfg.get("project_field", ""), "")).lower()
            return bool(project) and str(project).lower() in used
        return False

    def core(self) -> dict:
        return {k: v for k, v in self.fields.items() if k in self.config.get("core", [])}

    def skin(self) -> dict:
        return {k: v for k, v in self.fields.items() if k in self.config.get("skin", [])}


@dataclass
class Pool:
    name: str
    entries: list
    problems: list
    ignored: int
    by_title: dict
    by_id: dict


def _matches_filter(fm: dict, flt: dict) -> bool:
    if not flt:
        return True
    if "has_field" in flt:
        return flt["has_field"] in fm
    return fm.get(flt["field"]) in flt["values"]


def _read_cards(pool, cfg, folder, lmap):
    entries, problems, ignored = [], [], 0
    for f in _notes(folder, lmap):
        rel = f.relative_to(folder).as_posix()
        try:
            fm, body = parse_note(f.read_text(encoding="utf-8"))
        except (LibraryError, UnicodeDecodeError) as e:
            problems.append(f"{rel}: {e}")
            continue
        if not _matches_filter(fm, cfg.get("note_filter")) or \
                any(fnmatch.fnmatch(f.stem, pat) for pat in cfg.get("exclude_notes", [])):
            ignored += 1
            continue
        raw = dict(body_fields(body)) if cfg.get("body_fields") else {}
        raw.update(fm)                                           # frontmatter wins over the body
        fields = _map_keys(raw, cfg)
        sections = _sections(body)
        for sec, name in (cfg.get("sections_as_fields") or {}).items():
            if sections.get(sec):
                fields.setdefault(name, sections[sec])
        title = str(fields.get(cfg.get("title_field", "name")) or _heading(body, f.stem))
        fields.setdefault("title", title)
        private = {k: fields.pop(k) for k in list(fields) if k in cfg.get("private", [])}
        if cfg.get("id_field") and fields.get(cfg["id_field"]):
            eid = str(fields[cfg["id_field"]])
        elif cfg.get("id_from"):
            eid = cfg["id_prefix"] + "-" + "-".join(_slug(fields.get(k, "")) for k in cfg["id_from"])
        else:
            eid = f"{cfg['id_prefix']}-{_slug(f.stem)}"
        missing = [r for r in cfg.get("required", []) if _blank(fields.get(r))]
        label = f"{eid} ({f.name})" if cfg.get("id_field") else f.name
        if missing:
            problems.append(f"{label}: missing {', '.join(missing)}")
        for axis in cfg.get("axes", []):                         # content levels run 0 to 5
            v = fields.get(axis)
            if axis not in missing and not (isinstance(v, int) and 0 <= v <= 5):
                problems.append(f"{label}: {axis} is {v!r}, not a level from 0 to 5")
                missing.append(axis)
        st = fields.get("status")
        if cfg.get("status_values") and st is not None and st not in cfg["status_values"]:
            said = body_fields(body).get("status")
            hint = (f"; the card's body says {said!r}, so the frontmatter may have slipped a field"
                    if said in cfg["status_values"] else "")
            problems.append(f"{label}: status {st!r} is not in the Controlled Vocabulary{hint}")
        entries.append(Entry(pool, eid, title, fields, private, body, sections, f, missing, cfg))
    return entries, problems, ignored


_ENTRY = re.compile(r"^###\s+(.+?)\s*$", re.M)


def _read_pairings(pool, cfg, folder, lmap):
    rows_by, notes_by, others, problems, ignored, seen = {}, {}, [], [], 0, set()
    aliases_cfg = {"aliases": cfg.get("aliases") or {}}
    for f in _notes(folder, lmap):
        rel = f.relative_to(folder).as_posix()
        try:
            fm, body = parse_note(f.read_text(encoding="utf-8"))
        except (LibraryError, UnicodeDecodeError) as e:
            problems.append(f"{rel}: {e}")
            continue
        title = _heading(body, f.stem)
        if fm.get("type") in cfg["row_types"]:
            minor, base = title, _map_keys(fm, aliases_cfg)
            found = []
            if base.get(cfg["author_field"]):
                found.append(dict(base))
            else:                                                # one note, several entries (### blocks)
                blocks = _ENTRY.split(body)[1:]
                for head, text in zip(blocks[0::2], blocks[1::2]):
                    who = re.search(r"Author:\s*\[\[([^\]|]+)", text)
                    if not who:
                        continue
                    row = _map_keys(body_fields(text), aliases_cfg)
                    parts = [p.strip() for p in head.split("/")]
                    row.update({"primary_genre": base.get("primary_genre"), "secondary_genre": parts[0],
                                "major_subgenre": parts[1] if len(parts) > 1 else None,
                                cfg["author_field"]: who.group(1).strip()})
                    found.append(row)
            for row in found:
                author = str(row.pop(cfg["author_field"])).strip()
                keep = {k: row.get(k) for k in cfg["row_fields"] if row.get(k) not in (None, "")}
                keep["minor_subgenre"] = minor
                key = (author, minor, keep.get("secondary_genre"), keep.get("major_subgenre"))
                if key in seen:
                    continue
                seen.add(key)
                rows_by.setdefault(author, []).append(keep)
        elif not fm:
            others.append((f, title, body))
        else:
            ignored += 1
    for f, title, body in others:                                # a pen name's own note: in an Authors folder, or named after one
        if f.parent.name == cfg.get("author_folder") or title in rows_by:
            notes_by.setdefault(title, (f, body))
        else:
            ignored += 1
    entries = []
    for name in sorted(set(rows_by) | set(notes_by)):
        rows = sorted(rows_by.get(name, []), key=lambda r: (str(r.get("primary_genre")), r["minor_subgenre"],
                                                              str(r.get("secondary_genre")), str(r.get("major_subgenre"))))
        f, body = notes_by.get(name, (None, ""))
        if not rows:
            problems.append(f"{name}: a pen name note with no subgenre rows")
        fields = {"name": name, "rows": rows,
                  "primary_genres": sorted({str(r.get("primary_genre")) for r in rows if r.get("primary_genre")})}
        entries.append(Entry(pool, f"{cfg['id_prefix']}-{_slug(name)}", name, fields, {}, body, _sections(body),
                             f, [], cfg))
    return entries, problems, ignored


def _read_csv(pool, cfg, folder, lmap):
    """One entry per row of the first spreadsheet; the other spreadsheets add their columns to the same rows, matched
    by name. Fit columns become lists of genre terms. Any row that doesn't line up across the spreadsheets, and any
    partner that isn't in the list, is a problem."""
    entries, problems = [], []
    lists = set(cfg.get("fit_columns", {})) | set(cfg.get("list_fields", []))
    title_field = cfg.get("title_field", "name")
    by_key, first = {}, True
    for source, table in cfg["tables"].items():
        name = Path(source).name
        f = folder / name
        if not f.is_file():
            problems.append(f"{name}: not in the library; import it from the vault")
            first = False
            continue
        seen = set()
        for n, row in enumerate(csv.DictReader(io.StringIO(f.read_text(encoding="utf-8-sig"))), start=2):
            title = (row.get(table["key"]) or "").strip()
            key = _name_key(title)
            if not title:
                problems.append(f"{name} row {n}: no theme named")
                continue
            if key in seen:
                problems.append(f"{name}: {title} is listed twice")
                continue
            seen.add(key)
            cols = table["columns"] if isinstance(table["columns"], dict) else {c: c for c in table["columns"]}
            extra = {nm: (_genre_terms(row.get(col), cfg) if nm in lists else (row.get(col) or "").strip())
                     for col, nm in cols.items()}
            if table.get("group"):                                 # a sheet kept together, e.g. one worldbuilding approach
                extra = {table["group"]: {col: v for col, v in zip(table["columns"], extra.values())}}
            if first:
                fields = {title_field: title, "title": title, **extra}
                eid = cfg["id_prefix"] + "-" + "-".join(_slug(fields.get(k, "")) for k in cfg["id_from"])
                by_key[key] = Entry(pool, eid, title, fields, {}, "", {}, f, [], cfg)
                entries.append(by_key[key])
            elif key in by_key:
                by_key[key].fields.update(extra)
            else:
                problems.append(f"{name}: {title} isn't in {Path(next(iter(cfg['tables']))).name}")
        if not first:
            for k, e in by_key.items():
                if k not in seen:
                    problems.append(f"{name}: has no row for {e.title}")
        first = False
    partner = cfg.get("partner_field")
    for e in entries:
        e.missing[:] = [r for r in cfg.get("required", []) if _blank(e.fields.get(r))]
        if e.missing:
            problems.append(f"{e.title}: missing {', '.join(e.missing)}")
        kind = cfg.get("type_field")
        if kind and e.fields.get(kind) and e.fields[kind] not in cfg.get("type_values", []):
            problems.append(f"{e.title}: theme type {e.fields[kind]!r} is not one of {', '.join(cfg['type_values'])}")
        p = e.fields.get(partner) if partner else None
        if p and _name_key(p) not in by_key:
            problems.append(f"{e.title}: its {partner.replace('_', ' ')} {p!r} isn't in the list")
    return entries, problems, 0


def _office_files(cfg, folder, problems) -> dict:
    """{name the map gives: library path} for a pool kept as named Office files; a missing one is a problem."""
    out = {}
    for name in cfg["tables"]:
        f = folder / Path(name).name
        if f.is_file():
            out[name] = f
        else:
            problems.append(f"{Path(name).name}: not in the library; import it from the vault")
    return out


def _read_word_lists(pool, cfg, folder, lmap):
    """One entry per word on the sheets the map names: the words run down column A, below an optional header. Each
    sheet gives its words a kind (trait or strength; an epithet's descriptor, noun or domain). A synonyms sheet adds
    synonyms (columns B onward) to words already listed; a word there that isn't in the list is a problem."""
    entries, problems, seen = [], [], {}
    kind_field = cfg.get("kind_field", "kind")
    for name, f in _office_files(cfg, folder, problems).items():
        try:
            book = office.read_xlsx(f)
        except office.OfficeError as e:
            problems.append(str(e))
            continue
        sheets = cfg["tables"][name]["sheets"]
        for sheet, spec in sheets.items():
            if sheet not in book:
                problems.append(f"{f.name}: no sheet named {sheet!r}")
                continue
            if spec.get("synonyms"):
                continue
            header = _name_key(spec.get("header", ""))
            for row in book[sheet]:
                word = (row.get("A") or "").strip()
                if not word or (header and _name_key(word) == header):
                    continue
                key = (spec["kind"], word.lower())
                if key in seen:
                    problems.append(f"{f.name} · {sheet}: {word} is listed twice")
                    continue
                fields = {"name": word, "title": word, kind_field: spec["kind"]}
                seen[key] = Entry(pool, f"{cfg['id_prefix']}-{_slug(spec['kind'])}-{_slug(word)}", word, fields, {},
                                  "", {}, f, [], cfg)
                entries.append(seen[key])
        for sheet, spec in sheets.items():
            if not spec.get("synonyms") or sheet not in book:
                continue
            for row in book[sheet]:
                values = [row[c].strip() for c in sorted(row, key=lambda c: (len(c), c)) if row[c].strip()]
                if len(values) < 2:
                    continue                                       # the sheet's title row
                e = seen.get((spec["kind"], values[0].lower()))
                if e is None:
                    problems.append(f"{f.name} · {sheet}: {values[0]} has synonyms but isn't in the {spec['kind']} list")
                    continue
                e.fields["synonyms"] = values[1:]
    return entries, problems, 0


def _read_grouped(pool, cfg, folder, lmap):
    """One entry per group on a sheet: a name in column A starts a group, and the rows below it, until the next name,
    fill its list columns (an animal nature and its strengths and weaknesses)."""
    entries, problems = [], []
    for name, f in _office_files(cfg, folder, problems).items():
        spec = cfg["tables"][name]
        try:
            rows = office.read_xlsx(f).get(spec["sheet"])
        except office.OfficeError as e:
            problems.append(str(e))
            continue
        if rows is None:
            problems.append(f"{f.name}: no sheet named {spec['sheet']!r}")
            continue
        current = None
        for n, row in enumerate(rows, start=1):
            if n <= spec.get("header_rows", 1):
                continue
            head = (row.get("A") or "").strip()
            if head:
                fields = {"name": head, "title": head, **{v: [] for v in spec["columns"].values()}}
                current = Entry(pool, f"{cfg['id_prefix']}-{_slug(head)}", head, fields, {}, "", {}, f, [], cfg)
                entries.append(current)
            elif current is None and any(row.get(c) for c in spec["columns"]):
                problems.append(f"{f.name} row {n}: values before any {cfg.get('group_word', 'name')}")
                continue
            for col, fld in spec["columns"].items():
                v = (row.get(col) or "").strip()
                if v and current is not None:
                    current.fields[fld].append(v)
    for e in entries:
        e.missing[:] = [r for r in cfg.get("required", []) if not e.fields.get(r)]
        if e.missing:
            problems.append(f"{e.title}: missing {', '.join(e.missing)}")
    return entries, problems, 0


def _read_doc_sections(pool, cfg, folder, lmap):
    """One entry per section of a Word document; sections are separated by two or more empty paragraphs. A section is
    titled by its opening sentence and keeps its text as written."""
    entries, problems = [], []
    gap = cfg.get("section_gap", 2)
    for name, f in _office_files(cfg, folder, problems).items():
        try:
            paras = office.read_docx(f)
        except office.OfficeError as e:
            problems.append(str(e))
            continue
        blocks, cur, blanks = [], [], 0
        for p in paras:
            if not p.strip():
                blanks += 1
                continue
            if blanks >= gap and cur:
                blocks.append(cur)
                cur = []
            blanks = 0
            cur.append(p.rstrip())
        if cur:
            blocks.append(cur)
        for i, block in enumerate(blocks, start=1):
            first = re.sub(r"[*#]+", "", block[0]).strip()
            title = re.split(r"(?<=[.!?:])\s", first)[0][:100].rstrip(":")
            fields = {"title": title, "section": i}
            entries.append(Entry(pool, f"{cfg['id_prefix']}-{i:02d}", title, fields, {}, "\n".join(block), {}, f, [], cfg))
    return entries, problems, 0


def _name_key(text) -> str:
    """A name with case, spacing, hyphens and simple plurals set aside: 'Small-Town Romances' -> 'small town romance'."""
    def word(w):
        if w.endswith("ies") and len(w) > 4:
            return w[:-3] + "y"
        return w[:-1] if w.endswith("s") and not w.endswith("ss") and len(w) > 3 else w
    return " ".join(word(w) for w in re.findall(r"[a-z0-9]+", str(text).lower()))


def near_duplicates(entries, scope: str | None) -> list:
    """Groups of entries whose names differ only in case, spacing, hyphens or a plural, within the same scope field
    (for genres, the primary genre: a YA entry may share a name with a Literary Fiction one by design)."""
    groups = {}
    for e in entries:
        groups.setdefault((str(e.fields.get(scope, "")) if scope else "", _name_key(e.title)), []).append(e)
    return [g for g in groups.values() if len({e.title for e in g}) > 1]


def load_pool(pool: str, library_root, lmap: LibraryMap) -> Pool:
    cfg = _pool(lmap, pool)
    folder = Path(library_root) / cfg["folder"]
    reader = {"pairings": _read_pairings, "csv": _read_csv, "word_lists": _read_word_lists, "grouped": _read_grouped,
              "doc_sections": _read_doc_sections}.get(cfg.get("reader"), _read_cards)
    entries, problems, ignored = reader(pool, cfg, folder, lmap)
    by_id = {}
    for e in entries:
        if e.id in by_id:
            problems.append(f"{e.id}: used by two notes ({by_id[e.id].path.name}, {e.path.name})")
        by_id.setdefault(e.id, e)
    if "near_duplicate_scope" in cfg:
        for group in near_duplicates(entries, cfg["near_duplicate_scope"]):
            if len({e.id for e in group}) == 1:
                continue                                         # already reported as one id used by two notes
            names = sorted({e.title for e in group})
            where = f" in {group[0].fields.get(cfg['near_duplicate_scope'])}" if cfg["near_duplicate_scope"] else ""
            problems.append(f"near-duplicate names{where}: {' / '.join(names)}; keep one spelling in your vault")
    return Pool(pool, entries, problems, ignored, {e.title: e for e in entries}, by_id)


# ---------- what the components ask of the pools ----------

def role_functions(entry: Entry) -> set:
    """The archetype positions an entry's role_in_story can fill (vault vocabulary -> Appendix C11)."""
    words = str(entry.fields.get(entry.config.get("role_field", "role_in_story"), "")).lower()
    out = set()
    for word, fns in (entry.config.get("role_functions") or {}).items():
        if re.search(r"\b" + re.escape(word) + r"\b", words):
            out |= set(fns)
    return out


def is_setting(entry: Entry) -> bool:
    """A setting card (a place or vessel written as a character): offered to Worldbuilding and Locations, never cast."""
    role = str(entry.fields.get(entry.config.get("role_field", "role_in_story"), "")).strip().lower()
    return any(role.startswith(w) for w in entry.config.get("setting_words", []))


def settings(pool: Pool) -> list:
    """The pool's places, for Worldbuilding and Locations: the pool before creation holds for places too."""
    return [e for e in pool.entries if is_setting(e)]


def unclassified(pool: Pool) -> list:
    """Characters whose role_in_story uses no word the map knows: they fill no position until the Author adds one.
    Setting cards are places, not characters, and are not counted."""
    return [e for e in pool.entries if not role_functions(e) and not is_setting(e)]


def candidates_for_role(pool: Pool, functions, project: str, include_unclassified=False) -> list:
    """Characters Character Pool Match may score for a role: complete, offerable to this project, and able to fill
    one of the functions. Best overlap first. Code filters; the model scores. With include_unclassified, characters
    whose role words the map doesn't know follow the matches, so a free-text role never hides a character."""
    want, out, rest = set(functions), [], []
    for e in pool.entries:
        if not e.offered_to(project) or is_setting(e):
            continue
        fns = role_functions(e)
        if want & fns:
            out.append((len(want & fns), e))
        elif include_unclassified and not fns:
            rest.append(e)
    return [e for _, e in sorted(out, key=lambda t: (-t[0], t[1].title))] + sorted(rest, key=lambda e: e.title)


def profile_gaps(profile: dict, lmap: LibraryMap) -> dict:
    """What a developed character still lacks before gate G5, and which Character Development stage owes each field.
    A pool card is only the launchpad: adaptation mode keeps its Core, regenerates its Skin for the book and fills
    every gap (age, appearance, voice and the rest), marked provisional with its source."""
    need = _pool(lmap, "characters").get("profile_required", {})
    return {k: stage for k, stage in need.items() if _blank(profile.get(k))}


def settled_open(card: dict) -> list:
    """What the Author has deliberately left open on a card ('SETTLED-OPEN'): completing the character must not fill
    these. Each paragraph of the card's notes that says so is returned, to go into the development stages' prompts."""
    notes = " ".join(str(v) for k, v in card.items() if "open_question" in k or k == "notes")
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", notes) if "settled-open" in s.lower()]


def skin_carried_over(profile: dict, card: dict, lmap: LibraryMap, kept=()) -> list:
    """Skin fields the developed profile copies word for word from the pool card. Adaptation regenerates the Skin for
    the book's world (a river-crossing origin does not survive into a space opera unexamined); a field may stay only
    when the Author keeps it, as with a name approved at G2."""
    skin = _pool(lmap, "characters").get("skin", [])
    return [k for k in skin if k not in kept and not _blank(profile.get(k))
            and str(profile.get(k)).strip() == str(card.get(k, "")).strip()]


def may_promote(profile: dict, lmap: LibraryMap, card: dict | None = None, kept=()) -> bool:
    """Gate G5 (roster and canon promotion) opens only for a complete profile, and, for a character adapted from the
    pool, only once its Skin has been regenerated for the book or the Author has kept each unchanged field."""
    gaps = profile_gaps(profile, lmap)
    if gaps:
        owed = "; ".join(f"{k} ({stage})" for k, stage in gaps.items())
        raise LibraryError(f"the character isn't complete yet: missing {owed}")
    if card is not None:
        same = skin_carried_over(profile, card, lmap, kept)
        if same:
            raise LibraryError(f"the Skin hasn't been regenerated for this book: {', '.join(same)} still read as on the "
                               f"pool card; regenerate them, or keep them with the Author's approval")
    return True


def may_create_character(pool_checked: bool, fit_found: bool) -> bool:
    """Pool before creation (P4): New Character runs only after Character Pool Match found no fit."""
    if not pool_checked:
        raise PoolFirstError("search the Character Pool before creating a character")
    if fit_found:
        raise PoolFirstError("the Character Pool has a fit for this role; pitch it instead of creating one")
    return True


def pen_names_for(pool: Pool, genre: str) -> list:
    """Pen names with at least one row in this genre (primary, secondary, major or minor subgenre)."""
    g = genre.strip().lower()
    hits = []
    for e in pool.entries:
        for r in e.fields.get("rows", []):
            if g in {str(r.get(k, "")).strip().lower() for k in ("primary_genre", "secondary_genre", "major_subgenre", "minor_subgenre")}:
                hits.append(e)
                break
    return sorted(hits, key=lambda e: e.title)


def descriptor(text: str) -> str:
    """A style without the people or works it names: 'Author A & B fusion — spare prose' -> 'spare prose'."""
    text = str(text)
    for sep in (" — ", " - "):
        if sep in text:
            return text.split(sep, 1)[1].strip()
    return text


def prompt_view(entry: Entry, lmap: LibraryMap) -> dict:
    """What a model may see of an entry: never the private fields; styles as descriptions unless the setting allows names."""
    view = copy.deepcopy(entry.fields)
    named = entry.config.get("named_influence_fields", [])
    if named and not lmap.send_named_influences:
        for r in view.get("rows", []):
            for k in named:
                if k in r:
                    r[k] = descriptor(r[k])
    return view


def byline_collisions(pen: Entry, characters: Pool) -> list:
    """(character, shared word) wherever a character's name shares a word with the byline (Naming Checks)."""
    words = {w for w in re.findall(r"[a-z]+", pen.title.lower()) if len(w) >= 3}
    return [(e.title, w) for e in characters.entries for w in sorted(words & set(re.findall(r"[a-z]+", e.title.lower())))]


def pools_used_by(step: str, lmap: LibraryMap) -> dict:
    """Which pools a component reads and writes (shown in the Engine view and checked by the router)."""
    return {"reads": [c["title"] for c in lmap.pools.values() if step in c.get("read_by", [])],
            "writes": [c["title"] for c in lmap.pools.values() if step in c.get("written_by", [])]}


# ---------- writing back ----------

def write_character(fields: dict, library_root, lmap: LibraryMap, approval: Approval | None) -> Path:
    """Pool Write (Character Development stage 12): a new character enters the pool only at gate G5.
    It lands in characters/new/ with the next id, ready for the Author to copy into the vault."""
    cfg = _pool(lmap, "characters")
    _require_gate(cfg, approval, "a character enters the pool only with your {} approval (roster and canon promotion)")
    missing = [r for r in cfg["required"] if _blank(fields.get(r))]
    if missing:
        raise LibraryError(f"the character is missing {', '.join(missing)}")
    pool = load_pool("characters", library_root, lmap)
    if fields["name"].lower() in {t.lower() for t in pool.by_title}:
        raise LibraryError(f"{fields['name']} is already in the pool")
    nums = [int(m.group(1)) for e in pool.entries if (m := re.fullmatch(rf"{cfg['id_prefix']}-(\d+)", e.id))]
    cid = f"{cfg['id_prefix']}-{(max(nums) if nums else 0) + 1:0{cfg.get('id_width', 3)}d}"
    data = {cfg["id_field"]: cid, "name": fields["name"], "status": cfg.get("new_status", "Ready to Pull")}
    data.update({k: v for k, v in fields.items() if k != "name"})
    folder = Path(library_root) / cfg["folder"] / cfg.get("new_folder", "new")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (cid + " " + re.sub(r'[<>:"/\\|?*]', "", fields["name"]).strip() + ".md")
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n\n# "
                    + fields["name"] + "\n", encoding="utf-8")
    return path


def _require_gate(cfg: dict, approval, message: str):
    if approval is None or approval.gate != cfg["write_gate"]:
        raise LibraryError(message.format(cfg["write_gate"]))


# ---------- Story Pitch Pool ----------

def pitches(pool: Pool) -> list:
    """Topics offered as story pitches: complete and not doctrine."""
    doctrine_types = pool.entries[0].config.get("doctrine_types", []) if pool.entries else []
    return [e for e in pool.entries if not e.missing and e.fields.get("pitch_type") not in doctrine_types]


def doctrine(pool: Pool) -> list:
    """Framework topics: the laws and systems other stories run on. They go to the Story Bible, not a pitch list."""
    doctrine_types = pool.entries[0].config.get("doctrine_types", []) if pool.entries else []
    return [e for e in pool.entries if not e.missing and e.fields.get("pitch_type") in doctrine_types]


# ---------- Content Levels ----------

@dataclass(frozen=True)
class SceneLevels:
    tier: str                 # standard | mature
    mature_axes: list         # axes at or above the mature level
    over_ceiling: list        # (axis, scene level, book ceiling)


def content_levels_for(pool: Pool, minor: str, secondary: str | None = None, major: str | None = None):
    """The suggested ceiling for a subgenre, or None when the mapping has none (nonfiction, poetry and drama forms):
    then the Author sets the levels at Story Setup. One subgenre can sit under several genre paths with different
    levels; without the path that picks one, the Author is asked rather than one being guessed."""
    def same(a, b):
        return str(a or "").strip().lower() == str(b or "").strip().lower()
    hits = [e for e in pool.entries if not e.missing and same(e.fields.get("minor_subgenre"), minor)
            and (secondary is None or same(e.fields.get("secondary_genre"), secondary))
            and (major is None or same(e.fields.get("major_subgenre"), major))]
    if len(hits) > 1:
        paths = "; ".join(f"{e.fields.get('secondary_genre')} › {e.fields.get('major_subgenre')}" for e in hits)
        raise LibraryError(f"{minor} has levels under {len(hits)} genre paths ({paths}); choose the book's path")
    return hits[0] if hits else None


def reviewed(entry: Entry) -> bool:
    """False while the levels are still the generated suggestion awaiting the Author's review."""
    cfg = entry.config
    return entry.fields.get(cfg.get("review_field")) not in cfg.get("unreviewed_values", [])


def describe_levels(levels: dict, lmap: LibraryMap) -> dict:
    """{'spice': '3 · sensual, closed door', ...} in the vault's own words."""
    cfg = _pool(lmap, "content_levels")
    return {a: f"{levels[a]} · {cfg['scale'][a][levels[a]]}" for a in cfg["axes"] if a in levels}


def mature_axes(levels: dict, lmap: LibraryMap) -> list:
    cfg = _pool(lmap, "content_levels")
    return [a for a in cfg["axes"] if levels.get(a, 0) >= cfg["mature_at"][a]]


def book_needs_mature_tier(ceiling: dict, lmap: LibraryMap) -> bool:
    """A book whose ceiling reaches a mature level needs a mature_ok model assigned before drafting (P10)."""
    return bool(mature_axes(ceiling, lmap))


def check_scene_levels(scene: dict, ceiling: dict, lmap: LibraryMap) -> SceneLevels:
    """Route a scene by its planned levels and flag any level above the book's ceiling. Code decides the tier;
    a scene over the ceiling goes to the Author, never silently through."""
    cfg = _pool(lmap, "content_levels")
    over = [(a, scene[a], ceiling[a]) for a in cfg["axes"] if a in scene and a in ceiling and scene[a] > ceiling[a]]
    hot = mature_axes(scene, lmap)
    return SceneLevels("mature" if hot else "standard", hot, over)


# ---------- Conflict and Structure Map ----------

@dataclass(frozen=True)
class StructureFit:
    structure: str
    core: str                 # best | situational | none
    best: int                 # modifier values for which it is a best fit
    situational: int
    matched: list             # (axis, value, best|situational)


def structure_map(pool: Pool) -> dict:
    """{structure: {(axis, value): 'best' | 'situational'}} from the map's notes."""
    out = {}
    for e in pool.entries:
        key = (e.fields["axis"], e.title)
        for s in e.fields.get("best_fit_plot_structures") or []:
            out.setdefault(s, {})[key] = "best"
        for s in e.fields.get("situational_fit") or []:
            out.setdefault(s, {}).setdefault(key, "situational")
    return out


def rank_structures(pool: Pool, story: dict) -> list:
    """Every structure the map fits to this story, the core first and the modifiers second (the map's own rule).
    story is {'Conflict Core': 'Internal', 'Intensity': 'Severe', 'Pillars': ['Belonging'], ...}.
    A shortlist for the Author beside the formula's six scored structures; the pick stays the Author's."""
    core_axis = pool.entries[0].config.get("core_axis", "Conflict Core") if pool.entries else "Conflict Core"
    wanted = {(axis, v) for axis, vals in story.items() for v in ([vals] if isinstance(vals, str) else vals)}
    rows = []
    for s, fits in structure_map(pool).items():
        matched = sorted((a, v, fits[(a, v)]) for (a, v) in wanted if (a, v) in fits)
        if not matched:
            continue
        core = next((how for a, _, how in matched if a == core_axis), "none")
        mods = [how for a, _, how in matched if a != core_axis]
        rows.append(StructureFit(s, core, mods.count("best"), mods.count("situational"), matched))
    rank = {"best": 2, "situational": 1, "none": 0}
    return sorted(rows, key=lambda r: (-rank[r.core], -r.best, -r.situational, r.structure))


# ---------- Character Arc and Theme ----------

def uncast_roles(relationships, library_root, lmap: LibraryMap) -> list:
    """Return channel R6: the relationships a developed character needs that name no cast character (a deputy, a
    rival). Character Profile's output is run through this; each one goes back to Cast Roles and Character Pool Match,
    so the role is filled from the pool before anyone new is created. The arc entry refuses them as a backstop."""
    pool = load_pool("characters", library_root, lmap)
    known = {_name_key(n) for e in pool.entries if not is_setting(e) for n in (e.title, e.path.stem)}
    target = lambda r: re.sub(r"^\[\[([^\]|]+)(\|[^\]]*)?\]\]$", r"\1", str(r).strip())
    return [r for r in relationships if _name_key(target(r)) not in known]


def write_arc_entry(fields: dict, project: str, library_root, lmap: LibraryMap, approval: Approval | None,
                    themes: Pool | None = None, lead: bool = False) -> Path:
    """One Character Arc and Theme entry, in the Author's template shape. Cast and Structure drafts it on the chosen
    structure's beats; the Story Bible Builder finishes it, where characters get their finishing build, and it is
    written only at the Author's Story Bible lock. With the Themes in Literature pool,
    the theme must be one of its themes and is written in its spelling; a lead character's arc (Hero or Shadow
    position) must carry a Canon theme. It lands in arc-and-theme/new/<project>/ for the Author to copy to the vault."""
    cfg = _pool(lmap, "arc_themes")
    _require_gate(cfg, approval, "an arc entry is written only with your approval of {}")
    missing = [r for r in cfg["required"] if _blank(fields.get(r))]
    if missing:
        raise LibraryError(f"the arc entry is missing {', '.join(missing)}")
    if themes is not None:
        known = {_name_key(e.title): e.title for e in themes.entries}
        theme = known.get(_name_key(fields["theme"]))
        if theme is None:
            raise LibraryError(f"{fields['theme']!r} isn't in your Themes in Literature list")
        entry = _theme(themes, theme)
        need = entry.config.get("lead_type", "Canon")
        if lead and _type(entry) != need:
            raise LibraryError(f"{theme} is a {_type(entry)} theme; a lead character's arc carries a {need} theme")
        fields = {**fields, "theme": theme}
    rel = fields.get("relationships")
    uncast = uncast_roles(rel, library_root, lmap) if isinstance(rel, (list, tuple)) else []
    if uncast:
        raise LibraryError(f"a relationship names no cast character: {'; '.join(map(str, uncast))}. Cast the role "
                           f"through Character Pool Match first (the pool before creation)")
    name = str(fields["character_name"]).strip()
    folder = Path(library_root) / cfg["folder"] / cfg.get("new_folder", "new") / re.sub(r'[<>:"/\\|?*]', "", project).strip()
    path = folder / (re.sub(r'[<>:"/\\|?*]', "", name).strip() + ".md")
    if path.exists():
        raise LibraryError(f"{name} already has an arc entry for {project}")

    def text(v):
        if isinstance(v, (list, tuple)):                         # related characters become wikilinks
            return "\n".join(f"- [[{x}]]" for x in v)
        return "" if v is None else str(v)

    data = {k: (fields.get(k) if not isinstance(fields.get(k), (list, tuple)) else list(fields[k]))
            for k in cfg["template"]}
    data["type"] = cfg["note_filter"]["values"][0]
    body = [f"# {name}", ""]
    for key, heading in cfg["sections"].items():
        body += [f"## {heading}", text(fields.get(key)), ""]
    folder.mkdir(parents=True, exist_ok=True)
    path.write_text("---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n\n"
                    + "\n".join(body).rstrip() + "\n", encoding="utf-8")
    return path


# ---------- Themes in Literature ----------

@dataclass(frozen=True)
class ThemeFit:
    theme: str
    fit: str                  # good | situational | mixed | open | not_ideal
    reasons: list             # (column fit, genre term) that matched the book
    definition: str = ""      # the Author's definition of the theme, shown with every suggestion
    theme_type: str = ""      # Canon or Motif


_FIT_ORDER = {"good": 0, "situational": 1, "mixed": 2, "open": 3, "not_ideal": 4}


def _genre_terms(cell: str, cfg: dict) -> list:
    """'Adventure, Thriller, Western' -> ['Adventure', 'Thriller', 'Western']; a lone dash means none."""
    terms = [t.strip() for t in re.split(r",(?![^(]*\))", cell or "")]
    return [t for t in terms if t and t not in cfg.get("empty_marks", [])]


def _term_parts(term: str) -> list:
    """'Science Fiction — Dystopian' and 'Children's Literature (Picture Books)' -> [broad, narrow]."""
    return [p.strip() for p in re.split(r"\s+[—–]\s+|\(|\)", term) if p.strip()]


def _names_in_path(path: dict) -> list:
    return [str(path.get(k) or "") for k in ("primary_genre", "secondary_genre", "major_subgenre", "minor_subgenre")]


def term_depth(term: str, path: dict, cfg: dict) -> int:
    """How specifically a genre term from the themes list names the book's genre path: 0 when it doesn't, else the
    deepest level it reaches (1 primary, 2 secondary, 3 major, 4 minor subgenre). Every part of the term (the broad
    one, and the narrower one after a dash or in brackets) must be one of the path's levels, after the list's shorthand
    (Contemporary, Nonfiction), or appear as words in the minor subgenre's name (Dystopian in Dystopian Fiction)."""
    levels = [_name_key(n) for n in _names_in_path(path)]
    minor = levels[3]
    aliases = {_name_key(k): [_name_key(x) for x in v] for k, v in (cfg.get("genre_aliases") or {}).items()}

    def depth(part):
        keys = aliases.get(_name_key(part), [_name_key(part)])
        exact = [i for k in keys for i, name in enumerate(levels, start=1) if name and k == name]
        if exact:
            return max(exact)               # a term that names a level counts at that level
        return 4 if minor and any(re.search(rf"\b{re.escape(k)}\b", minor) for k in keys) else 0

    found = [depth(p) for p in _term_parts(term)]
    return max(found) if found and all(found) else 0


def term_matches(term: str, path: dict, cfg: dict) -> bool:
    return term_depth(term, path, cfg) > 0


def theme_fit(entry: Entry, path: dict) -> ThemeFit:
    """The theme's fit for the book. The most specific listing decides (a not-ideal listing for Thriller outweighs a
    good one for Contemporary in a contemporary thriller); equally specific listings that disagree make it mixed."""
    cfg = entry.config
    scored = [(term_depth(t, path, cfg), fit, t) for col, fit in cfg["fit_columns"].items()
              for t in entry.fields.get(col, [])]
    matched = [(fit, t) for d, fit, t in scored if d]
    if not matched:
        return ThemeFit(entry.title, "open", [], entry.fields.get("definition", ""), _type(entry))
    top = max(d for d, _, _ in scored)
    fits = {fit for d, fit, _ in scored if d == top}
    if "good" in fits and "not_ideal" in fits:
        fit = "mixed"                       # shown with both reasons; the Author decides
    else:
        fit = min(fits, key=_FIT_ORDER.get)
    return ThemeFit(entry.title, fit, matched, entry.fields.get("definition", ""), _type(entry))


def _type(entry: Entry) -> str:
    return entry.fields.get(entry.config.get("type_field", ""), "")


def themes_for(pool: Pool, path: dict, theme_type: str | None = None) -> list:
    """Every theme (or every theme of one type, Canon or Motif) with its fit for the book's genre path: good fits
    first, then situational, mixed, open and finally not an ideal fit. Suggestions only: the theme is the Author's."""
    return sorted((theme_fit(e, path) for e in pool.entries
                   if not e.missing and (theme_type is None or _type(e) == theme_type)),
                  key=lambda f: (_FIT_ORDER[f.fit], f.theme.lower()))


def book_theme(pool: Pool, name: str, path: dict) -> ThemeFit:
    """The book's own theme, proposed at Story Pitch and confirmed by the Author with the Conflict Core: it must be a
    Canon theme. Returns its fit for the book's genre so a poor fit is visible."""
    e = _theme(pool, name)
    lead = e.config.get("lead_type", "Canon")
    if _type(e) != lead:
        raise LibraryError(f"{e.title} is a {_type(e)} theme; the book's theme must be a {lead} theme")
    return theme_fit(e, path)


def unrecognised_terms(themes: Pool, genres: Pool) -> list:
    """Genre terms in the themes list that name nothing in the Narrative Genres Pool (for the import report)."""
    cfg = themes.entries[0].config if themes.entries else {}
    paths = [{k: e.fields.get(k) for k in ("primary_genre", "secondary_genre", "major_subgenre")} | {"minor_subgenre": e.title}
             for e in genres.entries]
    terms = {t for e in themes.entries for col in cfg.get("fit_columns", {}) for t in e.fields.get(col, [])}
    return sorted(t for t in terms if not any(term_matches(t, p, cfg) for p in paths))


@dataclass(frozen=True)
class ThemePair:
    theme: str
    partner: str
    intersection: str          # how the two themes meet, in the Author's words
    partner_fit: ThemeFit      # the partner's own fit for the book: a poor fit is shown, never hidden


def _theme(pool: Pool, name: str) -> Entry:
    for e in pool.entries:
        if _name_key(e.title) == _name_key(name):
            return e
    raise LibraryError(f"{name!r} isn't in your Themes in Literature list")


def theme_pair(pool: Pool, theme: str, path: dict):
    """The theme's complementary theme, how they intersect, and how well the partner suits this book."""
    e = _theme(pool, theme)
    partner = e.fields.get(e.config.get("partner_field", ""), "")
    if not partner:
        return None
    p = _theme(pool, partner)
    return ThemePair(e.title, p.title, e.fields.get("intersection", ""), theme_fit(p, path))


def theme_brief(pool: Pool, themes, path: dict) -> list:
    """What a model is told about the book's chosen themes: each one's definition and its complementary theme with
    how they intersect. Genre-fit lists stay out of the prompt; they guide the Author's choice, not the writing."""
    out = []
    for name in themes:
        e = _theme(pool, name)
        brief = {"theme": e.title, "type": _type(e), "definition": e.fields.get("definition", "")}
        pair = theme_pair(pool, e.title, path)
        if pair:
            brief |= {"pairs_with": pair.partner, "how_they_intersect": pair.intersection}
        out.append(brief)
    return out


# ---------- Story Bible elements from the themes workbook ----------

def theme_aspects(pool: Pool, theme: str, group: str) -> dict:
    """One theme's row in a grouped sheet: its dialogue and voice, colours, timeline devices or a worldbuilding approach."""
    return dict(_theme(pool, theme).fields.get(group, {}))


def world_approaches(lmap: LibraryMap) -> list:
    return list(_pool(lmap, "themes").get("world_approaches", {}))


def world_brief(pool: Pool, themes, approach: str, lmap: LibraryMap) -> dict:
    """Worldbuilding's starting directions for the book's themes under the approach the Author approved (Components,
    G.R.A.P.E.S. or M.E.R.P.S.): {aspect: [(theme, direction)]}, plus the Story Bible's world layout under 'layout'.
    Choosing the approach is Worldbuilding's job and the Author's approval; this only reads the Author's sheets."""
    cfg = _pool(lmap, "themes")
    groups = cfg.get("world_approaches", {})
    if approach not in groups:
        raise LibraryError(f"{approach!r} is not a worldbuilding approach; choose one of {', '.join(groups)}")
    out, layout = {}, {}
    for name in themes:
        e = _theme(pool, name)
        for aspect, direction in e.fields.get(groups[approach], {}).items():
            out.setdefault(aspect, []).append((e.title, direction))
        for part, direction in e.fields.get(cfg.get("world_layout", ""), {}).items():
            layout.setdefault(part, []).append((e.title, direction))
    return {"approach": approach, "aspects": out, "layout": layout}


def theme_structure_fit(pool: Pool, themes, structures) -> dict:
    """How each of the book's themes suits each structure (from the Author's Plot Structure and Theme sheet), shown
    beside the Structure Fit scores, never added to them: {structure: [(theme, good | situational | not_ideal | open)]}."""
    fields = _pool_cfg(pool).get("structure_fit_fields", {})
    out = {s: [] for s in structures}
    for name in themes:
        e = _theme(pool, name)
        listed = {_name_key(st): fit for field, fit in fields.items() for st in e.fields.get(field, [])}
        for st in structures:
            out[st].append((e.title, listed.get(_name_key(st), "open")))
    return out


def unknown_structures(pool: Pool, structures) -> list:
    """Structure names in the themes workbook that the formula does not know (for the import report)."""
    known = {_name_key(s) for s in structures}
    fields = _pool_cfg(pool).get("structure_fit_fields", {})
    return sorted({st for e in pool.entries for f in fields for st in e.fields.get(f, []) if _name_key(st) not in known})


def _pool_cfg(pool: Pool) -> dict:
    return pool.entries[0].config if pool.entries else {}


# ---------- character reference pools (the Author's Fictional Character Development knowledge base) ----------

def is_scaffolding(pool: str, lmap: LibraryMap) -> bool:
    """True for a pool the Author keeps as brainstorming material with incomplete information: a component may draw
    ideas from it, but it is never canon or a standard to meet, and its gaps are not errors to fix."""
    return _pool(lmap, pool).get("standing") == "scaffolding"


def words(pool: Pool, kind: str | None = None) -> list:
    """The words of a word-list pool, of one kind if given: traits or strengths, flaws, or an epithet slot."""
    field_name = pool.entries[0].config.get("kind_field", "kind") if pool.entries else "kind"
    return [e.title for e in pool.entries if kind is None or e.fields.get(field_name) == kind]


def synonyms(pool: Pool, word: str) -> list:
    """The synonyms the Author listed for a word, or [] when none are listed."""
    hits = [e for e in pool.entries if _name_key(e.title) == _name_key(word)]
    return list(hits[0].fields.get("synonyms", [])) if hits else []


def animal_traits(pool: Pool, animal: str) -> dict:
    """{'strengths': [...], 'weaknesses': [...]} for an animal nature (a card's animal_nature field)."""
    hits = [e for e in pool.entries if _name_key(e.title) == _name_key(animal)]
    if not hits:
        raise LibraryError(f"{animal!r} isn't in {pool.name}; the sheet has {', '.join(e.title for e in pool.entries)}")
    return {k: list(v) for k, v in hits[0].fields.items() if isinstance(v, list)}


def epithet_slots(pool: Pool) -> dict:
    """{slot: [words]} for the epithet word lists, in the sheet's order."""
    out = {}
    for e in pool.entries:
        out.setdefault(e.fields.get(e.config.get("kind_field", "kind")), []).append(e.title)
    return out


def sections_about(pool: Pool, *terms) -> list:
    """The sections of a document pool whose text mentions every term (case set aside)."""
    want = [str(t).lower() for t in terms]
    return [e for e in pool.entries if all(w in (e.title + " " + e.body).lower() for w in want)]
