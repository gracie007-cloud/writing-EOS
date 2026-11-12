"""Assemble Writing EOS screens from src/<Name>.main.html + src/<Name>.js inside the shared shell.

Macros (@NAME@) expand to the design system's inline styles; /*VIEW*/ and /*TONES*/ expand to shared JS.
Every board's data lives in its own src files: nothing is copied from older boards.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "src"
OUT = HERE.parent / "eos-design" / "project"

STYLE = {
    "CARD": "background: #FFFFFF; border: 1px solid #E3E8F0; border-radius: 16px; box-shadow: 0 1px 2px rgb(16 24 40 / 0.05), 0 1px 3px rgb(16 24 40 / 0.06)",
    "EYEBROW": "margin: 0; display: flex; align-items: center; gap: 10px; font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #2E75B6",
    "H2": "margin: 0; font-size: 17px; font-weight: 800",
    "LABEL": "font-size: 12px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #5F6E84",
    "MUTED": "color: #4B5B73",
    "SERIF": "font-family: 'Lora', Georgia, serif",
    "MONO": "font-family: 'JetBrains Mono', monospace",
    "BADGE": "font-size: 12px; font-weight: 600; padding: 2px 9px; border-radius: 999px; white-space: nowrap",
    "CHIP": "font-size: 13px; font-weight: 600; padding: 4px 10px; border-radius: 999px; background: #FFFFFF; box-shadow: inset 0 0 0 1px #D5DCE6",
    "BTN_PRIMARY": "min-height: 44px; padding: 0 18px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border-radius: 10px; border: 1px solid #1F4E79; background: #2E75B6; color: #FFFFFF; font: 600 14px 'Plus Jakarta Sans', sans-serif; text-decoration: none; cursor: pointer",
    "BTN_GOLD": "min-height: 44px; padding: 0 18px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border-radius: 10px; border: 1px solid #B98A00; background: #FFC000; color: #12244A; font: 700 14px 'Plus Jakarta Sans', sans-serif; text-decoration: none; cursor: pointer",
    "BTN_OUTLINE": "min-height: 44px; padding: 0 18px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border-radius: 10px; border: 1px solid #CBD5E1; background: #FFFFFF; color: #1F3864; font: 600 14px 'Plus Jakarta Sans', sans-serif; text-decoration: none; cursor: pointer",
    "BTN_GHOST": "min-height: 44px; padding: 0 14px; display: inline-flex; align-items: center; gap: 8px; border-radius: 10px; border: 0; background: transparent; color: #1F4E79; font: 600 14px 'Plus Jakarta Sans', sans-serif; text-decoration: none; cursor: pointer",
    "TABBAR": "display: flex; gap: 4px; padding: 4px; border-radius: 12px; background: #2E75B6; overflow-x: auto",
    "TAB": "flex: 1 0 auto; min-height: 40px; padding: 0 14px; border: 0; border-radius: 9px; font: 600 14px 'Plus Jakarta Sans', sans-serif; white-space: nowrap; cursor: pointer",
    "NOTE": "display: flex; align-items: flex-start; gap: 12px; padding: 14px 16px; border-radius: 16px; background: #F2F7FD; box-shadow: inset 0 0 0 1px #C9DDF1",
    "NOTEICON": "flex: none; display: grid; place-items: center; width: 32px; height: 32px; border-radius: 10px; background: #FFFFFF; color: #2E75B6",
    "GOLDBOX": "border-radius: 16px; background: #FFF5D6; box-shadow: inset 0 0 0 1px #FFD966",
    "NAVY": "border-radius: 16px; background: #1F3864; color: #FFFFFF",
    "INPUT": "min-height: 44px; padding: 0 12px; border-radius: 10px; border: 1px solid #CBD5E1; background: #FFFFFF; font: 14px 'Plus Jakarta Sans', sans-serif; color: #1B2A41",
    "FIELDLABEL": "font-size: 13px; font-weight: 600; color: #4B5B73",
    "SVG": "fill: none; stroke: currentColor; stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round",
}

ICON = {
    "info": "M12 2a10 10 0 1 0 0 20a10 10 0 1 0 0-20 M12 16v-4 M12 8h.01",
    "check": "M20 6 9 17l-5-5",
    "arrow": "M5 12h14 M12 5l7 7-7 7",
    "shield": "M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z M9 12l2 2 4-4",
    "back": "M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8 M3 3v5h5",
    "flag": "M4 22V4a1 1 0 0 1 .4-.8A6 6 0 0 1 8 2c3 0 5 2 7.333 2q2 0 3.067-.8A1 1 0 0 1 20 4v10a1 1 0 0 1-.4.8A6 6 0 0 1 16 16c-3 0-5-2-8-2a6 6 0 0 0-4 1.528",
    "lock": "M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z M7 11V7a5 5 0 0 1 10 0v4",
    "chevl": "M15 18l-6-6 6-6",
    "chevr": "M9 18l6-6-6-6",
    "cpu": "M6 4h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z M9 9h6v6H9z M15 2v2 M15 20v2 M2 15h2 M2 9h2 M20 15h2 M20 9h2 M9 2v2 M9 20v2",
    "alert": "M21.73 18l-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3 M12 9v4 M12 17h.01",
    "play": "M6 3l14 9-14 9z",
    "pause": "M8 4h2v16H8z M14 4h2v16h-2z",
    "x": "M18 6 6 18 M6 6l12 12",
}


def icon(name, size=18, color="currentColor", width="1.9"):
    return (f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" style="flex: none; fill: none; '
            f'stroke: {color}; stroke-width: {width}; stroke-linecap: round; stroke-linejoin: round"><path d="{ICON[name]}"></path></svg>')


HELMET = """<helmet>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&amp;family=Lora:ital,wght@0,400;0,500;0,600;1,400&amp;family=Plus+Jakarta+Sans:wght@400;500;600;700;800&amp;display=swap" rel="stylesheet">
<style>
body{margin:0}
a{color:#1F4E79}a:hover{color:#12244A}
:focus-visible{outline:2px solid #2E75B6;outline-offset:2px}
.eos-btn{transition:background-color .15s ease, box-shadow .15s ease, transform .15s ease}
.eos-btn:hover{box-shadow:0 10px 20px -12px rgb(31 56 100 / .5);transform:translateY(-1px)}
.eos-row{transition:background-color .15s ease}
.eos-row:hover{background:#F2F7FD}
.eos-navitem:hover{background:#F2F7FD}
.eos-navitem[aria-current="page"]:hover{background:#1F4E79}
@media (max-width: 900px){
.eos-side{flex:1 1 100% !important;max-width:none !important;min-height:0 !important;border-right:0 !important;border-bottom:1px solid #E3E8F0 !important;padding:12px !important;gap:10px !important}
.eos-nav{flex-direction:row !important;overflow-x:auto;gap:4px !important}
.eos-navgroup{flex-direction:row !important}
.eos-navlabel,.eos-sidefoot,.eos-search{display:none !important}
.eos-top{padding:12px 16px !important}
.eos-page{padding:24px 16px 40px !important}
}
@media (prefers-reduced-motion: reduce){*{transition:none !important}}
</style>
</helmet>"""

VIEW_JS = """var self = this;
var st = this.state;
var view = st.view || this.props.view || 'writer';
var engine = view === 'engine';
var viewOpts = [{ id: 'writer', name: 'Writer view' }, { id: 'engine', name: 'Engine view' }].map(function (v) {
var on = v.id === view;
return { name: v.name, on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F3864' : '#4B5B73', shadow: on ? '0 1px 3px rgb(16 24 40 / 0.12)' : 'none', pick: function () { self.setState({ view: v.id }); } };
});"""

TONES_JS = """var TONE = {
done: { bg: '#E7F3DF', fg: '#3B7020', ring: '#B9DCA4', dot: '#70AD47' },
run: { bg: '#DEEBF7', fg: '#1F4E79', ring: '#9DC3E6', dot: '#2E75B6' },
you: { bg: '#FFF5D6', fg: '#6B4E00', ring: '#FFD966', dot: '#FFC000' },
flag: { bg: '#FDE9DC', fg: '#A5470B', ring: '#F4B183', dot: '#ED7D31' },
mature: { bg: '#EFE8F8', fg: '#5B3A8C', ring: '#CDBDE6', dot: '#7B5BB0' },
wait: { bg: '#EEF1F5', fg: '#475569', ring: '#D5DCE6', dot: '#94A3B8' },
blocked: { bg: '#FDECEB', fg: '#A8321F', ring: '#F2B8B0', dot: '#E5604D' },
navy: { bg: '#1F3864', fg: '#FFFFFF', ring: '#1F3864', dot: '#FFFFFF' }
};
var tabsOf = function (defs, cur, key) {
return defs.map(function (t) { var on = t.id === cur; var o = {}; o[key] = t.id; return Object.assign({}, t, { on: on, bg: on ? '#FFFFFF' : 'transparent', fg: on ? '#1F4E79' : '#FFFFFF', pick: function () { self.setState(o); } }); });
};"""


def topbar(crumbs, search=True):
    parts = []
    for i, (label, href) in enumerate(crumbs):
        if i:
            parts.append(icon("chevr", 14, "#94A3B8", "2"))
        if href:
            parts.append(f'<a href="{href}" style="color: #4B5B73; text-decoration: none">{label}</a>')
        else:
            parts.append(f'<span aria-current="page" style="color: #1B2A41">{label}</span>')
    s = ('<header class="eos-top" style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px 16px; padding: 14px 32px; '
         'background: rgb(255 255 255 / 0.85); border-bottom: 1px solid #E3E8F0">\n'
         '<nav aria-label="Breadcrumb" style="display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600">'
         + "".join(parts) + "</nav>\n")
    if search:
        s += ('<div class="eos-search" style="flex: 1 1 260px; max-width: 420px; position: relative; margin-left: auto">\n'
              '<label for="top-search" style="position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0)">Search the Bible, chapters and chats</label>\n'
              '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" style="position: absolute; left: 12px; top: 14px; fill: none; stroke: #5F6E84; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round"><path d="M11 3a8 8 0 1 0 0 16a8 8 0 1 0 0-16 M21 21l-4.3-4.3"></path></svg>\n'
              '<input id="top-search" type="search" placeholder="Search the Bible, chapters and chats" style="width: 100%; box-sizing: border-box; min-height: 44px; padding: 0 12px 0 36px; border-radius: 10px; border: 1px solid #D5DCE6; background: #FFFFFF; font: 14px \'Plus Jakarta Sans\', sans-serif; color: #1B2A41">\n'
              '</div>\n')
    s += ('<div role="radiogroup" aria-label="View" style="display: inline-flex; gap: 4px; padding: 4px; border-radius: 12px; background: #E8EEF6' + ('' if search else '; margin-left: auto') + '">\n'
          '<sc-for list="{{viewOpts}}" as="v" hint-placeholder-count="2">\n'
          '<button type="button" role="radio" aria-checked="{{v.on}}" onClick="{{v.pick}}" style="min-height: 36px; padding: 0 14px; border: 0; border-radius: 9px; background: {{v.bg}}; color: {{v.fg}}; box-shadow: {{v.shadow}}; font: 600 13px \'Plus Jakarta Sans\', sans-serif; cursor: pointer">{{v.name}}</button>\n'
          '</sc-for>\n</div>\n</header>')
    return s


def pagehead(eyebrow, title, purpose, actions="", serif=False, extra=""):
    tfont = "font-family: 'Lora', Georgia, serif; font-size: 38px; font-weight: 500" if serif else "font-size: 32px; font-weight: 800; letter-spacing: -0.01em"
    return (f'<section aria-labelledby="page-title" style="display: flex; flex-wrap: wrap; align-items: flex-end; justify-content: space-between; gap: 18px">\n'
            f'<div style="flex: 1 1 520px; display: flex; flex-direction: column; gap: 10px">\n'
            f'<p style="@EYEBROW@"><span style="width: 24px; height: 1px; background: #9DC3E6"></span>{eyebrow}</p>\n'
            f'<h1 id="page-title" style="margin: 0; {tfont}; line-height: 1.15">{title}</h1>\n'
            + (f'<p style="margin: 0; max-width: 720px; font-size: 15px; line-height: 1.6; color: #4B5B73">{purpose}</p>\n' if purpose else '')
            + extra
            + '</div>\n'
            + (f'<div style="display: flex; flex-wrap: wrap; gap: 10px">{actions}</div>\n' if actions else '')
            + '</section>')


def expand(text):
    text = text.replace("/*VIEW*/", VIEW_JS).replace("/*TONES*/", TONES_JS)
    text = re.sub(r"@ICON:(\w+)(?::(\d+))?(?::([#\w]+))?@", lambda m: icon(m.group(1), int(m.group(2) or 18), m.group(3) or "currentColor"), text)
    for _ in range(2):
        for k, v in STYLE.items():
            text = text.replace(f"@{k}@", v)
    return text


def build(name, meta):
    main = (SRC / f"{name}.main.html").read_text(encoding="utf-8")
    js = (SRC / f"{name}.js").read_text(encoding="utf-8")
    head = pagehead(meta["eyebrow"], meta["title"], meta.get("purpose", ""), meta.get("actions", ""), meta.get("serif", False), expand(meta.get("extra", "")))
    props = {"view": {"editor": "enum", "options": ["writer", "engine"], "default": "writer"}, "$preview": {"width": 1440, "height": meta["h"]}}
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{meta['doctitle']}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
<div style="min-height: 100vh; display: flex; flex-wrap: wrap; align-items: stretch; background: #F5F7FB; color: #1B2A41; font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif">
<dc-import name="Sidebar" active="{meta['active']}" hint-size="264px,100%"></dc-import>
<div style="flex: 999 1 560px; min-width: 0; display: flex; flex-direction: column">
{topbar(meta['crumbs'], meta.get('search', True))}
<main class="eos-page" style="width: 100%; max-width: 1240px; margin: 0 auto; box-sizing: border-box; padding: 28px 32px 56px; display: flex; flex-direction: column; gap: 22px">
{head}
{main}
</main>
</div>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{json.dumps(props)}'>
{js}
</script>
</body>
</html>
"""
    html = expand(html)
    leftover = re.findall(r"@[A-Z_]+@|/\*OLD:|/\*VIEW\*/|/\*TONES\*/", html)
    assert not leftover, (name, leftover[:5])
    (OUT / f"{name}.dc.html").write_text(html, encoding="utf-8")
    print("built", name, len(html))


if __name__ == "__main__":
    metas = json.loads((SRC / "pages.json").read_text(encoding="utf-8"))
    for n in (sys.argv[1:] or list(metas)):
        m = metas[n]
        m["actions"] = expand(m.get("actions", ""))
        build(n, m)
