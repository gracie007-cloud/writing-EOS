import re, subprocess, sys, pathlib, tempfile
for f in sys.argv[1:]:
    s = pathlib.Path(f).read_text(encoding="utf-8")
    js = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', s, re.S).group(1)
    stub = "class DCLogic{constructor(p){this.props=p}setState(o){Object.assign(this.state,o)}}\n" + js + "\nvar c=new Component({});var v=c.renderVals();console.log(Object.keys(v).length+' keys ok');"
    t = pathlib.Path(tempfile.gettempdir())/"dc_check.js"; t.write_text(stub, encoding="utf-8")
    r = subprocess.run(["node", str(t)], capture_output=True, text=True)
    print(pathlib.Path(f).name, (r.stdout or r.stderr).strip()[:600])
