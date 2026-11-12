"""Push gate: keep keys and the Author's library out of the repository, and keep the app itself generic.

    python tools/check_public.py            # check every file git would send

It reads the files git tracks and stops if any of them is or holds

- a path that is never stored here: the library, a .env file, the real answer key, the private word list;
- something shaped like a provider key;
- outside the folders that may carry the Author's book (BOOK_OK below), a character or pen name from the Author's
  library pools, or a word from .private-words.txt, the Author's own list of private names, one per line.

The last rule is decision D10: the app, its tests and the requirements stay generic, so they can be shared without
the book. The bake-off harness, the worked examples and the canvas source may name the book; they are the reason
this repository is private. If the repository is ever made public again, empty BOOK_OK first and run this check.

It prints the file and line of each hit and exits 1. It runs before every push (tools/pre-push).
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEVER = (re.compile(r"(^|/)library/"), re.compile(r"(^|/)\.env$"), re.compile(r"(^|/)data/[^/]*ANSWER_KEY", re.I),
         re.compile(r"(^|/)\.private-words\.txt$"))
BOOK_OK = ("eos-bakeoff/", "experiments/", "canvas-source/", "docs/LIBRARY_IMPORT_REPORT_")
KEY_SHAPES = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|hf_[A-Za-z0-9]{20,}|Bearer [A-Za-z0-9._-]{20,}"
                        r"|api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9_-]{16,})")
BINARY = {".png", ".jpg", ".jpeg", ".gif", ".zip", ".xlsx", ".docx", ".pdf", ".woff2"}


def tracked() -> list:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    return [p for p in out.decode("utf-8").split("\0") if p]


def library_names() -> set:
    """Character and pen names from the Author's pools; empty when the library is not on this computer."""
    if not (ROOT / "library").is_dir():
        return set()
    sys.path.insert(0, str(ROOT / "eos-app"))
    from eos_app.library import load_map, load_pool
    lmap, names = load_map(), set()
    for pool in ("characters", "pen_names"):
        for entry in load_pool(pool, ROOT / "library", lmap).entries:
            title = (entry.title or "").strip()
            if len(title) >= 6 and " " in title:        # full names; one common word would flag ordinary prose
                names.add(title)
    return names


def private_words() -> set:
    f = ROOT / ".private-words.txt"
    if not f.is_file():
        return set()
    return {w.strip() for w in f.read_text(encoding="utf-8").splitlines() if w.strip() and not w.startswith("#")}


def check() -> list:
    words = library_names() | private_words()
    pattern = re.compile(r"(?<![A-Za-z])(" + "|".join(map(re.escape, sorted(words, key=len, reverse=True)))
                         + r")(?![A-Za-z])") if words else None
    hits = []
    for rel in tracked():
        if any(p.search(rel) for p in NEVER):
            hits.append(f"{rel}: this path is never stored here")
            continue
        path = ROOT / rel
        if path.suffix.lower() in BINARY or not path.is_file():
            continue
        generic = not rel.startswith(BOOK_OK)
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if generic and pattern and (m := pattern.search(line)):
                hits.append(f"{rel}:{n}: private name {m.group(1)!r} in a file that must stay generic")
            if KEY_SHAPES.search(line):
                hits.append(f"{rel}:{n}: looks like a provider key")
    return hits


if __name__ == "__main__":
    found = check()
    for h in found:
        print(h)
    print(f"push gate: {len(tracked())} files checked, {len(found)} problem(s)"
          + ("" if (ROOT / "library").is_dir() else " · library not present, so its names were not checked"))
    sys.exit(1 if found else 0)
