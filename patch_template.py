# -*- coding: utf-8 -*-
"""從 reference/dashboard_template.html 產生台股版 template_tw.html"""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "reference", "dashboard_template.html"), encoding="utf-8").read()

PAIRS = [
    # 標題（title 與 h1 共 2 處）
    ("<title>韓國股市去槓桿壓力儀表板</title>", "<title>台股融資去槓桿壓力儀表板</title>"),
    ("<h1>韓國股市去槓桿壓力儀表板</h1>", "<h1>台股融資去槓桿壓力儀表板</h1>"),
    # 頁首截止註記與資料源橫幅
    ("'（KOFIA T+1 公布）'", "'（融資數據 T+1 彙整）'"),
    ("— 待 KOFIA 真實歷史數據載入後自動替換",
     "— 待真實歷史數據載入後自動替換"),
    ("'📊 全部讀數均為<b>真實值</b>：日度數據（KOFIA，'", "'📊 全部讀數均為<b>真實值</b>：日度數據（TWSE/FinMind，'"),
    ("'📊 <b>真實數據</b>（KOFIA，'", "'📊 <b>真實數據</b>（TWSE/FinMind，'"),
    # ---- tiles ----
    ("{l:'信用融資餘額',v:fmtN(L.margin_total,1)+' 兆₩',d:(E.margin_d5_pct==null?'':'5日 '+(E.margin_d5_pct>0?'+':'')+E.margin_d5_pct+'%')+' · 距峰值 '+fmtN(100*(L.margin_total/U.peak-1),1)+'%',bad:E.margin_d5_pct>0},",
     "{l:'融資餘額（上市）',v:fmtN(L.margin_total*1e4,0)+' 億元',d:(E.margin_d5_pct==null?'':'5日 '+(E.margin_d5_pct>0?'+':'')+E.margin_d5_pct+'%')+' · 距峰值 '+fmtN(100*(L.margin_total/U.peak-1),1)+'%',bad:E.margin_d5_pct>0},"),
    ("{l:'融資／預託金',v:fmtN(L.margin_dep,1)+'%',d:'5年百分位 '+fmtN(E.pctl.margin_dep,0)+' · 越低=現金緩衝越足',bad:(E.pctl.margin_dep||0)>70},",
     "{l:'融資消化天數',v:fmtN(L.margin_val,2)+' 天',d:'5年百分位 '+fmtN(E.pctl.margin_val,0)+' · 券資比 '+fmtN(L.margin_dep,2)+'%',bad:(E.pctl.margin_val||0)>70},"),
    ("{l:'斷頭比率（5日均）',v:fmtN(E.bandae_ratio_ma,1)+'%',d:'斷頭金額5日均 '+fmtN(E.bandae_amt_ma,0)+' 億₩ · 百分位 '+fmtN(E.pctl.bandae_amt,0),bad:(E.pctl.bandae_amt||0)>70},",
     "{l:'融資淨減率（5日均）',v:fmtN(E.bandae_ratio_ma,2)+'%',d:'淨減金額5日均 '+fmtN(E.bandae_amt_ma,0)+' 億元 · 百分位 '+fmtN(E.pctl.bandae_amt,0),bad:(E.pctl.bandae_amt||0)>70},"),
    ("{l:'KOSPI 距52週最高收盤',v:fmtN(E.kospi_dd,1)+'%',d:'52週最高收盤 '+fmtN(E.kospi_hi52,0)+(E.kospi_hi52_date?'（'+fmtD(E.kospi_hi52_date).slice(5)+'）':'')+' · 現收 '+fmtN(L.kospi_idx,0)+' · 20日波動 '+fmtN(E.rv20,0)+'%',bad:(E.pctl.rv20||0)>70},",
     "{l:'加權指數 距52週最高收盤',v:fmtN(E.kospi_dd,1)+'%',d:'52週最高收盤 '+fmtN(E.kospi_hi52,0)+(E.kospi_hi52_date?'（'+fmtD(E.kospi_hi52_date).slice(5)+'）':'')+' · 現收 '+fmtN(L.kospi_idx,0)+' · 20日波動 '+fmtN(E.rv20,0)+'%',bad:(E.pctl.rv20||0)>70},"),
    # ---- 卡片 m: 融資餘額 ----
    ("{id:'m', t:'信用融資餘額（신용거래융자）', d:'散戶槓桿主體。單位：兆韓元。參考線＝近期峰值與 4/30 行情基期。',",
     "{id:'m', t:'融資餘額（上市）', d:'散戶槓桿主體。單位：兆元。參考線＝近期峰值與 4/30 行情基期。',"),
    ("這是散戶向券商借錢買股的餘額，本輪去槓桿的「本體」。看三點：<b>水位</b>——距峰值與 4/30 基期兩條參考線的位置；<b>進度條</b>——本輪行情新增的槓桿已退出幾成（100%＝這輪借的錢全數吐回）；<b>斜率</b>——曲線急跌代表強制去槓桿正在發生，走平代表賣壓衰竭、進入尾聲。KOSDAQ 融資盤通常更投機，去化也更劇烈，兩市分列可看出清的「質」。",
     "這是散戶向券商借錢買股的餘額，去槓桿分析的「本體」。看三點：<b>水位</b>——距峰值與 4/30 基期兩條參考線的位置；<b>進度條</b>——本輪行情新增的槓桿已退出幾成（100%＝這輪借的錢全數吐回）；<b>斜率</b>——曲線急跌代表強制去槓桿正在發生，走平代表賣壓衰竭、進入尾聲。（v1 僅上市；上櫃融資待接入）"),
    ("  series:[{name:'全市場',key:'margin_total',color:'--s1',type:'line'},{name:'KOSPI',key:'margin_kospi',color:'--s2',type:'line'},{name:'KOSDAQ',key:'margin_kosdaq',color:'--s3',type:'line'}],",
     "  series:[{name:'融資餘額',key:'margin_total',color:'--s1',type:'line'}],"),
    # 卡片 m Y軸/參考線: 兆 → 億元
    ("  yFmt:v=>fmtN(v,0), refs:()=>[{v:IND.unwind.peak,label:'峰值 '+fmtN(IND.unwind.peak,1)},{v:IND.unwind.baseline,label:'4月底基期'}],",
     "  yFmt:v=>fmtN(v*1e4,0), refs:()=>[{v:IND.unwind.peak,label:'峰值 '+fmtN(IND.unwind.peak*1e4,0)+' 億'},{v:IND.unwind.baseline,label:'4月底基期'}],"),
    # ---- 卡片 md: 券資比 ----
    ("{id:'md',t:'融資／預託金比（槓桿 vs 現金緩衝）', d:'借的錢 ÷ 帳上現金。比率下降＝散戶現金緩衝相對充裕，槓桿張力比表面溫和。',",
     "{id:'md',t:'券資比（融券 vs 融資）', d:'融券張數 ÷ 融資張數。上行＝空方對沖增加；急跌行情中融券回補反而是反彈燃料。',"),
    ("預託金＝散戶放在券商帳戶、還沒買進股票的現金（子彈）。<b>比率下行</b>＝子彈比槓桿長得快，即使融資額創新高、實際張力也沒表面緊——判斷「槓桿是否被高估」的關鍵反向證據；<b>比率上行且預託金同時下滑</b>＝沒子彈還在加槓桿，最脆弱的組合。下方預託金面積圖單獨看：暴跌後預託金反而跳增，常代表「跌出來的錢在場邊等」。",
     "台股沒有每日預託金公開數據，此卡改看多空槓桿結構：<b>券資比上行</b>＝融券（看空/避險）相對融資增長；高券資比＋指數止穩常醞釀軋空反彈。下方融券餘額單獨看：暴跌後融券暴增，代表空方追擊；融券快速回補則是反彈的技術性燃料。注意：此卡僅供結構參考，<b>不計入</b>壓力指數。"),
    ("  series:[{name:'融資/預託金 %',key:'margin_dep',color:'--s1',type:'line'}], yFmt:v=>fmtN(v,0)+'%',",
     "  series:[{name:'券資比 %',key:'margin_dep',color:'--s1',type:'line'}], yFmt:v=>fmtN(v,1)+'%',"),
    ("  panel2:{t:'投資者預託金（兆₩）',series:[{name:'預託金',key:'deposit',color:'--s2',type:'area'}],yFmt:v=>fmtN(v,0)}},",
     "  panel2:{t:'融券餘額（萬張）',series:[{name:'融券餘額',key:'deposit',color:'--s2',type:'area'}],yFmt:v=>fmtN(v,0)}},"),
    # ---- 卡片 fb: 融資淨減 ----
    ("{id:'fb',t:'斷頭賣壓（強制平倉）', d:'散戶繳不出保證金時，券商直接砍倉賣出的金額。斷頭單不看價格、不問基本面——「被動賣盤」最純粹的證據。',",
     "{id:'fb',t:'融資強制去化（單日淨減）', d:'融資餘額單日淨減金額——含主動了結與斷頭；台股斷頭金額無每日公開數據，以淨減作為被動賣壓代理。',"),
    ("下跌自我強化的引擎就在這裡：股價跌 → 保證金不足 → 券商<b>強制砍倉（斷頭）</b> → 賣壓再壓低股價 → 更多人被斷頭。上圖長條飆高＝斷頭潮正在發生；<b>連續數日回落</b>＝最兇的拋壓大概率已過，正是訊號①「技術性賣壓衰竭」等的畫面。下圖比率回答「欠款的人裡有多大比例被砍」——金額會隨市場規模水漲船高，比率更適合跨期比較。（韓文原詞 반대매매，台股俗稱「斷頭」）",
     "下跌自我強化的引擎：股價跌 → 維持率不足 → 追繳/斷頭 → 賣壓再壓低股價。上圖長條飆高＝融資盤集中去化正在發生；<b>連續數日回落</b>＝最兇的拋壓大概率已過，正是訊號①「技術性賣壓衰竭」等的畫面。下圖淨減率（淨減÷前日餘額）剔除規模因素，更適合跨期比較。注意此代理含主動降槓桿，會<b>高估</b>純斷頭金額。"),
    ("  series:[{name:'斷頭金額(億₩)',key:'bandae_amt',color:'--s1',type:'bar'}], yFmt:v=>fmtN(v,0), zero:true,",
     "  series:[{name:'融資淨減(億元)',key:'bandae_amt',color:'--s1',type:'bar'}], yFmt:v=>fmtN(v,0), zero:true,"),
    ("  panel2:{t:'斷頭比率＝斷頭金額 ÷ 散戶未繳款（%，5日均）',series:[{name:'斷頭比率5日均',key:'bandae_ratio_ma',color:'--s6',type:'line'}],yFmt:v=>fmtN(v,1)+'%'}},",
     "  panel2:{t:'融資淨減率＝淨減 ÷ 前日餘額（%，5日均）',series:[{name:'淨減率5日均',key:'bandae_ratio_ma',color:'--s6',type:'line'}],yFmt:v=>fmtN(v,2)+'%'}},"),
    # ---- 卡片 kx ----
    ("{id:'kx',t:'KOSPI 指數與市場應激', d:'指數走勢＋20日年化已實現波動率（VKOSPI 替代，待 KRX 解鎖後切換）。',",
     "{id:'kx',t:'加權指數與市場應激', d:'TAIEX 收盤走勢＋20日年化已實現波動率。',"),
    ("  series:[{name:'KOSPI',key:'kospi_idx',color:'--s1',type:'line'}], yFmt:v=>fmtN(v,0),",
     "  series:[{name:'加權指數',key:'kospi_idx',color:'--s1',type:'line'}], yFmt:v=>fmtN(v,0),"),
    # ---- 卡片 tv ----
    ("  series:[{name:'兩市成交額(兆₩)',key:'turn_val',color:'--s1',type:'bar'}], yFmt:v=>fmtN(v,0), zero:true,",
     "  series:[{name:'成交金額(兆元)',key:'turn_val',color:'--s1',type:'bar'}], yFmt:v=>fmtN(v,2), zero:true,"),
    # ---- 出清進度條 ----
    ("'%</span><span>剩餘超額 '+fmtN(IND.unwind.excess_now,1)+' 兆₩</span></div>';",
     "'%</span><span>剩餘超額 '+fmtN(IND.unwind.excess_now*1e4,0)+' 億元</span></div>';"),
    # ---- 卡片 m 註腳（單位換算 兆→億元）----
    ("   return '本輪加槓桿：基期 '+fmtN(U.baseline,1)+' 兆（'+fmtD(U.baseline_date)+'）→ 峰值 '+fmtN(U.peak,1)+' 兆（'+fmtD(U.peak_date)+'），共 +'+fmtN(added,1)+' 兆；現 '+fmtN(U.current,1)+' 兆＝已回吐 '+fmtN(gave,1)+' 兆、尚餘 '+fmtN(U.excess_now,1)+' 兆 → 出清 <b>'+fmtN(U.U*100,0)+'%</b>（'+fmtN(gave,1)+'÷'+fmtN(added,1)+'）';}},",
     "   return '本輪加槓桿：基期 '+fmtN(U.baseline*1e4,0)+' 億（'+fmtD(U.baseline_date)+'）→ 峰值 '+fmtN(U.peak*1e4,0)+' 億（'+fmtD(U.peak_date)+'），共 +'+fmtN(added*1e4,0)+' 億；現 '+fmtN(U.current*1e4,0)+' 億＝已回吐 '+fmtN(gave*1e4,0)+' 億、尚餘 '+fmtN(U.excess_now*1e4,0)+' 億 → 出清 <b>'+fmtN(U.U*100,0)+'%</b>（'+fmtN(gave*1e4,0)+'÷'+fmtN(added*1e4,0)+'）';}},"),
    # ---- 本期解讀 genComment ----
    ("  const s1='去槓桿壓力指數 '+fmtN(C.score,1)+'，處於'+zoneShort+'。出清進度這樣算：本輪行情中融資餘額從 '+fmtD(U.baseline_date)+' 基期的 '+fmtN(U.baseline,1)+' 兆韓元加到 '+fmtD(U.peak_date)+' 峰值 '+fmtN(U.peak,1)+' 兆，共多加 '+fmtN(added,1)+' 兆槓桿；目前 '+fmtN(U.current,1)+' 兆，已回吐 '+fmtN(gave,1)+' 兆、尚餘 '+fmtN(U.excess_now,1)+' 兆未退出——出清進度 '+fmtN(gave,1)+'÷'+fmtN(added,1)+' ≈ '+(U.U*100).toFixed(0)+'%（100%＝本輪新增槓桿全數退出，非指總融資減半）。';",
     "  const s1='去槓桿壓力指數 '+fmtN(C.score,1)+'，處於'+zoneShort+'。出清進度這樣算：本輪行情中融資餘額從 '+fmtD(U.baseline_date)+' 基期的 '+fmtN(U.baseline*1e4,0)+' 億元加到 '+fmtD(U.peak_date)+' 峰值 '+fmtN(U.peak*1e4,0)+' 億，共多加 '+fmtN(added*1e4,0)+' 億槓桿；目前 '+fmtN(U.current*1e4,0)+' 億，已回吐 '+fmtN(gave*1e4,0)+' 億、尚餘 '+fmtN(U.excess_now*1e4,0)+' 億未退出——出清進度 ≈ '+(U.U*100).toFixed(0)+'%（100%＝本輪新增槓桿全數退出，非指總融資減半）。';",),
    ("  if(P.bandae_amt!=null) ev.push('斷頭（強制平倉）金額處 5 年第 '+Math.round(P.bandae_amt)+' 百分位'+(P.bandae_amt>=70?'，被動賣壓仍強':(P.bandae_amt<=40?'，斷頭潮已明顯退坡':'，賣壓自高點回落中')));",
     "  if(P.bandae_amt!=null) ev.push('融資單日淨減金額處 5 年第 '+Math.round(P.bandae_amt)+' 百分位'+(P.bandae_amt>=70?'，去化賣壓仍強':(P.bandae_amt<=40?'，集中去化已明顯退坡':'，賣壓自高點回落中')));"),
    ("  if(P.margin_dep!=null) ev.push('融資/預託金比處第 '+Math.round(P.margin_dep)+' 百分位'+(P.margin_dep<=40?'，散戶現金緩衝相對充裕':(P.margin_dep>=70?'，槓桿相對子彈偏緊':'')));",
     "  if(P.margin_val!=null) ev.push('融資消化天數處第 '+Math.round(P.margin_val)+' 百分位'+(P.margin_val<=40?'，市場流動性足以吸收融資盤':(P.margin_val>=70?'，融資盤相對流動性偏重、去化承壓':'')));"),
    ("  if(E.deposit_peak&&E.deposit_peak[0]&&IND.latest.deposit!=null){const dp=E.deposit_peak; const chg=100*(IND.latest.deposit/dp[0]-1); if(chg<-10) ev.push('預託金自 '+fmtD(dp[1]).slice(5)+' 高點 '+fmtN(dp[0],0)+' 兆縮至 '+fmtN(IND.latest.deposit,0)+' 兆（'+fmtN(chg,1)+'%），場內現金正在流失');}",
     ""),
    ("斷頭金額5日均 '+fmtN(E.bandae_amt_ma,0)+' 億，較 '", "融資淨減5日均 '+fmtN(E.bandae_amt_ma,0)+' 億，較 '"),
    ("  if(IND.signals.s1.status!=='green') miss.push('①技術性賣壓衰竭（強平與融資降速回落）');",
     "  if(IND.signals.s1.status!=='green') miss.push('①技術性賣壓衰竭（融資淨減與降速回落）');"),
    ("  if(IND.signals.s2.status!=='green') miss.push('②外部催化劑落地（大型雲廠商財報）');",
     "  if(IND.signals.s2.status!=='green') miss.push('②外部催化劑落地（AI資本開支/台積電法說）');"),
    ("  const s4=(IND.etf&&IND.etf.enabled)?null:'註：槓桿 ETF 分項尚未接入，上述出清進度僅計信用融資口徑。';",
     "  const s4='註：口徑僅上市信用融資，不含上櫃、借券賣出與股票質押；淨減代理含主動降槓桿成分。';"),
    # ---- genVerdict ----
    ("  let watch='之後每天只需盯兩條線：<b>斷頭金額</b>與<b>融資餘額</b>——兩條都走平之日，就是出清接近完成之時。';",
     "  let watch='之後每天只需盯兩條線：<b>融資單日淨減</b>與<b>融資餘額</b>——兩條都走平之日，就是出清接近完成之時。';"),
    ("""  if(E.deposit_peak&&E.deposit_peak[0]&&IND.latest.deposit!=null){
    const chg=100*(IND.latest.deposit/E.deposit_peak[0]-1);
    if(chg<-10) watch+=' 另留意：散戶預託金自高點已流失 '+fmtN(-chg,0)+'%，反彈的燃料在變薄。';
  }""", ""),
    # ---- ETF 卡 → 口徑說明卡 ----
    ("  d.append(el('h3',null,'槓桿ETF出清程度（三星電子／SK海力士 單股2倍）'));",
     "  d.append(el('h3',null,'口徑與侷限'));"),
    ("    d.append(el('div','desc','市場焦點指標：追蹤三星電子/SK海力士的單股2倍槓桿ETF共14檔，截至7/8已有13檔跌破2萬韓元發行價；SK海力士槓桿ETF規模自峰值167億美元縮至78億（-53%）。'));",
     "    d.append(el('div','desc','台股版 v1 口徑：上市（TWSE）信用交易融資/融券，日頻。未涵蓋：上櫃（TPEx）融資、借券賣出、股票質押、權證與期選槓桿。'));"),
    ("    const dt=el('details','how'); dt.innerHTML='<summary>怎麼看這張圖</summary><div class=\"hb\">槓桿 ETF 每日再平衡會「越漲越買、越跌越賣」，規模夠大時足以主導三星電子／SK海力士的定價（極端交易日曾占個股總成交約六成）。屆時看兩個數：<b>AUM 距峰值萎縮幅度</b>＝已釋放的風險；<b>距 4 月底基期的剩餘規模</b>＝還沒退出的槓桿倉。規模停止快速萎縮，是訊號①「技術性賣壓衰竭」成立的必要條件之一。</div>'; d.append(dt);",
     "    const dt=el('details','how'); dt.innerHTML='<summary>已知的估計偏誤</summary><div class=\"hb\">①「融資淨減」含主動了結，會<b>高估</b>斷頭壓力；②市值以加權指數等比例代理，忽略增資/新上市，比率型指標長期有輕微漂移；③僅上市口徑，上櫃融資盤（投機性更強）未計入，去化劇烈度可能<b>低估</b>。</div>'; d.append(dt);",),
    ("    d.append(el('div','pending','⏳ 此模組待 KRX Data Marketplace 登入後自動補齊（逐檔規模淨值歷史、跌破發行價家數、再平衡衝擊估算）。目前綜合指數未計入ETF分項（權重已重新歸一）。'));",
     "    d.append(el('div','pending','⏳ 待接入：上櫃（TPEx）融資餘額、大盤實際總市值、借券賣出餘額。接入後比率型指標將改用真實市值。'));"),
    # ---- 方法論區塊整段重寫 ----
    ("  '<h4>綜合壓力指數（0-100）</h4>四大維度九分項：槓桿水位（融資餘額5年百分位 '+w.lvl_margin_pctl+'、融資/市值 '+w.lvl_mcap_pctl+'、融資/預託金 '+w.lvl_dep_pctl+'）＋出清進度（未出清比例 '+w.unwind_remaining+'、融資5日動能 '+w.momentum+'）＋被動賣壓（斷頭金額 '+w.forced_amt_pctl+'、斷頭比率 '+w.forced_ratio_pctl+'）＋市場應激（波動率 '+w.vol_pctl+'、成交熱度 '+w.turnover_pctl+'）。'+",
     "  '<h4>綜合壓力指數（0-100）</h4>四大維度九分項：槓桿水位（融資餘額5年百分位 '+w.lvl_margin_pctl+'、融資/市值(代理) '+w.lvl_mcap_pctl+'、融資消化天數 '+w.lvl_liq_pctl+'）＋出清進度（未出清比例 '+w.unwind_remaining+'、融資5日動能 '+w.momentum+'）＋被動賣壓（融資淨減金額 '+w.forced_amt_pctl+'、淨減率 '+w.forced_ratio_pctl+'）＋市場應激（波動率 '+w.vol_pctl+'、成交熱度 '+w.turnover_pctl+'）。'+"),
    ("  '<h4>數據源與時滯</h4>KOFIA 金融投資協會綜合統計（신용거래융자·투자자예탁금·미수금·반대매매·兩市指數/成交/市值，日度，1998至今）；KRX Data Marketplace（槓桿ETF，待啟用）。波動率以20日已實現波動率年化替代 VKOSPI。<b>回撤口徑</b>：距高點一律以「收盤對收盤」計（KOFIA 僅發布每日收盤指數）；盤中高點通常更高（例如 2026/6/19 盤中一度 9,385 vs 最高收盤 9,114），盤中口徑待 KRX 指數 OHLC 接入後提供切換。<b>公布時滯</b>：指數/成交額為 KRX 當日收盤後入庫；信用融資/預託金/斷頭數據為 KOFIA T+1 公布（實測常於次日下午更新），故信用類截止日通常比行情晚 1-2 個交易日，圖上融資線尾端較指數線短屬正常。'+",
     "  '<h4>數據源與時滯</h4>FinMind TaiwanStockTotalMarginPurchaseShortSale（上市全市場融資/融券餘額與張數，源自 TWSE MI_MARGN，日度）＋ TWSE FMTQIK（加權指數收盤、成交金額，月批次）。波動率＝TAIEX 收盤 20 日已實現波動率年化。<b>市值代理</b>：每日總市值以加權指數×常數等比例代理（比率型指標的百分位不受常數影響，但忽略增資/新上市造成的長期漂移）。<b>回撤口徑</b>：收盤對收盤。<b>時滯</b>：融資數據 T+1 彙整，融資線尾端較指數線短屬正常。'+"),
    ("  '<h4>訊號判定</h4>①技術性賣壓衰竭＝斷頭金額5日均百分位&lt;50 且 融資5日跌幅&lt;1%（ETF啟用後加入規模萎縮速度）；②③為人工旗標，依新聞更新。'+",
     "  '<h4>訊號判定</h4>①技術性賣壓衰竭＝融資淨減5日均百分位&lt;50 且 融資5日跌幅&lt;1%；②③為人工旗標，於 compute_indicators_tw.py 的 CONFIG 更新。'+"),
    ("  '<h4>韓文術語對照</h4>신용거래융자＝信用融資（散戶向券商借錢買股）；투자자예탁금＝預託金（散戶帳上待投現金）；미수금＝未繳款（散戶欠券商的交割/保證金款項）；반대매매＝斷頭（券商強制平倉賣出）。';",
     "  '<h4>與韓版指標對照</h4>신용거래융자→融資餘額；반대매매（斷頭）→融資單日淨減（代理，含主動了結）；투자자예탁금（預託金）→無台股日頻等價數據，計分分項改用融資消化天數（融資餘額÷日成交額）。';"),
    ("  $('#foot').innerHTML='指標定義與權重可在 compute_indicators.py 的 CONFIG 調整；KOFIA 口徑僅涵蓋場內信用融資（不含槓桿 ETF 內含槓桿、股票質押與場外配資），信用數據為 T+1 公布。';",
     "  $('#foot').innerHTML='台股版改自 <a href=\"https://kidd0368.github.io/\">kidd0368 韓版</a>；指標定義與權重在 compute_indicators_tw.py 的 CONFIG 調整。口徑僅上市信用交易（不含上櫃/借券/質押/衍生品槓桿），融資數據 T+1。僅供研究，非投資建議。';"),
]

for old, new in PAIRS:
    assert src.count(old) == 1, "NOT FOUND or DUP: " + old[:60]
    src = src.replace(old, new)

dst = os.path.join(HERE, "template_tw.html")
io.open(dst, "w", encoding="utf-8").write(src)
print("OK →", dst, len(src), "bytes,", len(PAIRS), "patches applied")
