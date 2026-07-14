@echo off
rem 台股去槓桿儀表板每日更新（可掛入既有 18:00 排程,放在 rStock 之後）
cd /d D:\claude\tw_deleverage
python fetch_tw.py && python compute_indicators_tw.py data\tw_leverage_bulk.json && python build_tw.py
echo done: out\tw_deleverage_dashboard.html
