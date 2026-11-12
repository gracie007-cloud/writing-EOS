import json, re, subprocess, sys, html
from pathlib import Path
HERE = Path(__file__).parent; PROJECT = HERE.parent / "eos-design" / "project"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
sources = {p.name: p.read_text(encoding="utf-8") for p in PROJECT.glob("*.dc.html")}
runtime = (HERE / "runtime.js").read_text(encoding="utf-8")
PAT = re.compile(r"\b(Run|RUN|Runs|RUNS) ?0\d|\b(FD|CC|CS|WS|SB|FM)-[A-Z0-9*]{1,3}\b|blind ID|v\d+\.\d|\bv\d\b")
states = {"Lab.dc.html": [{}, {"tab": "next"}, {"tab": "prompts"}, {"tab": "models"}, {"tab": "decisions"}, {"tab": "calib"}, {"tab": "tiers"}],
          "Bible.dc.html": [{"tab": t} for t in ["chars","arc","secrets","rel","naming","style","world","matrix","reserve"]],
          "Editor.dc.html": [{"tool": t} for t in ["write","rewrite","describe","brainstorm","workshop","changes"]] + [{"aiFree": True}, {"prov": True}, {"action": "show"}, {"hStr": "strong", "hDash": "none", "hDlg": False}, {"hStr": "light"}],
          "Board.dc.html": [{"tab": t} for t in ["lines", "beats", "time"]] + [{"moves": {"c1s4": "b"}}],
          "Export.dc.html": [{}, {"format": "docx", "scope": "locked"}],
          "Genre.dc.html": [{"tab": t} for t in ["promises", "tropes", "beats", "cliches"]] + [{"pack": p, "filter": "all"} for p in ["psych", "cozy", "mine"]],
          "Recipes.dc.html": [{"recipe": r} for r in ["plan", "draft", "polish", "summaries", "promise", "bible"]] + [{"run": "paused"}, {"run": "stopped"}],
          "History.dc.html": [{"sel": e} for e in ["d3", "r1", "p1", "b1", "b2", "s1", "g1"]] + [{"area": "lab"}, {"who": "recipe"}],
          "Library.dc.html": [{}, {"tab": "pen_names"}, {"tab": "genres"}, {"tab": "story_pitches"}, {"tab": "content_levels"}, {"tab": "conflict_map"}, {"tab": "arc_themes"}, {"tab": "themes"}],
          "Finish.dc.html": [{}, {"stage": "finishing"}, {"route": "trad"}],
          "Develop.dc.html": [{"sel": x} for x in ["intake","pitch","chars","plot","arc","cast","world","qa","outline"]],
          "Chapter.dc.html": [{"sel": s, "prompt": True} for s in ["brief","chars","chrono","first_draft","mature","lock"]] + [{"tab": "brief"}, {"tab": "state"}]}
bad = 0
for name in sorted(sources):
    if name == "Sidebar.dc.html": continue
    for stt in states.get(name, [{}]):
        page = (f'<!doctype html><html><head><meta charset="utf-8"><script>window.__DC_SOURCES__={json.dumps(sources).replace("</","<\\/")};'
                f'window.__DC_ENTRY__={json.dumps(name)};window.__DC_STATE__={json.dumps(stt)};</script><script>{runtime}</script></head>'
                '<body><div id="dc-root"></div></body></html>')
        f = HERE / "_dump.html"; f.write_text(page, encoding="utf-8")
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={HERE/'_chrome'}", "--virtual-time-budget=3000", "--dump-dom", f.resolve().as_uri()], capture_output=True, text=True, encoding="utf-8")
        dom = r.stdout.split('<div id="dc-root">', 1)[-1]
        text = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", " ", dom, flags=re.S)))
        hits = sorted(set(m.group(0) for m in PAT.finditer(text)))
        if hits: bad += 1
        print(f"{name:18} {json.dumps(stt):40} {'CLEAN' if not hits else 'FOUND ' + ', '.join(hits)}")
print("screens with codes in Writer view:", bad)
