# Investor Infographic Generator 投资人持仓信息图生成器

自动生成投资人/基金/公司的高质量持仓分析信息图。投资人主题通常输出 **3 张图**：1 张橙色长图 + 2 张手绘风格信息图；公司经营分析默认输出 **4 张图**：经营分析橙色长图、经营之道、经营全景、管理文化。

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Pillow](https://img.shields.io/badge/Pillow-10.0+-green) ![Chrome](https://img.shields.io/badge/Chrome-Headless-yellow)

## 效果预览

| 橙色长图 (Pillow) | 手绘图1 (HTML+SVG) | 手绘图2 (HTML+SVG) | 管理文化 (HTML+SVG) |
|:---:|:---:|:---:|:---:|
| 暖橙色系 · 4K · 2400px宽 | 经营之道/投资哲学 | 经营全景/持仓数据 | 组织文化/管理机制 |

## 已覆盖 44 个数据模块

### 知名投资人 (11位)
| 编号 | 投资人 | 基金/公司 | 数据文件 |
|------|--------|-----------|----------|
| 01 | 巴菲特 | 伯克希尔·哈撒韦 | `data_buffett.py` |
| 02 | 达利欧 | 桥水基金 | `data_bridgewater.py` |
| 03 | 木头姐 | ARK Invest | `data_cathie_wood.py` |
| 04 | 西蒙斯 | 文艺复兴科技 | `data_renaissance.py` |
| 05 | 格里芬 | 城堡投资 | `data_citadel.py` |
| 06 | 阿克曼 | 潘兴广场 | `data_pershing.py` |
| 07 | 索罗斯 | 索罗斯基金管理 | `data_soros.py` |
| 08 | 泰珀 | 阿帕卢萨管理 | `data_appaloosa.py` |
| 09 | 科尔曼 | 老虎全球 | `data_tiger_global.py` |
| 10 | 辛格 | 埃利奥特管理 | `data_elliott.py` |
| 11 | 李录 | 喜马拉雅资本 | `data_lilu.py` |

### 公司经营分析

覆盖全球大市值公司、重点中概/周期/半导体公司，以及用户指定公司。当前仓库包含：

- 全球市值前列公司：英伟达、谷歌、苹果、微软、亚马逊、台积电、博通、沙特阿美、Meta、特斯拉、沃尔玛、伯克希尔、三星、摩根大通、礼来、埃克森美孚、维萨、腾讯、SK海力士、阿斯麦。
- 21-30 扩展批次：腾讯、阿斯麦、AMD、甲骨文、万事达、好市多、英特尔、奈飞、卡特彼勒、美国银行。
- 其他补充公司：拼多多、茅台、雪佛龙、美光等。
- 前 30 公司刷新脚本：`generate_top30_refresh.py` 会补齐经营分析、经营之道、经营全景、管理文化，并额外生成前 30 管理文化对比图。

## 快速开始

### 环境要求
- Python 3.9+
- Pillow (`pip install Pillow`)
- Google Chrome（用于手绘图截图）
- macOS（字体依赖 STHeiti / Hiragino Sans GB）

### 安装
```bash
git clone https://github.com/jiangmingwu/investor-infographic.git
cd investor-infographic
pip install Pillow
```

### 生成橙色长图
```bash
# 基本用法
python3 investor_infographic.py data_buffett

# 指定输出路径
python3 investor_infographic.py data_buffett ~/Downloads/buffett_holdings.png

# 公司经营分析版
python3 company_infographic.py data_nvidia ~/Downloads/nvidia_analysis.png

# 批量刷新前 30 公司经营分析 + 管理文化对比
python3 generate_top30_refresh.py
```

### 生成手绘信息图
手绘图是 HTML+SVG 文件，通过 Chrome Headless 截图生成 4K PNG：
```bash
# 截图命令（4x缩放 = 3600×8400px）
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless \
  --screenshot=output.png \
  --window-size=900,2100 \
  --force-device-scale-factor=4 \
  "file:///path/to/sketch.html"
```

## 添加新的投资人/公司

### 第一步：创建数据文件
```bash
cp data/data_template.py data/data_yourname.py
```

### 第二步：填入数据
编辑 `data_yourname.py`，填入以下内容：
- `TITLE` / `SUBTITLE` / `UPDATE_DATE` — 标题信息
- `BASIC_INFO` — 人物/公司基本信息（键值对）
- `PORTFOLIO_SUMMARY` — 持仓/经营概览
- `TOP_HOLDINGS` — 前15大持仓表格（序号, 公司名, 代码, 占比, 市值, 持股数, 行业）
- `SECTOR_DISTRIBUTION` — 行业分布（行业名, 百分比）
- `RECENT_CHANGES` — 近期变动（操作, 标的, 说明, 颜色）
- `INVESTMENT_PHILOSOPHY` — 投资哲学/经营理念（标题, 描述）
- `KEY_METRICS` — 关键指标（指标名, 数值）
- `FAMOUS_QUOTES` — 经典语录

### 第三步：生成图片
```bash
python3 investor_infographic.py data_yourname ~/Downloads/yourname.png
```

### 第四步：创建手绘图
参考 `sketch_refs/` 下的 HTML 模板，创建对应的 `yourname_sketch1.html` 和 `yourname_sketch2.html`。

## 项目结构

```
investor-infographic/
├── README.md                      # 本文件
├── investor_infographic.py        # 橙色长图绘图引擎（投资人）
├── company_infographic.py         # 橙色长图绘图引擎（公司）
├── top30_enhancement_data.py      # 前30公司 ROI、2026 CapEx、管理文化资料
├── generate_top30_refresh.py      # 前30公司批量刷新脚本
├── data/                          # 数据文件
│   ├── data_template.py           # 空白数据模板
│   ├── data_buffett.py            # 巴菲特
│   ├── data_bridgewater.py        # 桥水
│   └── ...                        # 44个数据文件
├── sketch_refs/                   # 手绘HTML参考模板
│   ├── buffett_sketch1.html       # 巴菲特-投资之道
│   ├── buffett_sketch2.html       # 巴菲特-持仓全景
│   └── ...                        # 70个手绘模板
└── skills/
    └── investor-infographic/      # Codex 技能说明、引用文档和 GPT Image 2 辅助脚本
```

## 设计规范

### 橙色长图
| 项目 | 规格 |
|------|------|
| 引擎 | Pillow (PIL) |
| 配色 | 暖橙色系 `#E8883A` 主色 |
| 分辨率 | 4K（SCALE=3，宽度 2400px） |
| 字体 | STHeiti / Hiragino Sans GB |

### 手绘信息图
| 项目 | 规格 |
|------|------|
| 引擎 | HTML + inline SVG + Chrome Headless |
| 背景 | 浅米白 `#F7F4ED` + CSS网格线 |
| 标题字体 | Songti SC（宋体） |
| 正文字体 | Noto Sans SC |
| 插图 | 全部内联 SVG 手绘风（stroke-linecap: round） |
| 分辨率 | 4x缩放 → 3600×8400px+ |
| 尺寸 | 900px CSS宽度（竖版长图） |

### 设计原则
- **三色法则** — 每张图不超过 3 个主色
- **感受优先** — 做减法不做加法，信息密度适中
- **美元默认** — 所有主要金额默认转换为美元 / USD，并在脚注写明汇率口径
- **ROI + 2026 CapEx** — 公司经营分析/经营全景默认加入全年 ROI/ROIC 与 2026 资本开支，无法可靠取得时明确写 `未披露/不可比`
- **手绘分工** — `经营之道` 讲商业逻辑、护城河和飞轮；`经营全景` 讲财务、分部、ROI、2026 CapEx 和风险；`管理文化` 讲组织、招聘、绩效、待遇和管理机制
- **数据备注** — 底部分行列出经营数据来源、行情数据来源、汇率口径和免责声明
- **署名固定** — 所有最终图片底部单独居中显示 `by 江明`，样式与脚注一致
- **生成后复核** — 每批图片必须检查文件数、分辨率、字体、排版、脚注、币种、来源和图标语义
- **免责声明** — 底部标注"仅供学习参考，不构成投资建议"

## 数据来源规范

- 持仓数据：SEC EDGAR 13F、基金官网、WhaleWisdom、Nasdaq、Dataroma 等，并标明季度/日期。
- 经营数据：公司年报、10-K、20-F、年度业绩公告、Investor Relations 资料，并标明财年/发布日期。
- 行情数据：CompaniesMarketCap、StockAnalysis、Yahoo Finance、Nasdaq、Wind 等，并标明 `截至 YYYY-MM-DD`。
- 汇率口径：非美元公司必须写明换算来源或口径日期。

脚注推荐格式：

```text
经营数据：Alphabet FY2025 Form 10-K / FY2025 earnings release
行情数据：CompaniesMarketCap + StockAnalysis，截至 2026-04-29
汇率口径：USD/KRW、USD/TWD 等，截至 2026-04-29
免责声明：本图仅供学习参考，不构成投资建议
by 江明
```

## License
MIT License - 仅供学习研究使用，不构成投资建议。
