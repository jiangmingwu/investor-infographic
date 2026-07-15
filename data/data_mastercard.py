#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""万事达经营全解析 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
BLUE = "#3B6EA8"
GOLD = "#C4963C"

DATA = {'TITLE': '万事达经营全解析',
 'SUBTITLE': 'Mastercard Inc. (NYSE: MA) · 全球支付网络 + 增值服务',
 'UPDATE_DATE': '数据更新：FY2025 业绩公告（2026-01-29）',
 'COMPANY_PROFILE': {'公司全称': 'Mastercard Incorporated',
                     '上市代码': 'NYSE: MA',
                     '创立': '1966 年 · Interbank Card Association',
                     'CEO': 'Michael Miebach',
                     'CFO': 'Sachin Mehra',
                     '核心业务': '支付网络 + 跨境 + Value-added Services',
                     '员工': '约 3.5 万人',
                     '总部': 'Purchase, New York',
                     '最新股价 / 市值': '约 $508 / $4,489 亿美元 (2026-04-29)',
                     '最新 PE (TTM)': '约 30×'},
 'FINANCIAL_SUMMARY': {'FY2025 净收入': '$32.8B (+16% YoY)',
                       'FY2025 净利润': '$15.0B (+16% YoY)',
                       'FY2025 经营利润': '$18.9B (+21%)',
                       'FY2025 经营利润率': '57.6%',
                       'Adjusted 净利润': '$15.4B',
                       'GDV': '$10.6T (+9%)',
                       '跨境交易量': '+15%',
                       'Switched Transactions': '+10%',
                       'Mastercard/Maestro 卡': '37 亿张'},
 'SEGMENTS_LABEL': '业务分部 / 经营结构',
 'BUSINESS_SEGMENTS': [('1', 'Payment Network', '核心', '$26B+', '+12%', '▲稳定', 'GDV+跨境'),
                       ('2', 'Value-added Services', '高增', '$6B+', '+23%', '▲加速', '安全/数据'),
                       ('3', '跨境交易', '高毛利', '增速+15%', '+15%', '▲强劲', '旅行+电商')],
 'REVENUE_MIX': [('支付网络', '79%'), ('增值服务', '21%'), ('跨境交易增速', '15%')],
 'MOVES_LABEL': '关键战略动作',
 'STRATEGIC_MOVES': [('网络', 'GDV $10.6T', '双边网络效应继续扩大', '#3B6EA8'),
                     ('VAS', '增值服务 +23%', '风控、数据、身份认证提高客户粘性', '#5BA85B'),
                     ('跨境', '跨境 +15%', '旅游和电商带来高毛利增长', '#D4793A'),
                     ('Apple', 'Apple Card 项目', '与大型生态合作扩大触点', '#6B4E7A'),
                     ('回购', '持续资本回报', '高现金流支持回购和分红', '#C4963C'),
                     ('风险', '监管费率压力', '刷卡费、反垄断和实时支付带来压制', '#D9534F')],
 'MOAT': [('全球双寡头网络', 'Visa/Mastercard 构成全球卡组织核心基础设施'),
          ('高经营杠杆', '57.6% 经营利润率,新增交易边际成本低'),
          ('跨境定价权', '跨境、换汇和商业支付是高毛利来源'),
          ('银行和商户关系', '几十年合作协议和合规连接难复制'),
          ('VAS 数据层', '风控、身份、忠诚度和数据服务变成第二层护城河'),
          ('不承担信用风险', '主要赚网络费,不像银行承担贷款违约风险')],
 'KEY_METRICS': [('市值排名', '第 25 名'),
                 ('FY25 净收入', '$32.8B'),
                 ('净利润', '$15.0B'),
                 ('经营利润率', '57.6%'),
                 ('GDV', '$10.6T'),
                 ('跨境增速', '+15%'),
                 ('卡数量', '37 亿张'),
                 ('股价 / 市值', '$508 / $4,489 亿'),
                 ('PE', '约 30×'),
                 ('VAS 增速', '+23%')],
 'RISKS_HIGHLIGHTS': [('亮点', '收入 +16%', '支付网络和增值服务双轮驱动'),
                      ('亮点', 'VAS +23%', '高毛利服务提高天花板'),
                      ('亮点', '经营利润率 57.6%', '全球最优秀的网络型利润结构之一'),
                      ('风险', '刷卡费监管', '美国和欧洲费率上限会影响收入'),
                      ('风险', '实时支付/稳定币', '部分场景可能绕开卡网络'),
                      ('风险', '估值不便宜', '高质量资产长期享受高估值')],
 'QUOTES_LABEL': '管理层 & 分析师观点',
 'QUOTES': ['「2025 was another strong year。」— Michael Miebach',
            '「Value-added services 增长 23%。」— Mastercard 公告',
            '「宏观环境仍支持消费和商业支出。」— Miebach',
            '「支付网络是低资本开支高现金流机器。」— 分析师观点',
            '「监管是唯一长期折价来源。」— 行业观点',
            '— 分析师：Mastercard 是支付网络里的高质量复利资产'],
 'DATA_SOURCE': '经营数据：Mastercard FY2025 业绩公告/SEC 8-K（2026-01-29） · 行情数据：CompaniesMarketCap 全球市值排名页，页面查看 '
                '2026-04-29（市值/股价为页面展示口径）',
 'FOOTER_LINES': ['经营数据：Mastercard FY2025 业绩公告/SEC 8-K（2026-01-29）',
                  '行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
                  '免责声明：本图仅供学习参考，不构成投资建议',
                  'by 江明']}

# Codex latest-standard override (2026-06-07)
DATA['COMPANY_PROFILE'].update({
    '最新股价 / 市值': '约 $491 / $4,385 亿美元 (2026年6月)',
    '最新 PE (TTM)': '约 28×；Forward PE 约 27×',
})
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$32.8B (+16% YoY)',
    'FY2025 经营利润': '$18.9B (+21% YoY)',
    'FY2025 经营现金流': '$16B+级（高现金转化）',
    'FY2025 净利润': '$15.0B (+16% YoY)',
    '当前市值': '约 $4,385 亿美元',
    'PE / Forward PE': '约 28× / 27×',
})
for _k in ['FY2025 净收入']:
    DATA['FINANCIAL_SUMMARY'].pop(_k, None)
DATA['CAPITAL_AND_ROI'] = [
    ('ROI / ROIC', 'ROIC 50%+', '轻资产支付网络，新增交易边际成本低，资本回报率极高。'),
    ('2026E CapEx', '低资本强度', '核心投入是网络安全、Tokenization、数据服务和支付基础设施。'),
    ('股东回报', '年化股息约 $3.04/股 + 回购', '现金流主要通过回购和逐年增长股息返还股东。'),
]
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Payment Network', '约 79%', '$26B+级', '+12%', '▲稳定', 'GDV+跨境'),
    ('2', 'Value-added Services', '约 21%', '$6B+级', '+23%', '▲加速', '安全/数据'),
    ('3', '跨境交易', '15%增速', '+15%', '+15%', '▲强劲', '旅行+电商'),
]
DATA['REVENUE_MIX'] = [('支付网络', '79%'), ('增值服务', '21%'), ('跨境交易增速', '+15%')]
DATA['MOAT'] = [
    ('全球支付双寡头', 'Visa/Mastercard 构成全球银行卡网络核心基础设施，商户和发卡行两端锁定。'),
    ('57.6% 经营利润率', 'FY2025 经营利润率 57.6%，体现轻资产网络高经营杠杆。'),
    ('GDV $10.6T', '总交易额达到 $10.6T，规模越大，风控数据和网络接受度越强。'),
    ('增值服务 +23%', '安全、身份、咨询、数据服务形成第二层护城河，提高客户粘性。'),
    ('不承担信用风险', '主要收网络费和服务费，不像银行承担贷款违约风险。'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 25 名附近'),
    ('FY25 营收', '$32.8B'),
    ('经营利润', '$18.9B'),
    ('经营现金流', '$16B+级'),
    ('净利润', '$15.0B'),
    ('当前市值', '$4,385亿'),
    ('PE / Forward PE', '28× / 27×'),
    ('ROIC', '50%+'),
    ('GDV', '$10.6T'),
    ('股息', '$3.04/股'),
]
DATA['FOOTER_LINES'] = [
    '经营数据：Mastercard FY2025 earnings release / SEC 8-K，FY2025: 2025年1-12月',
    '同比口径：FY2025 vs FY2024；净收入 +16%，经营利润 +21%，净利润 +16%',
    '行情数据：OpenAI Finance / StockAnalysis / Macrotrends，查看：2026年6月；市值约 $438.5B，PE 约28×，Forward PE 约27×',
    'ROI口径：ROIC 50%+ 为轻资产网络公司资本回报区间判断；以年报现金流和资本结构为准',
    '2026 CapEx口径：Mastercard 未披露工业型 CapEx；网络安全、Tokenization、数据服务和基础设施为主要投入方向',
    '股东分红：Mastercard dividend history / Nasdaq，查看：2026年6月；年化股息约 $3.04/股，另有持续回购',
    '管理文化：Mastercard Annual Report / Careers / Proxy / Code of Conduct，核查：2026年6月',
    '免责声明：本图仅供学习参考，不构成投资建议',
    'by 江明',
]

for _i, _line in enumerate(DATA['FOOTER_LINES']):
    if _line.startswith('管理文化：'):
        DATA['FOOTER_LINES'][_i] = '管理文化：Mastercard Inclusive Growth / CEO Letter / Code of Conduct / Volunteer Time Off，核查：2026年6月'

DATA['LOGO_SLUG'] = 'mastercard'
