# -*- coding: utf-8 -*-
"""台股融資數據抓取 → data/tw_leverage_bulk.json（沿用 kidd KOFIA bulk 同構 schema）
資料源:
  1. FinMind TaiwanStockTotalMarginPurchaseShortSale — 上市全市場融資/融券（一次請求全歷史）
  2. TWSE FMTQIK — 大盤成交金額 + 加權指數收盤（月批次）
schema 對照（單位: 百萬元, 與 KOFIA 百萬韓元同構, compute /1e6 → 兆）:
  credit: [date, 融資餘額(百萬), null, null, 融資張數(張), null, null, null, null]
  funds : [date, 融券張數*100(→/1e6=萬張), null, null, 融資買進(百萬), 融資淨減(百萬), 融資淨減率%]
  kospi : [date, 加權指數, 成交股數, 成交金額(百萬), 市值代理=指數*2e6(百萬), null, null]
"""
import json, os, time, sys
from datetime import datetime, timedelta
import requests

START = "2019-01-01"
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
OUT = os.path.join(DATA, "tw_leverage_bulk.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def fetch_finmind():
    """全市場融資融券, date → {mp_sh, mp_yes_sh, ss_sh, mm, mm_yes, mm_buy}"""
    url = "https://api.finmindtrade.com/api/v4/data"
    r = requests.get(url, params={"dataset": "TaiwanStockTotalMarginPurchaseShortSale",
                                  "start_date": START}, headers=UA, timeout=60)
    r.raise_for_status()
    j = r.json()
    assert j.get("status") == 200, j.get("msg")
    days = {}
    for row in j["data"]:
        d = row["date"].replace("-", "")
        rec = days.setdefault(d, {})
        if row["name"] == "MarginPurchase":          # 張
            rec["mp_sh"], rec["mp_yes_sh"] = row["TodayBalance"], row["YesBalance"]
        elif row["name"] == "ShortSale":             # 張
            rec["ss_sh"] = row["TodayBalance"]
        elif row["name"] == "MarginPurchaseMoney":   # 元
            rec["mm"], rec["mm_yes"], rec["mm_buy"] = row["TodayBalance"], row["YesBalance"], row["buy"]
    print(f"FinMind: {len(days)} days, {min(days)} → {max(days)}")
    return days

def fetch_fmtqik():
    """TWSE 月批次: date → (index, volume, value元)。快取已完成月份。"""
    cache_p = os.path.join(DATA, "fmtqik_cache.json")
    cache = json.load(open(cache_p, encoding="utf-8")) if os.path.exists(cache_p) else {}
    today = datetime.now()
    cur = datetime.strptime(START, "%Y-%m-%d").replace(day=1)
    sess = requests.Session()
    while cur <= today:
        ym = cur.strftime("%Y%m")
        done_month = ym in cache and cur.replace(day=28) + timedelta(days=4) < today  # 已完整過去月
        if not done_month:
            j = None
            for att in range(4):
                try:
                    r = sess.get("https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK",
                                 params={"date": ym + "01", "response": "json"}, headers=UA, timeout=30)
                    j = r.json()
                    break
                except Exception:
                    if att == 3:
                        json.dump(cache, open(cache_p, "w", encoding="utf-8"))  # 保留進度
                        raise
                    time.sleep(6 * (att + 1))
            rows = []
            for row in j.get("data", []):
                y, m, dd = row[0].split("/")
                d = f"{int(y)+1911}{m}{dd}"
                vol = float(row[1].replace(",", ""))
                val = float(row[2].replace(",", ""))
                idx = float(row[4].replace(",", ""))
                rows.append([d, idx, vol, val])
            cache[ym] = rows
            print(f"FMTQIK {ym}: {len(rows)} days")
            json.dump(cache, open(cache_p, "w", encoding="utf-8"))  # 逐月存, 中斷可續
            time.sleep(1.2)
        cur = (cur + timedelta(days=32)).replace(day=1)
    json.dump(cache, open(cache_p, "w", encoding="utf-8"))
    days = {}
    for ym in cache:
        for d, idx, vol, val in cache[ym]:
            days[d] = (idx, vol, val)
    return days

def main():
    os.makedirs(DATA, exist_ok=True)
    fin = fetch_finmind()
    mkt = fetch_fmtqik()
    credit, funds, kospi = [], [], []
    for d in sorted(mkt):
        idx, vol, val = mkt[d]
        kospi.append([d, idx, vol, round(val / 1e6, 1), round(idx * 2e6, 0), None, None])
        f = fin.get(d)
        if not f or "mm" not in f:
            continue
        mm_m = round(f["mm"] / 1e6, 1)                      # 百萬元
        decline = max(0.0, (f.get("mm_yes") or f["mm"]) - f["mm"])
        dec_pct = round(100 * decline / f["mm_yes"], 3) if f.get("mm_yes") else None
        credit.append([d, mm_m, None, None, f.get("mp_sh"), None, None, None, None])
        funds.append([d, (f.get("ss_sh") or 0) * 100, None, None,
                      round((f.get("mm_buy") or 0) / 1e6, 1), round(decline / 1e6, 1), dec_pct])
    bulk = {"meta": {"generated": datetime.utcnow().isoformat(),
                     "unit": "million TWD", "source": "FinMind + TWSE FMTQIK",
                     "cols": {"credit": "date,margin_money_M,-,-,margin_shares,-,-,-,-",
                              "funds": "date,short_shares_x100,-,-,margin_buy_M,net_decline_M,net_decline_pct",
                              "kospi": "date,taiex,volume,value_M,mcap_proxy_M,-,-"}},
            "credit": credit, "funds": funds, "kospi": kospi, "kosdaq": []}
    json.dump(bulk, open(OUT, "w", encoding="utf-8"))
    print(f"bulk saved: credit={len(credit)} mkt={len(kospi)} → {OUT}")

if __name__ == "__main__":
    main()
