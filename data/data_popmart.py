#!/usr/bin/env python3
"""POP MART International · FY2025 company operating analysis data."""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
POP_PINK = "#C85A7A"
POP_BLUE = "#1E62A8"
POP_GOLD = "#C4963C"
POP_GREEN = "#2F9A65"
POP_VIOLET = "#7C5AA6"

DATA = {
    "TITLE": "泡泡玛特经营全解析",
    "SUBTITLE": "POP MART International · IP + Designer Toys + Global Retail",
    "UPDATE_DATE": "最新口径：FY2025 全年 + 2026年6月当前估值",

    "COMPANY_PROFILE": {
        "公司全称": "Pop Mart International Group Limited",
        "上市代码": "HKEX: 9992",
        "创始人": "王宁",
        "总部": "中国北京",
        "核心业务": "潮玩 IP 运营 + 设计师玩具 + 全球零售渠道",
        "员工": "约 17,466 人",
        "代表 IP": "THE MONSTERS / LABUBU / MOLLY / SKULLPANDA / CRYBABY",
        "核心定位": "把设计师 IP、会员社区和全球渠道做成情绪消费平台",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 营收": "约 $54.78 亿（YoY +106.9%）",
        "FY2025 经营利润": "约 $24.92 亿（YoY +185.3%）",
        "FY2025 经营现金流": "约 $16.03 亿",
        "FY2025 净利润": "约 $18.85 亿（YoY +188.2%）",
        "当前市值": "约 $297.5 亿",
        "PE / Forward PE": "16.55× / 14.48×",
    },

    "CAPITAL_AND_ROI": [
        (
            "ROI / ROE",
            "ROE 77.6%",
            "StockAnalysis / S&P Global Market Intelligence FY2025 口径；轻资产 IP 与高周转渠道共同放大股东权益回报。",
        ),
        (
            "2026E CapEx",
            "未披露；FY25 PPE约 $3.00亿",
            "公司未披露 2026 单年资本开支指引；FY2025 购买物业、厂房及设备约 RMB20.31亿。",
        ),
        (
            "股东分红",
            "HK$1.516/股",
            "FY2025 拟派末期+特别股息合计 HK$1.516/股，约 $0.194/股；按 HK$176.40 股价约 0.86%。",
        ),
    ],

    "SEGMENTS_LABEL": "产品收入结构（FY2025）",
    "BUSINESS_SEGMENTS": [
        ("1", "Plush 毛绒", "50.4%", "$27.61亿", "+1,289.1%", "爆发", "LABUBU主线"),
        ("2", "Figures 手办", "32.4%", "$17.75亿", "+30.7%", "稳健", "盲盒/潮玩"),
        ("3", "MEGA", "5.2%", "$2.83亿", "+98.0%", "高端", "大尺寸收藏"),
        ("4", "Others", "12.0%", "$6.60亿", "+58.7%", "延展", "配件/其他"),
    ],

    "REVENUE_MIX": [
        ("Plush 毛绒", "50.4%"),
        ("Figures 手办", "32.4%"),
        ("MEGA", "5.2%"),
        ("Others", "12.0%"),
    ],

    "MOVES_LABEL": "关键战略动作",
    "STRATEGIC_MOVES": [
        ("IP", "THE MONSTERS 收入 $20.90亿", "FY2025 占收入 38.1%，同比 +365.7%，LABUBU 成为全球爆款。", POP_PINK),
        ("全球化", "美洲收入 +767.6%", "美洲收入约 $10.04亿，亚太约 $11.82亿，海外增长远快于中国内地。", POP_GREEN),
        ("渠道", "净增109家门店+343台Robo Shops", "全球门店与机器人店继续扩张，线上渠道占 42.3%。", POP_BLUE),
        ("会员", "7258万内地会员", "会员贡献中国内地收入 93.7%，复购率 55.7%，不是一次性流量。", POP_VIOLET),
        ("风险", "单一爆款波动", "THE MONSTERS 占比高，关键风险是能否持续孵化下一批全球 IP。", RED),
    ],

    "MOAT": [
        ("THE MONSTERS $20.90亿", "FY2025 收入 RMB141.61亿，约 $20.90亿，占总收入 38.1%，同比 +365.7%；LABUBU 是全球爆发的核心证据。"),
        ("Artist IP 收入 90.1%", "艺术家 IP 收入 RMB334.42亿，约 $49.35亿，占总收入 90.1%，说明核心不是普通零售，而是 IP 孵化和运营。"),
        ("会员销售 93.7%", "中国内地注册会员 7,258 万，会员贡献中国内地收入 93.7%，会员复购率 55.7%，体现社区与复购能力。"),
        ("Plush 增长 +1,289.1%", "毛绒品类 FY2025 收入约 $27.61亿，占 50.4%，同比 +1,289.1%，爆款可以带动新品类放大。"),
        ("全球渠道扩张", "FY2025 全球净增 109 家零售店和 343 台 Robo Shops；美洲收入 +767.6%，亚太 +165.4%。"),
    ],

    "KEY_METRICS": [
        ("FY25 营收", "$54.78亿"),
        ("经营利润", "$24.92亿"),
        ("经营现金流", "$16.03亿"),
        ("净利润", "$18.85亿"),
        ("当前市值", "$297.5亿"),
        ("PE / Forward", "16.55× / 14.48×"),
        ("ROE", "77.6%"),
        ("2026E CapEx", "未披露"),
        ("FY25 PPE购买", "$3.00亿"),
        ("股息", "HK$1.516/股"),
        ("会员", "7258万"),
        ("THE MONSTERS", "收入占38.1%"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "全球 IP 变现", "THE MONSTERS 单 IP 收入已超过 $20亿，证明中国潮玩 IP 可以全球化。"),
        ("亮点", "会员复购强", "中国内地会员销售占 93.7%，复购率 55.7%。"),
        ("亮点", "现金流质量高", "FY2025 经营现金流约 $16.03亿，净利润约 $18.85亿。"),
        ("风险", "爆款生命周期", "LABUBU 热度若降温，会影响估值和增长预期。"),
        ("风险", "供应与品质", "毛绒品类暴涨后，补货、品控和库存管理压力更大。"),
        ("风险", "海外合规与渠道", "全球开店会带来租金、人工、税务、文化差异和本地化管理挑战。"),
    ],

    "QUOTES_LABEL": "公司使命与经营主线",
    "QUOTES": [
        "「to light up passion and bring joy around the world」— POP MART 官方使命",
        "「Creating more fun, building one world」— POP MART 官方愿景",
        "泡泡玛特的核心问题不是“还能不能卖盲盒”，而是能否持续把设计师 IP 做成全球化的情绪消费资产。",
    ],

    "DATA_SOURCE": "Pop Mart FY2025 Annual Report / Annual Results / StockAnalysis / XE",
    "FOOTER_LINES": [
        "经营数据：Pop Mart FY2025 Annual Report / Annual Results，FY2025: 2025年1-12月",
        "行情数据：StockAnalysis 9992.HK，截至2026年6月5日；市值 HK$2329.79亿，约 $297.5亿；PE 16.55×，Forward PE 14.48×",
        "ROI口径：StockAnalysis / S&P Global Market Intelligence FY2025 ROE 77.6%；ROE作为轻资产IP公司的ROI替代观察指标",
        "2026 CapEx口径：公司未披露2026单年CapEx指引；FY2025购买物业、厂房及设备 RMB20.31亿，约 $3.00亿",
        "股东回报：FY2025拟派末期+特别股息合计 HK$1.516/股，约 $0.194/股；按HK$176.40股价约0.86%",
        "护城河/管理文化：Pop Mart FY2025 Annual Report，IP、会员、门店、员工与福利章节；核查：2026年6月7日",
        "汇率口径：XE，2026年6月5日；1 USD=6.7764 CNY，1 USD=7.8342 HKD；图中金额均为 USD/美元",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
