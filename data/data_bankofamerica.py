#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""美国银行经营全解析 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
BLUE = "#3B6EA8"
GOLD = "#C4963C"

DATA = {'TITLE': '美国银行经营全解析',
 'SUBTITLE': 'Bank of America (NYSE: BAC) · 存款、消费金融与投行业务巨头',
 'UPDATE_DATE': '数据更新：FY2025 业绩公告/8-K（2026-01-14）',
 'COMPANY_PROFILE': {'公司全称': 'Bank of America Corporation',
                     '上市代码': 'NYSE: BAC',
                     '创立': '1904 年源起 Bank of Italy',
                     '董事长 / CEO': 'Brian Moynihan',
                     'CFO': 'Alastair Borthwick',
                     '核心业务': 'Consumer Banking + GWIM + Global Banking + Markets',
                     '员工': '约 21 万人',
                     '总部': 'Charlotte, North Carolina',
                     '最新股价 / 市值': '约 $52.7 / $3,755 亿美元 (2026-04-29)',
                     '最新 PE (TTM)': '约 12×'},
 'FINANCIAL_SUMMARY': {'FY2025 营收': '$113.1B (+7% YoY)',
                       'FY2025 净利润': '$30.5B (+13% YoY)',
                       'FY2025 EPS': '$3.81 (+19% YoY)',
                       'ROTCE': '14.2%',
                       'ROE': '10.6%',
                       '存款': '约 $1.9T+',
                       '消费者投资资产': '$599B (+16%)',
                       '客户余额': '$4.8T (+12%)',
                       'Q4 FY25 净利润': '$7.6B'},
 'SEGMENTS_LABEL': '业务分部 / 经营结构',
 'BUSINESS_SEGMENTS': [('1', 'Consumer Banking', '核心', '收入$11.2B(Q4)', '+5%', '▲稳定', '存款/信用卡'),
                       ('2', 'Global Wealth & IM', '财富', '收入$6.6B(Q4)', '+10%', '▲增长', 'Merrill/Private'),
                       ('3', 'Global Banking', '企业', '投行费用增长', '复苏', '▲改善', '贷款/投行'),
                       ('4', 'Global Markets', '交易', '费率/股票强', '强劲', '▲强劲', 'FICC/Equity')],
 'REVENUE_MIX': [('净利息收入', '53%'), ('非息收入', '47%'), ('消费银行', '38%'), ('财富/市场', '24%')],
 'MOVES_LABEL': '关键战略动作',
 'STRATEGIC_MOVES': [('NII', '净息收入恢复', '利率和资产重定价支撑 2025 增长', '#3B6EA8'),
                     ('财富', '客户余额 $4.8T', '市场上涨和净流入推动资产管理费', '#5BA85B'),
                     ('数字', '43 亿次数字登录', '消费者银行数字化降低成本', '#D4793A'),
                     ('投行', '费用收入复苏', '资本市场活跃带来弹性', '#6B4E7A'),
                     ('资本', 'ROTCE 14.2%', '大型银行里资本回报稳健', '#C4963C'),
                     ('风险', '信用周期', '失业率和商业地产是主要压力点', '#D9534F')],
 'MOAT': [('低成本存款基础', '庞大零售存款是银行最核心护城河'),
          ('全国消费者网络', '信用卡、按揭、小企业和日常银行账户形成粘性'),
          ('财富管理规模', 'Merrill 和 Private Bank 客户余额巨大'),
          ('交易和投行业务', '资本市场复苏时提供利润弹性'),
          ('数字化规模效应', '移动银行和数字销售降低边际成本'),
          ('监管大行护城河', '规模带来合规成本优势和信任门槛')],
 'KEY_METRICS': [('市值排名', '第 30 名'),
                 ('FY25 营收', '$113.1B'),
                 ('净利润', '$30.5B'),
                 ('EPS', '$3.81'),
                 ('ROTCE', '14.2%'),
                 ('ROE', '10.6%'),
                 ('客户余额', '$4.8T'),
                 ('数字登录', '43亿次'),
                 ('股价 / 市值', '$52.7 / $3,755 亿'),
                 ('PE', '约 12×')],
 'RISKS_HIGHLIGHTS': [('亮点', '净利润 +13%', '收入增长和费用控制带来经营杠杆'),
                      ('亮点', 'ROTCE 14.2%', '大型银行中资本回报稳健'),
                      ('亮点', '财富客户余额 $4.8T', '资产管理费随市场和净流入增长'),
                      ('风险', '信用损失周期', '经济下行会推高拨备'),
                      ('风险', '利率路径', '降息会影响净息收入'),
                      ('风险', '监管资本要求', '大行资本约束影响回购弹性')],
 'QUOTES_LABEL': '管理层 & 分析师观点',
 'QUOTES': ['「2025 年收入达 $113.1B。」— BofA 8-K',
            '「ROTCE 达 14.2%。」— BofA 8-K',
            '「客户余额达到 $4.8T。」— BofA 公告',
            '「低成本存款是银行护城河。」— 分析师观点',
            '「数字化让零售银行成本结构更轻。」— 行业观点',
            '— 分析师：BAC 是利率周期与美国消费的综合押注'],
 'DATA_SOURCE': '经营数据：Bank of America FY2025 业绩公告/8-K（2026-01-14） · 行情数据：CompaniesMarketCap 全球市值排名页，页面查看 '
                '2026-04-29（市值/股价为页面展示口径）',
 'FOOTER_LINES': ['经营数据：Bank of America FY2025 业绩公告/8-K（2026-01-14）',
                  '行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
                  '免责声明：本图仅供学习参考，不构成投资建议',
                  'by 江明']}

# Codex latest-standard override (2026-06-07)
DATA['COMPANY_PROFILE'].update({
    '最新股价 / 市值': '约 $56.2 / $3,988 亿美元 (2026年6月)',
    '最新 PE (TTM)': '约 14×；Forward PE 约 12×',
})
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$113.1B (+7% YoY)',
    'FY2025 经营利润': 'ROTCE 14.2%',
    'FY2025 经营现金流': '存款 $1.9T+',
    'FY2025 净利润': '$30.5B (+13% YoY)',
    '当前市值': '约 $3,988 亿美元',
    'PE / Forward PE': '约 14× / 12×',
})
DATA['CAPITAL_AND_ROI'] = [
    ('ROTCE / ROE', 'ROTCE 14.2% / ROE 10.6%', '银行不用传统 ROIC；重点看有形普通股回报、ROE、存款成本和信用损失。'),
    ('2026E CapEx', '不适用 / 技术投入', '银行资本投入主要体现为技术平台、风险资产、资本充足率和分行数字化。'),
    ('股东回报', '年化股息约 $1.12/股 + 回购', 'BAC 通过常规股息和监管框架内回购返还资本。'),
]
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Consumer Banking', '约 38%', '$42B级收入', '+5% Q4', '▲稳定', '存款/信用卡'),
    ('2', 'Global Wealth & IM', '约 23%', '$26B级收入', '+10% Q4', '▲增长', 'Merrill/Private'),
    ('3', 'Global Banking', '约 20%', '$22B级收入', '复苏', '▲改善', '贷款/投行'),
    ('4', 'Global Markets', '约 19%', '$21B级收入', '强劲', '▲强劲', 'FICC/Equity'),
]
DATA['REVENUE_MIX'] = [('消费银行', '38%'), ('财富管理', '23%'), ('全球银行', '20%'), ('全球市场', '19%')]
DATA['MOAT'] = [
    ('低成本存款基础', '约 $1.9T+ 存款是 BAC 最核心的资金成本护城河。'),
    ('全国零售网络', '信用卡、按揭、小企业和日常账户形成粘性，消费银行是稳定底盘。'),
    ('财富客户余额 $4.8T', 'Merrill 和 Private Bank 带来长期资产管理费和高净值客户关系。'),
    ('数字银行规模', '移动银行、Erica 和自动化服务降低边际成本，提高客户留存。'),
    ('监管大行门槛', '资本、合规、风控和品牌信任形成新进入者难以复制的成本。'),
]
DATA['MOAT_METRICS'] = {
    '低成本存款基础': '$1.9T+ 存款',
    '全国零售网络': '消费银行约38%收入',
    '财富客户余额 $4.8T': '$4.8T客户余额',
    '数字银行规模': '59M数字客户｜30B互动',
}
DATA['KEY_METRICS'] = [
    ('市值排名', '第 34 名'),
    ('FY25 营收', '$113.1B'),
    ('ROTCE', '14.2%'),
    ('存款', '$1.9T+'),
    ('净利润', '$30.5B'),
    ('当前市值', '$3,988亿'),
    ('PE / Forward PE', '14× / 12×'),
    ('ROE', '10.6%'),
    ('客户余额', '$4.8T'),
    ('股息', '$1.12/股'),
]
DATA['FOOTER_LINES'] = [
    '经营数据：Bank of America FY2025 earnings release / 8-K / annual report，FY2025: 2025年1-12月',
    '同比口径：FY2025 vs FY2024；营收 +7%，净利润 +13%，EPS +19%；银行经营现金流不可比',
    '行情数据：CompaniesMarketCap / StockAnalysis，查看：2026年6月；第34名，市值约 $398.8B，PE 约14×，Forward PE 约12×',
    'ROI口径：银行采用 ROTCE 14.2% / ROE 10.6% 替代 ROIC；重点看有形普通股回报、存款成本和信用损失',
    '2026 CapEx口径：银行不披露可比工业 CapEx；资本投入体现在技术平台、分行数字化、风险资产和资本充足率',
    '股东分红：Bank of America dividend history / company IR，查看：2026年6月；年化股息约 $1.12/股，另有监管框架内回购',
    '经营之道硬指标：Bank of America FY2025 annual report / Fast Facts（存款、客户余额、消费银行占比、59M数字客户、30B数字互动）',
    '管理文化：Bank of America Annual Report / Proxy / Careers / Code of Conduct，核查：2026年6月',
    '免责声明：本图仅供学习参考，不构成投资建议',
    'by 江明',
]

for _i, _line in enumerate(DATA['FOOTER_LINES']):
    if _line.startswith('管理文化：'):
        DATA['FOOTER_LINES'][_i] = '管理文化：BofA Responsible Growth / $25 Minimum Wage / Academy / Employee Benefits，核查：2026年6月'

DATA['LOGO_SLUG'] = 'bankofamerica'
