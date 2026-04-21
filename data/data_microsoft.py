#!/usr/bin/env python3
"""微软 Microsoft FY2025 年报 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
MS_BLUE = "#0078D4"

DATA = {
    "TITLE": "微软经营全解析",
    "SUBTITLE": "Microsoft Corp. (NASDAQ: MSFT) · AI 云巨头 · OpenAI 最大股东",
    "UPDATE_DATE": "数据更新:FY2025 年报 (2025-07-30 发布) · FY25=2024.07-2025.06",

    "COMPANY_PROFILE": {
        "公司全称": "Microsoft Corporation",
        "上市代码": "NASDAQ: MSFT",
        "创立": "1975 年 · 比尔·盖茨/保罗·艾伦 创立于新墨西哥州",
        "董事长": "John W. Thompson",
        "CEO": "Satya Nadella",
        "CFO": "Amy Hood",
        "核心业务": "Azure 云 + Office 365 + Windows + GitHub + LinkedIn + Xbox",
        "员工": "约 22.8 万人",
        "总部": "华盛顿州雷德蒙德 Redmond, WA",
        "最新股价 / 市值": "约 $475 / ¥3.52 万亿美元 (2026-04)",
        "最新 PE (TTM)": "约 36×",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 全年营收": "$2,817 亿 (+15% YoY)",
        "FY2025 净利润": "$1,018 亿 (+18% YoY)",
        "FY2025 营业利润率": "约 45%",
        "Q4 FY25 营收": "$764 亿 (+18% YoY)",
        "Azure 全年增速": "约 +33% (其中 AI 贡献 ~16pp)",
        "Intelligent Cloud 全年": "$1,150 亿 (+22%)",
        "Productivity 全年": "$1,208 亿 (+13%)",
        "More Personal Computing": "$551 亿 (+7%)",
        "FY25 经营现金流": "约 $1,300 亿",
        "FY25 资本开支": "约 $880 亿 (+80%)",
        "FY25 回购 + 分红": "约 $600 亿",
    },

    "SEGMENTS_LABEL": "业务分部营收(FY2025 全年)",
    "BUSINESS_SEGMENTS": [
        ("1", "Intelligent Cloud (Azure)", "41%", "$1,150亿", "+22%", "▲爆发", "Azure+AI 占核心"),
        ("2", "Productivity & Business", "43%", "$1,208亿", "+13%", "▲稳增", "M365 Copilot/LinkedIn"),
        ("3", "More Personal Computing", "20%", "$551亿", "+7%", "▲稳增", "Windows/Xbox/Surface"),
    ],

    "REVENUE_MIX": [
        ("Productivity 生产力", "42.9%"),
        ("Intelligent Cloud", "40.8%"),
        ("Personal Computing", "19.6%"),
    ],

    "MOVES_LABEL": "2025-2026 关键战略动作",
    "STRATEGIC_MOVES": [
        ("AI", "Azure AI 独占 OpenAI 模型接口", "ChatGPT/GPT-5/Sora 全部在 Azure 上运行,AI Capex 护城河", MS_BLUE),
        ("基建", "FY25 资本开支 $880 亿 +80%", "全球新建数据中心,Stargate $5,000 亿 10 年计划已启动", GREEN),
        ("Copilot", "M365 Copilot 渗透率突破 30%", "企业订阅 $30/月 · 企业侧真正规模化 AI 变现", ORANGE),
        ("GitHub", "Copilot 用户超 2,000 万", "开发者 AI 标配,垂直场景最成功的 AI 产品", PURPLE),
        ("OpenAI", "持有 OpenAI 约 49% 经济权益", "FY25 记入 OpenAI 亏损分担拖累非 GAAP 利润", RED),
        ("Xbox", "Activision 收购完整整合", "$687 亿并购完成整合,Xbox Game Pass 加速", GREEN),
    ],

    "MOAT": [
        ("企业软件 40 年垄断", "Windows + Office 是全球企业必备,装机量 15 亿+,切换成本极高"),
        ("Azure + OpenAI 双王牌", "独占 OpenAI 模型接口,同时拥有全球第二大云,AI 时代双重位置"),
        ("LinkedIn + GitHub 数据", "全球最大职业社交(10 亿用户)+最大代码托管(1.3 亿开发者)独有数据"),
        ("企业订阅黏性", "Office 365/M365/Azure 全部订阅化,净留存率 110%+,ARR 机器"),
        ("Copilot 生态壁垒", "M365/GitHub/Windows/Edge 全栈集成 AI,竞争对手单点难以撼动"),
        ("现金流护城河", "FY25 经营现金流 $1,300 亿,支持史无前例的 AI Capex 军备竞赛"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$2,817 亿"),
        ("营收同比", "+15%"),
        ("净利润", "$1,018 亿"),
        ("净利率", "约 36%"),
        ("营业利润率", "约 45%"),
        ("Azure 增速", "+33%"),
        ("云占比", "40.8%"),
        ("资本开支", "$880 亿 (+80%)"),
        ("最新股价 / 市值", "$475 / $3.52 万亿"),
        ("PE (TTM)", "约 36×"),
        ("回购 + 分红", "约 $600 亿"),
        ("M365 Copilot 渗透", "超 30%"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "Azure +33% 逆势加速", "AI 贡献 16pp,规模超过竞争对手,云端真正看到 AI 红利"),
        ("亮点", "营业利润率 45% 极高", "规模效应+软件本质,是大型科技公司中利润率最高的"),
        ("亮点", "Copilot 跑通企业侧", "M365 Copilot 渗透 30%+,AI 第一个规模化盈利产品"),
        ("风险", "CapEx $880 亿 +80%", "折旧压力巨大,若 AI 需求不及预期将严重拖累利润率"),
        ("风险", "OpenAI 关系不稳", "OpenAI 自研 GPU + 自研数据中心,长期可能绕开微软"),
        ("风险", "估值 PE 36×", "已反映 AI 溢价,任何 Azure 增速放缓都会被市场严重惩罚"),
    ],

    "QUOTES_LABEL": "管理层 & 分析师观点",
    "QUOTES": [
        "「我们已进入 AI 的通用阶段。」— Satya Nadella (FY25 业绩会)",
        "「Copilot 正在重新定义每一类企业工作流。」— Satya Nadella",
        "「每一美元 Azure 投入带来约 7 美元 ARR」— Amy Hood",
        "「Azure 增速正在重新加速,AI 需求超过产能。」— Nadella",
        "「Stargate 是一次世纪级算力投资」— Nadella (2026)",
        "— 分析师:微软是最完整的 AI 赢家,但估值已无明显安全边际",
    ],

    "DATA_SOURCE": "Microsoft FY2025 年报 · 业绩会 · 彭博",
}
