# 使用说明

本文档详细介绍如何使用现代精确叫牌练习系统。

## 目录

1. [安装指南](#安装指南)
2. [快速开始](#快速开始)
3. [命令行参数](#命令行参数)
4. [练习模式](#练习模式)
5. [规则说明](#规则说明)
6. [常见问题](#常见问题)

---

## 安装指南

### 系统要求

- **操作系统**：Windows / macOS / Linux
- **Python版本**：3.8 或更高版本
- **内存**：至少 512MB 可用内存
- **磁盘空间**：约 50MB

### 安装步骤

#### 方法一：使用 pip 安装（推荐）

```bash
# 1. 克隆项目
git clone <repository-url>
cd BidMeWell

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 安装项目（开发模式）
pip install -e .
```

#### 方法二：直接运行

```bash
# 1. 克隆项目
git clone <repository-url>
cd BidMeWell

# 2. 安装依赖
pip install -r requirements.txt

# 3. 直接运行
python scripts/run_practice.py
```

---

## 快速开始

### 第一次运行

```bash
# 启动练习程序
python scripts/run_practice.py
```

你将看到如下界面：

```
============================================================
        现代精确叫牌练习系统 v0.1.0
============================================================

数据来源：《现代精确叫牌法》
点力系统：Milton Work (A=4, K=3, Q=2, J=1)

------------------------------------------------------------
你坐在南家，第 1 副牌
局况：双无

你的持牌：
♠: A K 7 6
♥: K Q 8 3 2
♦: A 5 2
♣: J 7

点力计算：
- 高牌点(HCP): 15
- 黑桃: A(4) + K(3) = 7点
- 红心: K(3) + Q(2) = 5点
- 方块: A(4) = 4点
- 梅花: J(1) = 1点
- 牌型: 4-5-3-1 (不均型)

请选择你的开叫:
  1c  - 16+ HCP 强牌
  1d  - 11-15 HCP, 2+方块
  1h  - 11-15 HCP, 5+红心
  1s  - 11-15 HCP, 5+黑桃
  1n  - 13-15 HCP 均型
  2c  - 11-15 HCP, 6+梅花
  pass

你的叫牌 >
```

### 输入叫牌

输入叫品代码，例如：

```
你的叫牌 > 1h

✓ 正确！
你的叫牌：1♥ (11-15 HCP, 5张以上红心)
规则依据：MajorOpening - 高花开叫

------------------------------------------------------------
同伴(北家)应叫：1♠

请选择你的再叫:
  1n  - 12-14 HCP, 非低限
  2c  - 12+ HCP, 5+梅花
  2d  - 12+ HCP, 5+方块
  2h  - 6+红心
  2s  - 4张黑桃支持
  2n  - 15 HCP, 邀请

你的再叫 >
```

---

## 命令行参数

### run_practice.py 参数

```
用法: python scripts/run_practice.py [选项]

选项:
  -r, --rules FILE      指定规则文件 (默认: rules/modern_precision.xml)
  -a, --auto            自动模式，程序自动叫牌
  -b, --boards N        练习副数 (默认: 无限)
  -v, --verbose         显示详细信息
  -s, --seed SEED       随机种子，用于复现牌局
  -h, --help            显示帮助信息

示例:
  python scripts/run_practice.py                    # 交互模式
  python scripts/run_practice.py --auto --boards 10 # 自动模式，练习10副
  python scripts/run_practice.py --seed 42          # 固定随机种子
  python scripts/run_practice.py -r custom.xml      # 使用自定义规则
```

### validate_rules.py 参数

```
用法: python scripts/validate_rules.py [选项]

选项:
  -r, --rules FILE      指定规则文件
  -v, --verbose         显示详细信息
  -h, --help            显示帮助信息

示例:
  python scripts/validate_rules.py                  # 验证默认规则
  python scripts/validate_rules.py -r custom.xml    # 验证自定义规则
```

### run_practice2.py 参数

```
用法: python scripts/run_practice2.py [选项]

选项:
  -r, --rules FILE      指定规则文件 (默认: rules/modern_precision.xml)
  -a, --auto            自动模式
  -b, --boards N        练习副数 (默认: 无限)
  -s, --seed SEED       随机种子
  -h, --help            显示帮助信息

示例:
  python scripts/run_practice2.py                   # 交互模式练习应叫
  python scripts/run_practice2.py --auto --boards 5 # 自动模式练习5副
  python scripts/run_practice2.py --seed 42         # 固定随机种子

交互模式命令:
  quit/exit             退出程序
  partner               查看同伴持牌
  hint                  显示推荐应叫
  skip                  跳到下一副牌
```

---

## 练习模式

### 1. 交互模式（默认）

在交互模式下，你需要手动输入叫牌：

```
你的叫牌 > 1h
✓ 正确！1♥ - 11-15 HCP, 5张以上红心

同伴应叫：2♦

你的再叫 > 2h
✓ 正确！2♥ - 6张以上红心，低限
```

如果叫牌错误，系统会提示：

```
你的叫牌 > 1d

✗ 不正确！
你的叫牌：1♦ - 需要 11-15 HCP, 2张以上方块，无5张高花
但你有 5张红心，应该开叫 1♥

正确答案：1♥
```

### 2. 自动模式

自动模式下，程序会自动进行叫牌：

```bash
python scripts/run_practice.py --auto --boards 5

============================================================
        现代精确叫牌练习系统 - 自动模式
============================================================

第 1 副牌
南家持牌：♠AK76 ♥KQ832 ♦A52 ♣J7 (15 HCP)
叫牌进程：1♥-2♦-2♥-4♥
结果：4♥ 南家做庄

第 2 副牌
南家持牌：♠QJ874 ♥A3 ♦KQJ6 ♣A9 (14 HCP)
叫牌进程：1♠-2♣-2♠-3♠-4♠
结果：4♠ 南家做庄

...
统计：
- 总副数：5
- 局定约：3
- 部分定约：1
- Pass out：1
```

### 3. 单牌测试

单牌测试模式用于展示规则匹配过程，帮助理解为什么某个叫牌是正确的：

```bash
# 随机发一副牌，判断开叫
python scripts/test_single_hand.py

# 寻找可开叫的牌
python scripts/test_single_hand.py --find

# 显示详细的规则匹配过程
python scripts/test_single_hand.py --detail
```

输出示例：

```
============================================================
现代精确叫牌练习系统 - 单牌测试
============================================================

【步骤1】加载规则文件
  文件: rules/modern_precision.xml
  已加载 10 个开叫规则

【步骤2】随机发牌
  第 1 次发牌找到可开叫的牌

你的持牌：
----------------------------------------
  ♠: K A 7
  ♥: T Q J 6 3
  ♦: A 7 6 2
  ♣: 6

点力分析：
  高牌点(HCP): 14
  控制点: 4
  牌型: 3-5-4-1
  黑桃: 3张, 红心: 5张
  方块: 4张, 梅花: 1张

【步骤3】规则判断
----------------------------------------

检查 10 个开叫规则：

  ❌ 1C   - 16+ HCP 强牌约定叫
  ❌ 1D   - 11-15 HCP, 2张以上方块, 无5张高花
  ✅ 1H   - 11-15 HCP, 5张以上红心
  ❌ 1S   - 11-15 HCP, 5张以上黑桃
  ❌ 1N   - 13-15 HCP 均型牌
  ❌ 2C   - 11-15 HCP, 6张以上梅花
  ❌ 2D   - 特殊约定叫
  ❌ 2H   - 弱二红心, 5-10 HCP, 6张红心
  ❌ 2S   - 弱二黑桃, 5-10 HCP, 6张黑桃
  ❌ 2N   - 22-24 HCP 均型牌

----------------------------------------
【最终结论】
----------------------------------------

  开叫: 1H
  规则: 11-15 HCP, 5张以上红心

  匹配条件:
    - 高牌点: 14 HCP
    - 红心: 5 张
```

### 4. 应叫练习

使用 `run_practice2.py` 练习同伴开叫后的应叫：

```bash
# 交互模式 - 练习应叫
python scripts/run_practice2.py

# 自动模式
python scripts/run_practice2.py --auto --boards 10

# 固定随机种子
python scripts/run_practice2.py --seed 42
```

输出示例：

```
------------------------------------------------------------
第 1 副牌
------------------------------------------------------------

叫牌进程：
  北家(同伴): 1S - 11-15 HCP, 5张以上黑桃
  东家(对手): Pass

你的持牌（南家）：
  ♠: Q J 2
  ♥: J 6
  ♦: T 8 5 3 2
  ♣: 8 6 5

点力分析：
  高牌点(HCP): 4
  控制点: 0
  牌型: 3-2-5-3

请选择你的应叫:
  pass - 无法应叫

你的应叫 >
```

交互命令：
- `partner` - 查看同伴（北家）持牌
- `hint` - 显示推荐应叫
- `quit` / `exit` - 退出程序
- `skip` - 跳到下一副牌

---

## 规则说明

### 现代精确体系核心特点

| 特点 | 说明 |
|------|------|
| 1♣强开叫 | 16+ HCP，约定性开叫，与梅花张数无关 |
| 限制性开叫 | 除1♣外所有开叫均为11-15 HCP |
| 弱无将 | 1NT = 13-15 HCP 均型 |
| 转移示强 | 1♣后用转移叫显示5张以上套 |
| 二盖一逼局 | 2阶新花应叫逼叫到局 |

### 开叫一览表

| 开叫 | 点力 | 张数/牌型 | 说明 |
|------|------|----------|------|
| 1♣ | 16+ | 任意 | 强牌约定叫 |
| 1♦ | 11-15 | ♦≥2 | 限制性开叫 |
| 1♥ | 11-15 | ♥≥5 | 5张高花 |
| 1♠ | 11-15 | ♠≥5 | 5张高花 |
| 1NT | 13-15 | 均型 | 弱无将 |
| 2♣ | 11-15 | ♣≥6 | 限制性开叫 |
| 2♦ | 视约定 | 视约定 | 特殊约定 |
| 2♥/2♠ | 5-10 | ≥6 | 弱二高花 |
| 2NT | 22-24 | 均型 | 强无将 |

### 点力计算

#### 高牌点(HCP)

```
A = 4点
K = 3点
Q = 2点
J = 1点
全副牌共 40 点
```

#### 支持点

有将牌配合时计算：

```
支持点 = HCP + 牌型点
双张 = +1点
单张 = +2点
缺门 = +3点
```

#### 控制点

满贯试探时使用：

```
A = 2控制
K = 1控制
小满贯需联手 8-9 控制
```

---

## XML规则条件详解

本项目支持丰富的XML条件类型，可精确表达各种叫牌规则：

### 基本条件类型

#### 1. 点力条件
```xml

<evaluation>
  <hcp><min>10</min><max>13</max></hcp>
</evaluation>
```

#### 2. 张数条件
```xml

<shape type="diamonds"><min>7</min></shape>
```

#### 3. 牌型条件
```xml

<shape type="general">balanced</shape>  <!-- 均型牌 -->

<shape type="general">unbalanced</shape>  <!-- 非均型牌 -->
```

### 高级条件类型（新增）

#### 4. 顶部特定牌检查
检查花色前N张是否包含特定牌（如AKQ领头）：
```xml

<topCards suit="diamonds" positions="3" contains="AKQ"/>
```

#### 5. 边花条件
检查边花（非主套）是否包含/不包含特定牌：
```xml
<!-- 边花无A或K -->

<sideSuits exclude="diamonds" notContains="A,K"/>

<!-- 边花必须有A -->

<sideSuits exclude="clubs" contains="A"/>
```

#### 6. 止张检查
检查某花色是否有止张（A/K/Q为首）：
```xml

<stopper suit="hearts" has="true"/>   <!-- 有止张 -->

<stopper suit="spades" has="false"/>  <!-- 无止张 -->
```

#### 7. 分布检查
检查牌型分布（单缺、双张）：
```xml

<distribution type="singleton"/>  <!-- 有单张 -->

<distribution type="void"/>       <!-- 有缺门 -->

<distribution type="doubleton"/>  <!-- 有双张 -->
```

#### 8. 大牌分布
检查某花色的大牌数量和位置：
```xml
<!-- 前5张中有3张大牌（A/K/Q） -->
<honors suit="hearts" count="3" in="top5"/>

<!-- 某花色有至少2张大牌 -->
<honors suit="spades" count="2"/>
```

### 完整示例：3NT赌博性开叫

```xml

<bid id="3n-gambling">
  <value>3n</value>
  <desc>赌博性3NT，坚实低花长套（AKQ领头），边花无A或K，10-13 HCP</desc>
  <and>
    <evaluation><hcp><min>10</min><max>13</max></hcp></evaluation>
    <or>
      <and>
        <shape type="clubs"><min>7</min></shape>
        <topCards suit="clubs" positions="3" contains="AKQ"/>
        <sideSuits exclude="clubs" notContains="A,K"/>
      </and>
      <and>
        <shape type="diamonds"><min>7</min></shape>
        <topCards suit="diamonds" positions="3" contains="AKQ"/>
        <sideSuits exclude="diamonds" notContains="A,K"/>
      </and>
    </or>
  </and>
</bid>
```

---

## 常见问题

### Q1: 如何退出程序？

在叫牌提示时输入 `quit` 或 `exit`。

### Q2: 如何查看当前牌的详细信息？

输入 `desc` 或 `info` 查看牌型分析。

### Q3: 如何重新开始当前牌？

输入 `restart` 重新叫当前这副牌。

### Q4: 如何跳过当前牌？

输入 `skip` 跳到下一副牌。

### Q5: 叫牌规则可以修改吗？

可以。编辑 `rules/modern_precision.xml` 文件，按照 XML 格式修改规则。

### Q6: 如何添加自定义叫牌体系？

1. 创建新的 XML 规则文件
2. 运行时用 `-r` 参数指定：`python scripts/run_practice.py -r my_system.xml`

### Q7: 支持其他语言吗？

目前仅支持中文。如需其他语言，可修改 XML 文件中的描述文本。

---

## 高级用法

### 自定义规则文件

创建自定义规则文件 `my_system.xml`：

```xml
<?xml version="1.0" encoding="utf-8"?>
<openingBids hcp="standard" shape="standard">
  <!-- 1♣强开叫 -->
  <bid id="1c">
    <value>1c</value>
    <desc>16+ HCP强牌</desc>
    <evaluation>
      <hcp><min>16</min></hcp>
    </evaluation>
    
    <!-- 后续叫牌... -->
  </bid>
</openingBids>
```

### 批量测试

```bash
# 测试100副牌，统计正确率
python scripts/run_practice.py --auto --boards 100 --verbose > results.txt
```

---

## 技术支持

如遇问题，请：

1. 查看本文档
2. 提交 Issue 到 GitHub
3. 查看代码注释和开发文档

---

**更新日期**：2026-03-24
