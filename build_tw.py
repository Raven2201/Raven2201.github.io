# -*- coding: utf-8 -*-
"""組裝台股儀表板: out/indicators.json + template_tw.html → out/tw_deleverage_dashboard.html"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    ind_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "out", "indicators.json")
    with open(ind_path, encoding="utf-8") as f:
        ind = f.read()
    with open(os.path.join(HERE, "template_tw.html"), encoding="utf-8") as f:
        tpl = f.read()
    out = tpl.replace("/*__DATA__*/null", ind, 1)
    out = out.replace("/*__SRC__*/null", json.dumps({}), 1)
    dst = os.path.join(HERE, "out", "tw_deleverage_dashboard.html")
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print("OK", len(out), "bytes ->", dst)

if __name__ == "__main__":
    main()
