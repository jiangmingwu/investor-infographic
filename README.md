# Investor Infographic Generator 投资人持仓信息图生成器

自动生成投资人/基金/公司的高质量持仓分析信息图。每个主题输出 **3 张图**：1 张橙色长图 + 2 张手绘风格信息图。

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![Pillow](https://img.shields.io/badge/Pillow-10.0+-green) ![Chrome](https://img.shields.io/badge/Chrome-Headless-yellow)

## 效果预览

| 橙色长图 (Pillow) | 手绘图1 (HTML+SVG) | 手绘图2 (HTML+SVG) |
|:---:|:---:|:---:|
| 暖橙色系 · 4K · 2400px宽 | 经营之道/投资哲学 · 4800×3000px | 经营全景/持仓数据 · 4800×3000px |

## 已覆盖 34 个投资人/公司

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

### 全球市值 TOP20 公司 (23家)
| 编号 | 公司 | 数据文件 | 编号 | 公司 | 数据文件 |
|------|------|----------|------|------|----------|
| 01 | 英伟达 | `data_nvidia.py` | 13 | 三星 | `data_samsung.py` |
| 02 | 谷歌 | `data_alphabet.py` | 14 | 摩根大通 | `data_jpmorgan.py` |
| 03 | 苹果 | `data_apple.py` | 15 | 礼来 | `data_lilly.py` |
| 04 | 微软 | `data_microsoft.py` | 16 | 埃克森美孚 | `data_exxon.py` |
| 05 | 亚马逊 | `data_amazon.py` | 17 | 维萨 | `data_visa.py` |
| 06 | 台积电 | `data_tsmc.py` | 18 | 腾讯 | `data_tencent.py` |
| 07 | 博通 | `data_broadcom.py` | 19 | SK海力士 | `data_skhynix.py` |
| 08 | 沙特阿美 | `data_aramco.py` | 20 | 阿斯麦 | `data_asml.py` |
| 09 | Meta | `data_meta.py` | 21 | 茅台 | `data_moutai.py` |
| 10 | 特斯拉 | `data_tesla.py` | 22 | 拼多多 | `data_pdd.py` |
| 11 | 沃尔玛 | `data_walmart.py` | 23 | 伯克希尔 | `data_berkshire.py` |
| 12 | 伯克希尔 | `data_berkshire.py` | | | |

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
├── data/                          # 数据文件
│   ├── data_template.py           # 空白数据模板
│   ├── data_buffett.py            # 巴菲特
│   ├── data_bridgewater.py        # 桥水
│   └── ...                        # 34个数据文件
└── sketch_refs/                   # 手绘HTML参考模板
    ├── buffett_sketch1.html       # 巴菲特-投资之道
    ├── buffett_sketch2.html       # 巴菲特-持仓全景
    └── ...                        # 57个HTML模板
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
- **数据备注** — 所有数据标注脚注编号（¹²³），底部列出完整来源
- **免责声明** — 底部标注"仅供学习参考，不构成投资建议"

## 数据来源
- SEC EDGAR 13-F 文件（美股投资人持仓）
- 公司年报 10-K / 20-F
- Yahoo Finance / Bloomberg
- WhaleWisdom / Dataroma
- 各公司 Investor Relations 页面

## License
MIT License - 仅供学习研究使用，不构成投资建议。
