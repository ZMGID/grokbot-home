import re
TOK = re.compile(r'\s*(\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+)')
class Q(str): pass   # quoted string marker
def parse(s):
    stack=[[]]; pos=0
    for m in TOK.finditer(s):
        t=m.group(1)
        if t=='(': stack.append([])
        elif t==')': x=stack.pop(); stack[-1].append(x)
        elif t[0]=='"': stack[-1].append(Q(t[1:-1].replace('\\"','"').replace('\\\\','\\')))
        else: stack[-1].append(t)
    return stack[0][0]
def dump(x, ind=0):
    if isinstance(x, list):
        inner=" ".join(dump(i, ind+1) for i in x)
        return "(" + inner + ")" if len(inner) < 100 or not any(isinstance(i,list) for i in x) else \
            "(" + dump(x[0]) + "".join("\n"+"  "*(ind+1)+dump(i,ind+1) for i in x[1:]) + ")"
    if isinstance(x, Q): return '"' + x.replace('\\','\\\\').replace('"','\\"') + '"'
    if isinstance(x, float): return f"{x:.4f}".rstrip('0').rstrip('.')
    return str(x)
_libcache={}
def get_symbol(lib, name):
    if lib not in _libcache: _libcache[lib]=parse(open(f"/usr/share/kicad/symbols/{lib}.kicad_sym").read())
    L=_libcache[lib]
    syms={s[1]:s for s in L if isinstance(s,list) and s[0]=='symbol'}
    s=syms[name]
    ext=[e for e in s if isinstance(e,list) and e[0]=='extends']
    if ext:  # flatten derived symbol: take parent graphics/pins, child properties
        parent=get_symbol(lib, ext[0][1])
        props=[e for e in s if isinstance(e,list) and e[0]=='property']
        pn={p[1] for p in props}
        body=[e for e in parent if not (isinstance(e,list) and (e[0]=='property' and e[1] in pn))]
        out=['symbol',Q(name)]+[e for e in body[2:] if not (isinstance(e,list) and e[0]=='symbol')]+props
        for sub in parent:
            if isinstance(sub,list) and sub[0]=='symbol':
                out.append(['symbol',Q(sub[1].replace(ext[0][1] if False else sub[1].rsplit('_',2)[0], name,1))]+sub[2:])
        return out
    return s
def pins(sym):
    res=[]
    def walk(x):
        for e in x:
            if isinstance(e,list):
                if e[0]=='pin':
                    at=[a for a in e if isinstance(a,list) and a[0]=='at'][0]
                    nm=[a for a in e if isinstance(a,list) and a[0]=='name'][0][1]
                    nu=[a for a in e if isinstance(a,list) and a[0]=='number'][0][1]
                    ln=[a for a in e if isinstance(a,list) and a[0]=='length'][0][1]
                    res.append(dict(name=str(nm),num=str(nu),x=float(at[1]),y=float(at[2]),rot=float(at[3]) if len(at)>3 else 0,len=float(ln),type=e[1]))
                else: walk(e)
    walk(sym); return res
