#!/usr/bin/env python3
"""Eli Lilly 礼来 · FY2025 / 当前估值经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
LILLY_RED = "#D52B1E"
LILLY_GOLD = "#C4963C"
LILLY_GREEN = "#4A6B3B"
LILLY_WINE = "#8B3A4E"

DATA = {
    "TITLE": "礼来经营全解析",
    "SUBTITLE": "Eli Lilly · GLP-1 + Neuroscience + Oncology + Manufacturing Scale",
    "UPDATE_DATE": "最新口径：FY2025 + Q1 2026 指引更新 + 当前估值",

    "COMPANY_PROFILE": {
        "公司全称": "Eli Lilly and Company",
        "上市代码": "NYSE: LLY",
        "市值排名": "全球第 15 名附近（约 $9,289 亿）",
        "CEO": "David A. Ricks（2017 至今）",
        "总部": "Indianapolis, Indiana",
        "核心业务": "糖尿病/肥胖 + 肿瘤 + 免疫 + 神经科学",
        "员工": "约 5 万人",
        "核心产品": "Mounjaro + Zepbound + Verzenio",
        "2026 指引": "营收 $820-850 亿",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 营收": "$652 亿（YoY +45%）",
        "FY2025 经营利润": "$263 亿（YoY +104%）",
        "FY2025 经营现金流": "$168 亿（YoY +91%）",
        "FY2025 净利润": "$206 亿（YoY +95%）",
        "FY2025 ROIC": "约 25.3%（年度口径）",
        "FY2025 CapEx": "$78 亿",
        "当前市值": "约 $9,695 亿",
        "PE / Forward PE": "约 38.4× / 26.7×",
        "年度股息": "$6.92/股 · 股息率约 0.68%",
    },

    "CAPITAL_AND_ROI": [
        ("ROI / ROIC", "FY2025 ROIC 约 25.3%", "StockAnalysis 年度 ROIC；TTM ROIC 约 41.9% 仅作当前参考。"),
        ("2026E CapEx", "未披露具体额", "公司 Q1 2026 后上调营收指引，但未给出 2026 CapEx 单年额。"),
        ("股东分红", "$6.92/股 · 0.68%", "当前年化股息；FY2025 现金分红 $53.8 亿，回购 $41.1 亿。"),
    ],

    "SEGMENTS_LABEL": "重点产品营收（FY2025）",
    "BUSINESS_SEGMENTS": [
        ("1", "Mounjaro", "35%", "$230亿", "+99%", "爆发", "糖尿病/肥胖"),
        ("2", "Zepbound", "21%", "$135亿", "+175%", "爆发", "肥胖症"),
        ("3", "Verzenio", "9%", "$57亿", "+8%", "稳增", "乳腺癌"),
        ("4", "其他药品/管线", "35%", "$230亿", "组合", "多元", "免疫/神经/其他"),
    ],

    "REVENUE_MIX": [
        ("Mounjaro", "35%"),
        ("Zepbound", "21%"),
        ("Verzenio", "9%"),
        ("其他药品/管线", "35%"),
    ],

    "MOVES_LABEL": "关键战略布局",
    "STRATEGIC_MOVES": [
        ("GLP-1", "Mounjaro + Zepbound 合计 $365 亿", "两大产品已经贡献超过一半收入，是礼来估值的核心支柱。", LILLY_RED),
        ("口服", "Orforglipron 推进监管路径", "从注射走向口服，目标是扩大 GLP-1 使用人群。", ORANGE),
        ("产能", "美国/欧洲多项建厂计划", "阿拉巴马 $60 亿、欧洲 $30 亿等计划围绕活性成分和口服药。", PURPLE),
        ("神经", "Kisunla + 阿尔茨海默", "老龄化赛道打开第二增长曲线，但临床和支付仍需验证。", GREEN),
        ("指引", "Q1 2026 后营收指引上调至 $820-850 亿", "增长继续由 GLP-1 与产能交付驱动。", LILLY_RED),
        ("风险", "估值和政策压力", "药价、医保支付、竞争管线和产能交付决定高估值能否兑现。", RED),
    ],

    "MOAT": [
        ("双爆款药物", "Mounjaro/Zepbound FY25 合计约 $365亿，把糖尿病和肥胖两个大市场连在一起。"),
        ("临床管线", "口服 GLP-1、retatrutide、神经科学和肿瘤管线形成后续梯队。"),
        ("产能壁垒", "生物制药和注射/口服供应链复杂，产能兑现本身就是护城河。"),
        ("商业化能力", "美国市场放量、患者可及性和医保谈判决定销售上限。"),
        ("研发强度", "FY2025 R&D $133 亿，持续押注长期适应症扩展。"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$652 亿"),
        ("经营利润", "$263 亿"),
        ("经营现金流", "$168 亿"),
        ("净利润", "$206 亿"),
        ("Mounjaro", "$230 亿"),
        ("Zepbound", "$135 亿"),
        ("R&D", "$133 亿"),
        ("FY25 CapEx", "$78 亿"),
        ("ROIC", "25.3%"),
        ("当前市值", "$9,695 亿"),
        ("PE / Forward PE", "38.4× / 26.7×"),
        ("每股股息", "$6.92"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "营收 +45%", "GLP-1 需求推动公司进入高速增长期。"),
        ("亮点", "经营利润翻倍", "经营利润 $263 亿，同比增长 104%。"),
        ("亮点", "2026 指引上调", "Q1 2026 后公司将全年营收指引提高至 $820-850 亿。"),
        ("风险", "估值消化", "当前 PE 约 36×，市场已经预期高增长延续。"),
        ("风险", "价格和支付", "医保、政府谈判和实际药价会影响净价。"),
        ("风险", "产能交付", "扩产、质量和供应链任何延误都会放大需求缺口。"),
    ],

    "QUOTES_LABEL": "管理层观点",
    "QUOTES": [
        "「2025 年我们触达了更多患者。」— David Ricks",
        "「我们扩大了制造能力。」— FY2025 业绩公告",
        "「150 周年后继续以深管线扩大影响。」— Ricks",
    ],

    "DATA_SOURCE": "Eli Lilly FY2025 Results / StockAnalysis / Lilly news releases",
    "FOOTER_LINES": [
        "经营数据：Eli Lilly FY2025 Results / StockAnalysis，FY2025: 2025年1-12月",
        "同比口径：FY2025 vs FY2024；营收 +45%，经营利润 +104%，经营现金流 +90.7%",
        "行情数据：StockAnalysis LLY / market quote，查看：2026年6月；市值约 $969.5B，PE 约38.4×，Forward PE 约26.7×",
        "ROI口径：StockAnalysis 年度 ROIC 25.30%；TTM ROIC 41.92% 仅作当前参考",
        "2026 CapEx口径：Lilly Q1 2026 业绩公告将全年营收指引上调至 $82-85B；未披露单年 CapEx 额",
        "股东分红：StockAnalysis Dividend / FY2025 Cash Flow，查看：2026年5月；年化 $6.92/股，股息率约0.68%，FY25 现金分红 $53.8亿",
        "管理文化：Lilly Careers / Operating Ethically / Inclusion / Impact well-being，核查：2026年5月",
        "货币口径：Lilly 以 USD 报告；图中金额均为 USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
