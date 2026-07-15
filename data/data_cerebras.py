#!/usr/bin/env python3
"""Cerebras Systems · FY2025 / IPO operating analysis data"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
CB_ORANGE = "#F15A29"
CB_DARK = "#171717"
CB_RED = "#B33A2E"
CB_CYAN = "#167782"
CB_GOLD = "#C49336"
CB_GREEN = "#4E7C45"

DATA = {
    "TITLE": "Cerebras 经营全解析",
    "SUBTITLE": "Cerebras Systems · Wafer-Scale AI Infrastructure · NASDAQ: CBRS",
    "UPDATE_DATE": "最新口径：FY2025 S-1/A + 2026 IPO + 当前行情",

    "COMPANY_PROFILE": {
        "公司全称": "Cerebras Systems Inc.",
        "上市代码": "NASDAQ: CBRS",
        "上市时间": "2026-05-14 IPO，发行价 $185/股",
        "CEO": "Andrew D. Feldman",
        "总部": "Sunnyvale, California",
        "员工": "708 人（美国 426 人）",
        "核心业务": "晶圆级 AI 芯片 + AI 系统 + 云端推理服务",
        "核心产品": "WSE-3 / CS-3 / Cerebras Cloud",
        "最新催化": "OpenAI >$20B 合约 + AWS 合作 + IPO 募资 $5.55B",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 营收": "$5.10 亿（YoY +75.7%）",
        "FY2025 毛利": "$1.99 亿（毛利率 39%）",
        "FY2025 经营亏损": "$-1.46 亿（核心仍亏损）",
        "FY2025 GAAP净利润": "$2.38 亿（含一次性收益）",
        "非GAAP净亏损": "$-0.76 亿",
        "经营现金流": "$-0.10 亿",
        "剩余履约义务": "$246 亿（多数来自 OpenAI）",
        "IPO 募资": "$55.5 亿（发行价 $185）",
        "当前市值": "约 $636 亿（盘中）",
        "现金股息": "不派现金股息（$0/股）",
    },

    "CAPITAL_AND_ROI": [
        ("ROI / ROIC", "不可比", "GAAP净利润含一次性公允价值收益；核心经营仍亏损，IPO前后资本结构变化大。"),
        ("2026E CapEx", "未披露/不可比", "公司披露将用 IPO 资金和 OpenAI 贷款扩云与数据中心能力，但未给 2026 单年 CapEx。"),
        ("股东回报", "$0/股 · 不分红", "上市初期回报来自股价波动与增长预期；公司披露暂不计划现金分红。"),
    ],

    "SEGMENTS_LABEL": "收入结构（FY2025）",
    "BUSINESS_SEGMENTS": [
        ("1", "Hardware", "70%", "$3.58亿", "+69.1%", "高增", "WSE/CS系统"),
        ("2", "Cloud & Other", "30%", "$1.52亿", "+93.6%", "更快", "云推理/服务"),
    ],

    "REVENUE_MIX": [
        ("Hardware", "70%"),
        ("Cloud & Other Services", "30%"),
    ],

    "MOVES_LABEL": "关键战略布局",
    "STRATEGIC_MOVES": [
        ("IPO", "$185/股 · 募资 $55.5 亿", "2026-05-14 登陆 Nasdaq，补充云端扩张资金。", CB_ORANGE),
        ("OpenAI", "750MW + >$20B", "初始 750MW 推理算力，另有 1.25GW 追加容量选项。", CB_GREEN),
        ("AWS", "首个 hyperscaler 部署", "2026 年 3 月签署合作，让 AWS 在自有数据中心部署 Cerebras。", CB_CYAN),
        ("云", "$246 亿 RPO", "剩余履约义务提供需求能见度，但交付依赖数据中心、电力与供应链。", CB_GOLD),
        ("风险", "估值与集中度", "当前市销率极高，OpenAI/G42/MBZUAI/AWS 关系决定成败。", RED),
    ],

    "MOAT": [
        ("WSE-3 硬指标", "4 万亿晶体管、90 万核心、46,225mm² 硅面积、44GB 片上内存、21PB/s 内存带宽。"),
        ("推理速度证据", "公司 S-1/A 称多种开源模型上最高约 15× GPU 方案，特殊负载可超过 1,000×。"),
        ("订单可见度", "2025 年末 RPO $246 亿，OpenAI 合约为主要来源；前十客户 12 个月内追加支出约 +80%。"),
        ("商业模式切换", "硬件收入 70%，云和服务 30%；云服务增速 +93.6%，从卖系统转向卖推理能力。"),
        ("技术路线差异", "晶圆级集成减少跨芯片通信瓶颈，但也带来制造、供电、散热和供应链交付风险。"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$5.10 亿"),
        ("营收同比", "+75.7%"),
        ("FY25 毛利率", "39%"),
        ("FY25 经营亏损", "$-1.46 亿"),
        ("非GAAP净亏损", "$-0.76 亿"),
        ("经营现金流", "$-0.10 亿"),
        ("现金", "$7.02 亿"),
        ("RPO", "$246 亿"),
        ("当前股价", "$295.63"),
        ("当前市值", "$636 亿"),
        ("市销率", "~125×"),
        ("现金股息", "$0/股"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "差异化架构", "WSE-3 用晶圆级集成押注低延迟推理，路线不同于 GPU 堆叠。"),
        ("亮点", "OpenAI 背书", "750MW 初始容量 + >$20B 合约，把需求能见度直接拉长。"),
        ("亮点", "云服务高增", "Cloud & Other FY2025 收入 $1.52 亿，同比 +93.6%。"),
        ("风险", "核心经营仍亏损", "FY2025 经营亏损 $1.46 亿，GAAP盈利含一次性会计收益。"),
        ("风险", "客户高度集中", "S-1/A 披露重大客户包括 OpenAI、G42、MBZUAI、AWS。"),
        ("风险", "估值极度前置", "当前约 $636 亿市值对应 FY2025 收入约 125×，容错率低。"),
    ],

    "QUOTES_LABEL": "创始人与招股书观点",
    "QUOTES": [
        "「Fast AI is more useful than slow AI.」— Founder Letter",
        "「Fearless engineering + relentless drive.」— Founder Letter",
        "「We expect to deploy 750MW during 2026-2028.」— S-1/A",
    ],

    "DATA_SOURCE": "Cerebras FY2025 S-1/A / Cerebras IPO pricing release / StockAnalysis",
    "FOOTER_LINES": [
        "经营数据：Cerebras S-1/A，FY2025: 2025年1-12月；FY2024: 2024年1-12月",
        "行情数据：StockAnalysis，2026-05-15 10:41 EDT；股价 $295.63，市值约 $63.63B",
        "IPO口径：Cerebras 官方新闻稿，2026-05-14；发行 3,000万股，发行价 $185，募资 $5.55B",
        "ROI口径：GAAP净利润含一次性公允价值收益；核心经营亏损，IPO前后资本结构变化大，ROI不可比",
        "2026 CapEx口径：S-1/A 披露资金用于云/数据中心/营运资金，未披露 2026 单年 CapEx",
        "股东分红：S-1/A Dividend Policy；未曾派发现金股息，上市后短期无分红计划",
        "管理文化：S-1/A Human Capital / Founder Letter / Cerebras Careers，核查：2026年5月",
        "货币口径：Cerebras 以 USD 报告；图中金额均为 USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
