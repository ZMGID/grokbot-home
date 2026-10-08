"""Query JLCPCB parts library (public SMT component search API) for LCSC codes or keywords. Output JSON lines."""
import json, sys, urllib.request
API = "https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList"
def q(kw, n=5):
    req = urllib.request.Request(API, data=json.dumps({"keyword": kw, "currentPage": 1, "pageSize": n}).encode(),
                                 headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    out = []
    for c in (d.get("data") or {}).get("componentPageInfo", {}).get("list") or []:
        pr = c.get("componentPrices") or []
        out.append(dict(code=c.get("componentCode"), model=c.get("componentModelEn"), pkg=c.get("componentSpecificationEn"),
                        brand=c.get("componentBrandEn"), stock=c.get("stockCount"),
                        lib="Basic" if c.get("componentLibraryType") == "base" else ("Preferred" if c.get("preferredComponentFlag") else "Extended"),
                        price=pr[0]["productPrice"] if pr else None, url=c.get("lcscGoodsUrl"), desc=c.get("describe")))
    return out
if __name__ == "__main__":
    for kw in sys.argv[1:]:
        r = q(kw)
        exact = [x for x in r if x["code"] == kw] or r
        for x in exact[:5 if not kw.startswith("C") or not kw[1:].isdigit() else 1]:
            print(json.dumps(dict(query=kw, **x), ensure_ascii=False))
        if not r: print(json.dumps({"query": kw, "notfound": True}))
