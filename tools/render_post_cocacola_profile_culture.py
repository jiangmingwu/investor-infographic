#!/usr/bin/env python3
"""Refresh company-profile and management-culture pages after Coca-Cola.

Financial labels and all final text are deterministic HTML/SVG. The renderer
reuses the approved Coca-Cola visual system, but preserves each company's own
brand colors and verified official logo.
"""

from __future__ import annotations

import base64
import hashlib
import html
import json
import math
import re
import shutil
import subprocess
from datetime import datetime
from functools import lru_cache
from pathlib import Path


OUTPUT_ROOT = Path("/Users/jiangming/持仓分析/公司经营分析")
LOGO_ROOT = Path("/Users/jiangming/templates/assets/company_logos")
REVIEW_ROOT = OUTPUT_ROOT / "_review/post_cocacola_profile_culture_20260714"
HTML_ROOT = REVIEW_ROOT / "html"
PACKET_ROOT = REVIEW_ROOT / "packets"
BACKUP_ROOT = REVIEW_ROOT / "before"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
STOCK_HISTORY_PATH = Path("/Users/jiangming/templates/data/market_history/post_chevron_stock_history_20260715.json")
CHEVRON_STOCK_HISTORY_PATH = Path("/Users/jiangming/templates/data/market_history/cvx_stock_history_1962_2026.json")
RENDER_COMPLETE = (REVIEW_ROOT / ".complete").exists()
LEGACY_RENDERER_DISABLED = True


def culture(title: str, practice: str, case: str, lesson: str, lens: str,
            icon_name: str, source: str) -> dict[str, str]:
    return {
        "title": title, "practice": practice, "case": case, "lesson": lesson,
        "lens": lens, "icon": icon_name, "source": source,
    }


def company(**values):
    values.setdefault("profile_source", values["homepage"])
    values.setdefault("logo_path", str(LOGO_ROOT / f"{values['slug']}-official.png"))
    values.setdefault("logo_source", values["homepage"])
    return values


COMPANIES = [
    company(
        rank=39, slug="chevron", folder="39_雪佛龙", prefix="chevron", name="雪佛龙",
        en="Chevron Corporation", ticker="NYSE: CVX", founded="1879年", hq="Houston, Texas, USA",
        ceo="Mike Wirth", employees="约48,000人", position="全球一体化能源公司",
        color="#0054A6", deep="#123E66", gold="#E31937", homepage="https://www.chevron.com/",
        logo_path=str(LOGO_ROOT / "chevron-official-crop.png"),
        logo_source="https://www.chevron.com/-/media/shared-media/images/hallmark-2023.png",
        strap="上游资源 × 炼化销售 × LNG与新能源",
        thesis="从油气勘探到炼化和销售的一体化能源公司，规模、资源寿命和资本纪律共同决定穿越周期的能力。",
        businesses=[("drop", "上游油气", "勘探、开发和生产原油与天然气，资产覆盖美国、哈萨克斯坦、澳大利亚等核心区域。"), ("factory", "下游与化工", "炼油、燃料销售、润滑油与Chevron Phillips Chemical合资化工业务。"), ("leaf", "LNG与新能源", "澳大利亚LNG、可再生燃料、氢、碳捕集和新型能源投资。")],
        status=[("gauge", "3.3M桶油当量/日", "FY2024净产量，全球超大型上游规模"), ("globe", "180+个国家", "产品销售或业务触达范围"), ("coin", "38年连续提高股息", "截至2025年的年度每股分红纪录")],
        timeline=[("1879", "Pacific Coast Oil成立"), ("1984", "收购Gulf并更名Chevron"), ("2001", "与Texaco合并"), ("2025", "完成Hess收购")],
        profile_source="https://www.chevron.com/who-we-are",
        culture=[
            culture("任何人都有权停止不安全的工作", "做法：把人员与环境安全放在产量和进度之前，员工与承包商发现风险时可以停止或不启动作业。", "案例：Operational Excellence明确写入Stop-Work Authority，并要求风险消除后才恢复作业。", "可借鉴：把安全授权给离风险最近的人，而不是等管理层逐级批准。", "员工", "shield", "https://www.chevron.com/-/media/shared-media/documents/OE-workforce-overview.pdf"),
            culture("结果必须以正确的方式取得", "做法：The Chevron Way把诚信、信任、伙伴关系和高绩效同时作为行为标准，不能用短期结果抵消行为问题。", "案例：2025版Business Conduct and Ethics Code要求员工在疑虑出现时主动提问和报告，并禁止报复。", "可借鉴：绩效评价同时看结果与实现结果的方式。", "伦理", "scale", "https://www.chevron.com/-/media/shared-media/documents/chevronbusinessconductethicscode.pdf"),
        ],
    ),
    company(
        rank=40, slug="pg", folder="40_宝洁", prefix="pg", name="宝洁", en="The Procter & Gamble Company",
        ticker="NYSE: PG", founded="1837年", hq="Cincinnati, Ohio, USA", ceo="Shailesh Jejurikar",
        employees="约109,000人", position="全球日用消费品龙头", color="#163B7A", deep="#0E2A59", gold="#3C8DCC",
        homepage="https://us.pg.com/", logo_path=str(LOGO_ROOT / "pg-official.svg"),
        logo_source="https://images.ctfassets.net/oggad6svuzkv/7znyJc3Y7SecEoKSYKWoaQ/4a24e9015c360799cfb072adcd92cc5e/P_G_Logo_RGB.svg",
        strap="五大业务板块 × 十个品类 × 全球品牌系统",
        thesis="以少数大品类和强品牌服务日常生活，通过消费者洞察、产品创新和渠道执行形成长期复购。",
        businesses=[("spark", "美妆与个护", "美容、理容、健康护理和女性及家庭护理。"), ("home", "家庭护理", "织物护理、家居清洁及婴儿、女性和家庭护理。"), ("brands", "全球品牌组合", "围绕十个核心品类经营品牌、研发、营销与渠道。")],
        status=[("grid", "5大业务板块", "以品类为核心配置全球能力"), ("brands", "10个核心品类", "覆盖高频家庭消费场景"), ("globe", "约180个国家和地区", "品牌销售覆盖范围")],
        timeline=[("1837", "P&G在辛辛那提成立"), ("1946", "Tide洗衣粉上市"), ("2005", "收购Gillette"), ("2026", "Jejurikar接任CEO")],
        profile_source="https://us.pg.com/structure-and-governance/our-businesses/",
        culture=[
            culture("从内部培养领导者", "做法：招聘时按长期潜力而非第一份岗位选人，员工通过跨职能、跨市场轮岗成长，领导岗位主要由内部人才接续。", "数字：公司称员工入职前十年平均经历4个岗位；许多业务负责人从基层品牌或销售岗位起步。", "可借鉴：把人才梯队当成长期资产，岗位轮换必须服务能力成长。", "人才", "people", "https://us.pg.com/blogs/applying-to-pg/"),
            culture("从第一天就给真实责任", "做法：新人直接参与品牌、客户或供应项目，并配套经理和伙伴辅导，而不是长期旁观。", "案例：Power Pairs在新员工前30天连接经理与伙伴，帮助新人迅速进入真实业务与反馈循环。", "可借鉴：授权和辅导要同时发生，责任不能只停留在口号。", "领导", "rocket", "https://us.pg.com/blogs/secrets-to-the-art-of-leadership/"),
            culture("领导力、主人翁与数据诚实", "做法：Purpose, Values and Principles要求员工领导、负责、合作，并对数据和风险保持坦诚。", "案例：P&G把价值观用于招聘、绩效和领导发展，而不是仅用于外部品牌传播。", "可借鉴：将价值观转成招聘与评价中的可观察行为。", "组织", "chart", "https://us.pg.com/policies-and-practices/purpose-values-and-principles/"),
        ],
    ),
    company(
        rank=42, slug="roche", folder="42_罗氏", prefix="roche", name="罗氏", en="Roche Holding AG",
        ticker="SIX: RO / ROP", founded="1896年", hq="Basel, Switzerland", ceo="Thomas Schinecker",
        employees="约103,000人", position="制药与诊断一体化医疗集团", color="#0B52B5", deep="#173B73", gold="#56A0D3",
        homepage="https://www.roche.com/", logo_path=str(LOGO_ROOT / "roche-official.png"),
        logo_source="https://assets.roche.com/f/176343/801x529/f89c88a24c/roche-logo-blue.png?download=1",
        strap="创新药 × 诊断 × 个体化医疗",
        thesis="同时拥有制药与诊断两大能力，用疾病生物学、检测数据和临床开发连接诊断到治疗。",
        businesses=[("pill", "制药", "肿瘤、神经、免疫、血液和眼科等创新药。"), ("flask", "诊断", "体外诊断、分子诊断、病理与糖尿病管理。"), ("network", "个体化医疗", "将诊断标志物、临床数据与药物开发结合。")],
        status=[("grid", "2大核心事业部", "Pharmaceuticals与Diagnostics"), ("globe", "100+个国家", "研发、生产与商业覆盖"), ("people", "约103,000名员工", "全球科研与医疗服务团队")],
        timeline=[("1896", "Fritz Hoffmann创立罗氏"), ("1968", "建立诊断业务"), ("2009", "完成Genentech整合"), ("2023", "Schinecker出任集团CEO")],
        profile_source="https://www.roche.com/about",
        culture=[
            culture("领导者先听，再说明为什么", "做法：Seven Leadership Commitments要求领导倾听、解释决策逻辑、赋能团队并持续发展人才。", "案例：员工与经理通过频繁、非正式的Check-In讨论目标、支持和成长，不把反馈压到年终一次完成。", "可借鉴：把反馈从年度仪式改成持续的工作对话。", "领导", "speak", "https://sp-coc.roche.com/en/employment-at-roche.html"),
            culture("用匿名调查逼组织行动", "做法：Global Employee Opinion Survey让员工匿名评价领导、协作和工作体验，管理层必须基于结果制定行动。", "案例：罗氏公开把GEOS作为文化与领导改进工具，并要求团队讨论结果而非只看分数。", "可借鉴：员工调查的价值在后续行动和复盘，不在收集问卷。", "反馈", "feedback", "https://careers.roche.com/global/en/our-culture-in-canada"),
            culture("薪酬原则公开并按市场复核", "做法：全球薪酬哲学强调外部竞争力、内部公平、绩效联系和透明沟通。", "案例：公司公开说明每年用市场数据审视薪酬定位，并由当地方案落实福利。", "可借鉴：对员工好不只看福利项目，也看薪酬原则是否透明、可解释。", "员工", "coin", "https://careers.roche.com/global/en/compensation-philosophy"),
        ],
    ),
    company(
        rank=43, slug="homedepot", folder="43_家得宝", prefix="homedepot", name="家得宝", en="The Home Depot, Inc.",
        ticker="NYSE: HD", founded="1978年", hq="Atlanta, Georgia, USA", ceo="Ted Decker",
        employees="约470,000人", position="全球最大家居建材零售商", color="#F26A21", deep="#9D3A0A", gold="#E5A22D",
        homepage="https://corporate.homedepot.com/", logo_path=str(LOGO_ROOT / "homedepot-official.svg"), logo_bg="#F26A21",
        logo_source="https://corporate.homedepot.com/themes/custom/bootstrap_thd/images/logo-site-header-homedepot.svg",
        strap="大型门店 × 专业客户 × 全渠道履约",
        thesis="以大型仓储门店、专业服务和全渠道网络覆盖DIY消费者与专业承包商的装修需求。",
        businesses=[("store", "门店零售", "建材、工具、园艺、家电和装修用品的大型仓储门店。"), ("tools", "专业客户", "面向承包商和专业施工人员提供采购、信贷和履约服务。"), ("truck", "全渠道履约", "线上下单、门店自提、配送中心和上门交付。")],
        status=[("store", "2,350+家门店", "美国、加拿大和墨西哥网络"), ("people", "约470,000名员工", "全球最大零售用工团队之一"), ("trophy", "全球第1", "按规模计最大的家居建材零售商")],
        timeline=[("1978", "Blank与Marcus创立"), ("1981", "在NASDAQ上市"), ("2007", "出售HD Supply批发业务"), ("2024", "收购SRS Distribution")],
        profile_source="https://corporate.homedepot.com/page/about-us",
        culture=[
            culture("倒金字塔：管理层为一线服务", "做法：文化图把顾客置顶、门店员工居中、CEO和高管放在底部，管理者的职责是清除一线障碍。", "案例：公司培训和领导沟通长期使用倒金字塔，创始人把照顾员工视为照顾顾客的前提。", "可借鉴：组织图应体现谁为谁服务，而不只是权力层级。", "组织", "pyramid", "https://corporate.homedepot.com/news/company/home-depot-values-wheel"),
            culture("把经营成果分享给非管理层员工", "做法：Success Sharing按门店和业务表现向符合条件的非管理层员工发放半年一次的利润分享。", "案例：该机制让一线员工能直接分享所在团队创造的经营成果，而不只拿固定工资。", "可借鉴：让奖励与团队结果相连，并覆盖真正创造顾客体验的一线。", "员工", "coin", "https://corporate.homedepot.com/news/company/four-ways-working-home-depot-changes-lives"),
            culture("员工遇到困难时由同事共同托底", "做法：The Homer Fund由员工捐助，为遭遇自然灾害、疾病或突发困难的同事提供援助。", "数字：公司披露该基金在2018年帮助约7,500个员工家庭；Orange Scholars每年可提供最多1,000份奖学金。", "可借鉴：员工关怀要有常设机制和可量化的帮助结果。", "员工", "heart", "https://corporate.homedepot.com/news/company/four-ways-working-home-depot-changes-lives"),
        ],
    ),
    company(
        rank=44, slug="hsbc", folder="44_HSBC汇丰", prefix="hsbc", name="汇丰", en="HSBC Holdings plc",
        ticker="LSE/NYSE: HSBA / HSBC", founded="1865年", hq="London, United Kingdom", ceo="Georges Elhedery",
        employees="约210,000人", position="全球跨境银行集团", color="#DB0011", deep="#7B0B14", gold="#A97B45",
        homepage="https://www.hsbc.com/", logo_path=str(LOGO_ROOT / "hsbc-official.svg"),
        logo_source="https://www.hsbc.com/-/files/hsbc/header/hsbc-logo-200x25.svg",
        strap="财富与个人银行 × 商业银行 × 企业与机构银行",
        thesis="以亚洲和国际网络连接个人、企业与机构客户，跨境资金流和财富管理是核心定位。",
        businesses=[("people", "财富与个人银行", "零售银行、财富管理、保险和私人银行。"), ("building", "商业银行", "服务中小企业与跨境经营企业。"), ("globe", "企业与机构银行", "交易银行、市场、融资和国际网络服务。")],
        status=[("people", "约4,100万客户", "个人、企业与机构客户规模"), ("globe", "约56个国家和地区", "国际网络覆盖"), ("people", "约210,000名员工", "跨市场服务与风险团队")],
        timeline=[("1865", "香港上海汇丰银行成立"), ("1991", "HSBC Holdings在伦敦设立"), ("1999", "统一采用HSBC品牌"), ("2025", "重组为四大业务单元")],
        profile_source="https://www.hsbc.com/who-we-are",
        culture=[
            culture("用员工调查检验战略是否被理解", "做法：Snapshot survey持续询问员工对战略、领导和未来的判断，并把结果作为文化改进输入。", "数字：2023年调查中73%的员工看到战略带来的积极影响，81%对公司未来有信心。", "可借鉴：战略沟通不能只看是否发布，还要测量员工是否理解并相信。", "反馈", "feedback", "https://www.hsbc.com/-/files/hsbc/investors/hsbc-results/2023/annual/pdfs/hsbc-holdings-plc/240222-hsbc-holdings-plc-form-20-f.pdf?download=1"),
            culture("绩效要求与包容并行", "做法：公司公开把更强绩效文化、包容型组织和未来技能列为同一套People priorities。", "案例：管理层用员工调查、领导沟通和人才计划跟踪三项目标，而不是把绩效与员工体验分成两条线。", "可借鉴：高绩效并不等于压缩反馈空间，标准和心理安全要同时设计。", "组织", "scale", "https://www.hsbc.com/who-we-are/our-people-and-culture"),
        ],
    ),
    company(
        rank=45, slug="arm", folder="45_Arm", prefix="arm", name="Arm", en="Arm Holdings plc",
        ticker="NASDAQ: ARM", founded="1990年", hq="Cambridge, United Kingdom", ceo="Rene Haas",
        employees="约8,000人", position="全球CPU架构与IP平台", color="#0091BD", deep="#153B54", gold="#E69F23",
        homepage="https://www.arm.com/", logo_path=str(LOGO_ROOT / "arm-official.svg"),
        logo_source="https://www.arm.com/-/media/global/logos/arm-logo-blue-rgb.svg",
        strap="CPU架构 × 芯片IP × 软件生态",
        thesis="不直接大规模制造芯片，而是把计算架构、处理器IP与软件工具授权给全球芯片和设备公司。",
        businesses=[("chip", "CPU与系统IP", "Cortex、Neoverse、GPU及互连等处理器设计。"), ("code", "架构授权", "向芯片公司授权Arm架构并收取授权费与版税。"), ("network", "软件生态", "开发工具、操作系统适配与开发者社区。")],
        status=[("chip", "325B+颗芯片", "基于Arm技术的累计出货规模"), ("phone", "约99%智能手机", "Arm架构在手机处理器中的覆盖"), ("code", "2,000万+开发者", "围绕Arm的软件生态")],
        timeline=[("1990", "Acorn、Apple与VLSI合资成立"), ("1998", "在伦敦和NASDAQ上市"), ("2016", "被SoftBank收购"), ("2023", "重返NASDAQ")],
        profile_source="https://www.arm.com/company",
        culture=[
            culture("We, not I：评价个人也评价协作", "做法：Core Beliefs把团队成功置于个人英雄主义之上，员工年度评估同时看业绩与是否践行核心信念。", "案例：FY2025公司更新行为标准，推动One Arm的高挑战、高支持文化。", "可借鉴：协作价值观必须进入绩效评价，否则会输给短期个人指标。", "组织", "network", "https://investors.arm.com/node/7681/html"),
            culture("用多元团队解决全球工程问题", "做法：鼓励员工做真实的自己，并让不同国家和专业背景的人围绕同一技术目标协作。", "数字：Arm官方介绍的Trondheim团队拥有26种以上国籍，体现小型工程中心也能形成全球人才组合。", "可借鉴：多元化的价值要落在团队构成和协作质量上。", "人才", "people", "https://careers.arm.com/en/arm-stories-Deepali"),
        ],
    ),
    company(
        rank=47, slug="palantir", folder="47_Palantir", prefix="palantir", name="Palantir", en="Palantir Technologies Inc.",
        ticker="NASDAQ: PLTR", founded="2003年", hq="Denver, Colorado, USA", ceo="Alex Karp",
        employees="约4,300人", position="企业与政府AI软件平台", color="#111827", deep="#020617", gold="#7C98A6",
        homepage="https://www.palantir.com/", logo_path=str(LOGO_ROOT / "palantir-official.png"),
        logo_source="https://www.palantir.com/aws/ptlogo",
        strap="数据平台 × AI操作系统 × 前线部署工程",
        thesis="把分散数据、业务流程和AI模型连接到可运行的软件系统，服务政府和复杂企业决策。",
        businesses=[("grid", "Gotham", "面向政府与国防的情报、行动和任务软件。"), ("factory", "Foundry", "企业数据整合、运营分析与工作流平台。"), ("spark", "AIP与Apollo", "部署生成式AI应用，并跨环境持续交付软件。")],
        status=[("grid", "4个核心平台", "Gotham、Foundry、Apollo与AIP"), ("people", "约4,300名员工", "高密度软件与前线部署团队"), ("building", "政府+商业", "两类高复杂度客户市场")],
        timeline=[("2003", "公司成立"), ("2011", "Gotham进入更多政府场景"), ("2020", "在NYSE直接上市"), ("2023", "发布AIP")],
        profile_source="https://www.palantir.com/about/",
        culture=[
            culture("扁平组织让新人直接交付", "做法：减少层级，把问题和责任直接交给能解决它的人，年轻工程师从入职初期就参与生产系统。", "案例：招聘页面明确强调从第一天交付真实工作，而不是先在外围项目长期观察。", "可借鉴：授权的衡量标准是新人多久接触真实客户和生产责任。", "组织", "rocket", "https://www.palantir.com/careers/open-positions/"),
            culture("工程师必须靠近真实问题", "做法：Forward Deployed Engineers与客户并肩工作，把现场问题迅速转成软件、数据模型和工作流。", "案例：前线部署不是售后移交，而是产品团队持续从客户环境获得反馈并迭代平台。", "可借鉴：复杂B2B产品要缩短工程师与用户问题之间的距离。", "客户", "customer", "https://www.palantir.com/careers/teams/forward-deployed-software-engineering/"),
            culture("用真实项目筛选潜力", "做法：Meritocracy Fellowship把讨论、写作和实际项目结合，让非传统背景人才通过成果证明能力。", "案例：项目强调严谨辩论与实作，而不只按学校、专业或履历筛选。", "可借鉴：当岗位需要稀缺判断力时，用工作样本比标签更接近真实能力。", "人才", "book", "https://www.palantir.com/careers/meritocracy-fellowship/"),
        ],
    ),
    company(
        rank=48, slug="agriculturalbank", folder="48_农业银行", prefix="agriculturalbank", name="中国农业银行",
        en="Agricultural Bank of China Limited", ticker="SSE/HKEX: 601288 / 1288", founded="1951年",
        hq="Beijing, China", ceo="谷澍（董事长）", employees="约451,000人", position="中国国有大型商业银行",
        color="#00856A", deep="#125A4C", gold="#B9954B", homepage="https://www.abchina.com/",
        logo_path=str(LOGO_ROOT / "agriculturalbank-official-crop.png"), logo_source="https://www.abchina.com/en/images/logo_ue2.png",
        strap="县域金融 × 零售银行 × 公司与资金业务",
        thesis="以覆盖城乡的网点和客户基础服务农业农村、个人与企业，是中国规模最大的银行之一。",
        businesses=[("field", "三农与县域金融", "服务农业、农村、县域产业和乡村振兴。"), ("people", "个人银行", "存款、贷款、财富管理、银行卡和数字银行。"), ("building", "公司与金融市场", "企业融资、交易银行、托管和资金业务。")],
        status=[("store", "约23,000个境内网点", "覆盖城乡的线下服务网络"), ("people", "约451,000名员工", "超大型银行组织规模"), ("shield", "连续入选G-SIB", "全球系统重要性银行")],
        timeline=[("1951", "农业合作银行成立"), ("1979", "恢复中国农业银行"), ("2009", "改制为股份有限公司"), ("2010", "上海与香港上市")],
        profile_source="https://www.abchina.com/cn/aboutabc/nhfm/nhjj/",
        culture=[
            culture("把基层问题变成管理层必须解决的清单", "做法：管理人员走访基层网点、收集员工困难并形成问题台账，推动跨部门解决。", "数字：2025年领导干部走访超过17,000个网点，推动解决11,192项一线员工问题。", "可借鉴：关爱基层不能只做慰问，要有问题数量、责任人和解决闭环。", "员工", "store", "https://www.abchina.com/en/AboutUs/susReports/202603/P020260519520656605515.pdf"),
            culture("管理与专业双通道成长", "做法：员工可以沿管理岗位或专业岗位晋升，减少优秀专业人才只有当管理者一条路。", "案例：公司公开推动双通道职业发展，并通过线上课程、主题模块和轮训支持岗位能力升级。", "可借鉴：专业人才的晋升、薪酬与荣誉应有独立通道。", "人才", "ladder", "https://www.abchina.com/en/investor-relations/corporate-announcements/Announcements/202509/W020250925626807786746.pdf"),
            culture("员工关怀覆盖心理健康", "做法：通过员工关爱调查、心理咨询、测评和讲座识别压力并提供支持。", "数字：2025年上半年超过30万名员工参与关爱调查，提供53,700人次心理咨询、24,400人次测评。", "可借鉴：大组织的员工关怀要从福利清单升级为可持续的支持系统。", "员工", "heart", "https://www.abchina.com/en/investor-relations/corporate-announcements/Announcements/202509/W020250925626807786746.pdf"),
        ],
    ),
    company(
        rank=49, slug="merck", folder="49_默沙东", prefix="merck", name="默沙东", en="Merck & Co., Inc.",
        ticker="NYSE: MRK", founded="1891年", hq="Rahway, New Jersey, USA", ceo="Robert M. Davis",
        employees="约75,000人", position="全球研究型制药公司", color="#00857C", deep="#0A524D", gold="#B28746",
        homepage="https://www.merck.com/", logo_path=str(LOGO_ROOT / "merck-official.svg"),
        logo_source="https://www.merck.com/wp-content/uploads/sites/124/2025/08/site-logo.svg",
        strap="处方药 × 疫苗 × 动物保健",
        thesis="以临床研究和全球商业化开发处方药、疫苗与动物保健产品，研发管线决定长期增长。",
        businesses=[("pill", "处方药", "肿瘤、免疫、心血管与传染病药物。"), ("shield", "疫苗", "人用疫苗研发、生产与全球供应。"), ("paw", "动物保健", "伴侣动物与畜牧健康产品和技术。")],
        status=[("history", "135年历史", "研究型制药传统"), ("globe", "140+个国家", "产品与业务覆盖"), ("people", "约75,000名员工", "科研、生产与商业团队")],
        timeline=[("1891", "美国默沙东成立"), ("1953", "与Sharp & Dohme合并"), ("2009", "与Schering-Plough合并"), ("2021", "Organon分拆")],
        profile_source="https://www.merck.com/company-overview/",
        culture=[
            culture("药品首先是为人，而不是为利润", "做法：以患者需要和科学价值约束资源选择，把长期信任置于短期商业收益之前。", "案例：Mectizan捐赠计划自1987年承诺按需要长期免费供药，而不是设定一次性数量后退出。", "可借鉴：使命可信度来自长期、可验证且有成本的承诺。", "客户", "heart", "https://www.merck.com/stories/mectizan/"),
            culture("鼓励Speak Up并禁止报复", "做法：行为准则要求员工就伦理、合规和患者风险主动提问或报告，管理者必须保护提出问题的人。", "案例：公司公开把调查、根因分析和整改放在举报之后，避免只处理单个责任人。", "可借鉴：说真话文化需要报告渠道、反报复和整改闭环同时存在。", "伦理", "speak", "https://www.merck.com/company-overview/culture-and-values/code-of-conduct/"),
        ],
    ),
    company(
        rank=50, slug="icbc", folder="50_工商银行", prefix="icbc", name="中国工商银行", en="Industrial and Commercial Bank of China Limited",
        ticker="SSE/HKEX: 601398 / 1398", founded="1984年", hq="Beijing, China", ceo="廖林（董事长）",
        employees="约419,000人", position="全球规模最大的商业银行之一", color="#C8102E", deep="#7A1226", gold="#B79654",
        homepage="https://www.icbc-ltd.com/", logo_path=str(LOGO_ROOT / "icbc-official-crop.png"),
        logo_source="https://www.icbc-ltd.com/page/721854332839690284.html",
        strap="公司金融 × 个人金融 × 金融市场与国际业务",
        thesis="以超大客户、存款和网点基础服务个人与企业，并通过数字化和国际网络管理全球银行业务。",
        businesses=[("building", "公司金融", "企业存贷、结算、投行和交易银行。"), ("people", "个人金融", "零售存贷、财富管理、银行卡和养老金融。"), ("globe", "金融市场与国际业务", "资金交易、托管、跨境金融和境外机构。")],
        status=[("store", "17,000+家机构", "覆盖境内外的服务组织"), ("people", "约419,000名员工", "全球最大银行用工规模之一"), ("shield", "全球系统重要性银行", "持续接受更高资本与治理要求")],
        timeline=[("1984", "中国工商银行成立"), ("2005", "改制为股份有限公司"), ("2006", "上海与香港同步上市"), ("2024", "成立四十周年")],
        profile_source="https://www.icbc-ltd.com/column/1438058326469787849.html",
        culture=[
            culture("用企业大学统一超大组织能力", "做法：ICBC College把线上学习、实体校区、岗位认证和专业课程连接起来，服务不同地区和岗位。", "数字：官方介绍该体系面向40多万员工、17,000多家机构，并设有40多个实体校区。", "可借鉴：企业大学要与岗位认证和职业路径相连，不能只做课程仓库。", "人才", "book", "https://www.icbc-ltd.com/en/column/1438058326469787849.html"),
            culture("员工为本与稳健经营同时落地", "做法：企业文化框架将诚信、人本、稳健、创新和卓越并列，强调服务客户与控制风险的长期一致性。", "案例：公开选拔和跨区域交流让基层员工进入总部或跨机构历练，打通大组织内部流动。", "可借鉴：价值观要对应人才流动、选拔和风险决策等具体制度。", "组织", "ladder", "https://www.icbc-ltd.com/icbc/en/newsupdates/icbc%20news/ICBC%20Announces%20a%20Framework%20for%20Corporate%20Culture.htm"),
        ],
    ),
    company(
        rank=51, slug="goldmansachs", folder="51_高盛", prefix="goldmansachs", name="高盛", en="The Goldman Sachs Group, Inc.",
        ticker="NYSE: GS", founded="1869年", hq="New York, USA", ceo="David Solomon", employees="约46,500人",
        position="全球领先投资银行与资产管理机构", color="#7399C6", deep="#284C72", gold="#A9874C",
        homepage="https://www.goldmansachs.com/", logo_path=str(LOGO_ROOT / "goldmansachs-official.svg"),
        logo_source="https://cdn.gs.com/images/goldman-sachs/v2/gs-favicon.svg",
        strap="全球银行与市场 × 资产财富管理 × 平台业务",
        thesis="以高密度专业人才和长期客户关系连接融资、交易、投资与财富管理。",
        businesses=[("building", "全球银行与市场", "并购、融资、做市、风险管理和机构客户服务。"), ("chart", "资产与财富管理", "机构、私人财富和另类资产管理。"), ("code", "平台解决方案", "交易银行、金融科技与企业服务平台。")],
        status=[("history", "157年历史", "长期服务企业与机构客户"), ("people", "约46,500名员工", "全球专业人才网络"), ("trophy", "顶级全球投行", "并购与资本市场长期位居前列")],
        timeline=[("1869", "Marcus Goldman创立"), ("1896", "加入NYSE"), ("1999", "首次公开募股"), ("2019", "重构业务披露与战略")],
        profile_source="https://www.goldmansachs.com/our-firm",
        culture=[
            culture("学徒制：工作本身就是培养", "做法：新人通过与资深同事共同处理真实客户和市场问题学习，辅导嵌入项目而非只在课堂发生。", "数字：公司披露近9,000名员工曾正式参与暑期实习项目，担任导师、伙伴、教练或经理。", "可借鉴：让更多资深员工承担培养责任，学习速度才不会取决于运气。", "人才", "mentor", "https://www.goldmansachs.com/our-commitments/sustainability/2023-people-strategy-report/multimedia/report.pdf/"),
            culture("反馈来自上级、同事和下属", "做法：360度反馈让员工同时看到多方评价，减少单一主管对发展判断的垄断。", "案例：Three Conversations at GS把目标设定、年中Check-In和年终绩效对话拆成三次正式交流。", "可借鉴：绩效管理要有连续对话和多视角证据。", "反馈", "feedback", "https://www.goldmansachs.com/investor-relations/financials/subsidiary-financial-info/gsbank-usa/2022/gsbusa-annual-report-12-31-2022.pdf"),
        ],
    ),
    company(
        rank=52, slug="novartis", folder="52_诺华", prefix="novartis", name="诺华", en="Novartis AG", ticker="SIX/NYSE: NOVN / NVS",
        founded="1996年", hq="Basel, Switzerland", ceo="Vasant Narasimhan", employees="约76,000人",
        position="聚焦创新药的全球制药公司", color="#E85E27", deep="#8C2F18", gold="#7757A8",
        homepage="https://www.novartis.com/", logo_path=str(LOGO_ROOT / "novartis-official.svg"),
        logo_source="https://www.novartis.com/themes/custom/cosmos/logo.svg",
        strap="创新药 × 四大治疗领域 × 全球研发网络",
        thesis="剥离仿制药后聚焦高价值创新药，以临床开发和全球商业化服务重大疾病。",
        businesses=[("heart", "心血管与免疫", "慢病和免疫领域创新药。"), ("cell", "肿瘤与血液", "精准治疗、放射配体和细胞治疗。"), ("brain", "神经科学", "神经退行与罕见神经疾病。")],
        status=[("people", "近3亿患者", "公司药品年度触达规模"), ("people", "约76,000名员工", "全球研发和商业团队"), ("grid", "4大治疗领域", "聚焦资源的研发组合")],
        timeline=[("1996", "Ciba-Geigy与Sandoz合并"), ("2010", "完成Alcon收购"), ("2019", "Alcon分拆"), ("2023", "Sandoz分拆")],
        profile_source="https://www.novartis.com/about",
        culture=[
            culture("Unbossed：领导者提供方向而非控制", "做法：领导者减少命令和层层审批，明确目标后让团队承担决定与结果。", "案例：Unbossed Leadership Experience以自我觉察、反馈和个人成长帮助领导者改变控制式管理。", "可借鉴：授权不是取消管理，而是把管理从指令转为方向、资源和反馈。", "领导", "compass", "https://www.novartis.com/jp-ja/jp-ja/about-us/people-and-culture/unbossed"),
            culture("Choice with Responsibility", "做法：员工与经理、团队协调后选择工作地点、时间和方式，同时对客户、协作和结果负责。", "案例：公司把灵活工作定义为选择加责任，而不是所有人采用同一远程天数。", "可借鉴：灵活制度要明确团队约定与结果责任。", "员工", "balance", "https://www.novartis.com/jp-ja/about-us/people-and-culture/inspired"),
            culture("把家庭责任纳入全球福利底线", "做法：设定全球父母假最低标准，不因性别或是否生育方而改变基本支持。", "数字：诺华官方披露每位新生儿父母最低可享14周带薪育儿假。", "可借鉴：跨国福利先设全球底线，再允许各地向上增加。", "员工", "heart", "https://www.novartis.com/at-de/ueber-uns/was-wir-tun/unsere-werte/unbossed"),
        ],
    ),
    company(
        rank=53, slug="astrazeneca", folder="53_阿斯利康", prefix="astrazeneca", name="阿斯利康", en="AstraZeneca PLC",
        ticker="LSE/NASDAQ: AZN", founded="1999年", hq="Cambridge, United Kingdom", ceo="Pascal Soriot",
        employees="约94,000人", position="全球创新生物制药公司", color="#830051", deep="#50113B", gold="#00A3E0",
        homepage="https://www.astrazeneca.com/", logo_path=str(LOGO_ROOT / "astrazeneca-official.png"),
        logo_source="https://www.astrazeneca.com/etc/designs/az/img/logo-az.png",
        strap="肿瘤 × 生物制药 × 罕见病",
        thesis="以科学驱动的全球研发平台开发肿瘤、慢病和罕见病药物，临床管线与执行速度决定成长。",
        businesses=[("cell", "肿瘤", "肺癌、乳腺癌、血液肿瘤及新型治疗平台。"), ("heart", "生物制药", "心肾代谢、呼吸与免疫、疫苗和免疫疗法。"), ("dna", "罕见病", "通过Alexion平台开发罕见疾病疗法。")],
        status=[("globe", "85+个国家", "员工与运营覆盖"), ("people", "约94,000名员工", "全球研发、生产与商业团队"), ("grid", "3大治疗板块", "肿瘤、生物制药与罕见病")],
        timeline=[("1999", "Astra与Zeneca合并"), ("2013", "Soriot重塑研发战略"), ("2021", "收购Alexion"), ("2024", "扩大细胞治疗与ADC布局")],
        profile_source="https://www.astrazeneca.com/our-company.html",
        culture=[
            culture("Follow the science，但允许聪明冒险", "做法：以患者和科学为判断起点，鼓励团队提出假设、快速实验，并从失败中学习。", "案例：Values and Behaviours明确要求员工Play to Win、勇于承担smart risks，而不是为避免错误压制创新。", "可借鉴：创新文化要定义哪些风险可承担、如何复盘，而不是笼统鼓励冒险。", "组织", "flask", "https://careers.astrazeneca.com/values-behaviours"),
            culture("Speak Up必须让员工感到安全", "做法：通过伦理热线、管理者责任和反报复要求，让员工能够提出合规或团队问题。", "数字：公司披露2022年83%的员工认为阿斯利康具备Speak Up文化。", "可借鉴：心理安全要用员工感知数据持续检验。", "反馈", "speak", "https://careers.astrazeneca.com/sustainability"),
        ],
    ),
    company(
        rank=54, slug="philipmorris", folder="54_菲利普莫里斯", prefix="philipmorris", name="菲利普莫里斯国际",
        en="Philip Morris International Inc.", ticker="NYSE: PM", founded="2008年独立上市", hq="Stamford, Connecticut, USA",
        ceo="Jacek Olczak", employees="约83,000人", position="全球烟草与无烟产品公司", color="#243B53", deep="#14283B", gold="#B8944A",
        homepage="https://www.pmi.com/", logo_path=str(LOGO_ROOT / "philipmorris-official.svg"),
        logo_source="https://www.pmi.com/content/dam/pmicom/global/images/logos/pmi-logoaaf115bd6c7468f696e2ff0400458fff.svg",
        strap="传统烟草 × 加热不燃烧 × 口含尼古丁产品",
        thesis="以全球烟草现金流支持向无烟产品转型，组织同时管理成熟业务、科学研究和新产品商业化。",
        businesses=[("brands", "传统烟草", "Marlboro等国际品牌的生产与销售。"), ("spark", "加热不燃烧", "IQOS设备与烟草耗材。"), ("leaf", "口含与健康产品", "ZYN等尼古丁袋及相关无烟品类。")],
        status=[("globe", "180+个市场", "产品销售覆盖"), ("people", "约3,650万成年用户", "2024年末使用PMI无烟产品"), ("people", "约83,000名员工", "全球研发、生产与销售团队")],
        timeline=[("1847", "Philip Morris品牌源起"), ("2008", "从Altria分拆独立"), ("2014", "IQOS商业化"), ("2022", "收购Swedish Match")],
        profile_source="https://www.pmi.com/who-we-are",
        culture=[
            culture("混合工作以团队结果为边界", "做法：SMART WORK允许员工和团队结合岗位、客户与协作需求安排办公室和远程工作。", "案例：制度强调灵活性必须与绩效、连接和业务需要共同平衡，而不是单一考勤规则。", "可借鉴：混合办公要给团队原则和边界，而不是只规定天数。", "员工", "balance", "https://www.pmi.com/careers/why-work-at-pmi"),
            culture("同工同酬接受外部验证", "做法：通过EQUAL-SALARY第三方认证审查薪酬流程与性别公平，而不只发布内部承诺。", "数字：PMI于2025年获得第三次全球EQUAL-SALARY认证，有效期三年。", "可借鉴：重要的人才承诺应尽量引入独立审计。", "员工", "scale", "https://www.pmi.com/careers/inclusion-and-diversity"),
            culture("为所有员工提供可持续学习入口", "做法：全球员工可通过线上平台获取技能、语言和专业内容，并配合岗位发展。", "数字：官方职业页面披露平台支持24种语言，累计提供7,000小时以上学习内容。", "可借鉴：学习福利要降低地域和岗位门槛，并披露实际供给规模。", "人才", "book", "https://www.pmi.com/careers/areas-of-work/product"),
        ],
    ),
    company(
        rank=55, slug="kla", folder="55_KLA", prefix="kla", name="KLA", en="KLA Corporation", ticker="NASDAQ: KLAC",
        founded="1975年", hq="Milpitas, California, USA", ceo="Rick Wallace", employees="约15,000人",
        position="半导体过程控制设备龙头", color="#0099C6", deep="#15536A", gold="#1D7E9C",
        homepage="https://www.kla.com/", logo_path=str(LOGO_ROOT / "kla-official.jpg"),
        logo_source="https://ir.kla.com/sec-filings/all-sec-filings/content/0001193125-22-277886/0001193125-22-277886.pdf",
        strap="检测 × 量测 × 良率管理",
        thesis="为先进芯片制造寻找微小缺陷、测量关键结构并分析良率，是晶圆厂提升产出不可缺少的过程控制平台。",
        businesses=[("scan", "晶圆检测", "发现晶圆和掩模上的缺陷与异常。"), ("ruler", "量测与过程控制", "测量关键尺寸、薄膜和叠对精度。"), ("chart", "良率软件与服务", "将设备数据转成工艺诊断和生产改进。")],
        status=[("people", "约15,000名员工", "全球工程与客户服务团队"), ("flask", "约27%员工从事研发", "FY2024人才结构"), ("tools", "约28%员工服务客户", "FY2024现场支持结构")],
        timeline=[("1975", "KLA成立"), ("1997", "KLA与Tencor合并"), ("2019", "更名KLA Corporation"), ("2019", "完成Orbotech收购")],
        profile_source="https://www.kla.com/company",
        culture=[
            culture("高绩效团队建立在坦诚一致上", "做法：核心价值观要求员工诚实、直率、一致，并把团队结果置于部门边界之上。", "案例：公司把perseverance、drive to be better和high-performance teams写入招聘与员工沟通。", "可借鉴：高标准文化必须允许及时指出问题和不同意见。", "组织", "speak", "https://www.kla.com/wp-content/uploads/KLA-Global-Impact-Report-3.pdf"),
            culture("用股权和低流失保留专业人才", "做法：广泛使用限制性股票和员工购股计划，让员工分享长期价值。", "数字：KLA FY2024自愿离职率为3.7%，对高技能半导体设备人才而言体现较强留任。", "可借鉴：人才密集企业应同时看薪酬结构和真实离职结果。", "员工", "coin", "https://ir.kla.com/sec-filings/annual-reports/content/0001193125-24-224805/0001193125-24-224805.pdf"),
            culture("把员工公益参与做成制度", "做法：Donations for Doers按志愿小时捐款，并设置员工捐赠配捐额度。", "数字：每小时志愿服务可触发10美元捐款、每人每年最高500美元；配捐最高10,000美元。2023年员工志愿服务12,220小时。", "可借鉴：公益文化要给员工时间、匹配资金和可追踪结果。", "员工", "heart", "https://www.kla.com/wp-content/uploads/KLA-Global-Impact-Report-3.pdf"),
        ],
    ),
    company(
        rank=56, slug="gevernova", folder="56_GE_Vernova", prefix="gevernova", name="GE Vernova", en="GE Vernova Inc.",
        ticker="NYSE: GEV", founded="2024年独立上市", hq="Cambridge, Massachusetts, USA", ceo="Scott Strazik",
        employees="约75,000人", position="全球电力设备与能源技术公司", color="#006B63", deep="#164B47", gold="#4AA39A",
        homepage="https://www.gevernova.com/", logo_path=str(LOGO_ROOT / "gevernova-official.svg"),
        logo_source="https://www.gevernova.com/themes/custom/ge_vernova_unified/logo.svg",
        strap="Power × Wind × Electrification",
        thesis="覆盖发电、风电、电网和电气化技术，设备装机与长期服务连接全球电力系统。",
        businesses=[("bolt", "Power", "燃气轮机、蒸汽、核电与水电设备及服务。"), ("wind", "Wind", "陆上与海上风电设备和服务。"), ("grid", "Electrification", "电网设备、软件、转换与储能技术。")],
        status=[("people", "约75,000名员工", "全球工程与服务组织"), ("globe", "100+个国家", "设备、客户与服务覆盖"), ("bolt", "约25%全球电力", "由其技术设备参与发电或传输")],
        timeline=[("1892", "GE电力技术源起"), ("2015", "收购Alstom Power"), ("2021", "宣布拆分计划"), ("2024", "GE Vernova独立上市")],
        profile_source="https://www.gevernova.com/about",
        culture=[
            culture("用Lean让管理者和一线一起到现场", "做法：跨职能团队通过Kaizen在gemba观察流程、识别浪费并立即试验改进。", "案例：官方案例中管理人员与一线员工用一周集中改进现场流程，而不是只在会议室制定方案。", "可借鉴：持续改进必须让决策者亲眼看到工作如何发生。", "组织", "tools", "https://www.gevernova.com/news/articles/leaning-teams-use-lean-eliminate-waste-bolster-efficiency-and-drive-continuous-improvement"),
            culture("清晰角色、决策权和问责", "做法：GE Vernova Way要求团队明确谁做决定、谁负责结果，并鼓励在边界清楚后快速行动。", "案例：公司把customers、innovation、lean、one team和accountable作为独立后的共同工作方式。", "可借鉴：组织提速先解决决策权模糊，而不是单纯要求员工更快。", "组织", "compass", "https://www.gevernova.com/news/articles/opening-bell-ge-vernovas-culture-chimes-with-its-purpose"),
            culture("员工声音一年不只听一次", "做法：通过一年两次的全员调查跟踪工作体验，并要求领导团队讨论和响应结果。", "案例：2025可持续发展报告披露持续使用员工调查和团队行动推动文化落地。", "可借鉴：员工反馈需要固定节奏和团队级责任。", "反馈", "feedback", "https://www.gevernova.com/sustainability/documents/sustainability/ge-vernova-sustainability-report-2025.pdf?_rsc=1tenz"),
        ],
    ),
    company(
        rank=57, slug="rbc", folder="57_加拿大皇家银行", prefix="rbc", name="加拿大皇家银行", en="Royal Bank of Canada",
        ticker="TSX/NYSE: RY", founded="1864年", hq="Toronto, Canada", ceo="Dave McKay", employees="约96,000人",
        position="加拿大最大综合金融集团之一", color="#0051A5", deep="#183D69", gold="#D5A928",
        homepage="https://www.rbc.com/", logo_path=str(LOGO_ROOT / "rbc-official.svg"),
        logo_source="https://www.rbc.com/dvl/v1.0/assets/images/logos/rbc-logo-shield-blue.svg",
        strap="个人与商业银行 × 财富管理 × 资本市场",
        thesis="以加拿大客户基础为核心，连接零售银行、财富管理、保险与全球资本市场。",
        businesses=[("people", "个人与商业银行", "存贷、支付、信用卡和中小企业服务。"), ("chart", "财富管理", "加拿大、美国及国际财富与资产管理。"), ("building", "资本市场与保险", "企业融资、交易、投资银行和保险。")],
        status=[("people", "1,800万+客户", "个人、企业与机构客户"), ("people", "约96,000名员工", "北美综合金融团队"), ("globe", "加拿大+全球市场", "零售根基与国际资本市场并存")],
        timeline=[("1864", "Merchants Bank of Halifax成立"), ("1901", "更名Royal Bank of Canada"), ("1976", "总部迁至多伦多"), ("2024", "完成HSBC Canada收购")],
        profile_source="https://www.rbc.com/about-rbc.html",
        culture=[
            culture("无论职位都可以Speak Up", "做法：Speak Up for Inclusion要求员工在看到排斥、偏见或不公平时发声，并明确不应因提出问题受到报复。", "案例：That Little Voice项目用真实工作情境帮助员工练习如何介入，而不是只发布包容口号。", "可借鉴：包容文化要教员工在具体场景里怎么说、怎么做。", "反馈", "speak", "https://www.rbc.com/diversity-inclusion/that-little-voice.html"),
            culture("全年持续倾听员工", "做法：通过全员调查、脉冲反馈和团队对话，在一年中多次收集员工体验。", "案例：2025可持续发展报告把持续倾听与领导行动列为人才管理机制。", "可借鉴：大型组织不能只依赖年度敬业度分数。", "反馈", "feedback", "https://www.rbc.com/our-impact/_assets-custom/pdf/RBC-2025-sustainability-report.pdf"),
        ],
    ),
    company(
        rank=58, slug="ibm", folder="58_IBM", prefix="ibm", name="IBM", en="International Business Machines Corporation",
        ticker="NYSE: IBM", founded="1911年", hq="Armonk, New York, USA", ceo="Arvind Krishna", employees="约270,000人",
        position="全球企业级混合云与AI公司", color="#0F62FE", deep="#163A70", gold="#5A8DEE",
        homepage="https://www.ibm.com/", logo_path=str(LOGO_ROOT / "ibm-official.png"),
        logo_source="https://www.ibm.com/content/dam/connectedassets-adobe-cms/worldwide-content/creative-assets/s-migr/ul/g/18/f9/ibm_logo_pos_blue60_rgb.png/_jcr_content/renditions/cq5dam.thumbnail.1280.1280.png",
        strap="软件 × 咨询 × 基础设施",
        thesis="以Red Hat混合云、企业AI、咨询和主机系统服务复杂企业客户，长期关系与迁移成本构成黏性。",
        businesses=[("cloud", "软件", "Red Hat、混合云、自动化、数据与AI软件。"), ("people", "咨询", "技术转型、应用与业务流程服务。"), ("server", "基础设施", "IBM Z主机、Power服务器和存储。")],
        status=[("history", "115年历史", "企业计算与技术服务积累"), ("people", "约270,000名员工", "全球技术、咨询与销售团队"), ("globe", "175+个国家", "客户与运营覆盖")],
        timeline=[("1911", "CTR公司成立"), ("1924", "更名IBM"), ("1981", "IBM PC发布"), ("2019", "完成Red Hat收购")],
        profile_source="https://www.ibm.com/about",
        culture=[
            culture("每人每年至少40小时学习", "做法：把持续学习设为全员基本要求，并通过数字平台、徽章和技能路径连接岗位需要。", "数字：IBM公开要求员工每年至少投入40小时学习；最新披露年度员工学习总时数约2,310万小时。", "可借鉴：学习文化要有最低投入、内容入口和可追踪结果。", "人才", "book", "https://www.ibm.com/responsibility/data-and-policies"),
            culture("Skills First，不把四年学位当唯一门票", "做法：New Collar和学徒项目按技能与潜力招聘，为没有相关四年制学位的人提供带薪学习和实践。", "数字：IBM披露约90%的学徒项目毕业生转为全职员工。", "可借鉴：放宽学历门槛必须配套可验证的技能训练和转正路径。", "人才", "ladder", "https://www.ibm.com/careers/blog/the-ibm-apprenticeship-program-no-degree-no-problem"),
        ],
    ),
    company(
        rank=59, slug="dell", folder="59_Dell", prefix="dell", name="戴尔科技", en="Dell Technologies Inc.",
        ticker="NYSE: DELL", founded="1984年", hq="Round Rock, Texas, USA", ceo="Michael Dell", employees="约108,000人",
        position="全球端到端IT基础设施公司", color="#0076CE", deep="#164A70", gold="#59A4D7",
        homepage="https://www.dell.com/", logo_path=str(LOGO_ROOT / "dell-official.png"),
        logo_source="https://www.dell.com/en-us/lp/legal/trademarks",
        strap="客户端设备 × 服务器与存储 × 服务",
        thesis="从PC直销发展为覆盖终端、服务器、存储与企业服务的IT基础设施平台。",
        businesses=[("laptop", "Client Solutions", "商用与消费PC、显示器、外设和客户端服务。"), ("server", "Infrastructure Solutions", "服务器、AI基础设施、存储与数据保护。"), ("tools", "服务与金融", "部署、支持、托管和设备融资。")],
        status=[("history", "42年历史", "从PC创业公司到全球IT集团"), ("people", "约108,000名员工", "全球研发、销售与服务团队"), ("globe", "180+个国家", "客户与合作伙伴覆盖")],
        timeline=[("1984", "Michael Dell创立PC's Limited"), ("1988", "在NASDAQ上市"), ("2016", "完成EMC收购"), ("2018", "重返公开市场")],
        profile_source="https://www.dell.com/en-us/dt/corporate/about-us/who-we-are.htm",
        culture=[
            culture("ABCD：成就、平衡、连接与多元", "做法：People Philosophy用Achieve、Balance、Connect、Diverse四个维度讨论员工如何工作和成长。", "案例：Culture Code把这些原则连接到领导、协作和员工体验，而不是只罗列福利。", "可借鉴：人才理念要同时回答绩效、生活、归属和多元四类问题。", "组织", "balance", "https://www.dell.com/en-us/lp/dt/workplace"),
            culture("Tell Dell：用持续倾听改进工作体验", "做法：年度Tell Dell调查配合全年持续倾听，让团队根据反馈制定行动。", "案例：公司把员工声音纳入工作场所与领导改进，而不是把调查结果停留在人力资源部门。", "可借鉴：员工调查必须由业务团队共同承担改进责任。", "反馈", "feedback", "https://www.dell.com/en-us/lp/dt/workplace"),
            culture("把包容做成可使用的组织基础设施", "做法：通过员工资源小组和Assistive Technology Center of Excellence提供社群与辅助技术。", "数字：官方披露13个员工资源小组、469个分会，覆盖80个国家；辅助技术中心向所有员工提供保密自助服务。", "可借鉴：包容不只靠活动，还要有员工能直接使用的工具和服务。", "员工", "people", "https://www.dell.com/en-us/lp/dt/workplace"),
        ],
    ),
]


CURRENT_MARKET_CAPS = {
    "chevron": "$350.46B", "pg": "$345.56B", "roche": "$336.66B",
    "homedepot": "$335.24B", "hsbc": "$329.55B", "arm": "$320.67B",
    "palantir": "$316.97B", "agriculturalbank": "$321.64B",
    "merck": "$311.17B", "icbc": "$375.04B", "goldmansachs": "$315.69B",
    "novartis": "$284.61B", "astrazeneca": "$295.16B",
    "philipmorris": "$291.56B", "kla": "$288.92B",
    "gevernova": "$287.80B", "rbc": "$285.75B", "ibm": "$283.89B",
    "dell": "$279.11B",
}

for _company in COMPANIES:
    _company["core_business"] = "、".join(item[1] for item in _company["businesses"])
    _company["current_market_cap"] = CURRENT_MARKET_CAPS[_company["slug"]]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def data_uri(path: str) -> str:
    p = Path(path)
    mime = "image/svg+xml" if p.suffix.lower() == ".svg" else ("image/jpeg" if p.suffix.lower() in {".jpg", ".jpeg"} else "image/png")
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"


def icon(name: str, color: str, size: int = 38) -> str:
    shapes = {
        "drop":"<path d='M24 5S11 21 11 30a13 13 0 0 0 26 0C37 21 24 5 24 5z'/>",
        "factory":"<path d='M6 41V22l11 6V18l11 7V11h8v30z'/><path d='M11 34h5M22 34h5M33 34h4'/>",
        "leaf":"<path d='M39 8C20 8 9 19 10 39c17 2 29-9 29-31z'/><path d='M12 37c7-9 14-15 23-22'/>",
        "spark":"<path d='M24 4l3 13 13 3-13 4-3 13-4-13-12-4 12-3z'/>",
        "home":"<path d='M6 23L24 8l18 15M11 21v20h26V21M20 41V29h8v12'/>",
        "brands":"<circle cx='16' cy='17' r='9'/><circle cx='31' cy='17' r='9'/><circle cx='24' cy='31' r='9'/>",
        "pill":"<path d='M11 11a10 10 0 0 1 14 0l12 12a10 10 0 0 1-14 14L11 25a10 10 0 0 1 0-14z'/><path d='M17 31l14-14'/>",
        "flask":"<path d='M18 5h12M21 5v13L10 38a3 3 0 0 0 3 5h22a3 3 0 0 0 3-5L27 18V5'/><path d='M15 33h18'/>",
        "network":"<circle cx='12' cy='12' r='5'/><circle cx='36' cy='14' r='5'/><circle cx='24' cy='36' r='5'/><path d='M16 14l15 1M15 16l7 15M34 19l-7 12'/>",
        "store":"<path d='M7 18h34l-4-10H11z'/><path d='M9 18v23h30V18M16 41V28h9v13'/>",
        "tools":"<path d='M30 7a9 9 0 0 0-8 12L8 33l7 7 14-14a9 9 0 0 0 12-8l-8 4-6-6z'/>",
        "truck":"<path d='M5 13h24v22H5zM29 21h8l6 8v6H29z'/><circle cx='13' cy='38' r='4'/><circle cx='36' cy='38' r='4'/>",
        "people":"<circle cx='18' cy='15' r='7'/><circle cx='34' cy='17' r='5'/><path d='M5 42c1-11 7-17 15-17s14 6 15 17M30 28c7 1 11 6 12 14'/>",
        "building":"<path d='M8 42V13l16-7 16 7v29z'/><path d='M15 19h4M29 19h4M15 27h4M29 27h4M21 42V32h6v10'/>",
        "globe":"<circle cx='24' cy='24' r='18'/><path d='M6 24h36M24 6c7 7 7 29 0 36M24 6c-7 7-7 29 0 36'/>",
        "grid":"<rect x='6' y='6' width='14' height='14'/><rect x='28' y='6' width='14' height='14'/><rect x='6' y='28' width='14' height='14'/><rect x='28' y='28' width='14' height='14'/>",
        "chip":"<rect x='11' y='11' width='26' height='26' rx='3'/><path d='M17 17h14v14H17zM5 16h6M5 24h6M5 32h6M37 16h6M37 24h6M37 32h6M16 5v6M24 5v6M32 5v6M16 37v6M24 37v6M32 37v6'/>",
        "code":"<path d='M17 13L7 24l10 11M31 13l10 11-10 11M27 7l-6 34'/>",
        "phone":"<rect x='14' y='4' width='20' height='40' rx='4'/><path d='M20 9h8M22 39h4'/>",
        "field":"<path d='M5 37c10-12 28-12 38 0M5 27c10-10 28-10 38 0M24 8v34M15 13c6 1 9 5 9 11M33 13c-6 1-9 5-9 11'/>",
        "shield":"<path d='M24 5l15 6v10c0 10-7 17-15 21-8-4-15-11-15-21V11z'/><path d='M16 24l5 5 11-12'/>",
        "paw":"<circle cx='24' cy='30' r='8'/><circle cx='11' cy='21' r='4'/><circle cx='20' cy='13' r='4'/><circle cx='29' cy='13' r='4'/><circle cx='38' cy='21' r='4'/>",
        "chart":"<path d='M7 41V7M7 41h35M12 33l10-10 7 6 11-16'/>",
        "heart":"<path d='M24 41S7 31 7 18c0-9 11-12 17-4 6-8 17-5 17 4 0 13-17 23-17 23z'/>",
        "cell":"<circle cx='24' cy='24' r='17'/><circle cx='24' cy='24' r='7'/><path d='M14 12l5 7M34 13l-5 6M13 34l6-5M35 34l-6-5'/>",
        "brain":"<path d='M19 7c-6 0-9 5-8 10-5 2-6 10-1 13-2 6 4 12 10 9 3 5 11 2 10-3 7 0 10-8 6-12 3-5-1-11-6-11-2-5-9-6-11-2z'/><path d='M24 10v28M14 20h7M27 27h8'/>",
        "dna":"<path d='M12 6c24 12 0 24 24 36M36 6C12 18 36 30 12 42M16 12h16M14 23h20M16 36h16'/>",
        "scan":"<path d='M8 17V8h9M31 8h9v9M40 31v9h-9M17 40H8v-9'/><circle cx='24' cy='24' r='9'/>",
        "ruler":"<path d='M7 31L31 7l10 10-24 24z'/><path d='M27 11l4 4M21 17l4 4M15 23l4 4'/>",
        "bolt":"<path d='M28 4L10 27h13l-3 17 18-25H25z'/>",
        "wind":"<path d='M5 17h25c8 0 8-10 1-10-4 0-6 2-6 5M5 25h34c7 0 7 10 0 10-4 0-6-2-6-5M5 33h18'/>",
        "cloud":"<path d='M13 37h25a8 8 0 0 0 0-16 14 14 0 0 0-27-3A10 10 0 0 0 13 37z'/>",
        "server":"<rect x='8' y='7' width='32' height='14' rx='2'/><rect x='8' y='27' width='32' height='14' rx='2'/><path d='M14 14h.1M20 14h12M14 34h.1M20 34h12'/>",
        "laptop":"<rect x='10' y='7' width='28' height='25' rx='2'/><path d='M5 38h38l-3 4H8z'/>",
        "gauge":"<path d='M7 35a18 18 0 0 1 34 0'/><path d='M24 30l9-10M12 35h24'/>",
        "coin":"<circle cx='24' cy='24' r='17'/><path d='M29 16c-2-3-7-3-9 0-3 4 2 7 5 7 5 1 7 6 3 9-4 3-9 1-10-2M24 10v28'/>",
        "trophy":"<path d='M14 7h20v10c0 8-4 13-10 13s-10-5-10-13zM14 11H7v5c0 5 4 8 9 8M34 11h7v5c0 5-4 8-9 8M24 30v7M16 42h16M19 37h10'/>",
        "history":"<circle cx='24' cy='24' r='18'/><path d='M24 13v12l8 5'/>",
        "feedback":"<path d='M7 8h34v25H23l-9 8v-8H7z'/><path d='M15 17h18M15 24h12'/>",
        "speak":"<path d='M8 10h32v22H22l-8 8v-8H8z'/><path d='M17 18h14M17 25h9'/>",
        "scale":"<path d='M24 6v36M10 13h28M14 13L7 28h14zM34 13l-7 15h14zM16 42h16'/>",
        "rocket":"<path d='M20 31c-5 1-8 4-9 9 5-1 8-4 9-9zM28 31c5 1 8 4 9 9-5-1-8-4-9-9zM24 5c9 7 9 20 0 30-9-10-9-23 0-30z'/><circle cx='24' cy='19' r='4'/>",
        "customer":"<circle cx='24' cy='16' r='8'/><path d='M9 42c1-11 7-17 15-17s14 6 15 17'/><path d='M6 12l5-5M42 12l-5-5'/>",
        "book":"<path d='M6 9c7-3 13-1 18 4v29c-5-5-11-7-18-4zM42 9c-7-3-13-1-18 4v29c5-5 11-7 18-4z'/>",
        "ladder":"<path d='M14 5v38M34 5v38M14 13h20M14 23h20M14 33h20'/>",
        "mentor":"<circle cx='17' cy='14' r='6'/><circle cx='33' cy='16' r='5'/><path d='M6 40c1-9 6-14 12-14s11 5 12 14M28 27c7 1 11 5 13 13'/>",
        "compass":"<circle cx='24' cy='24' r='18'/><path d='M30 15l-4 11-11 7 5-12z'/>",
        "balance":"<path d='M24 6v36M11 13h26M14 13L7 28h14zM34 13l-7 15h14zM16 42h16'/>",
        "pyramid":"<path d='M24 5L5 42h38zM13 31h22M18 21h12'/>",
    }
    shape = shapes.get(name, shapes["spark"])
    return f"<svg width='{size}' height='{size}' viewBox='0 0 48 48' fill='none' stroke='{color}' stroke-width='2.7' stroke-linecap='round' stroke-linejoin='round'>{shape}</svg>"


def footer(lines: list[str]) -> str:
    return "<footer>" + "<br>".join(esc(x) for x in lines) + "<div class='signature'>by 江明</div></footer>"


@lru_cache(maxsize=1)
def load_stock_histories() -> dict[str, dict]:
    histories = json.loads(STOCK_HISTORY_PATH.read_text(encoding="utf-8"))
    chevron = json.loads(CHEVRON_STOCK_HISTORY_PATH.read_text(encoding="utf-8"))
    chevron_series = []
    for year, value in chevron["annual_close"]:
        date = f"{year}-07-14" if year == chevron["series_end"] else f"{year}-12-31"
        chevron_series.append([date, value])
    histories["chevron"] = {
        "symbol": "CVX",
        "listing_note": "NYSE 1921年上市",
        "listing_source": chevron["official_listing_source"],
        "source_name": "Yahoo Finance",
        "source_url": chevron["market_data_source"],
        "source_currency": "USD",
        "display_currency": "USD",
        "fx_to_usd": 1.0,
        "fx_date": "2026-07-15",
        "currency_note": "原始行情为美元，无需换汇。",
        "price_basis": "拆股调整收盘价，不含股息再投资",
        "as_of": "2026-07-14",
        "series_start": chevron_series[0][0],
        "series_end": chevron_series[-1][0],
        "series": chevron_series,
    }
    if not histories:
        raise ValueError("stock-history snapshot is empty")
    return histories


def profile_height(c: dict) -> int:
    if c["slug"] not in load_stock_histories():
        raise ValueError(f"missing stock history for {c['slug']}")
    return 1790


def _nice_axis(max_value: float) -> tuple[float, float]:
    raw_step = max_value / 4
    magnitude = 10 ** math.floor(math.log10(raw_step))
    normalized = raw_step / magnitude
    if normalized <= 1:
        step = magnitude
    elif normalized <= 2:
        step = 2 * magnitude
    elif normalized <= 5:
        step = 5 * magnitude
    else:
        step = 10 * magnitude
    return math.ceil(max_value / step) * step, step


def _price_label(value: float) -> str:
    if value < 1:
        return f"${value:.2f}"
    if value < 10:
        return f"${value:.1f}"
    return f"${value:,.0f}"


def stock_price_chart(c: dict) -> str:
    history = load_stock_histories()[c["slug"]]
    raw = history["series"]
    points = [(datetime.fromisoformat(date).date(), float(value)) for date, value in raw]
    start_date, start_price = points[0]
    end_date, end_price = points[-1]
    width, height = 760, 190
    left, right, top, bottom = 50, 14, 10, 29
    plot_width = width - left - right
    plot_height = height - top - bottom
    span_days = max(1, (end_date - start_date).days)
    y_max, y_step = _nice_axis(max(value for _, value in points))

    def x_pos(date) -> float:
        return left + (date - start_date).days / span_days * plot_width

    def y_pos(value: float) -> float:
        return top + (1 - value / y_max) * plot_height

    line = " ".join(
        ("M" if index == 0 else "L") + f"{x_pos(date):.1f},{y_pos(value):.1f}"
        for index, (date, value) in enumerate(points)
    )
    area = f"{line} L{x_pos(end_date):.1f},{top + plot_height:.1f} L{x_pos(start_date):.1f},{top + plot_height:.1f} Z"
    y_ticks = []
    value = 0.0
    while value <= y_max + y_step / 2:
        y = y_pos(value)
        y_ticks.append(
            f"<line x1='{left}' y1='{y:.1f}' x2='{width-right}' y2='{y:.1f}' stroke='#e8ddd3' stroke-width='1'/>"
            f"<text x='{left-7}' y='{y+4:.1f}' text-anchor='end' fill='#9b8776' font-size='10' font-weight='700'>{_price_label(value)}</text>"
        )
        value += y_step
    tick_indices = sorted(set(round(i * (len(points) - 1) / 4) for i in range(5)))
    recent = span_days < 365.25 * 4
    x_ticks = []
    for tick_position, index in enumerate(tick_indices):
        date = points[index][0]
        x = x_pos(date)
        label = date.strftime("%Y.%m") if recent else str(date.year)
        anchor = "start" if tick_position == 0 else ("end" if tick_position == len(tick_indices) - 1 else "middle")
        x_ticks.append(
            f"<line x1='{x:.1f}' y1='{top}' x2='{x:.1f}' y2='{top+plot_height}' stroke='#efe5dc' stroke-width='1' stroke-dasharray='3 4'/>"
            f"<text x='{x:.1f}' y='{height-7}' text-anchor='{anchor}' fill='#806d5d' font-size='10' font-weight='800'>{label}</text>"
        )
    multiple = end_price / start_price
    duration_years = max((end_date - start_date).days / 365.25, 0.25)
    annualized = (multiple ** (1 / duration_years) - 1) * 100
    if annualized > 999:
        annualized_label = "价格年化>999%"
    else:
        annualized_label = f"价格年化约{annualized:.1f}%"
    note = history["price_basis"]
    if history["source_currency"] != "USD":
        note += f"；{history['source_currency']}按2026年7月15日固定汇率换算美元"
    return f"""
    <div class='stock-wrap'>
      <div class='stock-meta'><div><b>{esc(history['listing_note'])}</b><span>公开价格序列{start_date.year}-{end_date.year} · USD</span></div><div class='stock-return'>{_price_label(start_price)} → {_price_label(end_price)}<small>约{multiple:.1f}倍 · {annualized_label}</small></div></div>
      <svg class='stock-chart' viewBox='0 0 {width} {height}' role='img' aria-label='{esc(c['en'])} long-term stock price chart'>
        <defs><linearGradient id='stockFill-{esc(c['slug'])}' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='{esc(c['color'])}' stop-opacity='.22'/><stop offset='100%' stop-color='{esc(c['color'])}' stop-opacity='.02'/></linearGradient></defs>
        {''.join(y_ticks)}{''.join(x_ticks)}<path d='{area}' fill='url(#stockFill-{esc(c['slug'])})'/><path d='{line}' fill='none' stroke='{esc(c['color'])}' stroke-width='3.2' stroke-linecap='round' stroke-linejoin='round'/>
        <circle cx='{x_pos(start_date):.1f}' cy='{y_pos(start_price):.1f}' r='4.5' fill='{esc(c['gold'])}' stroke='white' stroke-width='2'/><circle cx='{x_pos(end_date):.1f}' cy='{y_pos(end_price):.1f}' r='5' fill='{esc(c['deep'])}' stroke='white' stroke-width='2'/>
      </svg><div class='stock-note'>{esc(note)}。</div>
    </div>"""


def document(c: dict, title: str, subtitle: str, body: str, lines: list[str], height: int) -> str:
    accent, deep, gold = c["color"], c["deep"], c["gold"]
    return f"""<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><style>
*{{box-sizing:border-box}}html,body{{margin:0;width:900px;height:{height}px;overflow:hidden}}body{{color:#41372f;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;background-color:#f7f4ed;background-image:linear-gradient(rgba(174,142,105,.105) 1px,transparent 1px),linear-gradient(90deg,rgba(174,142,105,.105) 1px,transparent 1px);background-size:24px 24px}}.page{{width:900px;min-height:{height-1}px;padding:48px 52px 0}}.title{{margin:0;text-align:center;color:{accent};font-family:'Songti SC','STSong',serif;font-size:50px;font-weight:900;line-height:1.12;letter-spacing:0}}.subtitle{{margin:9px 0 0;text-align:center;color:#967c68;font-size:16px;font-weight:750}}.strap{{margin:17px auto 20px;border:2px solid {accent};color:#614f41;background:rgba(255,255,255,.62);border-radius:999px;padding:8px 18px;width:max-content;max-width:760px;text-align:center;font-size:17px;font-weight:850}}.logo-hero{{display:grid;grid-template-columns:190px 1fr;gap:24px;align-items:center;margin:5px 0 21px}}.logo-box{{height:132px;border:2px solid #d8c5b3;border-radius:12px;background:rgba(255,255,255,.78);display:flex;align-items:center;justify-content:center;padding:7px}}.logo-box img{{width:174px;max-height:116px;object-fit:contain}}.thesis{{border-left:7px solid {accent};padding:7px 0 7px 18px;color:#49392e;font-family:'Songti SC','STSong',serif;font-size:22px;font-weight:900;line-height:1.42}}.thesis small{{display:block;margin-top:5px;color:#8c7869;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;font-size:13px;font-weight:700}}.section{{margin:21px 0 0}}.section h2{{margin:0 0 13px;color:{accent};text-align:center;font-family:'Songti SC','STSong',serif;font-size:28px;line-height:1.15;font-weight:900}}.section h2:before,.section h2:after{{content:'';display:inline-block;width:70px;border-top:2px solid #d6a89c;margin:0 14px;vertical-align:middle}}.profile{{display:grid;grid-template-columns:repeat(2,1fr);gap:9px 14px}}.p{{border-bottom:1px solid #dfcfc0;padding:0 0 7px;min-height:40px}}.k{{display:block;color:#9b6c5d;font-size:12px;font-weight:850}}.v{{display:block;margin-top:2px;color:#42372f;font-size:15px;font-weight:800;line-height:1.25}}.grid2{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}}.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:11px}}.card{{border:2px solid #dfcabb;border-radius:10px;background:rgba(255,255,255,.7);padding:13px 14px}}.business-card{{display:grid;grid-template-columns:42px 1fr;gap:9px;min-height:112px}}.business-card h3{{margin:0;color:{deep};font-size:18px;line-height:1.22}}.business-card p{{margin:5px 0 0;color:#4c3b2f;font-size:13px;line-height:1.38;font-weight:680}}.wide{{grid-column:1/-1}}.status-card{{border:2px solid #dfcabb;border-radius:10px;background:rgba(255,255,255,.74);padding:11px 9px;text-align:center;min-height:105px}}.status-icon{{height:29px}}.big{{margin-top:3px;color:{accent};font-size:19px;line-height:1.18;font-weight:950}}.explain{{margin-top:5px;color:#6f5b4b;font-size:12px;line-height:1.33;font-weight:700}}.timeline{{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;position:relative}}.timeline:before{{content:'';position:absolute;left:8%;right:8%;top:18px;border-top:2px solid #d5aa95}}.time{{position:relative;z-index:1;text-align:center}}.dot{{width:11px;height:11px;margin:13px auto 6px;border-radius:50%;background:{accent};box-shadow:0 0 0 5px #f7f4ed}}.time b{{display:block;color:{deep};font-size:15px}}.time span{{display:block;margin-top:3px;color:#756352;font-size:11px;line-height:1.28;font-weight:700}}.stock-wrap{{border:2px solid #dfcabb;border-radius:10px;background:rgba(255,255,255,.74);padding:11px 13px 8px}}.stock-meta{{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:4px}}.stock-meta b{{display:block;color:{deep};font-size:15px}}.stock-meta span{{display:block;margin-top:3px;color:#8b7767;font-size:11px;font-weight:700}}.stock-return{{color:{accent};text-align:right;font-size:19px;font-weight:950;line-height:1.05;white-space:nowrap}}.stock-return small{{display:block;margin-top:4px;color:{gold};font-size:11px;font-weight:850}}.stock-chart{{display:block;width:100%;height:190px}}.stock-note{{margin-top:1px;color:#8b7767;text-align:center;font-size:10px;font-weight:700}}.culture-stack{{display:grid;grid-template-columns:1fr;gap:11px}}.culture-card{{display:grid;grid-template-columns:56px 1fr;gap:13px;min-height:0}}.culture-card h3{{margin:0;color:{deep};font-size:20px;line-height:1.2}}.rule{{margin-top:5px;color:#4c3b2e;font-size:13px;line-height:1.4;font-weight:680}}.case{{margin-top:5px;color:{accent};font-size:12px;line-height:1.38;font-weight:800}}.lesson{{margin-top:6px;padding:5px 8px;border-left:4px solid {gold};background:color-mix(in srgb,{gold} 10%,transparent);color:#465249;font-size:12px;line-height:1.33;font-weight:800}}.lens{{display:inline-block;margin-top:6px;padding:3px 7px;border-radius:5px;color:white;background:{accent};font-size:10px;font-weight:900}}footer{{width:100%;margin-top:20px;padding:11px 10px 16px;border-top:1px solid #e5d5c8;color:#9e8c7c;text-align:center;font-size:10px;font-weight:600;line-height:1.52}}.signature{{margin-top:6px;color:#9e8c7c;font-size:10px;font-weight:600}}
</style></head><body><main class='page'><h1 class='title'>{esc(title)}</h1><div class='subtitle'>{esc(subtitle)}</div>{body}{footer(lines)}</main></body></html>"""


def profile_page(c: dict) -> str:
    facts = [("公司全称", c["en"]), ("成立时间", c["founded"]), ("总部地址", c["hq"]), ("交易所及代码", c["ticker"]), ("CEO / 主要负责人", c["ceo"]), ("员工人数", c["employees"]), ("核心业务", c["core_business"]), ("当前市值", c["current_market_cap"])]
    fact_html = "".join(f"<div class='p'><span class='k'>{esc(k)}</span><span class='v'>{esc(v)}</span></div>" for k, v in facts)
    biz = []
    for i, (ico, title, text) in enumerate(c["businesses"]):
        wide = " wide" if len(c["businesses"]) == 3 and i == 2 else ""
        biz.append(f"<div class='card business-card{wide}'><div>{icon(ico,c['color'],36)}</div><div><h3>{esc(title)}</h3><p>{esc(text)}</p></div></div>")
    stat = "".join(f"<div class='status-card'><div class='status-icon'>{icon(ico,c['color'],28)}</div><div class='big'>{esc(big)}</div><div class='explain'>{esc(explain)}</div></div>" for ico,big,explain in c["status"])
    timeline = "".join(f"<div class='time'><div class='dot'></div><b>{esc(year)}</b><span>{esc(text)}</span></div>" for year,text in c["timeline"])
    history = load_stock_histories()[c["slug"]]
    stock_chart = stock_price_chart(c)
    logo_bg = c.get("logo_bg", "rgba(255,255,255,.78)")
    body = f"<div class='strap'>{esc(c['strap'])}</div><div class='logo-hero'><div class='logo-box' style='background:{esc(logo_bg)}'><img src='{data_uri(c['logo_path'])}'></div><div class='thesis'>{esc(c['thesis'])}<small>这张图只回答：它是谁、做什么、规模多大、处于什么行业位置。</small></div></div><section class='section'><h2>基本信息</h2><div class='profile'>{fact_html}</div></section><section class='section'><h2>业务范围</h2><div class='grid2'>{''.join(biz)}</div></section><section class='section'><h2>上市以来股价走势</h2>{stock_chart}</section><section class='section'><h2>行业地位与核心亮点</h2><div class='grid3'>{stat}</div></section><section class='section'><h2>关键历史节点</h2><div class='timeline'>{timeline}</div></section>"
    fx_footer = "原始行情为美元，无需换汇" if history["source_currency"] == "USD" else f"{history['source_currency']}/USD {history['fx_to_usd']:.4f}，汇率日2026年7月15日，整段固定汇率换算"
    lines = [f"档案与历史：{c['en']} 公司官网 / 最新年报，核查：2026年7月", f"业务与规模：公司官网与最新完整年度报告；人数为最近公开口径", f"行情数据：CompaniesMarketCap / StockAnalysis，查看：2026年7月；当前市值 {c['current_market_cap']}", f"股价走势：{history['listing_note']}；Yahoo Finance，{history['series_start']}至{history['series_end']}", f"股价口径：拆股调整收盘价，不含股息再投资；{fx_footer}", f"品牌资产：公司官方Logo，来源经官网或官方报告核对", "免责声明：本图仅供学习参考，不构成投资建议"]
    return document(c, f"{c['name']}公司档案", f"{c['en']} · {c['ticker']} · Company Profile", body, lines, profile_height(c))


def culture_page(c: dict) -> str:
    cards = []
    for item in c["culture"]:
        cards.append(f"<div class='card culture-card'><div>{icon(item['icon'],c['color'],45)}</div><div><h3>{esc(item['title'])}</h3><div class='rule'><b>做法：</b>{esc(item['practice'][3:])}</div><div class='case'><b>{esc(item['case'][:3])}</b>{esc(item['case'][3:])}</div><div class='lesson'>{esc(item['lesson'])}</div><span class='lens'>{esc(item['lens'])}</span></div></div>")
    strap = " × ".join(item["title"].split("：")[0][:11] for item in c["culture"])
    thesis = f"这家公司最值得观察的不是口号数量，而是它如何管理{c['employees'].replace('约','')}、如何让领导行为和员工体验形成可运行的机制。"
    logo_bg = c.get("logo_bg", "rgba(255,255,255,.78)")
    body = f"<div class='strap'>{esc(strap)}</div><div class='logo-hero'><div class='logo-box' style='background:{esc(logo_bg)}'><img src='{data_uri(c['logo_path'])}'></div><div class='thesis'>{esc(thesis)}<small>只写人与组织的真实做法，不把业务战略、产能或估值混入管理文化。</small></div></div><section class='section'><h2>{len(c['culture'])}个有辨识度的管理机制</h2><div class='culture-stack'>{''.join(cards)}</div></section>"
    source_names = "；".join(dict.fromkeys(re.sub(r"https?://(?:www\.)?([^/]+)/.*", r"\1", x["source"]) for x in c["culture"]))
    lines = [f"管理文化：{source_names} 官方Careers / 年报 / 行为准则，核查：2026年7月", "案例口径：仅采用公司公开机制、公开数字或公司官方案例；未为版式对称硬凑条目", "品牌资产：公司官方Logo，来源经官网或官方报告核对", "汇率口径：本页金额均为美元；本页如无金额则无需换汇", "免责声明：本图仅供学习参考，不构成投资建议"]
    height = 880 if len(c["culture"]) <= 2 else 1050
    return document(c, f"{c['name']}管理文化", f"{c['ticker']} · Management Culture · 公开机制与真实案例", body, lines, height)


def visible_text(source: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", source)).strip()


def render_html(source: str, html_path: Path, png_path: Path, height: int) -> None:
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(source, encoding="utf-8")
    text = visible_text(source)
    if "..." in text or "…" in text:
        raise ValueError(f"visible ellipsis: {html_path}")
    subprocess.run([str(CHROME), "--headless", "--hide-scrollbars", f"--screenshot={png_path}", f"--window-size=900,{height}", "--force-device-scale-factor=3", f"file://{html_path}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def packet(c: dict) -> dict:
    return {
        "company": c["name"], "rank": c["rank"], "generated": "2026-07-14",
        "company_profile": {k: c[k] for k in ("en", "founded", "hq", "ticker", "ceo", "employees", "position")},
        "businesses": c["businesses"], "industry_status": c["status"], "timeline": c["timeline"],
        "stock_history": load_stock_histories()[c["slug"]],
        "management_culture": c["culture"],
        "logo": {"path": c["logo_path"], "official_source_url": c["logo_source"], "sha256": hashlib.sha256(Path(c["logo_path"]).read_bytes()).hexdigest()},
        "sources": {"profile": c["profile_source"], "culture": [x["source"] for x in c["culture"]]},
        "currency": {"display": "USD", "note": "本次两页原则上不展示金额；出现的金额均为美元。"},
        "signature": "by 江明",
    }


def backup_existing(c: dict) -> None:
    out = OUTPUT_ROOT / c["folder"]
    backup = BACKUP_ROOT / c["folder"]
    backup.mkdir(parents=True, exist_ok=True)
    for pattern in (f"{c['prefix']}_经营分析.png", f"{c['prefix']}_公司档案.png", f"{c['prefix']}_管理文化.png"):
        src = out / pattern
        if src.exists() and not (backup / src.name).exists():
            shutil.copy2(src, backup / src.name)


def main() -> int:
    if LEGACY_RENDERER_DISABLED:
        raise RuntimeError(
            "旧两页生成器已禁用；请运行 render_post_chevron_standard_v2.py，"
            "四张图必须由同一研究底稿统一生成。"
        )
    global RENDER_COMPLETE
    for path in (HTML_ROOT, PACKET_ROOT, BACKUP_ROOT):
        path.mkdir(parents=True, exist_ok=True)
    manifest = ["# 可口可乐之后：公司档案与管理文化批量更新", "", "- 生成日期：2026-07-14", "- 仅替换公司档案与管理文化；经营之道、经营全景保持不动", "- 最终金融文字与图表：确定性 HTML/SVG 渲染", "- 邮件：未发送", ""]
    for c in COMPANIES:
        backup_existing(c)
        out = OUTPUT_ROOT / c["folder"]
        out.mkdir(parents=True, exist_ok=True)
        profile = profile_page(c)
        culture_html = culture_page(c)
        profile_png = out / f"{c['prefix']}_公司档案.png"
        culture_png = out / f"{c['prefix']}_管理文化.png"
        render_html(profile, HTML_ROOT / f"{c['rank']:02d}_{c['slug']}_profile.html", profile_png, profile_height(c))
        culture_height = 940 if len(c["culture"]) <= 2 else 1100
        render_html(culture_html, HTML_ROOT / f"{c['rank']:02d}_{c['slug']}_culture.html", culture_png, culture_height)
        old = out / f"{c['prefix']}_经营分析.png"
        if old.exists():
            old.unlink()
        p = packet(c)
        (PACKET_ROOT / f"{c['rank']:02d}_{c['slug']}.json").write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
        manifest.append(f"- #{c['rank']} {c['name']}：`{profile_png.name}`、`{culture_png.name}`")
    (REVIEW_ROOT / "manifest.md").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    (REVIEW_ROOT / ".complete").write_text(datetime.now().isoformat(timespec="seconds") + "\n", encoding="utf-8")
    RENDER_COMPLETE = True
    print(f"rendered {len(COMPANIES)} companies / {len(COMPANIES)*2} images")
    print(REVIEW_ROOT / "manifest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
