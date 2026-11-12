// Minimal local stand-in for the canvas runtime: {{holes}}, sc-for, sc-if, dc-import, on* events, setState.
// For local layout previews only.
(function () {
  const SOURCES = window.__DC_SOURCES__;      // { "Main.dc.html": "<source>" }
  const ENTRY = window.__DC_ENTRY__;
  const INIT_STATE = window.__DC_STATE__ || {};
  class DCLogic {
    constructor(props) { this.props = props || {}; this.state = this.state || {}; }
    setState(patch) { this.state = Object.assign({}, this.state, typeof patch === 'function' ? patch(this.state) : patch); schedule(); }
    forceUpdate() { schedule(); }
  }
  window.DCLogic = DCLogic;

  const parsed = {};
  function parse(name) {
    if (parsed[name]) return parsed[name];
    const doc = new DOMParser().parseFromString(SOURCES[name], 'text/html');
    const xdc = doc.querySelector('x-dc');
    const helmet = xdc.querySelector('helmet');
    if (helmet) helmet.remove();
    const scriptEl = doc.querySelector('script[data-dc-script]');
    let defaults = {};
    try {
      const dp = JSON.parse(scriptEl.getAttribute('data-props') || '{}');
      for (const k in dp) if (dp[k] && 'default' in dp[k]) defaults[k] = dp[k].default;
    } catch (e) { console.error('data-props', name, e); }
    const Cls = new Function('DCLogic', scriptEl.textContent + '\nreturn Component;')(DCLogic);
    parsed[name] = { xdc, helmet, Cls, defaults };
    if (helmet) for (const n of helmet.children) document.head.appendChild(n.cloneNode(true));
    return parsed[name];
  }

  const instances = {};
  function lookup(path, scope) {
    path = path.trim();
    if (path === 'true') return true;
    if (path === 'false') return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    if (/^'.*'$/.test(path)) return path.slice(1, -1);
    const parts = path.split('.');
    let v;
    for (let i = scope.length - 1; i >= 0; i--) if (scope[i] && parts[0] in scope[i]) { v = scope[i][parts[0]]; break; }
    for (let i = 1; i < parts.length && v != null; i++) v = v[parts[i]];
    return v;
  }
  const HOLE = /\{\{([^}]+)\}\}/g;
  const WHOLE = /^\s*\{\{([^}]+)\}\}\s*$/;
  function interp(s, scope) { return s.replace(HOLE, (_, p) => { const v = lookup(p, scope); return v == null ? '' : String(v); }); }

  function renderChildren(src, out, scope, key) {
    let i = 0;
    for (const n of src.childNodes) renderNode(n, out, scope, key + '.' + (i++));
  }
  function renderNode(n, out, scope, key) {
    if (n.nodeType === 3) { out.appendChild(document.createTextNode(interp(n.textContent, scope))); return; }
    if (n.nodeType !== 1) return;
    const tag = n.tagName.toLowerCase();
    if (tag === 'sc-if') {
      const m = WHOLE.exec(n.getAttribute('value') || '');
      if (m && lookup(m[1], scope)) renderChildren(n, out, scope, key);
      return;
    }
    if (tag === 'sc-for') {
      const m = WHOLE.exec(n.getAttribute('list') || '');
      const list = (m && lookup(m[1], scope)) || [];
      const as = n.getAttribute('as') || 'item';
      list.forEach((item, idx) => renderChildren(n, out, scope.concat([{ [as]: item, $index: idx }]), key + '[' + idx + ']'));
      return;
    }
    if (tag === 'dc-import') {
      const name = n.getAttribute('name') + '.dc.html';
      const props = {};
      for (const a of n.attributes) {
        if (a.name === 'name' || a.name.startsWith('hint-')) continue;
        const camel = a.name.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
        const m = WHOLE.exec(a.value);
        props[camel] = m ? lookup(m[1], scope) : interp(a.value, scope);
      }
      out.appendChild(renderComponent(name, props, key));
      return;
    }
    const SVGNS = 'http://www.w3.org/2000/svg';
    const inSvg = tag === 'svg' || (out.namespaceURI === SVGNS);
    const el = inSvg ? document.createElementNS(SVGNS, n.tagName === 'svg' ? 'svg' : n.localName) : document.createElement(tag);
    for (const a of n.attributes) {
      const m = WHOLE.exec(a.value);
      if (a.name.startsWith('on') && m) {
        const fn = lookup(m[1], scope);
        if (typeof fn === 'function') el.addEventListener(a.name.slice(2), fn);
        continue;
      }
      let v = m ? lookup(m[1], scope) : interp(a.value, scope);
      if (v === false || v == null) { if (a.name.startsWith('aria-')) el.setAttribute(a.name, 'false'); continue; }
      if (v === true) v = a.name.startsWith('aria-') ? 'true' : '';
      el.setAttribute(a.name, String(v));
    }
    if (tag === 'template') return;
    renderChildren(n, el, scope, key);
    out.appendChild(el);
  }
  function renderComponent(name, props, key) {
    const p = parse(name);
    const full = Object.assign({}, p.defaults, props);
    let inst = instances[key];
    if (!inst) {
      inst = new p.Cls(full);
      inst.props = full;
      if (key === 'root') inst.state = Object.assign({}, inst.state || {}, INIT_STATE);
      instances[key] = inst;
    } else inst.props = full;
    const vals = inst.renderVals.call(inst);
    const frag = document.createDocumentFragment();
    renderChildren(p.xdc, frag, [vals], key);
    return frag;
  }
  let pending = false;
  function schedule() { if (!pending) { pending = true; setTimeout(() => { pending = false; draw(); }, 0); } }
  function draw() {
    const root = document.getElementById('dc-root');
    root.innerHTML = '';
    try { root.appendChild(renderComponent(ENTRY, window.__DC_PROPS__ || {}, 'root')); }
    catch (e) { root.textContent = 'RENDER ERROR: ' + e.stack; console.error(e); }
  }
  window.addEventListener('DOMContentLoaded', draw);
})();
