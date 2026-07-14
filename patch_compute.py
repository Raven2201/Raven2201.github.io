# -*- coding: utf-8 -*-
"""從 reference/compute_indicators.py 產生台股版 compute_indicators_tw.py"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "reference", "compute_indicators.py"), encoding="utf-8").read()

PAIRS = [
    # 標頭
    ('韓國股市去槓桿壓力分析 — 指標計算引擎',
     '台股融資去槓桿壓力分析 — 指標計算引擎（改自 kidd0368 韓版）'),
    ('輸入: kofia_kr_leverage_bulk.json (KOFIA FreeSIS 原始數據, 單位: 百萬韓元)',
     '輸入: tw_leverage_bulk.json (FinMind + TWSE FMTQIK, 單位: 百萬元)'),
    # 人工旗標
    ('"note": "大型雲服務商財報將至，關注AI資本開支指引"',
     '"note": "美股AI資本開支與台積電法說指引"'),
    ('"note": "韓監管已多次釋放收緊訊號；關注限空/穩定基金等措施"',
     '"note": "金管會融資成數/處置股規範動態"'),
    # 權重鍵改名: 預託金 → 流動性(消化天數)
    ('"lvl_dep_pctl": 7.5,', '"lvl_liq_pctl": 7.5,'),
    # kosdaq 選配（台股 v1 僅上市）
    ('''        if not q or ki is None:
            continue
        qi, qv, qm = num(q[1]), num(q[3]), num(q[4])''',
     '''        if ki is None:
            continue
        qi, qv, qm = (num(q[1]), num(q[3]), num(q[4])) if q else (None, None, None)'''),
    # 讀入融資張數（credit idx4, 韓版未使用的貸株欄位）
    ('        pledge = num(c[8]) if c and len(c) > 8 else None',
     '''        pledge = num(c[8]) if c and len(c) > 8 else None
        msh = num(c[4]) if c and len(c) > 4 else None  # 融資張數'''),
    # margin_dep → 券資比%（dep=融券張*100, msh=融資張）
    ('        S["margin_dep"].append(None if (mt is None or not dep) else round(100 * mt / dep, 2))',
     '        S["margin_dep"].append(None if (not msh or dep is None) else round(dep / msh, 2))  # 券資比%'),
    # 計分百分位: 融資/預託金 → 融資/日成交值(消化天數)
    ('        "margin_dep": rolling_pctl(S["margin_dep"], W),',
     '        "margin_val": rolling_pctl(S["margin_val"], W),'),
    ('"margin_dep": "mdep"', '"margin_val": "mval"'),
    ('            "margin_dep": last_valid(S["margin_dep"])[0],',
     '            "margin_val": last_valid(S["margin_val"])[0],'),
    # 分項標籤
    ('        "槓桿水位·融資/預託金百分位": Wt["lvl_dep_pctl"] * lp("margin_dep") / 100,',
     '        "槓桿水位·融資消化天數百分位": Wt["lvl_liq_pctl"] * lp("margin_val") / 100,'),
    ('"被動賣壓·斷頭金額百分位"', '"被動賣壓·融資淨減金額百分位"'),
    ('"被動賣壓·斷頭比率百分位"', '"被動賣壓·融資淨減率百分位"'),
    # 訊號文案
    ('"斷頭金額5日均百分位 "', '"融資淨減5日均百分位 "'),
    # etf 註記
    ('"note": "待 KRX 登入後補齊：三星/SK海力士單股2倍ETF規模與價格"',
     '"note": "台股版口徑僅上市信用交易，不含上櫃/借券賣出/股票質押"'),
    # I/O 路徑
    ('"data/kofia_kr_leverage_bulk.json"', '"data/tw_leverage_bulk.json"'),
    ('"out/kr_leverage_daily.csv"', '"out/tw_leverage_daily.csv"'),
]

for old, new in PAIRS:
    assert src.count(old) == 1, "NOT FOUND or DUP: " + old[:60]
    src = src.replace(old, new)

dst = os.path.join(HERE, "compute_indicators_tw.py")
io.open(dst, "w", encoding="utf-8").write(src)
print("OK →", dst, len(src), "bytes,", len(PAIRS), "patches applied")
