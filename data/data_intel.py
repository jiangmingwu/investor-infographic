#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""英特尔经营全解析 · 经营分析数据"""

GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"
PURPLE = "#6B4E7A"
BLUE = "#3B6EA8"
GOLD = "#C4963C"

DATA = {'TITLE': '英特尔经营全解析',
 'SUBTITLE': 'Intel Corp. (NASDAQ: INTC) · x86 CPU + 美国本土先进制程复兴',
 'UPDATE_DATE': '数据更新：FY2025 业绩公告（2026-01-22）',
 'COMPANY_PROFILE': {'公司全称': 'Intel Corporation',
                     '上市代码': 'NASDAQ: INTC',
                     '创立': '1968 年 · Gordon Moore / Robert Noyce',
                     'CEO': 'Lip-Bu Tan',
                     'CFO': 'David Zinsner',
                     '核心业务': 'Client CPU + Data Center AI + Intel Foundry',
                     '员工': '约 10 万人',
                     '总部': 'Santa Clara, California',
                     '最新股价 / 市值': '约 $84.5 / $4,248 亿美元 (2026-04-29)',
                     '最新 PE (TTM)': 'GAAP 亏损；Non-GAAP 约 223×'},
 'FINANCIAL_SUMMARY': {'FY2025 营收': '$52.9B (YoY 持平)',
                       'FY2025 GAAP 净利润': '-$0.3B',
                       'FY2025 Non-GAAP 净利润': '$1.9B',
                       'FY2025 GAAP 毛利率': '34.8%',
                       'FY2025 Non-GAAP 毛利率': '36.7%',
                       'FY2025 经营现金流': '$9.7B',
                       'Client Computing': '$32.2B (-3%)',
                       'Data Center and AI': '$16.9B (+5%)',
                       'Intel Foundry': '$17.8B (+3%)'},
 'SEGMENTS_LABEL': '业务分部 / 经营结构',
 'BUSINESS_SEGMENTS': [('1', 'Client Computing', '60.9%', '$32.2B', '-3%', '▼承压', 'PC CPU'),
                       ('2', 'Data Center and AI', '31.9%', '$16.9B', '+5%', '▲恢复', '服务器/AI'),
                       ('3', 'Intel Foundry', '33.6%', '$17.8B', '+3%', '▲投入', '代工/制程'),
                       ('4', 'All Other', '6.8%', '$3.6B', '-1%', '→调整', 'Mobileye等')],
 'REVENUE_MIX': [('Client Computing', '60.9%'), ('DCAI', '31.9%'), ('Foundry', '33.6%'), ('All Other', '6.8%')],
 'MOVES_LABEL': '关键战略动作',
 'STRATEGIC_MOVES': [('18A', '首批 18A 产品推出', '美国本土先进制程复兴的关键节点', '#3B6EA8'),
                     ('Foundry', '代工业务继续烧钱', '长期价值取决于外部客户导入', '#D4793A'),
                     ('AI PC', 'x86 在 AI PC 中延续地位', '客户端仍是现金流基础', '#5BA85B'),
                     ('重组', 'Altera 去合并', '聚焦核心 CPU 与 Foundry', '#6B4E7A'),
                     ('风险', 'GAAP 仍亏损', '制程追赶和折旧压力巨大', '#D9534F'),
                     ('政策', '美国半导体战略资产', '政策支持带来估值溢价', '#C4963C')],
 'MOAT': [('x86 生态根基', '企业和 PC 软件生态仍深度依赖 x86'),
          ('美国本土制造战略', '地缘政治让 Intel Foundry 具战略稀缺性'),
          ('客户端规模', 'PC CPU 仍是收入和现金流基础'),
          ('封装与制程资产', '先进封装和晶圆厂资产重,复制难'),
          ('政府与企业关系', '国防、政府、企业供应链强调可控'),
          ('反转期弹性', '若 18A/14A 成功,估值弹性巨大')],
 'KEY_METRICS': [('市值排名', '第 27 名'),
                 ('FY25 营收', '$52.9B'),
                 ('GAAP 净利', '-$0.3B'),
                 ('Non-GAAP 净利', '$1.9B'),
                 ('经营现金流', '$9.7B'),
                 ('CCG', '$32.2B'),
                 ('DCAI', '$16.9B'),
                 ('Foundry', '$17.8B'),
                 ('股价 / 市值', '$84.5 / $4,248 亿'),
                 ('PE', 'GAAP亏损')],
 'RISKS_HIGHLIGHTS': [('亮点', '现金流仍正', '经营现金流 $9.7B 支撑转型'),
                      ('亮点', 'DCAI +5%', '服务器业务开始恢复'),
                      ('亮点', '18A 节点推进', '先进制程是反转核心'),
                      ('风险', 'GAAP 亏损', 'FY25 仍亏损 $0.3B'),
                      ('风险', 'Foundry 投资重', '高 CapEx 和折旧拖累利润'),
                      ('风险', 'AMD/ARM 竞争', '服务器和 PC 份额仍有压力')],
 'QUOTES_LABEL': '管理层 & 分析师观点',
 'QUOTES': ['「CPU 在 AI 时代仍扮演关键角色。」— Lip-Bu Tan',
            '「我们正在建设新的 Intel。」— Lip-Bu Tan',
            '「Q4 超出预期。」— David Zinsner',
            '「18A 是美国制造先进制程的关键节点。」— 行业观点',
            '「Foundry 成败决定 Intel 重估。」— 分析师观点',
            '— 分析师：Intel 是高风险高弹性的国家级半导体资产'],
 'DATA_SOURCE': '经营数据：Intel FY2025 业绩公告/10-K（2026-01-22） · 行情数据：CompaniesMarketCap 全球市值排名页，页面查看 '
                '2026-04-29（市值/股价为页面展示口径）',
 'FOOTER_LINES': ['经营数据：Intel FY2025 业绩公告/10-K（2026-01-22）',
                  '行情数据：CompaniesMarketCap 全球市值排名页，页面查看 2026-04-29（市值/股价为页面展示口径）',
                  '免责声明：本图仅供学习参考，不构成投资建议',
                  'by 江明']}

# Codex latest-standard override (2026-06-07)
DATA['COMPANY_PROFILE'].update({
    '最新股价 / 市值': '约 $114 / $5,044 亿美元 (2026年6月)',
    '最新 PE (TTM)': 'GAAP 亏损/不可比；Forward PE >100×估算',
})
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$52.9B (YoY 持平)',
    'FY2025 经营利润': 'GAAP 承压 / Non-GAAP 低利润',
    'FY2025 经营现金流': '$9.7B',
    'FY2025 净利润': '-$0.3B GAAP / $1.9B Non-GAAP',
    '当前市值': '约 $5,044 亿美元',
    'PE / Forward PE': 'N.M. / >100×估算',
})
for _k in ['FY2025 GAAP 净利润', 'FY2025 Non-GAAP 净利润']:
    DATA['FINANCIAL_SUMMARY'].pop(_k, None)
DATA['CAPITAL_AND_ROI'] = [
    ('ROI / ROIC', 'ROI（净利口径）约 -1%', 'FY2025 GAAP 净亏损，重资产转型期资本回报为负；看 18A/Foundry 修复。'),
    ('2026E CapEx', '高位投入', '晶圆厂、先进封装、18A/14A 和政府补贴项目；重资产转型风险高。'),
    ('股东回报', '不派现金股息', 'Intel 已暂停普通股息；现金优先投向制程和代工转型。'),
]
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Client Computing', '60.9%', '$32.2B', '-3%', '▼承压', 'PC CPU'),
    ('2', 'Data Center and AI', '31.9%', '$16.9B', '+5%', '▲恢复', '服务器/AI'),
    ('3', 'Intel Foundry', '33.6%', '$17.8B', '+3%', '▲投入', '代工/制程'),
    ('4', 'All Other', '6.8%', '$3.6B', '-1%', '→调整', 'Mobileye等'),
]
DATA['MOAT'] = [
    ('x86 生态根基', '企业和 PC 软件生态仍深度依赖 x86，但服务器份额受到 AMD/ARM 持续挑战。'),
    ('美国先进制造战略资产', 'Intel Foundry 是美国本土先进制程复兴的核心载体，具地缘和政策稀缺性。'),
    ('18A/先进封装', '18A 与先进封装是反转关键；成功与否直接决定代工客户信任。'),
    ('客户端规模', 'Client Computing 约 $32.2B，是当前现金流基础和 AI PC 切入口。'),
    ('高风险重资产', '晶圆厂、设备和折旧形成高门槛，也带来现金流和执行压力。'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 27 名附近'),
    ('FY25 营收', '$52.9B'),
    ('经营利润', '低利润/转型期'),
    ('经营现金流', '$9.7B'),
    ('净利润', '-$0.3B GAAP'),
    ('当前市值', '$5,044亿'),
    ('PE / Forward PE', 'N.M. / >100×'),
    ('ROI', '约 -1%'),
    ('2026E CapEx', '高位投入'),
    ('股息', '暂停/0'),
]
DATA['FOOTER_LINES'] = [
    '经营数据：Intel FY2025 earnings release / Form 10-K，FY2025: 2025年1-12月',
    '同比口径：FY2025 vs FY2024；营收大致持平，经营现金流 $9.7B，GAAP 净亏损约 $0.3B',
    '行情数据：OpenAI Finance / StockAnalysis / CompaniesMarketCap，查看：2026年6月；市值约 $504.4B，GAAP PE 不可比，Forward PE >100×估算',
    'ROI口径：FY2025 ROI（净利润口径）约为负；重资产 Foundry 转型期，ROIC 与 GAAP 盈利受折旧和重组影响',
    '2026 CapEx口径：晶圆厂、先进封装、18A/14A 和政策补贴项目；公司未给可简单比较的单项全年美元数',
    '股东分红：Intel dividend history / company IR，查看：2026年6月；普通现金股息暂停，股息率 0%',
    '管理文化：Intel Annual Report / Careers / Proxy / Lip-Bu Tan public remarks，核查：2026年6月',
    '免责声明：本图仅供学习参考，不构成投资建议',
    'by 江明',
]

# Display cleanup override: keep main cards Chinese and uncluttered.
DATA['COMPANY_PROFILE'].update({
    '最新 PE (TTM)': '通用会计亏损/不可比；Forward PE >100×估算',
})
DATA['FINANCIAL_SUMMARY'].update({
    'FY2025 营收': '$529亿（同比持平）',
    'FY2025 经营利润': '亏损/低利润（转型期）',
    'FY2025 经营现金流': '$97亿',
    'FY2025 净利润': '-$3亿（通用会计亏损）',
    '当前市值': '约 $5,044 亿美元',
    'PE / Forward PE': '不适用 / >100×估算',
})
DATA['BUSINESS_SEGMENTS'] = [
    ('1', 'Client Computing', '60.9%', '$322亿', '-3%', '▼承压', 'PC CPU'),
    ('2', 'Data Center and AI', '31.9%', '$169亿', '+5%', '▲恢复', '服务器/AI'),
    ('3', 'Intel Foundry', '33.6%', '$178亿', '+3%', '▲投入', '代工/制程'),
    ('4', 'All Other', '6.8%', '$36亿', '-1%', '→调整', 'Mobileye等'),
]
DATA['KEY_METRICS'] = [
    ('市值排名', '第 27 名附近'),
    ('FY25 营收', '$529亿'),
    ('经营利润', '亏损/低利润'),
    ('经营现金流', '$97亿'),
    ('净利润', '-$3亿'),
    ('当前市值', '$5,044亿'),
    ('PE / Forward PE', '不适用 / >100×'),
    ('调整后净利润', '$19亿'),
    ('2026E CapEx', '高位投入'),
    ('股息', '暂停/0'),
]
DATA['FOOTER_LINES'][1] = '同比口径：FY2025 vs FY2024；营收大致持平，经营现金流约 $97亿；通用会计净亏损约 $3亿，调整后净利润约 $19亿'
DATA['FOOTER_LINES'][2] = '行情数据：OpenAI Finance / StockAnalysis / CompaniesMarketCap，查看：2026年6月；市值约 $504.4B，通用会计 PE 不可比，Forward PE >100×估算'
for _i, _line in enumerate(DATA['FOOTER_LINES']):
    if _line.startswith('管理文化：'):
        DATA['FOOTER_LINES'][_i] = '管理文化：Intel Values / Copy EXACTLY! / Intel Benefits / Working with Intel，核查：2026年6月'

DATA['LOGO_SLUG'] = 'intel'
