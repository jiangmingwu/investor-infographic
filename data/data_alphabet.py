#!/usr/bin/env python3
"""谷歌 Alphabet FY2025 年报 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
GOOGLE_BLUE = "#4285F4"
GOOGLE_RED = "#EA4335"
GOOGLE_YELLOW = "#FBBC05"
GOOGLE_GREEN = "#34A853"

DATA = {
    "TITLE": "谷歌经营全解析",
    "SUBTITLE": "Alphabet Inc. (NASDAQ: GOOGL) · 全球搜索与 AI 基础设施巨头",
    "UPDATE_DATE": "数据更新:FY2025 年报 (2026-02 发布) · 日历年口径",

    "COMPANY_PROFILE": {
        "公司全称": "Alphabet Inc.",
        "上市代码": "NASDAQ: GOOGL / GOOG",
        "创立": "1998 年 · Larry Page & Sergey Brin 创立(2015 年重组为 Alphabet)",
        "董事长 / CEO": "Sundar Pichai",
        "CFO": "Anat Ashkenazi",
        "核心业务": "搜索广告 + YouTube + Google Cloud + Android/Play + Waymo",
        "员工": "约 18.3 万人",
        "总部": "加州山景城 Mountain View, CA",
        "最新股价 / 市值": "约 $205 / ¥2.50 万亿美元 (2026-04)",
        "最新 PE (TTM)": "约 22×",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 全年营收": "$3,500 亿 (+14% YoY)",
        "FY2025 净利润": "$1,000 亿 (+28% YoY)",
        "FY2025 营业利润率": "约 33%",
        "Q4 FY25 营收": "约 $965 亿 (+12% YoY)",
        "Google Cloud 全年": "约 $500 亿 (+32%)",
        "Google Cloud Q4 营业利润率": "约 18%",
        "YouTube 广告": "约 $380 亿 (+15%)",
        "FY25 经营现金流": "约 $1,300 亿",
        "FY25 资本开支": "约 $750 亿 (+75%)",
        "FY25 回购": "约 $650 亿",
    },

    "SEGMENTS_LABEL": "业务分部营收(FY2025 全年)",
    "BUSINESS_SEGMENTS": [
        ("1", "Google 搜索广告", "56.0%", "$1,960亿", "+12%", "▲稳增", "AI Overviews"),
        ("2", "YouTube 广告", "10.9%", "$380亿", "+15%", "▲加速", "Shorts 货币化"),
        ("3", "Google 网络联盟", "8.0%", "$280亿", "-2%", "▼承压", "传统展示"),
        ("4", "Google 订阅+设备", "11.4%", "$400亿", "+18%", "▲稳增", "One/Play/Pixel"),
        ("5", "Google Cloud", "14.3%", "$500亿", "+32%", "▲爆发", "Gemini/TPU/Vertex"),
        ("6", "Other Bets", "-", "$15亿", "+30%", "▲长期", "Waymo 自动驾驶"),
    ],

    "REVENUE_MIX": [
        ("搜索广告", "56.0%"),
        ("Google Cloud", "14.3%"),
        ("订阅+设备", "11.4%"),
        ("YouTube 广告", "10.9%"),
        ("网络联盟", "8.0%"),
    ],

    "MOVES_LABEL": "2025-2026 关键战略动作",
    "STRATEGIC_MOVES": [
        ("AI", "Gemini 3.0 全面开放 · 超越 GPT-5", "原生多模态+长上下文,在 LMSYS 登顶,搜索入口全面 AI 化", GOOGLE_BLUE),
        ("基建", "资本开支 $750 亿 · 自研 TPU v7", "Anthropic 使用 TPU 训练,Cloud 算力自给率持续提升", GREEN),
        ("云", "Google Cloud 营业利润率首破 18%", "从亏损到可观盈利,Gemini+Vertex AI 拉动订单饱满", GREEN),
        ("Waymo", "覆盖旧金山/凤凰城/LA/奥斯汀/迈阿密", "每周 30 万次付费打车,商业化节点真正到来", PURPLE),
        ("反垄断", "美国司法部搜索反垄断案执行阶段", "可能被迫剥离 Chrome 或默认搜索协议,不确定性最大", RED),
        ("回报", "FY25 回购 $650 亿 + 首次分红", "持续回报股东,管理层对现金流与估值有信心", ORANGE),
    ],

    "MOAT": [
        ("搜索市占 89%+ 全球垄断", "搜索是全世界最赚钱的单一产品,20 年未被撼动,广告定价权极强"),
        ("YouTube 视频生态", "全球最大长视频+Shorts 短视频平台,月活 25 亿,内容飞轮难以复制"),
        ("Android 生态 30 亿设备", "全球移动操作系统龙头,Play Store 服务分成+默认搜索位全球独占"),
        ("自研 TPU + 全栈 AI", "唯一一家同时拥有模型(Gemini)+芯片(TPU)+云(GCP)+数据(搜索)的厂商"),
        ("DeepMind 顶级 AI 研究", "AlphaFold/AlphaGo/Gemini 背后的世界级研究院,人才密度仅次于 OpenAI"),
        ("现金流机器", "FY25 经营现金流 $1,300 亿,自循环支持 AI 军备竞赛 + 回购 + Waymo 长线投入"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$3,500 亿"),
        ("营收同比", "+14%"),
        ("净利润", "$1,000 亿"),
        ("净利率", "约 28.6%"),
        ("营业利润率", "约 33%"),
        ("搜索占比", "56.0%"),
        ("Cloud 增速", "+32%"),
        ("Cloud 利润率", "18%"),
        ("最新股价 / 市值", "$205 / $2.50 万亿"),
        ("PE (TTM)", "约 22×"),
        ("资本开支", "$750 亿"),
        ("回购 + 分红", "$650 亿 + 首发"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "净利润 +28% 跑赢营收", "规模效应+Cloud 扭亏,利润增速显著高于营收"),
        ("亮点", "Cloud 真正盈利", "从连年亏损到营业利润率 18%,Gemini 驱动订单质量跃升"),
        ("亮点", "Waymo 商业化突破", "全美 5 城覆盖,每周 30 万次打车,长期期权真正兑现中"),
        ("风险", "搜索反垄断判决落地", "可能被强制剥离 Chrome 或禁止向苹果支付默认搜索费(年 $200 亿)"),
        ("风险", "AI 搜索自蚕食风险", "AI Overviews 直接回答问题会减少传统搜索点击,广告模型受冲击"),
        ("风险", "资本开支陡升", "$750 亿 CapEx +75%,若 AI 需求放缓则折旧压力巨大"),
    ],

    "QUOTES_LABEL": "管理层 & 分析师观点",
    "QUOTES": [
        "「Gemini 是我们 25 年来最重要的产品」— Sundar Pichai (FY25 业绩会)",
        "「AI 让搜索变得更有用,不是取代」— Sundar Pichai",
        "「Cloud 已进入可持续盈利轨道」— Anat Ashkenazi",
        "「Waymo 的拐点已经到来」— Sundar Pichai",
        "「我们同时拥有模型、芯片、云和数据,这在全球独一份」— Pichai",
        "— 分析师:谷歌是 AI 时代被低估的全栈玩家,PE 22× 具备安全边际",
    ],

    "DATA_SOURCE": "Alphabet FY2025 年报 · 业绩会 · 彭博",
}
