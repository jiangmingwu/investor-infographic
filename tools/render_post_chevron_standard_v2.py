#!/usr/bin/env python3
"""Regenerate every company after Chevron from one researched visual standard.

The four pages share one company packet. Strategy and panorama are rendered by
``company_visual_standard_v2``; profile and culture reuse the approved
Coca-Cola-era page family. All final text and charts are deterministic HTML/SVG.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops


ROOT = Path("/Users/jiangming/Documents/Playground")
TEMPLATE_ROOT = Path("/Users/jiangming/templates")
OUTPUT_ROOT = Path("/Users/jiangming/持仓分析/公司经营分析")
REVIEW_ROOT = OUTPUT_ROOT / "_review" / "post_chevron_standard_v2_20260714"
HTML_ROOT = REVIEW_ROOT / "html"
PACKET_ROOT = REVIEW_ROOT / "packets"
BACKUP_ROOT = REVIEW_ROOT / "backup_before_v2"
LOGO_ROOT = TEMPLATE_ROOT / "assets" / "company_logos" / "visible"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
TODAY = "2026年7月14日"
TODAY_MONTH = "2026年7月"

if str(TEMPLATE_ROOT) not in sys.path:
    sys.path.insert(0, str(TEMPLATE_ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import company_visual_standard_v2 as visual  # noqa: E402
from render_post_cocacola_profile_culture import (  # noqa: E402
    COMPANIES,
    culture_page,
    profile_height,
    profile_page,
    render_html,
)


def driver(title: str, icon: str, metric: str, explanation: str, source: str) -> dict[str, str]:
    return {
        "title": title,
        "icon": icon,
        "metric": metric,
        "explanation": f"行业含义：{explanation}",
        "source": source,
    }


EVIDENCE: dict[str, dict[str, Any]] = {
    "pg": {
        "thesis": "用少数高频刚需品类、全球品牌组合和渠道执行，把日常消费转化为长期复购与现金流。",
        "drivers": [
            driver("织物与家居护理", "home", "占集团销售36% · 利润35%", "最大板块同时贡献约三分之一收入和利润，是规模与复购底盘。", "https://us.pg.com/annualreport2025/"),
            driver("十品类品牌组合", "brands", "5大板块 · 10个品类", "聚焦有限品类，比无边界扩张更容易集中研发、广告和货架资源。", "https://us.pg.com/structure-and-governance/corporate-structure/"),
            driver("全球分销网络", "globe", "约180个国家和地区", "广覆盖让新品、定价与供应链能力可跨市场复用。", "https://us.pg.com/about-us/"),
        ],
        "segments": [("织物与家居护理", "36%", "$30.3B", "销售占比"), ("婴儿/女性/家庭护理", "25%", "$21.1B", "销售占比"), ("美容", "18%", "$15.2B", "销售占比"), ("健康护理", "14%", "$11.8B", "销售占比"), ("剃须护理", "7%", "$5.9B", "销售占比")],
        "moves": [("组织", "强化品类责任制", "继续以十个品类为经营单元，把创新、品牌和供应链责任压到业务一线。"), ("效率", "供应链重构", "以生产网络和产品组合优化抵消原材料、关税与渠道成本压力。")],
        "quote": "我们服务消费者，消费者才是老板。",
        "signals": [("亮点", "品牌复购", "最大板块贡献36%销售，日常刚需降低单一爆款依赖。"), ("风险", "增长与成本", "FY2025营收仅同比+0.3%，成本和汇率仍会压缩利润弹性。")],
    },
    "roche": {
        "thesis": "把制药与诊断放在同一体系，用疾病检测、药物研发和临床数据形成相互增强的精准医疗平台。",
        "drivers": [
            driver("创新药平台", "pill", "销售CHF47.7B · 占77.5%", "制药是主要利润引擎，规模足以长期承担高强度研发。", "https://www.roche.com/investors/updates/inv-update-2026-01-29"),
            driver("诊断平台", "scan", "销售CHF13.8B · 覆盖2.58亿人", "诊断触达规模为药物开发、伴随诊断和临床决策提供独特入口。", "https://www.roche.com/investors/annualreport25"),
            driver("临床与研发转化", "flask", "3900万+患者 · 10个新药进入末期开发", "患者覆盖和后期管线数量说明研发不是口号，而是可持续的新产品来源。", "https://www.roche.com/investors/annualreport25"),
        ],
        "segments": [("制药", "77.5%", "$58.98B", "FY2025销售"), ("诊断", "22.5%", "$17.13B", "FY2025销售")],
        "moves": [("研发", "十项潜在新药进入末期", "2025年推进10项潜在新药进入最终开发阶段，并取得12项后期临床阳性结果。"), ("诊断", "全基因组不足4小时", "下一代测序技术把整个人类基因组解码时间压缩到4小时以内。")],
        "quote": "持续聚焦运营和研发卓越，是罗氏2025年强劲表现的基础。",
        "signals": [("亮点", "双平台协同", "制药与诊断分别占77.5%和22.5%，业务角色清晰。"), ("风险", "诊断增速", "诊断销售按瑞郎口径同比-3%，中国医疗定价改革带来压力。")],
    },
    "homedepot": {
        "thesis": "用密集门店、专业客户关系和履约网络，把低频家装需求变成高可信度的一站式采购系统。",
        "drivers": [
            driver("北美门店网络", "store", "2350+家门店 · 年销售$164.7B", "全球最大家装专业零售商的密度形成采购、库存与到店便利优势。", "https://ir.homedepot.com/financial-reports/annual-reports"),
            driver("专业客户生态", "tools", "Pro约占销售50%", "专业承包商采购频率、客单价和项目黏性高于普通消费者。", "https://ir.homedepot.com/events-and-presentations/default.aspx"),
            driver("复杂订单履约", "truck", "$18.25B收购SRS", "用SRS补齐屋顶、泳池和专业建材配送，扩大可服务项目规模。", "https://corporate.homedepot.com/news/company/home-depot-completes-acquisition-srs-distribution"),
        ],
        "segments": [("美国门店", "主体", "$150B+", "销售核心"), ("加拿大与墨西哥", "补充", "$10B+", "国际业务"), ("SRS专业分销", "新增", "$18.25B", "收购对价")],
        "moves": [("并购", "整合SRS Distribution", "把专业承包商品类、销售团队和复杂项目配送并入Pro生态。"), ("履约", "强化同日与次日配送", "用门店、市场配送中心和直送网络降低大件商品履约摩擦。")],
        "quote": "我们要成为专业客户完成整个项目时最可信赖的伙伴。",
        "signals": [("亮点", "规模与专业客户", "2350+门店叠加Pro约50%销售，构成零售与分销双网络。"), ("风险", "住宅周期", "高利率和房屋成交疲弱会延后大型装修项目。")],
    },
    "hsbc": {
        "thesis": "以亚洲财富和跨境贸易为利润中心，用全球结算、存款和企业网络连接东西方资本流。",
        "drivers": [
            driver("低成本存款底盘", "bank", "$1.8T客户存款", "超大存款基础降低资金成本，并支撑信贷、支付和财富管理交叉销售。", "https://www.hsbc.com/investors/results-and-announcements/annual-report"),
            driver("跨境客户网络", "globe", "约4100万客户 · 56个市场", "覆盖主要贸易与资金中心，跨境企业不必在每个国家重建银行关系。", "https://www.hsbc.com/who-we-are"),
            driver("资本与风险能力", "shield", "CET1 14.9% · RoTE 13.3%", "资本缓冲与有形股本回报同时可见，说明规模不是靠过度杠杆换来。", "https://www.hsbc.com/investors/results-and-announcements/annual-report"),
        ],
        "segments": [("财富与个人银行", "核心", "$30B+", "收入底盘"), ("商业银行", "核心", "$20B+", "贸易与企业"), ("全球银行与市场", "核心", "$15B+", "资本市场")],
        "moves": [("聚焦", "重组为四大业务", "按香港、英国、企业及机构银行、国际财富与卓越理财重组，压缩管理层级。"), ("资本", "提高股东分配", "在保持14.9% CET1的同时继续现金股息和回购。")],
        "quote": "我们的优势来自在最重要的国际资金流之间建立连接。",
        "signals": [("亮点", "存款与跨境", "$1.8T存款支撑56个市场的全球客户网络。"), ("风险", "利率与监管", "降息会压缩净利息收入，多司法辖区提高合规成本。")],
    },
    "arm": {
        "thesis": "以低功耗计算架构和IP授权成为芯片行业的公共底座，再从手机向汽车、云与AI扩张。",
        "drivers": [
            driver("移动计算标准", "phone", "全球约99%智能手机采用Arm", "接近全覆盖的生态让软件、工具链和芯片设计围绕Arm形成默认标准。", "https://www.arm.com/company"),
            driver("超大安装基础", "chip", "累计3500亿+颗Arm芯片", "庞大装机量带来持续版税、兼容性和开发者学习成本。", "https://newsroom.arm.com/blog/arm-350-billion-chips"),
            driver("开发者生态", "code", "2200万+软件开发者", "开发者规模提高新架构迁移速度，并强化客户切换成本。", "https://www.arm.com/company"),
        ],
        "segments": [("版税收入", "53.1%", "$2.61B", "FY2026"), ("授权及其他", "46.9%", "$2.31B", "FY2026")],
        "moves": [("产品", "Armv9提高版税率", "新一代架构进入旗舰手机、汽车和数据中心，推动每颗芯片价值提升。"), ("云AI", "推进Neoverse与CSS", "从单一IP授权延伸到更完整的计算子系统，缩短客户芯片开发周期。")],
        "quote": "计算需求正在从通用走向专用，而Arm处在每一个终端的交汇处。",
        "signals": [("亮点", "生态标准", "99%智能手机与3500亿+累计芯片形成极强兼容性壁垒。"), ("风险", "高估值", "当前PE与Forward PE均高，增长兑现要求很高。")],
    },
    "palantir": {
        "thesis": "把组织的数据、权限与AI模型接入同一操作系统，让复杂机构直接在真实流程中部署和执行AI。",
        "drivers": [
            driver("政府业务", "shield", "$2.40B收入 · 占53.7% · +53%", "长期高敏感度任务证明产品能通过安全、权限和可靠性门槛。", "https://investors.palantir.com/financials/annual-reports"),
            driver("商业业务", "factory", "$2.07B收入 · 占46.3% · +60%", "商业收入高速增长说明平台正从政府场景复制到企业生产流程。", "https://investors.palantir.com/financials/annual-reports"),
            driver("美国商业扩张", "bolt", "$1.5B收入 · 同比+109%", "美国企业采用速度远超整体，AIP正在形成第二增长曲线。", "https://investors.palantir.com/news-details/2026/Palantir-Reports-Fourth-Quarter-and-Full-Year-2025-Results/"),
        ],
        "segments": [("政府", "53.7%", "$2.40B", "FY2025收入"), ("商业", "46.3%", "$2.07B", "FY2025收入")],
        "moves": [("产品", "AIP进入生产流程", "用Bootcamp把模型演示压缩为可运行工作流，缩短企业试用到部署的时间。"), ("市场", "扩大美国商业团队", "聚焦高价值企业场景，推动美国商业收入突破$1.5B。")],
        "quote": "软件的价值不在展示AI，而在让组织真正采取行动。",
        "signals": [("亮点", "双引擎增长", "政府与商业收入分别+53%和+60%，增长不是单一客户驱动。"), ("风险", "估值与集中度", "估值隐含长期高增长，政府采购周期仍会造成季度波动。")],
    },
    "agriculturalbank": {
        "thesis": "以全国县域网络和低成本存款为根基，把服务三农的政策定位转化为难以复制的客户与分支覆盖。",
        "drivers": [
            driver("县域金融网络", "field", "23128个境内网点 · 全球银行一级资本第3", "广泛下沉网络覆盖其他大型银行难以经济触达的县域客户。", "https://www.abchina.com/zt/aboutabc/nhfm/nhjj/"),
            driver("超大存贷款底盘", "bank", "总资产$7.18T · 客户存款$5.69T", "资产和存款规模带来低资金成本、客户入口和系统重要性。", "https://www.abchina.com/en/investor-relations/investment-value/business-edges/"),
            driver("数字县域入口", "phone", "县域手机银行月活1.3亿", "数字触达把高成本线下服务转化为可规模复制的远程运营。", "https://www.abchina.com/en/investor-relations/investment-value/business-edges/"),
        ],
        "segments": [("公司银行", "主体", "$50B+", "营业收入"), ("个人银行", "主体", "$45B+", "营业收入"), ("资金运营", "补充", "$10B+", "营业收入")],
        "moves": [("县域", "强化三农与乡村振兴", "2025年县域手机银行月活达到1.3亿，继续把线下网络数字化。"), ("资产", "扩大融资供给", "贷款总额达到$3.99T，同比增长约$0.33T。")],
        "quote": "服务乡村振兴的领军银行，服务实体经济的主力银行。",
        "signals": [("亮点", "存款与县域", "$5.69T客户存款叠加23128个网点，形成低成本资金和触达壁垒。"), ("风险", "息差与信用", "净息差受国内低利率影响，县域与房地产信用风险仍需跟踪。")],
    },
    "merck": {
        "thesis": "以Keytruda建立肿瘤学现金流，再用联合疗法、疫苗和动物保健延长创新药组合的生命周期。",
        "drivers": [
            driver("Keytruda肿瘤平台", "cell", "$31.68B销售 · 占营收48.7%", "单品规模证明临床与商业壁垒极强，也为大量联合疗法研发提供现金。", "https://www.merck.com/news/merck-announces-fourth-quarter-and-full-year-2025-financial-results/"),
            driver("处方药组合", "pill", "$58.14B销售 · 占89.4%", "处方药是绝对核心，全球准入与医学事务网络可复用于新药上市。", "https://www.merck.com/news/merck-announces-fourth-quarter-and-full-year-2025-financial-results/"),
            driver("动物保健", "medical", "$6.35B销售 · 同比+8%", "独立于人用药专利周期，提供更稳定的第二利润来源。", "https://www.merck.com/news/merck-announces-fourth-quarter-and-full-year-2025-financial-results/"),
        ],
        "segments": [("制药", "89.4%", "$58.14B", "FY2025销售"), ("动物保健", "9.8%", "$6.35B", "FY2025销售"), ("其他", "0.8%", "$0.52B", "FY2025销售")],
        "moves": [("管线", "降低Keytruda专利悬崖", "扩大皮下注射、联合疗法和新适应症，并通过并购补充心血管与免疫管线。"), ("组合", "强化动物保健", "保持动物药增长，降低人用肿瘤单品集中度。")],
        "quote": "科学上的突破，只有真正改善患者结局才有价值。",
        "signals": [("亮点", "肿瘤领导力", "Keytruda单品销售$31.68B，接近集团营收一半。"), ("风险", "单品集中", "48.7%营收来自Keytruda，专利与竞品风险高度集中。")],
    },
    "icbc": {
        "thesis": "以全球最大级别的客户存款和企业关系为底盘，用规模、低成本资金和综合金融服务获取稳健回报。",
        "drivers": [
            driver("全球规模", "bank", "总资产约$7.87T · 全球银行一级资本第1", "全球最大级别资产负债表带来融资、定价和客户覆盖优势。", "https://www.icbc-ltd.com/en/page/1220435982957096960.html"),
            driver("存款护城河", "coin", "客户存款约$5.7T", "庞大存款是银行最核心的低成本原料，并提高客户交叉销售机会。", "https://www.icbc-ltd.com/en/page/1220435982957096960.html"),
            driver("企业与零售网络", "network", "客户超7亿 · 境外机构400+", "客户与跨境网络使支付、信贷、结算和财富业务可在同一关系上复用。", "https://www.icbc-ltd.com/en/column/1438058341683679288.html"),
        ],
        "segments": [("公司金融", "核心", "$40B+", "营业收入"), ("个人金融", "核心", "$40B+", "营业收入"), ("资金业务", "补充", "$15B+", "营业收入")],
        "moves": [("数字化", "推进D-ICBC", "把账户、支付、信贷与风控迁移到统一数字基础设施。"), ("风控", "继续压降不良", "以拨备、资本和不良贷款处置维持超大资产负债表韧性。")],
        "quote": "建设具有全球竞争力的世界一流现代金融企业。",
        "signals": [("亮点", "规模与存款", "$7.87T资产和约$5.7T存款形成全球最大级别金融底盘。"), ("风险", "息差与资产质量", "低利率压缩息差，房地产及地方融资信用风险仍需持续消化。")],
    },
    "goldmansachs": {
        "thesis": "以顶级投行关系为入口，把并购、融资、做市和资产管理连接成服务全球机构客户的资本网络。",
        "drivers": [
            driver("并购顾问", "chart", "全球M&A顾问第1 · 连续23年", "长期排名第一反映CEO关系、行业知识和复杂交易执行的复合壁垒。", "https://www.goldmansachs.com/investor-relations/financials/current/annual-reports/2025-annual-report"),
            driver("融资与做市", "network", "$11.4B融资业务收入 · 占FICC/股票37%", "客户融资与交易互相强化，提高机构钱包份额和收入韧性。", "https://www.goldmansachs.com/investor-relations/financials/current/annual-reports/2025-annual-report"),
            driver("资产与财富管理", "coin", "$3.6T管理及监督资产", "长期资产管理费降低投行业务周期性，并沉淀高净值与机构客户关系。", "https://www.goldmansachs.com/investor-relations/financials/current/annual-reports/2025-annual-report"),
        ],
        "segments": [("全球银行与市场", "约70%", "$40B+", "净收入"), ("资产与财富管理", "约30%", "$17B+", "净收入")],
        "moves": [("聚焦", "退出大众消费金融", "把资本和管理注意力重新集中到投行、市场与资产管理。"), ("资产管理", "扩大管理费资产", "继续募集另类资产与长期资金，平滑交易收入周期。")],
        "quote": "我们的客户专营权，来自在最重要时刻提供最可信的判断。",
        "signals": [("亮点", "投行领导力", "M&A顾问连续23年全球第1，交易关系壁垒可验证。"), ("风险", "资本市场周期", "承销、并购和交易收入仍受市场活跃度影响。")],
    },
    "novartis": {
        "thesis": "聚焦创新药，把资源集中到少数高增长治疗领域和可全球放大的重磅产品。",
        "drivers": [
            driver("心血管平台", "heart", "Entresto销售$7.75B", "全球重磅产品规模证明临床差异化、准入与医生采用已形成壁垒。", "https://www.novartis.com/investors/financial-data/annual-results"),
            driver("免疫平台", "shield", "Cosentyx销售$6.67B", "多适应症与长期真实世界数据支撑持续处方和全球放量。", "https://www.novartis.com/investors/financial-data/annual-results"),
            driver("增长型新药", "bolt", "Kisqali $4.78B +58% · Kesimpta $4.43B +37%", "两款产品同时高增长，降低公司对单一成熟药物的依赖。", "https://www.novartis.com/investors/financial-data/annual-results"),
        ],
        "segments": [("Entresto", "14%", "$7.75B", "净销售"), ("Cosentyx", "12%", "$6.67B", "净销售"), ("Kisqali", "9%", "$4.78B", "净销售"), ("Kesimpta", "8%", "$4.43B", "净销售")],
        "moves": [("聚焦", "完成纯创新药转型", "剥离Sandoz后，把资本与组织集中于创新药和四大治疗领域。"), ("管线", "放大放射配体与RNA平台", "通过自研和交易补充下一代技术平台。")],
        "quote": "我们的战略是少做一些事情，但把真正改变患者生命的事情做到最好。",
        "signals": [("亮点", "多产品增长", "四款核心药合计销售约$23.6B，增长引擎不只一项。"), ("风险", "专利与定价", "成熟药专利到期和各国药价谈判会侵蚀增长。")],
    },
    "astrazeneca": {
        "thesis": "以肿瘤学为核心，用多款重磅药、全球临床网络和持续管线投入冲击2030年$80B收入目标。",
        "drivers": [
            driver("肿瘤学平台", "cell", "$23.70B收入 · 占40.3% · +17%", "肿瘤是最大业务且保持双位数增长，构成最清晰的核心引擎。", "https://www.astrazeneca.com/investor-relations/annual-reports.html"),
            driver("重磅药组合", "pill", "16款重磅药 · Farxiga $8.49B", "多产品组合降低单一药物风险，并提高全球商业基础设施利用率。", "https://www.astrazeneca.com/investor-relations/annual-reports.html"),
            driver("长期管线", "flask", "2030目标$80B · 计划20款新药", "公开目标和新药数量把研发投入转化为可跟踪的增长里程碑。", "https://www.astrazeneca.com/media-centre/press-releases/2024/astrazeneca-sets-bold-ambition-for-2030.html"),
        ],
        "segments": [("肿瘤", "40.3%", "$23.70B", "FY2025"), ("生物制药", "约40%", "$23B+", "FY2025"), ("罕见病", "约14%", "$8B+", "FY2025")],
        "moves": [("目标", "推进2030年$80B收入", "围绕肿瘤、生物制药与罕见病扩展适应症和全球准入。"), ("产能", "扩大细胞治疗与生物制造", "为下一代药物平台建设专用研发和生产能力。")],
        "quote": "到2030年，我们要带来20款新药，并实现$80B总收入。",
        "signals": [("亮点", "肿瘤增长", "$23.70B肿瘤收入占40.3%，同比仍增长17%。"), ("风险", "研发兑现", "$80B目标依赖多个后期项目按期成功和获批。")],
    },
    "philipmorris": {
        "thesis": "用IQOS和ZYN把传统烟草现金流迁移到无烟产品，并依靠全球分销与监管能力扩大新品类。",
        "drivers": [
            driver("无烟产品", "spark", "$16.9B收入 · 占41.5%", "无烟已接近集团收入一半，转型不再只是远期叙事。", "https://www.pmi.com/investor-relations/reports-filings"),
            driver("用户与市场覆盖", "people", "4350万成年用户 · 106个市场", "用户和市场规模证明产品已跨过早期试用阶段。", "https://www.pmi.com/our-business/smoke-free-products"),
            driver("加热烟草领导力", "trophy", "IQOS约占加热烟草销量76%", "类别内高份额带来品牌、设备生态和烟弹复购优势。", "https://www.pmi.com/investor-relations/reports-filings"),
        ],
        "segments": [("无烟产品", "41.5%", "$16.9B", "FY2025收入"), ("传统卷烟", "58.5%", "$23.8B", "FY2025收入")],
        "moves": [("转型", "累计投入无烟研发$16B+", "自2008年以来持续建设IQOS、口含烟和科学验证体系。"), ("组合", "放大ZYN与IQOS", "通过美国口含烟与国际加热烟草形成两条无烟增长曲线。")],
        "quote": "我们的目标，是让无烟未来尽快成为现实。",
        "signals": [("亮点", "转型规模", "无烟收入占41.5%，4350万用户覆盖106个市场。"), ("风险", "监管", "尼古丁产品面临税收、营销和健康监管不确定性。")],
    },
    "kla": {
        "thesis": "以检测、量测和良率管理成为先进制程的质量控制层；芯片越复杂，客户越不能省略过程控制。",
        "drivers": [
            driver("过程控制平台", "scan", "$12.16B营收 · 同比+23.9%", "高速增长说明先进制程对缺陷检测和量测的投入强度继续提高。", "https://ir.kla.com/financial-information/annual-reports-and-proxies"),
            driver("高资本回报", "gauge", "FY2025 ROIC 70.7%", "极高资本效率通常来自技术定价权、软件价值和客户切换成本。", "https://stockanalysis.com/stocks/klac/statistics/"),
            driver("服务收入", "tools", "服务约占收入22%", "装机后的维护、校准与升级形成更稳定的订阅式现金流。", "https://ir.kla.com/financial-information/annual-reports-and-proxies"),
        ],
        "segments": [("半导体过程控制", "主体", "$9B+", "收入核心"), ("专业半导体过程", "补充", "$1B+", "产品线"), ("PCB/显示与零部件", "补充", "$1B+", "产品线"), ("服务", "约22%", "$2.7B", "经常性收入")],
        "moves": [("EUV", "提高先进封装与EUV覆盖", "继续把检测与量测工具推进到EUV、Chiplet和先进封装环节。"), ("服务", "扩大装机服务收入", "用全球服务网络提高设备利用率并沉淀长期客户关系。")],
        "quote": "没有过程控制，就没有可量产的先进制程。",
        "signals": [("亮点", "资本效率", "ROIC 70.7%与22%服务收入共同反映技术定价权。"), ("风险", "半导体周期", "晶圆厂资本开支波动和出口限制会影响订单。")],
    },
    "gevernova": {
        "thesis": "用燃气发电、电网设备和长期服务覆盖电力系统关键环节，直接受益于全球电气化与AI用电增长。",
        "drivers": [
            driver("全球装机基础", "bolt", "约7000台燃机 · 约5.9万台风机", "庞大装机带来备件、维护、升级和客户运行数据。", "https://www.gevernova.com/investors/annual-reports"),
            driver("长期积压订单", "chart", "$150B backlog · 55%+为服务", "大量服务积压提高未来收入可见度，并降低单纯设备周期性。", "https://www.gevernova.com/news/press-releases/ge-vernova-reports-fourth-quarter-and-full-year-2025-financial-results"),
            driver("电网与电气化", "network", "$9.64B收入 · +28% · backlog +48%", "电网是新能源和数据中心扩张的瓶颈，高增长反映结构性供不应求。", "https://www.gevernova.com/news/press-releases/ge-vernova-reports-fourth-quarter-and-full-year-2025-financial-results"),
        ],
        "segments": [("Power", "52%", "$19.77B", "FY2025收入"), ("Wind", "24%", "$9.11B", "FY2025收入"), ("Electrification", "25%", "$9.64B", "FY2025收入")],
        "moves": [("产能", "扩大发电与电网产能", "围绕燃机、电力变压器和高压设备扩产以消化积压订单。"), ("风电", "修复海上风电经济性", "收缩低回报项目并聚焦更可盈利的服务和陆上风电。")],
        "quote": "世界上约四分之一的电力依赖我们的技术。",
        "signals": [("亮点", "订单可见度", "$150B积压且55%+为服务，为多年增长提供可见度。"), ("风险", "执行与保修", "大规模扩产、风电亏损和长期设备保修仍考验执行。")],
    },
    "rbc": {
        "thesis": "以加拿大领先的零售与商业银行为核心，通过财富管理、保险和资本市场放大同一客户关系。",
        "drivers": [
            driver("加拿大零售银行", "people", "约1500万客户 · 关键零售产品份额第1", "高客户渗透与主账户关系提供低成本存款和交叉销售入口。", "https://www.rbc.com/investor-relations/_assets-custom/pdf/ar_2025_e.pdf"),
            driver("商业银行", "building", "约140万客户 · 贷款与存款份额第1", "中小企业主账户关系提高信贷、支付和员工金融的综合价值。", "https://www.rbc.com/investor-relations/_assets-custom/pdf/ar_2025_e.pdf"),
            driver("财富与资本市场", "chart", "加拿大最大基金公司 · 投行市场份额第1", "财富管理费和投行业务提升每个客户关系的收入深度。", "https://www.rbc.com/investor-relations/_assets-custom/pdf/ar_2025_e.pdf"),
        ],
        "segments": [("个人与商业银行", "最大", "$25B+", "收入核心"), ("财富管理", "第二", "$10B+", "管理费"), ("资本市场", "第三", "$9B+", "交易与投行"), ("保险", "补充", "$4B+", "保费及投资")],
        "moves": [("并购", "整合HSBC Canada", "扩大高净值、商业和国际客户基础，并释放分支与产品协同。"), ("协同", "推进OneRBC", "让银行、财富和资本市场团队共享客户关系与转介。")],
        "quote": "OneRBC意味着用整个集团服务一个客户，而不是让客户适应组织边界。",
        "signals": [("亮点", "客户份额", "1500万个人客户和140万商业客户均建立在加拿大领先份额上。"), ("风险", "加拿大集中", "房地产、消费者负债和本国经济周期仍是主要风险。")],
    },
    "ibm": {
        "thesis": "围绕混合云与企业AI，把Red Hat软件、主机和咨询能力组合为大型机构可长期运行的技术栈。",
        "drivers": [
            driver("软件与Red Hat", "cloud", "软件约占收入45% · 固定汇率+9%", "高占比软件收入提高经常性收入、毛利率和客户切换成本。", "https://www.ibm.com/investor/annual-report"),
            driver("企业AI订单", "brain", "生成式AI业务账簿$12.5B+", "真实签约规模说明AI已经转化为软件与咨询需求。", "https://newsroom.ibm.com/2026-01-28-IBM-RELEASES-FOURTH-QUARTER-RESULTS"),
            driver("现金与研发", "flask", "$14.7B自由现金流 · $8.3B研发", "现金流足以同时支持研发、并购和股东回报。", "https://www.ibm.com/investor/annual-report"),
        ],
        "segments": [("Software", "约45%", "$30B+", "FY2025收入"), ("Consulting", "约29%", "$19B+", "FY2025收入"), ("Infrastructure", "约22%", "$15B+", "FY2025收入"), ("Financing", "约3%", "$2B+", "FY2025收入")],
        "moves": [("并购", "整合HashiCorp", "补齐混合云基础设施自动化，与Red Hat形成更完整企业云工具链。"), ("AI", "扩展watsonx与咨询交付", "用软件平台和咨询团队把模型接入受监管企业流程。")],
        "quote": "企业AI的竞争，不只是谁有模型，而是谁能把它安全地放进核心流程。",
        "signals": [("亮点", "AI商业化", "$12.5B+生成式AI账簿证明需求已进入合同和交付。"), ("风险", "传统业务", "主机周期和咨询增速可能抵消软件增长。")],
    },
    "dell": {
        "thesis": "以全球供应链和企业客户渠道为基础，把AI服务器、存储与服务组合成数据中心基础设施平台。",
        "drivers": [
            driver("AI服务器", "server", "FY2026订单$64B+ · 出货$25B+", "订单与出货规模说明戴尔已成为企业AI基础设施的主要整机入口。", "https://investors.delltechnologies.com/news-releases/news-release-details/2026/dell-technologies-delivers-record-full-year-results/default.aspx"),
            driver("可见订单", "chart", "AI服务器backlog $43B", "积压订单为未来收入提供较强可见度，也反映供应与交付能力稀缺。", "https://investors.delltechnologies.com/news-releases/news-release-details/2026/dell-technologies-delivers-record-full-year-results/default.aspx"),
            driver("现金与回报", "coin", "$11B+经营现金流 · $7.5B资本返还", "硬件薄利模式仍能产生大量现金，说明供应链与营运资本执行有效。", "https://investors.delltechnologies.com/news-releases/news-release-details/2026/dell-technologies-delivers-record-full-year-results/default.aspx"),
        ],
        "segments": [("Infrastructure Solutions", "增长核心", "$50B+", "服务器与存储"), ("Client Solutions", "规模底盘", "$50B+", "PC与商用终端")],
        "moves": [("AI", "扩大AI Factory生态", "与NVIDIA等伙伴整合服务器、网络、存储和部署服务。"), ("资本", "提高股东回报", "FY2026向股东返还$7.5B，同时维持AI服务器营运资金。")],
        "quote": "客户需要的不是一台AI服务器，而是一套能真正投入生产的AI工厂。",
        "signals": [("亮点", "AI订单", "$64B+订单与$43B backlog提供强劲增长可见度。"), ("风险", "利润率与供应", "AI服务器竞争激烈、组件昂贵，收入增长不必然等于利润率扩张。")],
    },
}


FX = {"CHF": 0.80825, "CNY": 6.79725, "CAD": 1.41860, "HKD": 7.79595}


def metric(label: str, value: str, sub: str) -> dict[str, str]:
    return {"label": label, "value": value, "sub": sub}


FINANCIALS: dict[str, dict[str, Any]] = {
    "pg": dict(fy="FY2025", fiscal="2024年7月-2025年6月", source="P&G FY2025 Annual Report", metrics=[metric("FY2025 营收", "$84.28B", "同比 +0.3%"), metric("FY2025 经营利润", "$20.45B", "同比 +10.3%"), metric("FY2025 经营现金流", "$17.82B", "同比 -10.2%"), metric("FY2025 净利润", "$16.07B", "同比 +7.4%")], market_cap="$345.56B", pe="21.70x", fpe="21.54x", roic="22.1%", wacc="5.9%", capex="$3.8B-4.2B", capex_note="FY2026公开规划约为销售额4%-5%", capex_source="P&G FY2025 Annual Report / FY2026 outlook", shareholder="$4.36/股 · 2.85%", shareholder_note="年度股息与当前股息率", dividend_source="P&G dividend history / StockAnalysis"),
    "roche": dict(fy="FY2025", fiscal="2025年1-12月", source="Roche FY2025 Annual Results", metrics=[metric("FY2025 营收", "$76.11B", "CER同比 +7%"), metric("FY2025 经营利润", "$27.01B", "核心口径 · CER +13%"), metric("FY2025 经营现金流", "$23.32B", "瑞郎口径 -6.2%"), metric("FY2025 净利润", "$17.07B", "CER同比 +58%")], market_cap="$336.66B", pe="23.8x", fpe="20.6x", roic="约18.0%", wacc="约6.0%", capex="未披露", capex_note="未见公司给出2026全年CapEx金额", capex_source="Roche FY2025 Finance Report / 2026 outlook", shareholder="CHF9.80/股 · 约1.8%", shareholder_note="拟议年度股息；主图收益率按当前价格", dividend_source="Roche FY2025 results", fx="USD/CHF 0.80825（2026年7月8日）"),
    "homedepot": dict(fy="FY2025", fiscal="2025年2月-2026年2月", source="Home Depot FY2025 10-K", metrics=[metric("FY2025 营收", "$164.68B", "同比 +3.2%"), metric("FY2025 经营利润", "$20.89B", "同比 -3.0%"), metric("FY2025 经营现金流", "$16.33B", "同比 -17.6%"), metric("FY2025 净利润", "$14.16B", "同比 -4.4%")], market_cap="$335.24B", pe="23.88x", fpe="22.01x", roic="20.6%", wacc="8.4%", capex="$3.8B-4.2B", capex_note="按FY2026门店、供应链和技术计划估算", capex_source="Home Depot FY2025 10-K / FY2026 outlook", shareholder="$9.32/股 · 2.70%", shareholder_note="年度股息与当前股息率", dividend_source="Home Depot dividend history / StockAnalysis"),
    "hsbc": dict(fy="FY2025", fiscal="2025年1-12月", source="HSBC FY2025 Annual Results", industry_exception="银行经营现金流受存贷款变动影响，不与工业公司直接比较；改用税前利润和客户存款。", metrics=[metric("FY2025 营收", "$68.3B", "同比 +4%"), metric("FY2025 税前利润", "$29.9B", "报告口径"), metric("FY2025 客户存款", "$1.80T", "资金底盘"), metric("FY2025 净利润", "$23.1B", "股东应占口径")], market_cap="$329.55B", pe="17.2x", fpe="14.6x", roic="RoTE 13.3%", wacc="银行口径不可比", capex="未披露", capex_note="银行未提供可比的2026 CapEx总额", capex_source="HSBC FY2025 Annual Report", shareholder="$0.75/股 · 3.88%", shareholder_note="2025股息与当前股息率", dividend_source="HSBC FY2025 results / StockAnalysis"),
    "arm": dict(fy="FY2026", fiscal="2025年4月-2026年3月", source="Arm FY2026 Annual Results / 20-F", metrics=[metric("FY2026 营收", "$4.92B", "同比 +23%"), metric("FY2026 经营利润", "$0.90B", "同比 +8.3%"), metric("FY2026 经营现金流", "$1.52B", "同比 +283.9%"), metric("FY2026 净利润", "$0.90B", "同比 +14.1%")], market_cap="$320.67B", pe="约355x", fpe="约96x", roic="约12.5%", wacc="约11.0%", capex="未披露", capex_note="IP公司资本开支轻，未披露2026自然年总额", capex_source="Arm FY2026 20-F", shareholder="不派现金股息 · 0%", shareholder_note="回报主要依赖利润再投资与估值", dividend_source="Arm FY2026 20-F"),
    "palantir": dict(fy="FY2025", fiscal="2025年1-12月", source="Palantir FY2025 10-K", metrics=[metric("FY2025 营收", "$4.48B", "同比 +56.2%"), metric("FY2025 经营利润", "$1.41B", "同比 +355.5%"), metric("FY2025 经营现金流", "$2.13B", "同比 +85.0%"), metric("FY2025 净利润", "$1.64B", "同比 +251.6%")], market_cap="$316.97B", pe="148.63x", fpe="83.21x", roic="306.8%", wacc="12.8%", capex="未披露", capex_note="软件公司未给出2026全年CapEx指引", capex_source="Palantir FY2025 10-K / earnings call", shareholder="不派现金股息 · 0%", shareholder_note="回报来自增长与股份价值", dividend_source="Palantir FY2025 10-K"),
    "agriculturalbank": dict(fy="FY2025", fiscal="2025年1-12月", source="农业银行2025年度报告", industry_exception="银行经营利润和经营现金流不具工业公司可比性；改用客户存款与净利润。", metrics=[metric("FY2025 营收", "$106.71B", "同比 +1.9%"), metric("FY2025 总资产", "$7.18T", "全球一级资本第3"), metric("FY2025 客户存款", "$5.69T", "同比 +10.6%"), metric("FY2025 净利润", "$42.96B", "同比 +3.3%")], market_cap="$321.64B", pe="8.00x", fpe="7.36x", roic="ROE 9.17%", wacc="银行口径不可比", capex="未披露", capex_note="银行未公开2026全年CapEx总额", capex_source="农业银行2025年度报告", shareholder="股息率约3.83%", shareholder_note="当前股息率；每股股息以A/H股公告为准", dividend_source="农业银行分红公告 / StockAnalysis", fx="USD/CNY 6.79725（2026年7月8日）"),
    "merck": dict(fy="FY2025", fiscal="2025年1-12月", source="Merck FY2025 10-K", metrics=[metric("FY2025 营收", "$65.01B", "同比 +1.3%"), metric("FY2025 经营利润", "$21.22B", "同比 +6.6%"), metric("FY2025 经营现金流", "$16.47B", "同比 -23.3%"), metric("FY2025 净利润", "$18.26B", "同比 +6.6%")], market_cap="$311.17B", pe="35.23x", fpe="20.52x", roic="21.2%", wacc="5.0%", capex="$4.0B-4.5B", capex_note="依据制造扩建与最新年度投入区间", capex_source="Merck FY2025 10-K / 2026 outlook", shareholder="$3.40/股 · 2.64%", shareholder_note="年度股息与当前股息率", dividend_source="Merck dividend history / StockAnalysis"),
    "icbc": dict(fy="FY2025", fiscal="2025年1-12月", source="工商银行2025年度报告", industry_exception="银行经营利润和经营现金流不具工业公司可比性；改用总资产与客户存款。", metrics=[metric("FY2025 营收", "$98.34B", "报告口径"), metric("FY2025 总资产", "$7.87T", "全球一级资本第1"), metric("FY2025 客户存款", "$5.70T", "低成本资金底盘"), metric("FY2025 净利润", "$54.22B", "同比约 +1%")], market_cap="$375.04B", pe="7.19x", fpe="6.74x", roic="ROE 8.89%", wacc="银行口径不可比", capex="未披露", capex_note="银行未公开2026全年CapEx总额", capex_source="工商银行2025年度报告", shareholder="股息率约4.00%", shareholder_note="当前股息率；每股股息以A/H股公告为准", dividend_source="工商银行分红公告 / StockAnalysis", fx="USD/CNY 6.79725（2026年7月8日）"),
    "goldmansachs": dict(fy="FY2025", fiscal="2025年1-12月", source="Goldman Sachs FY2025 10-K", industry_exception="投行经营现金流受交易资产变化影响，不具工业公司可比性；改用管理及监督资产。", metrics=[metric("FY2025 营收", "$58.28B", "同比 +8.9%"), metric("FY2025 经营利润", "$21.85B", "同比 +18.8%"), metric("FY2025 管理及监督资产", "$3.60T", "经常性收入底盘"), metric("FY2025 净利润", "$17.18B", "同比 +20.5%")], market_cap="$315.69B", pe="18.85x", fpe="16.96x", roic="ROE约15%", wacc="银行口径不可比", capex="未披露", capex_note="未披露2026全年CapEx总额", capex_source="Goldman Sachs FY2025 10-K", shareholder="$18.00/股 · 1.73%", shareholder_note="年度股息与当前股息率", dividend_source="Goldman Sachs dividend history / StockAnalysis"),
    "novartis": dict(fy="FY2025", fiscal="2025年1-12月", source="Novartis FY2025 Annual Results", metrics=[metric("FY2025 营收", "$54.5B", "同比约 +8%"), metric("FY2025 经营利润", "$17.64B", "同比 +21.3%"), metric("FY2025 经营现金流", "$19.14B", "同比增长"), metric("FY2025 净利润", "$13.97B", "同比增长")], market_cap="$284.61B", pe="21.03x", fpe="16.85x", roic="21.1%", wacc="6.3%", capex="$3.5B-4.0B", capex_note="按最新年度制造与研发设施计划估算", capex_source="Novartis FY2025 Annual Report / 2026 outlook", shareholder="$3.95/ADR · 1.99%", shareholder_note="年度分配折算及当前收益率", dividend_source="Novartis dividend proposal / StockAnalysis"),
    "astrazeneca": dict(fy="FY2025", fiscal="2025年1-12月", source="AstraZeneca FY2025 Annual Report", metrics=[metric("FY2025 营收", "$58.74B", "同比 +8.6%"), metric("FY2025 经营利润", "$13.74B", "同比 +37.4%"), metric("FY2025 经营现金流", "$14.58B", "同比 +22.9%"), metric("FY2025 净利润", "$10.23B", "同比 +45.3%")], market_cap="$295.16B", pe="28.41x", fpe="17.95x", roic="16.4%", wacc="5.2%", capex="$5.0B-6.0B", capex_note="依据全球制造与研发扩建项目区间", capex_source="AstraZeneca FY2025 Annual Report / announced investments", shareholder="$3.20/ADR · 1.68%", shareholder_note="年度股息与当前股息率", dividend_source="AstraZeneca dividend history / StockAnalysis"),
    "philipmorris": dict(fy="FY2025", fiscal="2025年1-12月", source="PMI FY2025 10-K", metrics=[metric("FY2025 营收", "$40.65B", "同比 +7.3%"), metric("FY2025 经营利润", "$14.89B", "同比 +11.1%"), metric("FY2025 经营现金流", "$12.23B", "同比 +0.1%"), metric("FY2025 净利润", "$11.14B", "同比 +60.8%")], market_cap="$291.56B", pe="26.35x", fpe="21.87x", roic="31.0%", wacc="5.9%", capex="$1.6B-1.9B", capex_note="无烟产能与传统供应链投资区间", capex_source="PMI FY2025 10-K / 2026 outlook", shareholder="$5.88/股 · 3.13%", shareholder_note="年度股息与当前股息率", dividend_source="PMI dividend history / StockAnalysis"),
    "kla": dict(fy="FY2025", fiscal="2024年7月-2025年6月", source="KLA FY2025 10-K", metrics=[metric("FY2025 营收", "$12.16B", "同比 +23.9%"), metric("FY2025 经营利润", "$4.78B", "同比 +42.7%"), metric("FY2025 经营现金流", "$4.08B", "同比 +23.4%"), metric("FY2025 净利润", "$4.06B", "同比 +47.1%")], market_cap="$288.92B", pe="62.61x", fpe="46.38x", roic="70.7%", wacc="11.8%", capex="$0.5B-0.7B", capex_note="按近期产能与设施投资水平估计", capex_source="KLA FY2025 10-K / 2026 earnings materials", shareholder="$0.92/股 · 0.43%", shareholder_note="拆股调整后年度股息与当前收益率", dividend_source="KLA dividend history / StockAnalysis"),
    "gevernova": dict(fy="FY2025", fiscal="2025年1-12月", source="GE Vernova FY2025 10-K", metrics=[metric("FY2025 营收", "$38.07B", "同比 +9.0%"), metric("FY2025 经营利润", "$1.39B", "同比 +194.7%"), metric("FY2025 经营现金流", "$4.99B", "同比 +93.1%"), metric("FY2025 净利润", "$4.88B", "同比 +214.7%")], market_cap="$287.80B", pe="31.34x", fpe="57.73x", roic="35.7%", wacc="9.3%", capex="$2.0B-2.5B", capex_note="燃机、电网和制造扩产规划区间", capex_source="GE Vernova FY2025 results / 2026 outlook", shareholder="$2.00/股 · 0.19%", shareholder_note="年度化股息与当前收益率", dividend_source="GE Vernova dividend declaration / StockAnalysis"),
    "rbc": dict(fy="FY2025", fiscal="2024年11月-2025年10月", source="RBC 2025 Annual Report", industry_exception="银行经营现金流受存贷款与交易资产变化影响，不具工业公司可比性；改用客户资产。", metrics=[metric("FY2025 营收", "$62.24B", "同比 +15.0%"), metric("FY2025 税前利润", "$24.7B", "银行盈利口径"), metric("FY2025 客户资产", "$794B", "财富与投资入口"), metric("FY2025 净利润", "$20.37B", "同比 +25.5%")], market_cap="$285.75B", pe="18.01x", fpe="17.82x", roic="ROE约17%", wacc="银行口径不可比", capex="未披露", capex_note="银行未披露2026自然年CapEx总额", capex_source="RBC 2025 Annual Report", shareholder="C$6.16/股 · 2.24%", shareholder_note="年度化股息与当前股息率", dividend_source="RBC dividend history / StockAnalysis", fx="USD/CAD 1.41860（2026年7月8日）"),
    "ibm": dict(fy="FY2025", fiscal="2025年1-12月", source="IBM FY2025 Annual Report", metrics=[metric("FY2025 营收", "$67.54B", "同比 +7.6%"), metric("FY2025 经营利润", "$12.26B", "同比 +63.3%"), metric("FY2025 经营现金流", "$13.19B", "同比 -1.9%"), metric("FY2025 净利润", "$10.57B", "同比 +75.9%")], market_cap="$283.89B", pe="26.76x", fpe="24.02x", roic="14.9%", wacc="6.8%", capex="$2.0B-2.5B", capex_note="数据中心、实验室与云基础设施投入区间", capex_source="IBM FY2025 Annual Report / 2026 outlook", shareholder="$6.76/股 · 2.21%", shareholder_note="年度股息与当前股息率", dividend_source="IBM dividend history / StockAnalysis"),
    "dell": dict(fy="FY2026", fiscal="2025年2月-2026年1月", source="Dell FY2026 10-K", metrics=[metric("FY2026 营收", "$113.54B", "同比 +18.8%"), metric("FY2026 经营利润", "$8.15B", "同比 +30.7%"), metric("FY2026 经营现金流", "$11.19B", "同比 +147.4%"), metric("FY2026 净利润", "$5.94B", "同比 +29.3%")], market_cap="$279.11B", pe="34.53x", fpe="23.31x", roic="24.0%", wacc="11.0%", capex="$3.0B-3.5B", capex_note="AI服务器、供应链与数据中心基础设施投入区间", capex_source="Dell FY2026 10-K / FY2027 outlook", shareholder="$2.52/股 · 0.60%", shareholder_note="年度股息与当前股息率", dividend_source="Dell dividend history / StockAnalysis"),
}


HOLDER_SYMBOLS = {
    "pg": "PG", "homedepot": "HD", "hsbc": "HSBC", "arm": "ARM",
    "palantir": "PLTR", "merck": "MRK", "goldmansachs": "GS",
    "novartis": "NVS", "astrazeneca": "AZN", "philipmorris": "PM",
    "kla": "KLAC", "gevernova": "GEV", "ibm": "IBM", "dell": "DELL",
}


def _manual_holders() -> dict[str, list[dict[str, str]]]:
    return {
        "roche": [
            {"name": "Hoffmann/Oeri一致行动组", "kind": "创始家族", "stake": "64.97%", "value": "$218.7B", "period": "2025年末", "note": "有表决权股份口径"},
            {"name": "Maja Oeri", "kind": "家族股东", "stake": "3.79%", "value": "$12.8B", "period": "2025年末", "note": "估算权益市值"},
            {"name": "Melchior Oeri", "kind": "家族股东", "stake": "3.79%", "value": "$12.8B", "period": "2025年末", "note": "估算权益市值"},
        ],
        "agriculturalbank": [
            {"name": "中央汇金", "kind": "国有股东", "stake": "40.03%", "value": "$128.8B", "period": "2025年末", "note": "年报"},
            {"name": "财政部", "kind": "国有股东", "stake": "35.29%", "value": "$113.5B", "period": "2025年末", "note": "年报"},
            {"name": "香港中央结算（代理人）", "kind": "名义持有人", "stake": "8.82%", "value": "$28.4B", "period": "2025年末", "note": "H股汇总"},
            {"name": "全国社会保障基金理事会", "kind": "国家基金", "stake": "6.72%", "value": "$21.6B", "period": "2025年末", "note": "年报"},
        ],
        "icbc": [
            {"name": "中央汇金", "kind": "国有股东", "stake": "34.71%", "value": "$130.2B", "period": "2025年末", "note": "年报"},
            {"name": "财政部", "kind": "国有股东", "stake": "31.14%", "value": "$116.8B", "period": "2025年末", "note": "年报"},
            {"name": "香港中央结算（代理人）", "kind": "名义持有人", "stake": "24.15%", "value": "$90.6B", "period": "2025年末", "note": "H股汇总"},
            {"name": "全国社会保障基金理事会", "kind": "国家基金", "stake": "3.46%", "value": "$13.0B", "period": "2025年末", "note": "年报"},
        ],
        "rbc": [
            {"name": "Vanguard Capital Management", "kind": "机构", "stake": "3.04%", "value": "$8.81B", "period": "2026Q1", "note": "FinanceCharts"},
            {"name": "RBC Global Asset Management", "kind": "机构", "stake": "2.67%", "value": "$7.74B", "period": "2026Q1", "note": "FinanceCharts"},
            {"name": "BlackRock Institutional Trust", "kind": "机构", "stake": "2.20%", "value": "$6.38B", "period": "2026年4月", "note": "FinanceCharts"},
            {"name": "TD Asset Management", "kind": "机构", "stake": "1.70%", "value": "$4.92B", "period": "2026Q1", "note": "FinanceCharts"},
        ],
    }


def _parse_number(value: str) -> float:
    return float(str(value).replace("$", "").replace(",", "").strip())


def _quarter(date_text: str) -> str:
    match = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(20\d{2})", date_text.strip())
    if not match:
        return date_text
    month, _day, year = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    return f"{year}Q{(month - 1) // 3 + 1}"


def _holder_family(name: str) -> str:
    lowered = name.lower()
    for family in ("vanguard", "blackrock", "state street", "geode", "fidelity", "morgan stanley"):
        if family in lowered:
            return family
    return re.sub(r"[^a-z]", "", lowered)[:18]


def nasdaq_holders(symbol: str) -> list[dict[str, str]]:
    url = f"https://api.nasdaq.com/api/company/{symbol}/institutional-holdings?limit=16&type=TOTAL&sortColumn=marketValue&sortOrder=DESC"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.load(response).get("data") or {}
    summary = data.get("ownershipSummary") or {}
    total_text = (summary.get("ShareoutstandingTotal") or {}).get("value", "")
    total_shares = _parse_number(total_text) * 1_000_000
    rows = (((data.get("holdingsTransactions") or {}).get("table") or {}).get("rows") or [])
    selected: list[dict[str, str]] = []
    families: set[str] = set()
    for row in rows:
        name = str(row.get("ownerName", "")).strip()
        family = _holder_family(name)
        if not name or family in families:
            continue
        shares = _parse_number(row.get("sharesHeld", "0"))
        value_b = _parse_number(row.get("marketValue", "0")) / 1_000_000
        if shares <= 0 or total_shares <= 0 or value_b <= 0:
            continue
        selected.append({
            "name": name.replace("Blackrock", "BlackRock").replace(" Inc.", "").replace(" Llc", "").rstrip(" ,"),
            "kind": "机构",
            "stake": f"{shares / total_shares * 100:.2f}%",
            "value": f"${value_b:.2f}B",
            "period": _quarter(str(row.get("date", ""))),
            "note": "Nasdaq 13F",
        })
        families.add(family)
        if len(selected) == 4:
            break
    if len(selected) < 3:
        raise ValueError(f"{symbol}可核验机构持仓不足3项")
    return selected


def holders_for(slug: str) -> list[dict[str, str]]:
    manual = _manual_holders()
    if slug in manual:
        return copy.deepcopy(manual[slug])
    symbol = HOLDER_SYMBOLS.get(slug)
    if not symbol:
        raise ValueError(f"{slug}缺少机构持仓来源")
    return nasdaq_holders(symbol)


def _crop_raster_logo(source: Path, slug: str) -> Path:
    LOGO_ROOT.mkdir(parents=True, exist_ok=True)
    target = LOGO_ROOT / f"{slug}-official-visible.png"
    image = Image.open(source).convert("RGBA")
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox and bbox == (0, 0, image.width, image.height):
        background = Image.new("RGB", image.size, image.convert("RGB").getpixel((0, 0)))
        difference = ImageChops.difference(image.convert("RGB"), background).convert("L")
        difference = difference.point(lambda pixel: 255 if pixel > 12 else 0)
        content_bbox = difference.getbbox()
        if content_bbox:
            bbox = content_bbox
    if bbox:
        image = image.crop(bbox)
    padding = max(8, int(max(image.size) * 0.045))
    canvas = Image.new("RGBA", (image.width + padding * 2, image.height + padding * 2), (255, 255, 255, 0))
    canvas.alpha_composite(image, (padding, padding))
    canvas.save(target)
    return target


def prepare_logo(company: dict[str, Any]) -> dict[str, Any]:
    item = copy.deepcopy(company)
    source = Path(item["logo_path"])
    if source.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        item["logo_path"] = str(_crop_raster_logo(source, item["slug"]))
    item["logo_sha256"] = hashlib.sha256(Path(item["logo_path"]).read_bytes()).hexdigest()
    return item


def batch_companies() -> list[dict[str, Any]]:
    return [prepare_logo(company) for company in COMPANIES if company["rank"] >= 40]


def sample_financials() -> dict[str, Any]:
    return copy.deepcopy(FINANCIALS["pg"])


def sample_holders() -> list[dict[str, str]]:
    return [
        {"name": "Vanguard", "kind": "机构", "stake": "9.10%", "value": "$31.4B", "period": "2026Q1", "note": "Nasdaq 13F"},
        {"name": "BlackRock", "kind": "机构", "stake": "7.20%", "value": "$24.9B", "period": "2026Q1", "note": "Nasdaq 13F"},
        {"name": "State Street", "kind": "机构", "stake": "4.30%", "value": "$14.9B", "period": "2026Q1", "note": "Nasdaq 13F"},
    ]


def build_packet(company: dict[str, Any], financials: dict[str, Any], holders: list[dict[str, str]]) -> dict[str, Any]:
    evidence = EVIDENCE[company["slug"]]
    metrics = copy.deepcopy(financials["metrics"])
    metrics.extend([
        metric("当前市值", financials["market_cap"], f"截至{TODAY}"),
        metric("PE / Forward PE", f"{financials['pe']} / {financials['fpe']}", "当前估值"),
    ])
    source_urls = sorted({item["source"] for item in evidence["drivers"]})
    packet = {
        "company": company["name"],
        "ticker": company["ticker"],
        "company_profile": {
            "公司全称": company["en"],
            "成立时间": company["founded"],
            "总部地址": company["hq"],
            "交易所及代码": company["ticker"],
            "CEO / 主要负责人": company["ceo"],
            "员工人数": company["employees"],
            "核心业务": company["core_business"],
            "当前市值": financials["market_cap"],
        },
        "management_culture": copy.deepcopy(company["culture"]),
        "colors": {"accent": company["color"], "deep": company["deep"], "gold": company["gold"]},
        "logo": {
            "path": company["logo_path"],
            "official_source_url": company["logo_source"],
            "sha256": company.get("logo_sha256") or hashlib.sha256(Path(company["logo_path"]).read_bytes()).hexdigest(),
            "background": company.get("logo_bg", "rgba(255,255,255,.82)"),
        },
        "strategy": {
            "thesis": evidence["thesis"],
            "drivers": copy.deepcopy(evidence["drivers"]),
            "moves": [{"tag": tag, "title": title, "detail": detail} for tag, title, detail in evidence["moves"]],
            "quote": evidence["quote"],
        },
        "panorama": {
            "thesis": evidence["thesis"],
            "metrics": metrics,
            "segments": [{"name": name, "share": share, "value": value, "note": note} for name, share, value, note in evidence["segments"]],
            "capital": [
                {"label": "ROIC", "value": financials["roic"], "note": f"WACC：{financials['wacc']}"},
                {"label": "2026E CapEx", "value": financials["capex"], "note": financials["capex_note"]},
                {"label": "股东回报", "value": financials["shareholder"], "note": financials["shareholder_note"]},
            ],
            "signals": [{"kind": kind, "title": title, "detail": detail} for kind, title, detail in evidence["signals"]],
            "holders": copy.deepcopy(holders),
        },
        "footer_lines": [
            f"经营数据：{financials['source']}，{financials['fy']}：{financials['fiscal']}",
            f"行情数据：StockAnalysis / CompaniesMarketCap，查看：{TODAY}；市值及PE均为当前口径",
            f"核心证据：公司官网、年报及投资者资料，核查：{TODAY}；来源共{len(source_urls)}项",
            f"ROI口径：公司ROIC；银行/投行采用ROE或RoTE并明确标注，{financials['fy']}，来源同经营数据",
            f"2026 CapEx口径：{financials['capex_source']}；无可靠公开总额时明确写未披露",
            f"股东分红：{financials['dividend_source']}，查看：{TODAY}；{financials['shareholder']}",
            f"机构持仓：{'公司年报股东表 / FinanceCharts' if company['slug'] in _manual_holders() else 'Nasdaq Institutional Holdings / 13F'}，各行按所示报告期，抓取：{TODAY}",
            f"汇率口径：主图金额统一美元；{financials.get('fx', '美元财报无需换汇；非美元数据使用2026年7月8日市场汇率')}",
            "免责声明：本图仅供学习参考，不构成投资建议",
        ],
    }
    if financials.get("industry_exception"):
        packet["panorama"]["industry_exception"] = financials["industry_exception"]
    visual.validate_packet(packet)
    return packet


def _backup(company: dict[str, Any]) -> None:
    source_dir = OUTPUT_ROOT / company["folder"]
    target_dir = BACKUP_ROOT / company["folder"]
    target_dir.mkdir(parents=True, exist_ok=True)
    for source in source_dir.glob("*.png"):
        target = target_dir / source.name
        if not target.exists():
            shutil.copy2(source, target)


def _write_packet(company: dict[str, Any], packet: dict[str, Any]) -> Path:
    path = PACKET_ROOT / f"{company['rank']:02d}_{company['slug']}.json"
    path.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _render_company(company: dict[str, Any], packet: dict[str, Any]) -> list[Path]:
    output_dir = OUTPUT_ROOT / company["folder"]
    output_dir.mkdir(parents=True, exist_ok=True)
    company["current_market_cap"] = FINANCIALS[company["slug"]]["market_cap"]

    profile_html = profile_page(company)
    strategy_html = visual.strategy_page(packet, 1260)
    panorama_html = visual.panorama_page(packet, 1670)
    culture_html = culture_page(company)

    culture_height = 880 if len(company["culture"]) <= 2 else 1050
    pages = [
        (profile_html, HTML_ROOT / f"{company['rank']:02d}_{company['slug']}_profile.html", output_dir / f"{company['prefix']}_公司档案.png", profile_height(company)),
        (strategy_html, HTML_ROOT / f"{company['rank']:02d}_{company['slug']}_strategy.html", output_dir / f"{company['prefix']}_sketch1.png", 1260),
        (panorama_html, HTML_ROOT / f"{company['rank']:02d}_{company['slug']}_panorama.html", output_dir / f"{company['prefix']}_sketch2.png", 1670),
        (culture_html, HTML_ROOT / f"{company['rank']:02d}_{company['slug']}_culture.html", output_dir / f"{company['prefix']}_管理文化.png", culture_height),
    ]
    for source, html_path, png_path, height in pages:
        render_html(source, html_path, png_path, height)

    obsolete = output_dir / f"{company['prefix']}_经营分析.png"
    if obsolete.exists():
        obsolete.unlink()
    return [item[2] for item in pages]


def _validate_rendered(company: dict[str, Any], paths: list[Path]) -> None:
    if len(paths) != 4 or not all(path.is_file() for path in paths):
        raise ValueError(f"{company['name']}未生成完整四图")
    expected_heights = [profile_height(company), 1260, 1670, 880 if len(company["culture"]) <= 2 else 1050]
    for path, expected_height in zip(paths, expected_heights):
        with Image.open(path) as image:
            if image.size != (2700, expected_height * 3):
                raise ValueError(f"{path}分辨率错误：{image.size}")
            alpha = image.convert("RGB").getbbox()
            if not alpha:
                raise ValueError(f"{path}为空白图")


def _contact_sheet(items: list[tuple[str, Path]], target: Path, columns: int = 4) -> None:
    thumb_width = 360
    label_height = 42
    thumbs: list[tuple[str, Image.Image]] = []
    for label, path in items:
        image = Image.open(path).convert("RGB")
        height = int(image.height * thumb_width / image.width)
        image.thumbnail((thumb_width, height), Image.Resampling.LANCZOS)
        thumbs.append((label, image.copy()))
    rows = (len(thumbs) + columns - 1) // columns
    cell_height = max(image.height for _, image in thumbs) + label_height
    sheet = Image.new("RGB", (columns * thumb_width, rows * cell_height), "white")
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
    except OSError:
        font = ImageFont.load_default()
    for index, (label, image) in enumerate(thumbs):
        x = (index % columns) * thumb_width
        y = (index // columns) * cell_height
        draw.text((x + 8, y + 6), label, fill="#222222", font=font)
        sheet.paste(image, (x, y + label_height))
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target, quality=92)


def main() -> int:
    if not CHROME.is_file():
        raise FileNotFoundError(CHROME)
    for directory in (REVIEW_ROOT, HTML_ROOT, PACKET_ROOT, BACKUP_ROOT, LOGO_ROOT):
        directory.mkdir(parents=True, exist_ok=True)

    companies = batch_companies()
    preflight: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for company in companies:
        print(f"preflight #{company['rank']} {company['name']}", flush=True)
        holder_rows = holders_for(company["slug"])
        packet = build_packet(company, copy.deepcopy(FINANCIALS[company["slug"]]), holder_rows)
        _write_packet(company, packet)
        preflight.append((company, packet))

    outputs: list[tuple[dict[str, Any], list[Path]]] = []
    for company, packet in preflight:
        print(f"render #{company['rank']} {company['name']}", flush=True)
        _backup(company)
        paths = _render_company(company, packet)
        _validate_rendered(company, paths)
        outputs.append((company, paths))

    sheet_paths = []
    labels = ("公司档案", "经营之道", "经营全景", "管理文化")
    for page_index, label in enumerate(labels):
        target = REVIEW_ROOT / f"contact_{page_index + 1}_{label}.jpg"
        _contact_sheet([(f"#{company['rank']} {company['name']}", paths[page_index]) for company, paths in outputs], target)
        sheet_paths.append(target)

    manifest = [
        "# 雪佛龙之后公司四图统一更新",
        "",
        f"- 生成时间：{datetime.now().isoformat(timespec='seconds')}",
        "- 范围：排名40-59现有18家公司，共72张图",
        "- 规则：可口可乐视觉基线 + 官方Logo + 语义小图标 + 机构持仓 + 六项经营数据",
        "- 金额：统一美元；非美元汇率日期见页脚",
        "- 邮件：未发送",
        "",
    ]
    for company, paths in outputs:
        manifest.append(f"- #{company['rank']} {company['name']}：" + "、".join(f"`{path.name}`" for path in paths))
    manifest.extend(["", "## 视觉复核联系表", *[f"- `{path.name}`" for path in sheet_paths]])
    (REVIEW_ROOT / "manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (REVIEW_ROOT / ".render_complete").write_text(datetime.now().isoformat(timespec="seconds") + "\n", encoding="utf-8")
    print(f"rendered {len(outputs)} companies / {len(outputs) * 4} images")
    print(REVIEW_ROOT / "manifest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
