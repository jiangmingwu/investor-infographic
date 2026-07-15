#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""甲骨文经营全解析 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
BLUE = "#3B6EA8"
GOLD = "#C4963C"

DATA = {'TITLE': '甲骨文经营全解析',
 'SUBTITLE': 'Oracle Corp. (NYSE: ORCL) · 数据库 + 云基础设施 + 企业软件',
 'UPDATE_DATE': '数据更新：FY2025 业绩公告（2025-06-11）',
 'COMPANY_PROFILE': {'公司全称': 'Oracle Corporation',
                     '上市代码': 'NYSE: ORCL',
                     '创立': '1977 年 · Larry Ellison 等创立',
                     '董事长 / CTO': 'Larry Ellison',
                     'CEO': 'Safra Catz',
                     '核心业务': '数据库 + OCI + Fusion/NetSuite SaaS + Java',
                     '员工': '约 16 万人',
                     '总部': 'Austin, Texas',
                     '最新股价 / 市值': '约 $166 / $4,773 亿美元 (2026-04-29)',
                     '最新 PE (TTM)': '约 39×'},
 'FINANCIAL_SUMMARY': {'FY2025 总收入': '$57.4B (+8% YoY)',
                       'FY2025 GAAP 净利润': '$12.4B',
                       'FY2025 Non-GAAP 净利润': '$17.3B',
                       'FY2025 GAAP 经营利润': '$17.7B',
                       'FY2025 Non-GAAP 经营利润': '$25.0B',
                       'Cloud Services + License Support': '$44.0B (+12%)',
                       'Cloud License + On-Prem': '$5.2B (+2%)',
                       '经营现金流': '$20.8B (+12%)',
                       'Q4 RPO': '$138B (+41%)'},
 'SEGMENTS_LABEL': '业务分部 / 经营结构',
 'BUSINESS_SEGMENTS': [('1', 'Cloud+License Support', '76.7%', '$44.0B', '+12%', '▲主力', 'SaaS+支持'),
                       ('2', 'Cloud License/On-Prem', '9.1%', '$5.2B', '+2%', '→稳定', '传统授权'),
                       ('3', 'Hardware+Services', '14.2%', '$8.2B', '低增', '→配套', '设备+咨询')],
 'REVENUE_MIX': [('Cloud+License Support', '76.7%'), ('License/On-Prem', '9.1%'), ('Hardware+Services', '14.2%')],
 'MOVES_LABEL': '关键战略动作',
 'STRATEGIC_MOVES': [('OCI', '云基础设施 +52%', 'Q4 OCI 继续高速增长,AI 训练需求拉动', '#3B6EA8'),
                     ('RPO', '$138B 待履约订单', '云数据中心合同把未来收入锁住', '#5BA85B'),
                     ('多云', 'AWS/Google/Azure 多云数据库', '把 Oracle Database 带进三大云', '#D4793A'),
                     ('SaaS', 'Fusion + NetSuite', '企业应用云仍是现金牛', '#6B4E7A'),
                     ('风险', 'CapEx 与租赁承诺', 'AI 云扩张需要巨额数据中心投入', '#D9534F'),
                     ('护城河', '数据库粘性', '核心业务系统迁移成本极高', '#C4963C')],
 'MOAT': [('Oracle Database 粘性', '银行、政府和大型企业核心系统迁移成本高'),
          ('OCI 差异化云', '围绕数据库和 AI 训练做垂直优化'),
          ('多云策略反常识', '不只和三大云竞争,也把数据库卖进三大云'),
          ('RPO 高可见度', '待履约订单给未来增长提供可见性'),
          ('企业销售网络', '长期 CIO 关系和复杂实施能力'),
          ('高利润软件基因', '授权、支持和 SaaS 现金流支撑云扩张')],
 'KEY_METRICS': [('市值排名', '第 24 名'),
                 ('FY25 收入', '$57.4B'),
                 ('GAAP 净利', '$12.4B'),
                 ('Non-GAAP 净利', '$17.3B'),
                 ('经营现金流', '$20.8B'),
                 ('Q4 RPO', '$138B'),
                 ('Cloud+Support', '$44.0B'),
                 ('股价 / 市值', '$166 / $4,773 亿'),
                 ('PE', '约 39×'),
                 ('OCI Q4 增速', '+52%')],
 'RISKS_HIGHLIGHTS': [('亮点', 'OCI 高速增长', '云基础设施成为第二增长曲线'),
                      ('亮点', 'RPO +41%', '未来收入可见度强'),
                      ('亮点', '数据库多云', '把护城河延伸进 AWS/Google/Azure'),
                      ('风险', '云 CapEx 压力', '数据中心扩张会消耗现金流'),
                      ('风险', '云竞争激烈', 'AWS/Azure/GCP 都是强对手'),
                      ('风险', '债务与租赁承诺', '云基础设施扩张放大资产负债表压力')],
 'QUOTES_LABEL': '管理层 & 分析师观点',
 'QUOTES': ['「FY26 会更好。」— Safra Catz',
            '「OCI demand is skyrocketing。」— Larry Ellison',
            '「多云数据库收入 Q3 到 Q4 增长 115%。」— Oracle 公告',
            '「Oracle 可能成为大型 AI 云基础设施玩家。」— 分析师观点',
            '「数据库护城河仍然深。」— 行业观点',
            '— 分析师：Oracle 是老软件公司云化最强样本'],
 'DATA_SOURCE': '经营数据：Oracle FY2025 业绩公告（2025-06-11） · 行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
 'FOOTER_LINES': ['经营数据：Oracle FY2025 业绩公告（2025-06-11）',
                  '行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
                  '免责声明：本图仅供学习参考，不构成投资建议',
                  'by 江明']}

# Codex latest-standard override (2026-06-07)
DATA['COMPANY_PROFILE'].update({
    '最新股价 / 市值': '约 $214 / $6,222 亿美元 (2026年6月)',
    '最新 PE (TTM)': '约 38×；Forward PE 约 25×',
})
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$57.4B (+8% YoY)',
    'FY2025 经营利润': '$25.0B Non-GAAP / $17.7B GAAP',
    'FY2025 经营现金流': '$20.8B (+12% YoY)',
    'FY2025 净利润': '$17.3B Non-GAAP / $12.4B GAAP',
    '当前市值': '约 $6,222 亿美元',
    'PE / Forward PE': '约 38× / 25×',
})
for _k in ['FY2025 总收入', 'FY2025 GAAP 净利润', 'FY2025 Non-GAAP 净利润', 'FY2025 GAAP 经营利润', 'FY2025 Non-GAAP 经营利润']:
    DATA['FINANCIAL_SUMMARY'].pop(_k, None)
DATA['CAPITAL_AND_ROI'] = [
    ('ROI / ROIC', 'ROIC 约 10%+', '数据库现金流稳定；OCI AI 云扩张和租赁承诺会拉高资本压力。'),
    ('2026E CapEx', 'FY26 高位投入', '数据中心、GPU 集群和 OCI 扩张是主要资本投入方向。'),
    ('股东回报', '年化股息约 $2.00/股', 'Oracle 保留现金投云，同时维持股息和机会性回购。'),
]
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Cloud Services + License Support', '76.7%', '$44.0B', '+12%', '▲主力', '云服务+支持'),
    ('2', 'Cloud License / On-Prem', '9.1%', '$5.2B', '+2%', '→稳定', '授权/本地部署'),
    ('3', 'Hardware + Services', '14.2%', '$8.2B', '低增', '→配套', '设备+咨询'),
]
DATA['MOAT'] = [
    ('数据库核心系统锁定', 'Oracle Database 深入银行、政府和大型企业核心交易系统，迁移成本高。'),
    ('RPO 高可见度', 'FY2025 RPO 达 $138B，同比增长 41%，云合同锁住未来收入。'),
    ('OCI AI 集群', 'OCI 围绕数据库、GPU 训练和企业 AI 工作负载优化，是云增长主线。'),
    ('多云数据库', 'Oracle Database 进入 AWS、Azure、Google Cloud，把老护城河迁移到三大云。'),
    ('强销售网络', '大型企业合同、续费和复杂实施能力，是老软件公司云化的关键组织资产。'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 24 名附近'),
    ('FY25 营收', '$57.4B'),
    ('经营利润', '$25.0B Non-GAAP'),
    ('经营现金流', '$20.8B'),
    ('净利润', '$17.3B Non-GAAP'),
    ('当前市值', '$6,222亿'),
    ('PE / Forward PE', '38× / 25×'),
    ('RPO', '$138B'),
    ('2026E CapEx', '云基建高投入'),
    ('股息', '约 $2.00/股'),
]
DATA['FOOTER_LINES'] = [
    '经营数据：Oracle FY2025 results / Form 10-K，FY2025: 2024年6月-2025年5月',
    '同比口径：FY2025 vs FY2024；收入 +8%，经营现金流 +12%，RPO +41%',
    '行情数据：OpenAI Finance / StockAnalysis / CompaniesMarketCap，查看：2026年6月；市值约 $622.2B，PE 约38×，Forward PE 约25×',
    'ROI口径：ROIC 近似区间；数据库现金流与云基础设施投入并存，租赁和数据中心扩张会影响回报',
    '2026 CapEx口径：公司 FY26 云基础设施/OCI 数据中心扩张和 AI 集群投入口径，未给单一精确全年数',
    '股东分红：Oracle dividend history / Nasdaq，查看：2026年6月；年化股息约 $2.00/股',
    '管理文化：Oracle Annual Report / Careers / Proxy / Larry Ellison & Safra Catz public remarks，核查：2026年6月',
    '免责声明：本图仅供学习参考，不构成投资建议',
    'by 江明',
]

# Display cleanup override: keep main cards Chinese and uncluttered.
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$574亿（同比 +8%）',
    'FY2025 经营利润': '$177亿（通用会计口径）',
    'FY2025 经营现金流': '$208亿（同比 +12%）',
    'FY2025 净利润': '$124亿（通用会计口径）',
    '当前市值': '约 $6,222 亿美元',
    'PE / Forward PE': '约 38× / 25×',
})
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Cloud Services + License Support', '76.7%', '$440亿', '+12%', '▲主力', '云服务+支持'),
    ('2', 'Cloud License / On-Prem', '9.1%', '$52亿', '+2%', '→稳定', '授权/本地部署'),
    ('3', 'Hardware + Services', '14.2%', '$82亿', '低增', '→配套', '设备+咨询'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 24 名附近'),
    ('FY25 营收', '$574亿'),
    ('经营利润', '$177亿'),
    ('经营现金流', '$208亿'),
    ('净利润', '$124亿'),
    ('当前市值', '$6,222亿'),
    ('PE / Forward PE', '38× / 25×'),
    ('RPO', '$1,380亿'),
    ('调整后经营利润', '$250亿'),
    ('股息', '约 $2.00/股'),
]
DATA['FOOTER_LINES'][1] = '同比口径：FY2025 vs FY2024；收入 +8%，经营现金流 +12%，RPO +41%；调整后经营利润约 $250亿，调整后净利润约 $173亿'
