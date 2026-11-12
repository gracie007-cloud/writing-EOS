"""Bundle every screen into one self-contained HTML file that opens in any browser, offline.

usage: python make_viewer.py <out.html>
The page reads ?screen=Main&view=writer|engine; links between screens keep the view the screen's own switch is on.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
PROJECT = HERE.parent / "eos-design" / "project"
out = Path(sys.argv[1])

sources = {p.name: p.read_text(encoding="utf-8") for p in PROJECT.glob("*.dc.html")}
boards = json.loads((PROJECT / "canvas.json").read_text(encoding="utf-8"))["boards"]
screens = [[name[:-8], b["title"]] for name, b in boards.items() if name != "Sidebar.dc.html"]

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Writing EOS</title>
<style>
  body {{ margin: 0; background: #F5F7FB; }}
  #eos-bar {{ position: sticky; top: 0; z-index: 50; display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px;
    padding: 8px 16px; background: #12244A; color: #FFFFFF; font: 600 13px 'Plus Jakarta Sans', system-ui, sans-serif; }}
  #eos-bar strong {{ font-weight: 800; letter-spacing: 0.02em; }}
  #eos-bar span.note {{ color: #B6C3D6; font-weight: 500; }}
  #eos-bar select, #eos-bar button {{ min-height: 34px; border-radius: 8px; font: 600 13px 'Plus Jakarta Sans', system-ui, sans-serif; }}
  #eos-bar select {{ padding: 0 8px; border: 1px solid #3B5683; background: #1F3864; color: #FFFFFF; }}
  #eos-bar .push {{ margin-left: auto; }}
</style>
<script>
  (function () {{
    var q = new URLSearchParams(location.search);
    var screens = {json.dumps(screens)};
    var screen = q.get('screen') || 'Main';
    if (!screens.some(function (s) {{ return s[0] === screen; }})) screen = 'Main';
    var view = q.get('view') === 'engine' ? 'engine' : 'writer';
    window.__EOS__ = {{ screens: screens, screen: screen, view: view }};
    window.__DC_SOURCES__ = {json.dumps(sources).replace("</", "<\\/")};
    window.__DC_ENTRY__ = screen + '.dc.html';
    window.__DC_PROPS__ = {{ view: view }};
    window.__DC_STATE__ = {{}};
  }})();
  function eosGo(screen, view) {{
    location.search = '?screen=' + encodeURIComponent(screen) + '&view=' + (view || window.__EOS__.view);
  }}
  // links between screens point at <Name>.dc.html; route them through this page instead
  document.addEventListener('click', function (e) {{
    var a = e.target.closest && e.target.closest('a[href]');
    if (!a) return;
    var m = /([A-Za-z]+)\\.dc\\.html/.exec(a.getAttribute('href'));
    if (!m) return;
    e.preventDefault();
    var view = window.__EOS__.view;
    document.querySelectorAll('#dc-root [role="radio"][aria-checked="true"]').forEach(function (r) {{
      var t = r.textContent.trim();
      if (t === 'Engine view') view = 'engine';
      else if (t === 'Writer view') view = 'writer';
    }});
    eosGo(m[1], view);
  }}, true);
  document.addEventListener('DOMContentLoaded', function () {{
    var E = window.__EOS__, bar = document.getElementById('eos-bar');
    var sel = bar.querySelector('select');
    E.screens.forEach(function (s) {{
      var o = document.createElement('option'); o.value = s[0]; o.textContent = s[1];
      if (s[0] === E.screen) o.selected = true; sel.appendChild(o);
    }});
    sel.addEventListener('change', function () {{ eosGo(sel.value); }});
  }});
</script>
<script>{(HERE / "runtime.js").read_text(encoding="utf-8")}</script>
</head><body>
<div id="eos-bar" role="navigation" aria-label="Prototype controls">
  <strong>Writing EOS</strong><span class="note">Clickable prototype · sample data</span>
  <label class="push">Jump to <select aria-label="Jump to screen"></select></label>
</div>
<div id="dc-root"></div>
</body></html>"""
out.write_text(page, encoding="utf-8")
print("wrote", out, f"{len(page) // 1024} KB,", len(screens), "screens")
