#!/usr/bin/env python3
"""ASML 阿斯麦 FY2025 年报 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
ASML_ORANGE = "#FF6A13"
ASML_BLUE = "#0066CC"
FX_NOTE = "欧元金额按 2026年5月近似汇率 1 EUR≈1.18 USD 折算"

DATA = {
    "TITLE": "阿斯麦经营全解析",
    "SUBTITLE": "ASML Holding (AEX/NASDAQ: ASML) · 全球光刻机垄断 · EUV 独家供应",
    "UPDATE_DATE": "数据更新:FY2025 年报 (2026-01 发布)",

    "COMPANY_PROFILE": {
        "公司全称": "ASML Holding N.V.",
        "上市代码": "AEX: ASML · NASDAQ: ASML",
        "创立": "1984 年 · 飞利浦+ASM 合资",
        "CEO": "Christophe Fouquet (2024 至今)",
        "CFO": "Roger Dassen",
        "核心业务": "EUV + DUV 光刻机 + 服务",
        "员工": "约 4.4 万人",
        "总部": "荷兰 Veldhoven",
        "最新股价 / 市值": "约 $1,629 / $6,407 亿美元 (2026年6月)",
        "最新 PE (TTM)": "约 53.4×",
        "光刻机全球市占": "约 90% (EUV 100% 独占)",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 全年营收": "约 $384 亿美元 (+15% YoY)",
        "FY2025 经营利润": "约 $133 亿美元（经营利润率约 35%）",
        "FY2025 经营现金流": "约 $150 亿美元",
        "FY2025 毛利率": "约 52% (EUV 拉动)",
        "FY2025 净利润": "约 $113 亿美元 (+17% YoY)",
        "FY2025 自由现金流": "约 $146 亿美元",
        "FY2025 订单积压": "约 $456 亿美元 (1 年以上)",
        "FY2025 分红": "约 $35 亿美元；€7.50/股",
        "FY2025 回购": "约 $54 亿美元",
        "FY25 CapEx": "约 $26 亿美元（折旧/产能口径）",
        "EUV 出货": "约 48 台 (含 High-NA)",
        "High-NA EUV 订单": "约 20 台",
        "当前市值": "约 $6,407 亿",
        "PE / Forward PE": "约 53.4× / 40.6×",
    },

    "CAPITAL_AND_ROI": [
        ("股东回报", "€7.50/股 + $54亿回购", "FY2025 拟派 €7.50/股；同时回购约 $54 亿美元。"),
    ],

    "SEGMENTS_LABEL": "业务分部营收(FY2025 全年)",
    "BUSINESS_SEGMENTS": [
        ("1", "EUV 光刻机", "47%", "$180亿", "+35%", "▲爆发", "台积电/三星/Intel"),
        ("2", "DUV 光刻机", "28%", "$108亿", "+10%", "▲稳定", "成熟制程主力"),
        ("3", "服务+升级 (IBS)", "22%", "$96亿", "+26%", "▲稳定", "装机基数扩大"),
        ("4", "Applications (量测/软件)", "3%", "$12亿", "+10%", "▲稳定", "YieldStar 量测"),
    ],

    "REVENUE_MIX": [
        ("EUV 光刻机", "47%"),
        ("DUV 光刻机", "28%"),
        ("服务+升级", "22%"),
        ("Applications", "3%"),
    ],

    "MOVES_LABEL": "FY25-27 关键战略动作",
    "STRATEGIC_MOVES": [
        ("EUV", "High-NA EUV 商业化 TWINSCAN EXE:5200", "首批 Intel/台积电交付,$3.5 亿/台", ASML_ORANGE),
        ("产能", "EUV 年产 70 台目标 FY26", "产能翻倍满足 AI 芯片需求", ASML_BLUE),
        ("客户", "英伟达/苹果/Meta 自研芯片", "AI 芯片自研浪潮推动 2nm 需求", GREEN),
        ("研发", "Hyper-NA EUV 研发中", "下一代光刻,2030 年商业化目标", PURPLE),
        ("美国", "美国亚利桑那+台积电联动", "CHIPS 法案受益,FY27 美国订单爆发", ORANGE),
        ("风险", "中国市场+中美科技战", "对华 DUV 限制扩大,20%+ 中国营收受影响", RED),
    ],

    "MOAT": [
        ("EUV 100% 全球垄断", "全球唯一能量产 EUV 光刻机,单台 $2-3 亿,无替代者"),
        ("30+ 年研发积累", "每台 EUV 含 10 万+ 零件,Zeiss 光学+Cymer 光源独家"),
        ("台积电/三星/Intel 锁定", "全球 2nm 以下制程必须用 ASML,客户被锁死"),
        ("装机基数服务收入", "Installed Base 管理销售约 €8.2B，随全球在机系统和升级需求复利。"),
        ("$389 亿美元订单积压", "超过 1 年生产交付周期,可见度极高"),
        ("荷兰+美国+日本全球供应链", "Zeiss 德国+Cymer 美国+Cymer 日本,全球独家"),
    ],

    "KEY_METRICS": [
        ("市值排名", "第 20 名附近"),
        ("FY25 营收", "$384 亿"),
        ("净利润", "$113 亿"),
        ("毛利率", "约 52%"),
        ("自由现金流", "$146 亿"),
        ("订单积压", "$456 亿"),
        ("分红", "€7.50/股"),
        ("回购", "$54 亿"),
        ("EUV 出货", "约 48 台"),
        ("High-NA 订单", "约 20 台"),
        ("光刻机市占", "约 90%"),
        ("最新股价 / 市值", "$1,629 / $6,407 亿"),
        ("PE (TTM)", "约 53.4×"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "High-NA EUV 订单 20 台", "Intel+台积电抢购,2nm 以下光刻唯一选择"),
        ("亮点", "订单积压 $456 亿", "超过 1 年产能，FY26-27 营收可见度高"),
        ("亮点", "服务收入 $96 亿稳定", "装机基数带动，毛利率高于整机周期。"),
        ("风险", "中国 DUV 出口限制", "对华 20%+ 营收受影响,FY25 已降至 15%"),
        ("风险", "AI 需求周期波动", "如 AI CapEx 放缓,EUV 订单可能延迟"),
        ("风险", "High-NA 技术爬坡", "客户导入慢,可能影响 FY26-27 营收节奏"),
    ],

    "QUOTES_LABEL": "管理层 & 分析师观点",
    "QUOTES": [
        "「EUV 是 2nm 以下芯片的唯一路径。」— CEO Fouquet (FY25 业绩会)",
        "「High-NA 已进入商业化阶段。」— Fouquet",
        "「FY26 年产 EUV 翻倍至 70 台。」— Fouquet",
        "「中国市场长期仍是重要组成。」— CFO Dassen",
        "「订单可见度史上最高。」— Dassen",
        "— 分析师:ASML 是 AI 算力的最终卖铲人",
    ],

    "DATA_SOURCE": '经营数据：ASML 2025 Annual Report / Q4 2025 transcript · 行情数据：StockAnalysis ASML，查看 2026年5月 · 欧元金额按 1 EUR≈1.18 USD 折算',
    "FOOTER_LINES": [
        '经营数据：ASML 2025 Annual Report / Q4 2025 transcript，FY2025: 2025年1-12月',
        '同比口径：FY2025 vs FY2024；净销售额 +15%，毛利率 52.8%，净利润 +17%',
        '行情数据：StockAnalysis ASML / market quote，查看：2026年6月；市值约 $640.7B，PE 约53.4×，Forward PE 约40.6×',
        'ROI口径：采用 ROIC/资本效率结合 EUV/High-NA 订单与服务现金流判断；设备周期与出口管制会影响回报',
        '2026 CapEx口径：ASML 未披露单年精确工业 CapEx；重点 High-NA、EUV产能、服务网络和研发投入',
        '股东分红：ASML Annual Report / StockAnalysis Dividend，查看：2026年5月；FY2025 拟派 €7.50/股，折合约 $8.8/股',
        '管理文化：ASML Careers / Annual Report / Sustainability / supplier ecosystem materials，核查：2026年5月',
        '汇率口径：欧元按 1 EUR≈1.18 USD 折算，查看：2026年5月',
        '免责声明：本图仅供学习参考，不构成投资建议',
        'by 江明',
    ],
}
