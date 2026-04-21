#!/usr/bin/env python3
"""Meta Platforms FY2025 年报 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
META_BLUE = "#1877F2"
META_PURPLE = "#845BFF"

DATA = {
    "TITLE": "Meta 经营全解析",
    "SUBTITLE": "Meta Platforms (NASDAQ: META) · Facebook/Instagram/WhatsApp · AI + 元宇宙",
    "UPDATE_DATE": "数据更新:FY2025 年报 (2026-01 发布)",

    "COMPANY_PROFILE": {
        "公司全称": "Meta Platforms, Inc.",
        "上市代码": "NASDAQ: META",
        "创立": "2004 年 · Mark Zuckerberg 于哈佛宿舍",
        "CEO / 创始人": "Mark Zuckerberg (持股+超级投票权)",
        "CFO": "Susan Li",
        "核心业务": "广告 + AI 助手 + Reality Labs (VR/AR)",
        "员工": "约 7.8 万人",
        "总部": "Menlo Park, California",
        "最新股价 / 市值": "约 $720 / $1.80 万亿 (2026-04)",
        "最新 PE (TTM)": "约 28×",
        "Family DAP": "日活约 34 亿人 (Facebook+IG+WA+Messenger)",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 全年营收": "$1,750 亿 (+20% YoY)",
        "FY2025 广告营收": "$1,700 亿 (+21%)",
        "FY2025 净利润": "$620 亿 (+40% YoY)",
        "FY2025 营业利润率": "约 42%",
        "Reality Labs 亏损": "约 $200 亿 (CapEx 持续投入)",
        "FY2025 CapEx": "约 $750 亿 (+100% YoY)",
        "自由现金流": "约 $450 亿",
        "回购 + 分红": "约 $500 亿",
        "Family 日活": "34 亿人 · +6% YoY",
    },

    "SEGMENTS_LABEL": "业务分部营收(FY2025 全年)",
    "BUSINESS_SEGMENTS": [
        ("1", "Family of Apps 广告", "97%", "$1,700亿", "+21%", "▲AI推荐", "广告核心"),
        ("2", "其他收入 (订阅+硬件)", "2%", "$35亿", "+45%", "▲增长", "Ray-Ban Meta"),
        ("3", "Reality Labs (VR/AR)", "1%", "$15亿", "-5%", "▼亏损", "Quest+Ray-Ban"),
    ],

    "REVENUE_MIX": [
        ("Family 广告", "97%"),
        ("其他收入", "2%"),
        ("Reality Labs", "1%"),
    ],

    "MOVES_LABEL": "2025-2026 关键战略动作",
    "STRATEGIC_MOVES": [
        ("AI", "Llama 4 开源 · Meta AI 助手十亿用户", "AI 重塑推荐+广告+搜索,广告效果提升 20%+", META_BLUE),
        ("智能眼镜", "Ray-Ban Meta 销量破 500 万", "AR 眼镜意外成爆款,与 EssilorLuxottica 深度合作", META_PURPLE),
        ("CapEx", "FY26 资本支出 $1,000-1,200 亿", "AI 基建大幅加码,堪比云厂商,自建数据中心+自研 MTIA 芯片", RED),
        ("Reels", "Reels 货币化追平 Feed 广告", "短视频收入规模突破,对抗 TikTok 的核心护城河", GREEN),
        ("订阅", "WhatsApp Business 付费扩张", "电商+客服 SaaS,印度+东南亚小商户付费占比上升", ORANGE),
        ("元宇宙", "Reality Labs FY25 累亏 $600 亿", "Zuck 坚持长期投入,但市场要求 2027 前控制亏损", PURPLE),
    ],

    "MOAT": [
        ("34 亿日活的超级网络效应", "Family of Apps 覆盖全球一半人口,广告主无可替代的触达规模"),
        ("AI 驱动的精准投放", "Advantage+ 广告系统用 AI 自动生成+定向,中小企业广告 ROI 提升 30%"),
        ("Instagram Reels 护城河", "短视频时长反超 Feed,成功狙击 TikTok 在欧美市场的增长"),
        ("开源 Llama 生态", "Llama 4 成为全球最大开源大模型,吸引开发者生态,对抗 OpenAI/Google"),
        ("Zuck 绝对控制", "创始人 13% 经济权 + 55% 投票权,可长期投入 VR/AR 不受华尔街干扰"),
        ("现金流机器 + 回购", "每年 $450 亿自由现金流,$500 亿回购,股东回报规模巨大"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$1,750 亿"),
        ("营收同比", "+20%"),
        ("净利润", "$620 亿"),
        ("净利率", "约 35%"),
        ("营业利润率", "约 42%"),
        ("自由现金流", "$450 亿"),
        ("CapEx (FY25)", "$750 亿"),
        ("Family 日活", "34 亿"),
        ("广告 ARPU", "约 $50/年"),
        ("Reality Labs 亏损", "$200 亿"),
        ("最新股价 / 市值", "$720 / $1.80T"),
        ("PE (TTM)", "约 28×"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "AI 驱动广告 ROI 提升", "Advantage+ 让中小广告主自动化投放,广告 CPM 与转化率双升"),
        ("亮点", "Ray-Ban Meta 爆款", "AR 眼镜意外成功,打开 Zuck 十年元宇宙赌局的突破口"),
        ("亮点", "Llama 开源生态", "全球最大开源大模型,对抗 OpenAI/Google 闭源模型,吸引开发者"),
        ("风险", "CapEx 重投拖累 ROIC", "FY26 CapEx $1,000-1,200 亿,折旧+能源成本压制短期利润"),
        ("风险", "Reality Labs 持续亏损", "累计亏损已超 $600 亿,市场对元宇宙长期回报失去耐心"),
        ("风险", "监管与隐私挑战", "欧盟 DMA / 美国 FTC / 印度数据本地化,广告精准度受限"),
    ],

    "QUOTES_LABEL": "管理层 & 分析师观点",
    "QUOTES": [
        "「AI 将重塑我们的每一款产品。」— Mark Zuckerberg (FY25 业绩会)",
        "「Llama 将成为开源 AI 的标准。」— Zuckerberg",
        "「Ray-Ban Meta 是十年来最成功的新品类。」— Zuckerberg",
        "「Reality Labs 是长期投资,但我们会严控亏损。」— CFO Susan Li",
        "「Reels 的货币化已经追平 Feed。」— Meta 业绩会",
        "— 分析师:Meta 是 AI 时代最被低估的超级现金流机器",
    ],

    "DATA_SOURCE": "Meta FY2025 年报 · 业绩会 · 彭博",
}
