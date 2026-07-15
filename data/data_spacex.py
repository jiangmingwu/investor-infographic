#!/usr/bin/env python3
"""SpaceX · FY2025 / IPO 2026 operating analysis data."""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
SPX_NAVY = "#16324F"
SPX_BLUE = "#1D5E95"
SPX_GOLD = "#C69234"
SPX_CYAN = "#2E9BB5"
SPX_RED = "#A84A4A"
SPX_GREEN = "#4A7A4C"

DATA = {
    "TITLE": "SpaceX 经营全解析",
    "SUBTITLE": "Space Exploration Technologies · Space + Starlink + AI Infrastructure",
    "UPDATE_DATE": "最新口径：S-1/A 2026-06-03 + IPO路演材料 + FY2025",

    "COMPANY_PROFILE": {
        "公司全称": "Space Exploration Technologies Corp.",
        "拟上市代码": "Nasdaq / Nasdaq Texas: SPCX",
        "IPO条款": "$135/股，发行约 5.556 亿股，拟募资约 $750 亿",
        "创始人/CEO": "Elon Musk",
        "COO": "Gwynne Shotwell",
        "总部": "Starbase, Texas",
        "核心业务": "可复用火箭 + Starlink卫星互联网 + AI算力基础设施",
        "员工": "超过 22,000 名全职员工",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 营收": "$186.74 亿（YoY +33.2%）",
        "FY2025 经营亏损": "$-25.89 亿（GAAP）",
        "FY2025 经营现金流": "$67.85 亿（YoY +17.5%）",
        "FY2025 净亏损": "$-49.37 亿（GAAP）",
        "IPO隐含市值": "约 $1.69 万亿",
        "PE / Forward PE": "N.M. / N.A.",
    },

    "CAPITAL_AND_ROI": [
        (
            "ROI / ROIC",
            "N.M.；经营利润率 -13.9%",
            "FY2025 GAAP经营亏损 $25.89亿，重投资与AI并入口径下标准ROIC为负且不可比。",
        ),
        (
            "2026E CapEx",
            "未披露；Q1已 $101.07亿",
            "公司未给2026全年CapEx指引；S-1披露Q1 2026 CapEx $101.07亿，FY2025 CapEx $207.37亿。",
        ),
        (
            "股东回报",
            "不派现金股息",
            "S-1称可预见未来不派现金股息；IPO为100% primary，募资用于AI算力、发射设施、卫星星座扩张等。",
        ),
        (
            "IPO价格",
            "$135/股；净募资约 $745亿",
            "发行约5.556亿股；基础股本口径隐含股权价值约 $1.69万亿，未包含全部潜在稀释项。",
        ),
    ],

    "SEGMENTS_LABEL": "业务分部收入（FY2025）",
    "BUSINESS_SEGMENTS": [
        ("1", "Connectivity / Starlink", "61.0%", "$113.87亿", "+49.8%", "赚钱", "EBITDA $71.68亿"),
        ("2", "Space 发射业务", "21.9%", "$40.86亿", "+7.6%", "基础", "质量入轨80%+"),
        ("3", "AI / X / Grok", "17.1%", "$32.01亿", "+22%+", "重投", "经营亏损$63.55亿"),
    ],

    "REVENUE_MIX": [
        ("Connectivity / Starlink", "61.0%"),
        ("Space 发射业务", "21.9%"),
        ("AI / X / Grok", "17.1%"),
    ],

    "MOVES_LABEL": "关键战略布局",
    "STRATEGIC_MOVES": [
        ("IPO", "$135/股，预计6月11日定价", "Nasdaq / Nasdaq Texas: SPCX，预计6月12日开始交易。", SPX_GOLD),
        ("Starship", "H2 2026 开始轨道载荷", "V3星链、移动直连和AI compute satellites都依赖Starship降低运力成本。", SPX_BLUE),
        ("Starlink", "V3带宽/发射 >20倍", "V3卫星计划每颗1,024Gbps、每次发射61,000Gbps带宽。", SPX_CYAN),
        ("AI", "1.0GW nameplate compute", "COLOSSUS/COLOSSUS II 构成千兆瓦级AI训练集群。", PURPLE),
        ("风险", "估值与控制权很集中", "Musk IPO后预计约82.4%投票权，Class A投资者治理权有限。", SPX_RED),
    ],

    "MOAT": [
        ("全球入轨质量 80%+", "路演材料称SpaceX自2023年以来贡献全球入轨质量80%+，是其发射业务最硬的份额证据。"),
        ("Falcon 2025发射 165次", "2025年Falcon家族发射165次，其中95%+任务使用至少一枚复用助推器，形成高频低成本飞轮。"),
        ("Starlink 10.3M用户", "截至2026年3月31日，Starlink约1,030万订户、覆盖164个国家/地区，拥有9,600+在轨卫星。"),
        ("V3每次发射带宽 >20倍", "V3星链每次发射带宽计划61,000Gbps，对比V2的2,600Gbps，容量扩张是Starlink第二曲线。"),
        ("Dragon载人78人次", "自2020年以来Dragon 50+次到访ISS、运送78名宇航员，是NASA认证能力的信用资产。"),
        ("AI算力1.0GW", "AI业务FY2025收入$32.01亿但经营亏损$63.55亿；这是潜在上限，也是当前估值风险来源。"),
    ],

    "KEY_METRICS": [
        ("FY25营收", "$186.74亿"),
        ("Adj. EBITDA", "$65.84亿"),
        ("经营亏损", "$-25.89亿"),
        ("净亏损", "$-49.37亿"),
        ("经营现金流", "$67.85亿"),
        ("FY25 CapEx", "$207.37亿"),
        ("Q1 2026 CapEx", "$101.07亿"),
        ("IPO募资", "$750亿"),
        ("入轨份额", "80%+"),
        ("Starlink订户", "1030万"),
        ("发射次数", "2025年165次"),
        ("Musk投票权", "约82.4%"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "Starlink是现金引擎", "FY2025收入$113.87亿、经营利润$44.23亿、Adj. EBITDA $71.68亿。"),
        ("亮点", "发射垂直整合", "可复用火箭降低成本，支撑Starlink和未来AI/空间制造业务。"),
        ("亮点", "经营现金流为正", "FY2025经营现金流$67.85亿，但CapEx更高。"),
        ("风险", "GAAP仍净亏损", "FY2025净亏损$49.37亿，AI并入口径放大亏损和不确定性。"),
        ("风险", "估值极高", "IPO隐含PS约90倍；需要Starlink、Starship、AI三条线长期兑现。"),
        ("风险", "控制权集中", "Class B每股10票，Musk预计控制约82.4%投票权。"),
    ],

    "QUOTES_LABEL": "公司使命与管理方法",
    "QUOTES": [
        "「make life multiplanetary, understand the true nature of the universe, and extend the light of consciousness to the stars」— SpaceX IPO路演材料",
        "「The Algorithm」：让需求更不蠢、删除、优化、加速、再自动化 — S-1术语定义",
        "投资判断的核心：业务质量罕见，但 IPO 价格已经把 Starlink、Starship 和 AI 的长期想象提前压进估值。",
    ],

    "DATA_SOURCE": "SEC S-1/A 2026-06-03 / SEC Free Writing Prospectus 2026-06-04 / SpaceX IPO materials",
    "FOOTER_LINES": [
        "经营数据：SpaceX S-1/A（SEC 2026-06-03），FY2025: 2025年1-12月；Q1 2026: 2026年1-3月",
        "IPO/估值：SEC FWP 2026-06-04；发行5.556亿股，$135/股，预计2026年6月11日定价、6月12日交易；基础股本隐含约$1.69T",
        "ROI口径：FY2025经营亏损$2.589B，经营利润率-13.9%；重投资与AI并入口径下标准ROIC为负且不可比",
        "2026 CapEx口径：公司未披露全年指引；S-1披露Q1 2026 CapEx $10.107B、FY2025 CapEx $20.737B",
        "股东分红：S-1 Dividend Policy，预计可预见未来不派现金股息；回报主要来自股价上涨而非现金分红",
        "管理文化：S-1 Human Capital / SEC FWP Mission-Driven Culture，核查：2026年6月9日",
        "货币口径：SpaceX以USD披露；图中金额均为USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
