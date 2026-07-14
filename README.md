# 台股融資去槓桿壓力儀表板

改自 [kidd0368 韓股版](https://kidd0368.github.io/)(原始碼公開於其 GitHub repo,已歸檔至 `reference/`)。

## 一鍵更新
```
update_tw.bat        # fetch → compute → build,產出 out\tw_deleverage_dashboard.html
```
產出為自包含單檔 HTML,直接雙擊開啟即可(無需伺服器)。

## 管線
| 步驟 | 檔案 | 說明 |
|---|---|---|
| 抓取 | `fetch_tw.py` | FinMind 全市場融資融券(1 請求)＋TWSE FMTQIK 月批次(有快取,日常只補當月) |
| 計算 | `compute_indicators_tw.py` | 9 分項加權 0-100 壓力指數,權重/基期/人工旗標在 CONFIG |
| 組裝 | `build_tw.py` + `template_tw.html` | 資料烤進模板 |

`patch_compute.py` / `patch_template.py`:從 `reference/` 的韓版原始檔重新生成台股版(改補丁後重跑即可)。

## 與韓版的指標對照
| 韓版 | 台股版 | 備註 |
|---|---|---|
| 신용거래융자 信用融資 | 融資餘額(上市) | FinMind, T+1 |
| 반대매매 斷頭金額/比率 | 融資單日淨減金額/淨減率 | 代理,含主動了結、高估斷頭 |
| 투자자예탁금 預託金 | (無日頻等價)計分改用融資消化天數 | 融資÷日成交額 |
| 市值 | TAIEX×常數 代理 | 百分位不受常數影響 |
| KOSPI/KOSDAQ 雙市 | 僅上市 | 上櫃待接入 |

## 已知侷限
見 `reference/設計盲點分析.md`(韓版框架的盲點＋台股代理誤差)。
s2/s3 為人工旗標,在 `compute_indicators_tw.py` CONFIG 手動更新。
僅供研究,非投資建議。
