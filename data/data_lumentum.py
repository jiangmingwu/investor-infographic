#!/usr/bin/env python3
"""Lumentum Holdings · FY2025 / Q3 FY2026 operating analysis data"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
LUM_PURPLE = "#6B3FA0"
LUM_TEAL = "#167782"
LUM_GOLD = "#C4963C"
LUM_WINE = "#8B3A4E"
LUM_GREEN = "#4A6B3B"

DATA = {
    "TITLE": "Lumentum 经营全解析",
    "SUBTITLE": "Lumentum Holdings · Photonics + Cloud Networking + AI Optics",
    "UPDATE_DATE": "最新口径：FY2025 + Q3 FY2026 + 当前估值",

    "COMPANY_PROFILE": {
        "公司全称": "Lumentum Holdings Inc.",
        "上市代码": "NASDAQ: LITE",
        "市值排名": "全球第 309 名（约 $779 亿）",
        "CEO": "Michael Hurlston",
        "总部": "San Jose, California",
        "核心业务": "光芯片/光模块 + 云网络 + 工业激光",
        "员工": "约 10,562 人",
        "核心客户": "云数据中心 / AI 基础设施 / 通信设备商",
        "最新催化": "NVIDIA $20 亿战略投资",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 营收": "$16.45 亿（YoY +21.0%）",
        "FY2025 经营亏损": "$-1.80 亿（GAAP，亏损收窄）",
        "FY2025 非GAAP经营利润": "$1.60 亿（Margin 9.7%）",
        "FY2025 净利润": "$0.26 亿（扭亏）",
        "FY2025 经营现金流": "$1.26 亿（YoY +411%）",
        "FY2025 CapEx": "$2.31 亿",
        "Q3 FY2026 营收": "$8.08 亿（YoY +90.1%）",
        "Q4 FY2026 指引": "$9.60-10.10 亿",
        "当前市值": "约 $779.4 亿（#309）",
        "股东分红": "不派现金股息（$0/股）",
    },

    "CAPITAL_AND_ROI": [
        ("ROI / ROIC", "FY25 ROI ~1.0%", "净利润口径；GAAP 年度仍处修复期，Q3 FY2026 盈利能力已明显抬升。"),
        ("2026E CapEx", "未披露/不可比", "公司披露 Greensboro 多年数亿美元扩产，但未给 2026 单年 CapEx 指引。"),
        ("股东分红", "$0/股 · 无现金股息", "Lumentum 没有现金分红历史；回报主要来自再投资、AI 光互联增长与股价波动。"),
    ],

    "SEGMENTS_LABEL": "业务分部营收（FY2025）",
    "BUSINESS_SEGMENTS": [
        ("1", "Cloud & Networking", "86%", "$14.11亿", "+30.0%", "高增", "AI云网络"),
        ("2", "Industrial Tech", "14%", "$2.34亿", "-14.6%", "承压", "工业激光/传感"),
    ],

    "REVENUE_MIX": [
        ("Cloud & Networking", "86%"),
        ("Industrial Tech", "14%"),
    ],

    "MOVES_LABEL": "关键战略布局",
    "STRATEGIC_MOVES": [
        ("AI", "Q3 FY26 营收 $8.08 亿", "AI 数据中心光连接推动营收同比 +90.1%。", LUM_PURPLE),
        ("NVIDIA", "$20 亿战略投资", "资金与客户信号强化光子供应链地位。", LUM_GREEN),
        ("制造", "Greensboro 新 InP 工厂", "240,000 平方英尺，预计 2028 年中爬坡。", LUM_TEAL),
        ("产品", "1.6T / CPO / UHP Lasers", "400G EML、CPO 激光源与光交换持续迭代。", LUM_GOLD),
        ("风险", "估值与交付压力", "当前估值已大幅计入 AI 光互联预期。", RED),
    ],

    "MOAT": [
        ("200G EML 份额", "Aletheia/Investing.com 估算 Lumentum 在 200Gbps EML 约 90% 份额；这是分析师估算，不是公司官方披露。"),
        ("EML 供应商稀缺", "TrendForce 列举 EML 主要供应商仅少数几家：Lumentum、Coherent、Mitsubishi、Sumitomo、Broadcom。"),
        ("利润率验证", "Q3 FY2026 非GAAP毛利率 47.9%、经营利润率 32.2%，说明 AI 光器件景气开始转化为盈利能力。"),
        ("AI 云收入占比", "FY2025 Cloud & Networking 收入 $14.11 亿，占全年收入 86%；Q3 FY2026 Components 收入占 66%。"),
        ("NVIDIA 锁定", "$20 亿投资 + 多年采购承诺 + 未来产能 access rights，是供应链地位的强信号。"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$16.45 亿"),
        ("营收同比", "+21.0%"),
        ("非GAAP经营利润", "$1.60 亿"),
        ("GAAP净利润", "$0.26 亿"),
        ("经营现金流", "$1.26 亿"),
        ("FY25 CapEx", "$2.31 亿"),
        ("Q3 FY26营收", "$8.08 亿"),
        ("Q4 FY26指引", "$9.60-10.10 亿"),
        ("当前市值", "$779.4 亿"),
        ("市值排名", "#309"),
        ("ROI", "~1.0%"),
        ("现金分红", "$0/股"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "云网络 86% 收入", "Cloud & Networking 成为公司绝对主线。"),
        ("亮点", "Q3 FY26 +90%", "AI 数据中心需求推动营收和利润率同步跃迁。"),
        ("亮点", "NVIDIA 资金信号", "$20 亿优先股投资改善现金与战略能见度。"),
        ("风险", "单年 CapEx 未披露", "扩产方向清楚，但 2026 单年投入无法精确核算。"),
        ("风险", "客户认证和良率", "新产线爬坡、客户认证、质量问题都可能拖慢交付。"),
        ("风险", "估值大幅前置", "市值与 PE 已反映高增长预期，波动会很大。"),
    ],

    "QUOTES_LABEL": "管理层观点",
    "QUOTES": [
        "「AI 数据中心需求推动云产品组合强劲增长。」— FY2025 Q4 业绩会",
        "「OCS 与 CPO 是两个重大机会，我们仍在起点。」— Q2 FY2026 业绩会",
        "「新增 InP 工厂将扩大 AI 光器件产能。」— 2026 年 3 月公告",
    ],

    "DATA_SOURCE": "Lumentum FY2025 10-K / FY2025 Results / Q3 FY2026 Results / CompaniesMarketCap / StockAnalysis",
    "FOOTER_LINES": [
        "经营数据：Lumentum FY2025 10-K / FY2025 Results，FY2025: 2024年6月-2025年6月；Q3 FY2026: 2025年12月-2026年3月",
        "同比口径：FY2025 vs FY2024；营收 +21.0%，GAAP经营亏损收窄，经营现金流 +411%；Q3 FY2026 营收 +90.1%",
        "行情数据：CompaniesMarketCap / Nasdaq，查看：2026年5月；市值约 $77.94B，全球排名 #309",
        "ROI口径：FY2025 净利润 $25.9M / 平均(债务+权益-现金及短投)约 $2.70B，约 1.0%",
        "2026 CapEx口径：公司披露 Greensboro 多年数亿美元扩产，未披露 2026 单年指引；FY2025 CapEx $231M",
        "股东分红：StockAnalysis Dividend，查看：2026年5月；无现金分红历史，$0/股不代表总回报为零",
        "护城河数据：TrendForce 2025-12 EML供应链；Investing.com/Aletheia 2026-04 200Gbps EML份额估算；NVIDIA新闻稿 2026年3月",
        "管理文化：FY2025 10-K Human Capital / Lumentum Careers / Sustainability People，核查：2026年5月",
        "货币口径：Lumentum 以 USD 报告；图中金额均为 USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
