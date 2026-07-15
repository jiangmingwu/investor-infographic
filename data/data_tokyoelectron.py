#!/usr/bin/env python3
"""Tokyo Electron 东京电子 · FY2026 operating analysis data."""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
TEL_BLUE = "#005BAC"
TEL_CYAN = "#00A0E9"
TEL_NAVY = "#153B6F"
TEL_GOLD = "#C4963C"
TEL_GREEN = "#4A7C59"

DATA = {
    "TITLE": "东京电子经营全解析",
    "SUBTITLE": "Tokyo Electron (TSE:8035) · 半导体设备 · 涂胶显影 + 刻蚀 + 沉积 + 清洗",
    "UPDATE_DATE": "最新口径：FY2026 官方业绩 + 2026-05-31 修正版",

    "COMPANY_PROFILE": {
        "公司全称": "Tokyo Electron Ltd.",
        "上市代码": "TSE:8035 / OTC:TOELY",
        "成立": "1963 年 · 总部东京赤坂",
        "CEO": "Toshiki Kawai",
        "核心业务": "半导体生产设备 SPE + Field Solutions",
        "员工与网络": "20,812 人 · 18 个国家/地区 · 102 个站点",
        "核心产品": "Coater/developer、Etch、Deposition、Cleaning、Test",
        "客户位置": "DRAM / NAND / Foundry / Logic 前沿晶圆厂",
        "当前市值": "约 $1,411 亿 美元（StockAnalysis，2026-05）",
        "当前股价": "约 $313/股（JPY 49,830）",
    },

    "FINANCIAL_SUMMARY": {
        "FY2026 营收": "约 $153.3 亿 美元（YoY +0.5%）",
        "FY2026 经营利润": "约 $39.2 亿 美元（YoY -10.4%）",
        "FY2026 经营现金流": "约 $33.9 亿 美元（YoY -7.3%）",
        "FY2026 净利润": "约 $36.0 亿 美元（YoY +5.6%）",
        "当前市值": "约 $1,411 亿 美元",
        "当前 PE": "约 39.8×",
        "Forward PE": "约 32.6×",
        "FY2026 ROE": "29.6%",
        "FY2026 自由现金流": "约 $20.3 亿 美元（OCF - CapEx）",
        "FY2026 CapEx": "约 $13.6 亿 美元",
        "2026E CapEx": "约 $11.9 亿 美元（FY2027 公司计划）",
        "FY2026 R&D": "约 $17.4 亿 美元",
        "FY2026 股东回报": "约 $27.4 亿 美元（股息+回购）",
        "年度股息": "约 $3.94/股（JPY 628/股）",
    },

    "CAPITAL_AND_ROI": [
        ("ROI / ROE", "ROE 29.6%", "官方 FY2026 ROE；半导体设备周期性强，需结合订单、毛利率、CapEx 和客户投资节奏看。"),
        ("2026E CapEx", "约 $11.9 亿", "公司 FY2027 CapEx 计划 JPY 1,900 亿；对应 2026年4月-2027年3月财年。"),
        ("股东分红", "$3.94/股 · 派息约50%", "FY2026 年度股息 JPY 628/股；公司政策为净利润约 50% payout，并可灵活回购。"),
        ("股东回报", "约 $27.4 亿", "FY2026 现金股息 JPY 2,716 亿 + 回购 JPY 1,500 亿，合计约为净利润 73%。"),
        ("现金与资产", "现金约 $31.8 亿", "FY2026 期末现金及等价物 JPY 5,054 亿，权益比率 71.5%。"),
    ],

    "SEGMENTS_LABEL": "业务结构（FY2026，SPE 新设备 + 服务）",
    "BUSINESS_SEGMENTS": [
        ("1", "Etch 刻蚀系统", "36%", "$40.1亿", "产品占比", "主力", "SPE新设备"),
        ("2", "Coater/Developer", "28%", "$31.2亿", "产品占比", "强项", "涂胶显影"),
        ("3", "Deposition 沉积", "20%", "$22.3亿", "产品占比", "扩张", "薄膜设备"),
        ("4", "Cleaning 清洗", "9%", "$10.0亿", "产品占比", "稳定", "良率环节"),
        ("5", "Field Solutions", "约27%", "$38.1亿", "估算", "复利", "服务/备件"),
    ],

    "REVENUE_MIX": [
        ("Etch 刻蚀", "36%"),
        ("Coater/Developer", "28%"),
        ("Deposition 沉积", "20%"),
        ("Cleaning 清洗", "9%"),
        ("Wafer Prober/Other", "7%"),
    ],

    "MOVES_LABEL": "2026-2027 关键战略布局",
    "STRATEGIC_MOVES": [
        ("AI", "FY2027 H1 设备销售预计 +41%", "公司预计 AI server demand 推动 DRAM 和 leading-edge logic 发货。", TEL_BLUE),
        ("研发", "FY2027 R&D 计划约 $20.7 亿", "研发继续加码，重点围绕刻蚀、沉积、涂胶显影、清洗和先进封装。", TEL_CYAN),
        ("产能", "宫城/岩手/熊本多基地扩建", "Miyagi、Iwate、Kumamoto 新楼/物流中心强化生产和工艺开发。", TEL_GOLD),
        ("产品", "刻蚀 + 涂胶显影双核心", "FY2026 SPE 新设备中 Etch 36%、Coater/developer 28%。", TEL_NAVY),
        ("服务", "Field Solutions 单季约 ¥1,616 亿", "装机维护、备件、升级形成高粘性服务收入。", TEL_GREEN),
        ("风险", "客户 CapEx 周期波动", "半导体设备受大客户投资周期、地缘管制和存储价格影响很大。", RED),
    ],

    "MOAT": [
        ("涂胶显影 90% 份额", "TEL 产品页披露 Coater/Developer 整体市场约 90% 份额，High-NA 工艺接近 100%；FY2026 SPE 新设备占比约 28%。"),
        ("刻蚀全球第二", "TEL 产品页披露 Dry Etch 全球第二；FY2026 SPE 新设备中 Etch 占比约 36%，是收入占比最大的产品组。"),
        ("清洗全球第二", "TEL 产品页披露 Wafer Cleaning 全球第二；清洗设备虽占比约 9%，但直接影响先进制程良率。"),
        ("多工艺组合", "Etch、Deposition、Cleaning、Test 与 Coater/Developer 覆盖多道关键制程，单一客户扩产可带动多类设备订单。"),
        ("Field Solutions 装机复利", "FY2026 Q4 Field Solutions 销售约 JPY 1,616 亿，装机维护、备件、升级提高客户粘性。"),
        ("研发与工艺开发网络", "FY2026 R&D 约 $17.4 亿，FY2027 计划约 $20.7 亿；宫城/熊本等工艺开发基地继续扩建。"),
    ],

    "KEY_METRICS": [
        ("FY26 营收", "$153.3 亿"),
        ("营收同比", "+0.5%"),
        ("经营利润", "$39.2 亿"),
        ("经营利润同比", "-10.4%"),
        ("经营现金流", "$33.9 亿"),
        ("净利润", "$36.0 亿"),
        ("ROE", "29.6%"),
        ("FY26 CapEx", "$13.6 亿"),
        ("2026E CapEx", "$11.9 亿"),
        ("R&D", "$17.4 亿"),
        ("年度股息", "$3.94/股"),
        ("当前市值", "$1,411 亿"),
        ("PE", "39.8×"),
        ("Forward PE", "32.6×"),
        ("员工", "20,812 人"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "AI 服务器拉动 FY2027 H1", "公司预计 FY2027 H1 新设备销售同比 +41%，DRAM 与先进逻辑增量在 2026 下半年发货。"),
        ("亮点", "ROE 仍高达 29.6%", "即使 FY2026 经营利润下滑，净利润与资本回报仍处高位。"),
        ("亮点", "涂胶显影近垄断", "TEL 官方披露 Coater/Developer 整体约 90% 份额，High-NA 工艺接近 100%。"),
        ("风险", "设备周期波动", "客户晶圆厂 CapEx 如果延后，TEL 营收和订单会被放大影响。"),
        ("风险", "估值已较高", "当前 PE 约 39.8×，Forward PE 约 32.6×，市场已经计入 AI 设备周期回暖。"),
        ("风险", "区域与地缘", "中国、台湾、韩国、美国客户投资和出口管制都会影响订单节奏。"),
    ],

    "QUOTES_LABEL": "官方披露要点",
    "QUOTES": [
        "FY2026：营收 JPY 2.4435 万亿、经营利润 JPY 6,249 亿、ROE 29.6%。",
        "FY2027 H1：公司预计营收 JPY 1.57 万亿、经营利润 JPY 4,310 亿。",
        "FY2027 CapEx 计划 JPY 1,900 亿，R&D 计划 JPY 3,300 亿。",
        "股东政策：分红约为净利润 50%，并可灵活回购。",
    ],

    "DATA_SOURCE": "Tokyo Electron FY2026 Results / FY2026 Q4 Presentation / Company Info / StockAnalysis / Exchange-Rates.org",
    "FOOTER_LINES": [
        "经营数据：Tokyo Electron FY2026 Results / FY2026 Q4 Presentation，FY2026: 2025年4月-2026年3月",
        "同比口径：FY2026 vs FY2025；营收 +0.5%，经营利润 -10.4%，经营现金流 -7.3%，净利润 +5.6%",
        "行情数据：StockAnalysis TYO:8035，查看：2026年5月31日；页面延迟行情股价 JPY 49,830，市值 JPY 22.49T，PE 39.84×，Forward PE 32.56×",
        "ROI口径：官方 ROE 29.6%；自由现金流按 OCF - CapEx 近似；半导体设备需结合周期观察",
        "2026 CapEx口径：FY2027 公司计划 JPY 1,900亿，期间 2026年4月-2027年3月；非自然年单年指引",
        "股东分红：FY2026 年度股息 JPY 628/股，派息率约 50%；另回购 JPY 1,500亿",
        "护城河数据：Coater/Developer 90% 与 High-NA 接近 100%、Etch/清洗全球第二来自 TEL Product 页面；产品结构来自 FY2026 Q4 Presentation",
        "管理文化：TEL Corporate Principles / TEL Values / Human Resource / Company Info，核查：2026年5月",
        "汇率口径：Exchange-Rates.org，2026年5月27日，1 USD=159.379 JPY；图中金额均为 USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
