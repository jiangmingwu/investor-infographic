#!/usr/bin/env python3
"""JPMorgan Chase 摩根大通 · FY2025 / 当前估值经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
JPM_BLUE = "#002D72"
JPM_GOLD = "#C8A951"
JPM_GREEN = "#4A6B3B"
JPM_WINE = "#8B3A4E"

DATA = {
    "TITLE": "摩根大通经营全解析",
    "SUBTITLE": "JPMorgan Chase · Universal Bank + Fortress Balance Sheet",
    "UPDATE_DATE": "最新口径：FY2025 + 当前估值",

    "COMPANY_PROFILE": {
        "公司全称": "JPMorgan Chase & Co.",
        "上市代码": "NYSE: JPM",
        "市值排名": "全球第 14 名附近（约 $8,058 亿）",
        "CEO": "Jamie Dimon（2005 至今）",
        "总部": "New York City",
        "核心业务": "消费银行 + 投行/市场 + 资产财富管理 + 支付",
        "员工": "约 31.9 万人",
        "总资产": "约 $4.4 万亿",
        "CET1": "14.5%",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 净营收": "$1,824 亿（YoY +3%）",
        "FY2025 拨备前利润": "$868 亿（YoY +1%）",
        "FY2025 净利润": "$570 亿（YoY -2%）",
        "FY2025 EPS": "$20.02（YoY +1%）",
        "FY2025 ROTCE": "20%",
        "FY2025 技术/通信/设备费": "$110 亿（YoY +12%）",
        "当前市值": "约 $8,058 亿",
        "PE / PB": "约 14.4× / 2.34×",
        "年度股息": "$6.00/股 · 股息率约 2.0%",
    },

    "CAPITAL_AND_ROI": [
        ("ROI / ROIC", "FY25 ROTCE 20%", "银行以资本回报率衡量更合适；StockAnalysis 对银行 ROIC 标为 n/a。"),
        ("2026E CapEx", "未披露/不可比", "银行不按工业 CapEx 指引经营；可跟踪技术、网点和风险加权资产投入。"),
        ("股东分红", "$6.00/股 · 2.0%", "当前年化股息；FY2025 年报披露普通股股息 $5.80/股。"),
    ],

    "SEGMENTS_LABEL": "业务分部净营收（FY2025）",
    "BUSINESS_SEGMENTS": [
        ("1", "CIB 投行/市场", "42%", "$785亿", "+12%", "增长", "交易+投行"),
        ("2", "CCB 消费银行", "41%", "$760亿", "+6%", "稳健", "零售+信用卡"),
        ("3", "AWM 资管财富", "13%", "$241亿", "+12%", "增长", "AUM 规模"),
        ("4", "Corporate", "4%", "$70亿", "-60%", "波动", "投资/对冲"),
    ],

    "REVENUE_MIX": [
        ("CIB 投行/市场", "42%"),
        ("CCB 消费银行", "41%"),
        ("AWM 资管财富", "13%"),
        ("Corporate", "4%"),
    ],

    "MOVES_LABEL": "关键战略布局",
    "STRATEGIC_MOVES": [
        ("规模", "全能银行平台", "零售、支付、投行、市场与财富管理在同一客户网络里交叉变现。", JPM_BLUE),
        ("资本", "CET1 14.5%", "监管资本保持厚垫，支撑危机期进攻和高股东派现。", JPM_GREEN),
        ("技术", "技术/通信/设备费 $110 亿", "银行业越来越像技术公司，AI、支付、风控和移动端是投入重点。", ORANGE),
        ("财富", "First Republic 高净值客户沉淀", "私人银行与财富管理把存款、贷款、投资服务绑定起来。", JPM_GOLD),
        ("风险", "商业地产和信用周期", "银行最大的敌人不是增长慢，而是信用损失突然变大。", RED),
    ],

    "MOAT": [
        ("低成本资金", "$2T+ 存款基础让资金成本长期低于许多同业。"),
        ("市场份额", "2025 全球投行业务费用份额 8.4%，保持 #1。"),
        ("危机声誉", "强资本与交易执行力，让它能在压力周期接手资产。"),
        ("技术规模", "每年百亿美元级技术投入，风控、支付、移动银行形成复利。"),
        ("客户网络", "家庭、企业、机构和高净值客户在同一体系内流动。"),
    ],

    "KEY_METRICS": [
        ("FY25 净营收", "$1,824 亿"),
        ("拨备前利润", "$868 亿"),
        ("净利润", "$570 亿"),
        ("EPS", "$20.02"),
        ("ROTCE", "20%"),
        ("ROE", "17%"),
        ("CET1", "14.5%"),
        ("技术费用", "$110 亿"),
        ("当前市值", "$8,058 亿"),
        ("PE", "约 14.4×"),
        ("每股股息", "$6.00"),
        ("股息率", "2.0%"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "ROTCE 20%", "在大银行监管框架下仍保持高资本回报。"),
        ("亮点", "CIB +12%", "市场交易和投行业务成为 FY2025 增长主力。"),
        ("亮点", "技术投入扩大", "技术/通信/设备费 $110 亿，同比 +12%。"),
        ("风险", "信用成本上升", "FY2025 信用损失拨备 $142 亿，同比 +33%。"),
        ("风险", "净息收入周期", "降息周期可能压缩存款利差。"),
        ("风险", "大银行监管", "资本、流动性和消费者业务监管会压低估值弹性。"),
    ],

    "QUOTES_LABEL": "管理层观点",
    "QUOTES": [
        "「Fortress balance sheet 是我们的经营前提。」— JPMorgan 体系",
        "「我们必须准备好应对各种环境。」— Jamie Dimon",
        "「规模只有在风险纪律之上才有价值。」— 年报口径整理",
    ],

    "DATA_SOURCE": "JPMorgan Chase 2025 Annual Report / 4Q25 Earnings Release / Financial Supplement / StockAnalysis",
    "FOOTER_LINES": [
        "经营数据：JPMorgan Chase 2025 Annual Report / 4Q25 Release / Financial Supplement",
        "财年口径：FY2025，2025年1-12月",
        "同比口径：FY2025 vs FY2024；净营收 +3%，拨备前利润 +1%，净利润 -2%，技术/通信/设备费 +12%",
        "行情数据：StockAnalysis JPM，查看：2026年5月18日；股价 $300.73，市值约 $805.81B，PE 14.41×，PB 2.34×",
        "ROI口径：银行采用 ROTCE；JPM FY2025 ROTCE 20%，StockAnalysis 银行 ROIC 为 n/a",
        "2026 CapEx口径：银行不披露可比工业 CapEx；以技术投入、网点和 RWA 为经营投入线索",
        "股东分红：StockAnalysis Dividend / JPMorgan 2025 Annual Report，查看：2026年5月；年化 $6.00/股，FY2025 普通股股息 $5.80/股",
        "管理文化：JPMorgan Careers Benefits / Business Principles / Code of Conduct / Jamie Dimon 2025 CEO Letter，核查：2026年5月",
        "货币口径：JPM 以 USD 报告；图中金额均为 USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
