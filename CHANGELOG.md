# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-03-24

### Changed
- 项目重命名为 BidMeWell
- 更新所有文档和代码中的项目引用
- setup.py 包名改为 bidmewell
- 命令行入口改为 `bidmewell`

### Added
- 扩展 XML 规则文件，实现 122 条规则
- 新增竞争叫牌规则 (25条)
- 新增满贯叫牌规则 (10条)
- 新增转移示强应叫后的详细叫牌规则
- 扩展开叫及应叫规则 (87条)
- 新增单牌测试脚本 (test_single_hand.py)
- 新增应叫练习脚本 (run_practice2.py) - 练习同伴开叫后的应叫能力

## [0.2.0] - 2026-03-24

### Added
- ✅ 集成 redeal 发牌引擎
- ✅ 集成规则解析框架
- ✅ 实现真正的随机发牌功能
- ✅ 实现基于规则的叫牌判断
- ✅ 自动模式和交互模式均可工作

### Features
- 随机发牌，每次生成不同的牌局
- 根据XML规则自动判断开叫
- 显示点力分析和牌型分类
- 统计开叫/Pass比例

### Changed
- 重命名 `practice_bidding` 目录为 `practice`
- 更新所有导入路径

### Fixed
- 修复控制点计算错误
- 修复XML规则格式问题

### Rules
- 开叫规则 (10条)
- 应叫规则 (44条)
- 再叫规则 (17条)
- 总计：71条规则

## [0.1.0] - 2026-03-24

### Added
- 初始项目结构搭建
- README.md 和 USAGE.md 文档
- 点力计算模块 (precision_formulas.py)
- XML规则文件 (modern_precision.xml)
- 启动脚本 (run_practice.py)
- 规则验证脚本 (validate_rules.py)
- 单元测试框架 (20个测试用例)
- 开发指南和规则说明文档

### Technical
- Python 3.8+ 支持
- MIT 许可证
- 标准 Python 包结构
- XML 规则定义格式

## [Unreleased]

### Planned
- 交互模式完善
- 规则扩展到129条
- Web 界面
- SAYC 叫牌体系支持
