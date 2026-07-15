#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMD经营全解析 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
BLUE = "#3B6EA8"
GOLD = "#C4963C"

DATA = {'TITLE': 'AMD经营全解析',
 'SUBTITLE': 'Advanced Micro Devices (NASDAQ: AMD) · CPU + GPU + AI 加速器',
 'UPDATE_DATE': '数据更新：FY2025 业绩公告（2026-02-03）',
 'COMPANY_PROFILE': {'公司全称': 'Advanced Micro Devices, Inc.',
                     '上市代码': 'NASDAQ: AMD',
                     '创立': '1969 年 · Jerry Sanders 等创立',
                     '董事长 / CEO': 'Lisa Su',
                     'CFO': 'Jean Hu',
                     '核心业务': 'EPYC 服务器 CPU + Instinct AI GPU + Ryzen 客户端 + Embedded',
                     '员工': '约 3.0 万人',
                     '总部': 'Santa Clara, California',
                     '最新股价 / 市值': '约 $323 / $5,270 亿美元 (2026-04-29)',
                     '最新 PE (TTM)': '约 122×（按 GAAP 净利 $4.3B）'},
 'FINANCIAL_SUMMARY': {'FY2025 营收': '$34.6B (+34% YoY)',
                       'FY2025 GAAP 净利润': '$4.3B (+164% YoY)',
                       'FY2025 Non-GAAP 净利润': '$6.8B (+26% YoY)',
                       'FY2025 GAAP 毛利率': '50%',
                       'FY2025 Non-GAAP 毛利率': '52%',
                       'FY2025 GAAP 经营利润': '$3.7B',
                       'FY2025 Non-GAAP 经营利润': '$7.8B',
                       'Q4 FY25 营收': '$10.3B (+34% YoY)',
                       'Q1 FY26 指引': '约 $9.8B'},
 'SEGMENTS_LABEL': '业务分部 / 经营结构',
 'BUSINESS_SEGMENTS': [('1', 'Data Center', '47.9%', '$16.6B', '+32%', '▲强劲', 'EPYC + Instinct'),
                       ('2', 'Client + Gaming', '42.1%', '$14.6B', '+51%', '▲爆发', 'Ryzen + Radeon'),
                       ('3', 'Embedded', '10.1%', '$3.5B', '-3%', '▼调整', 'Xilinx/工业')],
 'REVENUE_MIX': [('Data Center', '47.9%'), ('Client+Gaming', '42.1%'), ('Embedded', '10.1%')],
 'MOVES_LABEL': '关键战略动作',
 'STRATEGIC_MOVES': [('AI', 'MI400 / Helios 平台', '向 NVIDIA Blackwell 生态正面追赶', '#3B6EA8'),
                     ('CPU', 'EPYC 持续拿份额', '云厂商与企业服务器替换周期延续', '#5BA85B'),
                     ('客户端', 'Ryzen AI PC 份额提升', '高端 PC 需求复苏 + 产品组合改善', '#D4793A'),
                     ('生态', 'ROCm 软件栈补课', 'AI GPU 成败不只看芯片,还看开发者生态', '#6B4E7A'),
                     ('风险', '估值极高', '市值已按 AI GPU 大规模成功定价', '#D9534F'),
                     ('供应链', '依赖台积电先进制程', 'N3/N2 产能与封装是核心约束', '#C4963C')],
 'MOAT': [('x86 双寡头地位', '服务器和 PC CPU 只剩 Intel/AMD 双主线竞争'),
          ('EPYC 性能功耗比', '云厂商重视 TCO, AMD 在服务器份额持续提升'),
          ('CPU + GPU 组合', '用 EPYC 拉动 Instinct,提供平台级替代方案'),
          ('Xilinx 嵌入式资产', 'FPGA/自适应计算为工业、通信和汽车提供粘性'),
          ('Lisa Su 执行力', '过去十年产品节奏和供应链管理明显改善'),
          ('AI GPU 可选项', '客户需要第二供应商,AMD 是最自然的替代选择')],
 'KEY_METRICS': [('市值排名', '第 23 名'),
                 ('FY25 营收', '$34.6B'),
                 ('GAAP 净利', '$4.3B'),
                 ('Non-GAAP 净利', '$6.8B'),
                 ('Data Center', '$16.6B'),
                 ('Client+Gaming', '$14.6B'),
                 ('毛利率', '50% / 52%'),
                 ('Q4 营收', '$10.3B'),
                 ('股价 / 市值', '$323 / $5,270 亿'),
                 ('PE', '约 122×')],
 'RISKS_HIGHLIGHTS': [('亮点', '营收 +34%', 'Data Center 和客户端共同驱动创纪录收入'),
                      ('亮点', '服务器 CPU 份额提升', 'EPYC 是现金流基本盘'),
                      ('亮点', 'AI GPU 第二供应商', '客户不愿被单一生态锁死'),
                      ('风险', 'ROCm 生态短板', '软件生态仍落后 CUDA'),
                      ('风险', '估值提前反映 AI 成功', 'PE 很高,容错率低'),
                      ('风险', '先进封装供给', 'HBM/CoWoS 和台积电产能是约束')],
 'QUOTES_LABEL': '管理层 & 分析师观点',
 'QUOTES': ['「2025 是 AMD 的定义之年。」— Lisa Su',
            '「我们进入 2026 时拥有强劲动能。」— Lisa Su',
            '「全栈 AI 解决方案正在推动增长。」— AMD 业绩公告',
            '「客户需要 AI 加速器第二来源。」— 分析师观点',
            '「ROCm 是 AMD 追赶 CUDA 的关键。」— 行业观点',
            '— 分析师：AMD 是 AI GPU 竞赛中最重要的挑战者'],
 'DATA_SOURCE': '经营数据：AMD FY2025 业绩公告（2026-02-03） · 行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
 'FOOTER_LINES': ['经营数据：AMD FY2025 业绩公告（2026-02-03）',
                  '行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
                  '免责声明：本图仅供学习参考，不构成投资建议',
                  'by 江明']}

# Codex latest-standard override (2026-06-07)
DATA['COMPANY_PROFILE'].update({
    '最新股价 / 市值': '约 $466 / $7,695 亿美元 (2026年6月)',
    '最新 PE (TTM)': '约 153×；Forward PE 约 58-62×',
})
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$34.6B (+34% YoY)',
    'FY2025 经营利润': '$7.8B Non-GAAP / $3.7B GAAP',
    'FY2025 经营现金流': '$5.0B 级（公司现金流口径）',
    'FY2025 净利润': '$6.8B Non-GAAP / $4.3B GAAP',
    '当前市值': '约 $7,695 亿美元',
    'PE / Forward PE': '约 153× / 58-62×',
})
for _k in ['FY2025 GAAP 净利润', 'FY2025 Non-GAAP 净利润', 'FY2025 GAAP 经营利润', 'FY2025 Non-GAAP 经营利润']:
    DATA['FINANCIAL_SUMMARY'].pop(_k, None)
DATA['CAPITAL_AND_ROI'] = [
    ('ROI / ROIC', 'ROIC 约 5%-10%', 'AI GPU 仍在爬坡；CPU/EPYC 提供现金流，但整体资本效率低于 NVIDIA。'),
    ('2026E CapEx', '低资本强度', 'Fabless 模式；2026 重点是研发、封装合作、MI/ROCm 生态，不是自建晶圆厂。'),
    ('股东回报', '不派现金股息', 'AMD 长期不派常规股息；股东回报主要来自回购、再投资和股价增长。'),
]
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Data Center', '47.9%', '$16.6B', '+32%', '▲强劲', 'EPYC + Instinct'),
    ('2', 'Client', '约 29%', '$10.1B级', '+高增', '▲复苏', 'Ryzen PC'),
    ('3', 'Gaming', '约 13%', '$4.5B级', '+周期', '→波动', 'Radeon/主机'),
    ('4', 'Embedded', '10.1%', '$3.5B', '-3%', '▼调整', 'Xilinx/工业'),
]
DATA['REVENUE_MIX'] = [('Data Center', '47.9%'), ('Client', '29%'), ('Gaming', '13%'), ('Embedded', '10.1%')]
DATA['MOAT'] = [
    ('服务器 CPU 双寡头', 'EPYC 让 AMD 在 x86 服务器 CPU 中成为 Intel 之外最重要的第二供给，云客户有双供需求。'),
    ('Chiplet 架构优势', 'Zen/Chiplet 路线提升良率和成本弹性，是 AMD 过去十年翻盘的核心工程证据。'),
    ('AI GPU 第二供给', 'Instinct MI 系列进入云厂商 AI 供应链；与 NVIDIA 差距仍大，但客户需要替代选择。'),
    ('Xilinx 自适应计算', 'FPGA/嵌入式资产给工业、通信、汽车客户带来更长认证周期和更高粘性。'),
    ('台积电先进制程', 'Fabless + TSMC 先进节点降低自建厂负担，把资本更多投向架构、封装和软件生态。'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 23 名附近'),
    ('FY25 营收', '$34.6B'),
    ('经营利润', '$7.8B Non-GAAP'),
    ('经营现金流', '$5.0B级'),
    ('净利润', '$6.8B Non-GAAP'),
    ('当前市值', '$7,695亿'),
    ('PE / Forward PE', '153× / 58-62×'),
    ('ROIC', '约 5%-10%'),
    ('2026E CapEx', '低资本强度'),
    ('股东回报', '不派现金股息'),
]
DATA['FOOTER_LINES'] = [
    '经营数据：AMD FY2025 earnings release / FY2025 results，FY2025: 2025年1-12月',
    '同比口径：FY2025 vs FY2024；营收 +34%，Non-GAAP净利润 +26%；经营现金流为公司现金流口径整理',
    '行情数据：OpenAI Finance / StockAnalysis / CompaniesMarketCap，查看：2026年6月；市值约 $769.5B，PE 约153×，Forward PE 约58-62×',
    'ROI口径：ROIC/净利润口径区间估算；AI GPU 爬坡期回报不稳定，具体以年报资产负债表为准',
    '2026 CapEx口径：AMD 为 Fabless，未披露可比工业 CapEx；2026 重点为研发、封装、MI/ROCm 生态投入',
    '股东分红：Nasdaq / company dividend history，查看：2026年6月；不派常规现金股息，股东回报主要看回购和再投资',
    '管理文化：AMD Annual Report / Careers / Proxy / Lisa Su interviews，核查：2026年6月',
    '免责声明：本图仅供学习参考，不构成投资建议',
    'by 江明',
]

# Display cleanup override: keep main cards Chinese and uncluttered.
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$346亿（同比 +34%）',
    'FY2025 经营利润': '$37亿（通用会计口径）',
    'FY2025 经营现金流': '$50亿级',
    'FY2025 净利润': '$43亿（通用会计口径）',
    '当前市值': '约 $7,695 亿美元',
    'PE / Forward PE': '约 153× / 58-62×',
})
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Data Center', '47.9%', '$166亿', '+32%', '▲强劲', 'EPYC + Instinct'),
    ('2', 'Client', '约 29%', '$101亿级', '+高增', '▲复苏', 'Ryzen PC'),
    ('3', 'Gaming', '约 13%', '$45亿级', '+周期', '→波动', 'Radeon/主机'),
    ('4', 'Embedded', '10.1%', '$35亿', '-3%', '▼调整', 'Xilinx/工业'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 23 名附近'),
    ('FY25 营收', '$346亿'),
    ('经营利润', '$37亿'),
    ('经营现金流', '$50亿级'),
    ('净利润', '$43亿'),
    ('当前市值', '$7,695亿'),
    ('PE / Forward PE', '153× / 58-62×'),
    ('调整后经营利润', '$78亿'),
    ('调整后净利润', '$68亿'),
    ('股东回报', '不派现金股息'),
]
DATA['FOOTER_LINES'][1] = '同比口径：FY2025 vs FY2024；营收 +34%；调整后净利润 +26%；通用会计与调整后口径差异见 AMD FY2025 results'
