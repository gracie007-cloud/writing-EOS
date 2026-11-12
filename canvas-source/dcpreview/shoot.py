"""Render a .dc.html artboard locally and screenshot it with headless Chrome.

usage: python shoot.py <artboard file name> <out.png> [width] [height] [state-json]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROJECT = HERE.parent / "eos-design" / "project"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

name, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
height = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
state = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}

sources = {p.name: p.read_text(encoding="utf-8") for p in PROJECT.glob("*.dc.html")}
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>window.__DC_SOURCES__ = {json.dumps(sources).replace("</", "<\\/")};
window.__DC_ENTRY__ = {json.dumps(name)}; window.__DC_STATE__ = {json.dumps(state)};</script>
<script>{(HERE / "runtime.js").read_text(encoding="utf-8")}</script>
</head><body style="margin:0"><div id="dc-root"></div></body></html>"""
html = HERE / "_preview.html"
html.write_text(page, encoding="utf-8")
if width < 600:  # headless Chrome will not open a window this narrow: frame it instead
    frame = HERE / "_phone.html"
    frame.write_text(f'<!doctype html><body style="margin:0"><iframe src="_preview.html" style="border:0;width:{width}px;height:{height}px"></iframe></body>', encoding="utf-8")
    html, width = frame, 800
prof = HERE / "_chrome"
r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                    f"--window-size={width},{height}", "--virtual-time-budget=4000",
                    f"--screenshot={Path(out).resolve()}", html.resolve().as_uri()],
                   capture_output=True, text=True)
print(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "done")
