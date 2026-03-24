# 现代精确叫牌练习系统

基于《现代精确叫牌法》的桥牌叫牌练习工具，集成 redeal 发牌引擎和规则解析框架。

## 项目简介

本项目将权威的桥牌叫牌规则文档转化为可执行的练习系统，让牌手能够：

- 📚 学习现代精确叫牌法
- 🎮 通过随机发牌练习叫牌
- ✅ 验证叫牌决策是否正确
- 📊 统计分析叫牌路径

## 项目结构

```
BidMeWell/
├── README.md                 # 项目说明
├── USAGE.md                  # 使用说明
├── CHANGELOG.md              # 版本历史
├── LICENSE                   # MIT许可证
├── Makefile                  # 常用命令
├── requirements.txt          # Python依赖
├── setup.py                  # 安装脚本
│
├── src/                      # 源代码
│   ├── __init__.py
│   ├── precision_formulas.py # 点力计算模块
│   └── practice/             # 核心框架
│       ├── bridge_parser.py  # 输入解析
│       ├── robot_bidding.py  # 自动叫牌
│       ├── standard_formulas.py
│       ├── redeal/           # 发牌引擎
│       │   ├── redeal.py     # 核心 Hand/Deal 类
│       │   ├── dds.py        # 双明手求解
│       │   └── ...
│       └── xml_parsing/      # XML规则解析
│           ├── conditions.py # 条件判断
│           └── xml_parser.py # XML解析器
│
├── rules/                    # 规则文件
│   ├── modern_precision.xml  # 现代精确规则 (71条)
│   └── legacy/               # 原始文档
│       ├── 现代精确叫牌法规则库.xlsx
│       └── 现代精确叫牌法规则库.docx
│
├── scripts/                  # 脚本工具
│   ├── run_practice.py       # 启动练习（开叫练习）
│   ├── run_practice2.py      # 应叫练习
│   ├── test_single_hand.py   # 单牌测试
│   └── validate_rules.py     # 规则验证
│
├── tests/                    # 测试用例
│   └── test_precision.py     # 20个测试用例
│
└── docs/                     # 文档
    ├── 规则说明.md
    └── 开发指南.md
```

## 快速开始

### 环境要求

- Python 3.8+
- pip 包管理器

### 安装步骤

```bash
# 克隆项目
git clone <repository-url>
cd BidMeWell

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .
```

### 运行练习

```bash
# 交互模式 - 开叫练习
python scripts/run_practice.py

# 自动模式（程序自动叫牌）
python scripts/run_practice.py --auto --boards 10

# 应叫练习 - 练习同伴开叫后的应叫
python scripts/run_practice2.py

# 单牌测试 - 展示规则匹配过程
python scripts/test_single_hand.py

# 验证规则文件
python scripts/validate_rules.py
```

## 核心特性

### 1. 随机发牌

使用 redeal 发牌引擎，每次生成不同的牌局：

```
第 1 副牌
  持牌: ♠Q 3 ♥J A 8 7 ♦5 ♣T K J 5 3 2
  点力: 11 HCP, 牌型: 2-4-1-6
  开叫: 2C - 11-15 HCP, 6张以上梅花
```

### 2. 标准点力计算

采用 Milton Work 标准点力系统：

| 牌 | 点力 |
|----|------|
| A | 4点 |
| K | 3点 |
| Q | 2点 |
| J | 1点 |

### 3. 规则驱动

基于 XML 定义的叫牌规则，程序自动判断开叫是否正确：

```xml

<bid id="1c">
  <value>1c</value>
  <desc>16+ HCP强牌约定叫</desc>
  <evaluation><hcp><min>16</min></hcp></evaluation>
</bid>
```

支持精确条件检查：
- **点力范围**：HCP、支持点、控制点
- **张数检查**：花色张数、牌型分布
- **特定牌检查**：AKQ领头、坚固套、边花无A/K
- **止张检查**：是否有止张、无止张
- **分布检查**：单缺、双张、均型/非均型

### 4. 规则覆盖

| 分类 | 规则数 |
|------|--------|
| 开叫及应叫规则 | 87条 |
| 竞争叫牌规则 | 25条 |
| 满贯叫牌规则 | 10条 |
| **总计** | **122条** |

## 命令行参数

```
用法: python scripts/run_practice.py [选项]

选项:
  -r, --rules FILE      规则文件路径
  -a, --auto            自动模式
  -b, --boards N        练习副数
  -s, --seed SEED       随机种子
  -v, --verbose         详细信息
  -h, --help            帮助信息
```

## 数据来源

本项目的叫牌规则基于以下权威资料：

- **书名**：《现代精确叫牌法》
- **作者**：大卫·伯科维兹、布兰特·曼雷
- **译者**：杨静、于红英
- **出版社**：人民体育出版社
- **出版时间**：2002年2月
- **ISBN**：9787500926795

## 技术栈

| 组件 | 说明 |
|------|------|
| Python 3.8+ | 编程语言 |
| redeal | 发牌引擎 |
| xml.etree.ElementTree | XML解析 |
| Milton Work | 点力系统 |

## 项目状态

- [x] 项目结构搭建
- [x] redeal 发牌引擎集成
- [x] XML规则解析
- [x] 自动模式
- [x] 交互模式
- [x] 测试框架
- [x] 扩展规则 (122条完成)
- [x] 单牌测试脚本
- [ ] Web界面

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

## 致谢

- [practice_bidding](https://github.com/andrewimcclement/practice_bidding) - 叫牌练习框架参考
- [redeal](https://github.com/anntzer/redeal) - 桥牌发牌引擎
- 《现代精确叫牌法》- 规则来源

---

**版本历史**

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.3.0 | 2026-03-24 | 重命名项目为 BidMeWell，扩展规则至122条，添加单牌测试脚本 |
| v0.2.0 | 2026-03-24 | 集成发牌引擎和规则解析 |
| v0.1.0 | 2026-03-24 | 初始版本 |
