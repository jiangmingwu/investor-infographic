#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Micron 美光科技 FY2025 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
BLUE = "#3B6EA8"
GOLD = "#C4963C"

DATA = {
    "TITLE": "美光科技经营全解析",
    "SUBTITLE": "Micron Technology (NASDAQ: MU) · DRAM + NAND + HBM 存储龙头",
    "UPDATE_DATE": "数据更新：FY2025 业绩公告（2025-09-23）",

    "COMPANY_PROFILE": {
        "公司全称": "Micron Technology, Inc.",
        "上市代码": "NASDAQ: MU",
        "创立": "1978 年 · Idaho Boise 创立",
        "董事长 / CEO": "Sanjay Mehrotra",
        "CFO": "Mark Murphy",
        "核心业务": "DRAM、NAND、HBM、高性能 SSD 与汽车/嵌入式存储",
        "员工": "约 4.3 万人",
        "总部": "Boise, Idaho",
        "最新股价 / 市值": "约 $482 / $5,433 亿美元 (2026-04-29)",
        "最新 PE (TTM)": "约 64×（按 FY25 GAAP 净利）",
    },

    "FINANCIAL_SUMMARY": {
        "FY2025 营收": "$37.38B (+49% YoY)",
        "FY2025 GAAP 净利润": "$8.54B",
        "FY2025 Non-GAAP 净利润": "$9.47B",
        "FY2025 GAAP 毛利率": "39.8%",
        "FY2025 Non-GAAP 毛利率": "40.9%",
        "FY2025 GAAP 经营利润": "$9.77B",
        "FY2025 经营现金流": "$17.53B",
        "FY2025 调整自由现金流": "$3.72B",
        "FY2025 CapEx": "$13.80B",
        "现金+投资": "$11.94B",
    },

    "SEGMENTS_LABEL": "业务分部 / Q4 FY2025 收入",
    "BUSINESS_SEGMENTS": [
        ("1", "Cloud Memory", "40.1%", "$4.54B", "高增", "▲强劲", "HBM/云端DRAM"),
        ("2", "Mobile+Client", "33.2%", "$3.76B", "修复", "▲恢复", "手机/PC"),
        ("3", "Core Data Center", "13.9%", "$1.58B", "稳定", "→消化", "服务器SSD"),
        ("4", "Auto+Embedded", "12.7%", "$1.43B", "稳定", "▲改善", "汽车/工业"),
    ],

    "REVENUE_MIX": [
        ("Cloud Memory", "40.1%"),
        ("Mobile+Client", "33.2%"),
        ("Core Data Center", "13.9%"),
        ("Auto+Embedded", "12.7%"),
    ],

    "MOVES_LABEL": "关键战略动作",
    "STRATEGIC_MOVES": [
        ("HBM", "AI 数据中心存储爆发", "HBM 与高端 DRAM 成为收入和利润核心弹性", BLUE),
        ("DRAM", "供需紧张支撑价格", "AI 服务器挤占先进 DRAM 产能,周期从复苏进入紧平衡", GREEN),
        ("NAND", "高性能 SSD 受益 AI", "数据中心 SSD 与企业存储需求改善", ORANGE),
        ("美国", "本土存储制造稀缺性", "唯一美国大型存储制造商,受益供应链安全政策", PURPLE),
        ("CapEx", "$13.8B 年度资本开支", "扩 HBM/先进节点,现金流再投资强度高", GOLD),
        ("风险", "存储强周期", "价格反转会迅速压缩毛利率和估值", RED),
    ],

    "MOAT": [
        ("DRAM/HBM 技术壁垒", "先进制程、封装和良率决定客户导入速度"),
        ("AI 数据中心绑定", "HBM 与高带宽内存成为 GPU 集群关键瓶颈"),
        ("全球前三存储规模", "与三星、SK 海力士构成存储行业核心供给"),
        ("美国制造稀缺性", "供应链安全和本土制造政策提升战略价值"),
        ("客户认证周期长", "云厂商、汽车和工业客户认证后迁移成本高"),
        ("周期底部生存能力", "强资产负债表帮助穿越存储价格下行周期"),
    ],

    "KEY_METRICS": [
        ("市值排名", "第 22 名"),
        ("FY25 营收", "$37.38B"),
        ("GAAP 净利", "$8.54B"),
        ("Non-GAAP 净利", "$9.47B"),
        ("GAAP 毛利率", "39.8%"),
        ("经营现金流", "$17.53B"),
        ("调整 FCF", "$3.72B"),
        ("CapEx", "$13.80B"),
        ("现金+投资", "$11.94B"),
        ("股价 / 市值", "$482 / $5,433 亿"),
        ("PE", "约 64×"),
    ],

    "RISKS_HIGHLIGHTS": [
        ("亮点", "FY25 营收创纪录", "AI 数据中心推动全年营收达到 $37.38B"),
        ("亮点", "Q4 毛利率明显扩张", "GAAP 毛利率 44.7%,价格与产品结构改善"),
        ("亮点", "HBM 带来结构升级", "从普通存储周期股向 AI 基础设施供应商重估"),
        ("风险", "强周期属性", "DRAM/NAND 价格一旦回落,利润弹性反向放大"),
        ("风险", "CapEx 压力", "先进产能投入重,自由现金流对周期敏感"),
        ("风险", "头部客户集中", "AI 客户需求节奏会影响 HBM 排产和定价"),
    ],

    "QUOTES_LABEL": "管理层 & 市场观点",
    "QUOTES": [
        "「FY2025 创下纪录性全年收入。」— Micron 业绩公告",
        "「AI 数据中心增长推动 Q4 和全年收入。」— Micron 业绩公告",
        "「我们是唯一美国本土存储制造商。」— Sanjay Mehrotra",
        "「进入 FY2026 时产品组合最具竞争力。」— Sanjay Mehrotra",
        "「HBM 是 AI 服务器的关键瓶颈。」— 行业观点",
        "— 分析师：Micron 是 AI 存储周期里弹性最大的标的之一",
    ],

    "DATA_SOURCE": "经营数据：Micron FY2025 Q4/FY 业绩公告（2025-09-23） · 行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）",
    "FOOTER_LINES": [
        "经营数据：Micron FY2025 Q4/FY 业绩公告（2025-09-23）",
        "行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）",
        "免责声明：本图仅供学习参考，不构成投资建议",
        "by 江明",
    ],
}
