#!/usr/bin/env python3
"""
数据模板 - 复制此文件并填入对应投资人数据
文件命名: data_xxx.py（如 data_cathie_wood.py, data_bridgewater.py）
运行: cd ~/templates && python3 investor_infographic.py data_xxx
"""

# 颜色常量（用于 RECENT_CHANGES 的标签颜色）
GREEN = "#5BA85B"
RED = "#D9534F"
ORANGE = "#D4793A"

DATA = {
    # ===== 必填 =====
    "TITLE": "XXX投资全解析",
    "SUBTITLE": "英文名 · 基金/公司名称",
    "UPDATE_DATE": "数据更新：2025Qx",

    # ===== 人物简介（键值对）=====
    "BASIC_INFO": {
        "全名": "",
        "出生": "",
        "公司": "",
        "身份": "",
        "净资产": "",
        "投资年限": "",
        "年化收益": "",
        "总部": "",
    },

    # ===== 持仓概览 =====
    "PORTFOLIO_SUMMARY": {
        "持仓总市值": "",
        "持仓数量": "",
        "前5大持仓占比": "",
        "最大单一持仓": "",
    },

    # ===== 持仓表格 =====
    # 格式: (序号, 公司名, 代码, 占比, 市值, 持股数, 行业)
    "HOLDINGS_LABEL": "前15大持仓",  # 可改为"前10大持仓"等
    "TOP_HOLDINGS": [
        ("1", "公司名", "CODE", "xx%", "$xx亿", "xx万股", "行业"),
    ],

    # ===== 行业分布 =====
    # 格式: (行业名, 百分比)
    "SECTOR_DISTRIBUTION": [
        ("科技", "50.0%"),
        ("医疗", "20.0%"),
    ],

    # ===== 近期变动 =====
    # 格式: (操作, 标的, 说明, 颜色)
    "CHANGES_LABEL": "近期持仓变动（2024-2025）",
    "RECENT_CHANGES": [
        ("新建仓", "公司名 (CODE)", "说明", GREEN),
        ("清仓", "公司名 (CODE)", "说明", RED),
    ],

    # ===== 投资哲学 =====
    # 格式: (标题, 描述)
    "INVESTMENT_PHILOSOPHY": [
        ("理念一", "详细描述"),
        ("理念二", "详细描述"),
    ],

    # ===== 关键指标 =====
    # 格式: (指标名, 数值)
    "KEY_METRICS": [
        ("年化收益率", "xx%"),
        ("管理规模", "$xx亿"),
    ],

    # ===== 经典语录 =====
    "FAMOUS_QUOTES": [
        "\"语录一\"",
        "\"语录二\"",
    ],

    # ===== 底部信息 =====
    "DATA_SOURCE": "公开信息",
    # 或自定义:
    # "FOOTER_LINES": ["第一行", "第二行"],

    # ===== 可选：额外章节 =====
    # "EXTRA_SECTIONS": [
    #     {"title": "章节标题", "icon": "📌", "data": {"key": "value"}},
    # ],
}
