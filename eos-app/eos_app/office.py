"""Read the Author's spreadsheets (.xlsx) and Word documents (.docx) with the standard library only.

Both formats are zipped XML. Only what the library pools need is read: each sheet's cell text by column letter,
and each paragraph's text in order. Formatting, formulas and images are ignored.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

_S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


class OfficeError(ValueError):
    """The file is not a spreadsheet or document this reader understands."""


def _open(path) -> zipfile.ZipFile:
    try:
        return zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as e:
        raise OfficeError(f"{Path(path).name}: not a readable Office file ({e})") from None


def read_xlsx(path) -> dict:
    """{sheet name: [row, ...]} in workbook order; each row is {column letter: text}, blank cells left out."""
    z = _open(path)
    names = set(z.namelist())
    shared = []
    if "xl/sharedStrings.xml" in names:
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(_S + "si"):
            shared.append("".join(t.text or "" for t in si.iter(_S + "t")))
    try:
        book = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    except KeyError:
        raise OfficeError(f"{Path(path).name}: no workbook inside") from None
    target = {r.get("Id"): r.get("Target") for r in rels}
    sheets = {}
    for s in book.find(_S + "sheets"):
        part = target[s.get(_R + "id")].lstrip("/")
        part = part if part.startswith("xl/") else "xl/" + part
        rows = []
        for row in ET.fromstring(z.read(part)).iter(_S + "row"):
            cells = {}
            for c in row.findall(_S + "c"):
                col = re.match(r"[A-Z]+", c.get("r", "")).group()
                v, kind = c.find(_S + "v"), c.get("t")
                if kind == "s" and v is not None:
                    text = shared[int(v.text)]
                elif kind == "inlineStr":
                    text = "".join(t.text or "" for t in c.iter(_S + "t"))
                else:
                    text = v.text if v is not None and v.text else ""
                if text.strip():
                    cells[col] = text
            rows.append(cells)
        sheets[s.get("name")] = rows
    return sheets


def read_docx(path) -> list:
    """The document's paragraphs in order, as plain text; an empty paragraph is ''."""
    z = _open(path)
    try:
        doc = ET.fromstring(z.read("word/document.xml"))
    except KeyError:
        raise OfficeError(f"{Path(path).name}: no document inside") from None
    out = []
    for p in doc.iter(_W + "p"):
        parts = []
        for node in p.iter():
            if node.tag == _W + "t":
                parts.append(node.text or "")
            elif node.tag == _W + "tab":
                parts.append("\t")
            elif node.tag == _W + "br":
                parts.append("\n")
        out.append("".join(parts))
    return out
