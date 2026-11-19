<div align="center">

# MECHA·MON

### 机甲兽竞技场 · 回合制机甲竞技游戏

[![UE5](https://img.shields.io/badge/Engine-Unreal%20Engine%205-0a1120?style=flat-square)](https://www.unrealengine.com/)
[![GAS](https://img.shields.io/badge/Framework-Gameplay%20Ability%20System-00e5ff?style=flat-square)](https://dev.epicgames.com/documentation/)
[![Version](https://img.shields.io/badge/Version-v1.0%20Vertical%20Slice-ff6b1a?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-PC%20%7C%20Console-33e08b?style=flat-square)](#)

**机甲觉醒 · 策略竞技 · 属性压制**

</div>

---

## 项目简介

**MECHA·MON（机甲兽竞技场）** 是一款以机甲收集与回合制策略对战为核心的竞技游戏。玩家扮演机甲指挥官，组建三机甲作战小队，通过属性克制、技能组合与能量管理击败对手。

项目采用 **Unreal Engine 5 + Gameplay Ability System** 作为核心技术栈，以数据驱动架构贯穿策划、工程与演示全流程，目标是打造具备电竞深度与高保真表现力的机甲竞技产品。

| 项目要素 | 说明 |
|---|---|
| 游戏类型 | 回合制策略竞技 / 机甲收集养成 |
| 核心玩法 | 3v3 小队对战 · 属性克制 · Ban/Pick · 天梯排位 |
| 目标平台 | PC（首发）/ 主机（后续） |
| 技术引擎 | Unreal Engine 5，C++ 主程 + 蓝图工具 |
| 能力框架 | Gameplay Ability System（GAS） |

---

## 内容一览

### 设计文档

| 文档 | 路径 | 说明 |
|---|---|---|
| 游戏设计文档（GDD） | `docs/01_游戏设计文档_GDD.md` | 玩法循环、属性体系、机甲图鉴、养成与竞技模式 |
| 技术架构 | `docs/02_技术架构_UE5_GAS.md` | GAS 分层、标签体系、伤害管线、网络权威模型 |
| 项目规划 | `docs/03_项目规划_路线图.md` | 四阶段里程碑、团队配置、风险对策 |
| 竞技规则与数值 | `docs/04_竞技规则与数值.md` | 伤害公式、状态表、平衡性约束 |
| **技术愿景（评审版）** | `docs/05_技术愿景与开发规划_评审版.md` | 完整技术路线、混合动画管线、预算分配与交付标准 |

### 工程资产

| 资产 | 路径 | 说明 |
|---|---|---|
| UE5 战斗系统代码基座 | `generated/ue5/Source/MechaMon/` | ASC / AttributeSet / Ability / GameplayTags / BattleManager |
| 交互式产品演示 | `demo/index.html` | 战斗模拟 / 机甲图鉴 / 属性拓扑 / 技术架构 / 路线图 |
| 数据驱动构建系统 | `main.py` + `generators/` | 由统一数据源自动生成全部文档与代码 |

---

## 交互式产品演示

`demo/index.html` 是一个自包含的交互式演示，无需安装任何依赖，直接用浏览器打开即可体验：

- **实时战斗模拟** —— 按属性克制、能量消耗与伤害公式演算，支持 AI 对战与自动演示
- **机甲图鉴** —— 8 台机甲、32 个能力的完整数据，五维属性雷达图
- **属性克制拓扑** —— 8 属性动态关系网络，悬停高亮克制链路
- **技术架构与路线图** —— 可视化展示 GAS 分层与四阶段规划

> 演示由统一数据源驱动，与文档、代码共享同一套游戏数据，确保三端一致。

---

## 数据驱动架构

项目以 `config/game_data.py` 作为唯一数据源，文档、代码基座与交互演示均由生成器自动产出，实现"一处修改、三端同步"。

```bash
# 生成全部产物
python main.py

# 分项生成
python main.py docs    # 设计文档
python main.py ue5     # UE5 代码基座
python main.py demo    # 交互式演示
python main.py check   # 数据完整性校验
```

项目仅依赖 Python 标准库，无需安装第三方包。

---

## 目录结构

```
MECHA·MON/
├── config/            # 统一数据源与项目配置
├── generators/        # 文档 / 代码 / 演示生成器
├── templates/         # 演示模板
├── docs/              # 设计与技术文档
├── generated/ue5/     # UE5 战斗系统代码基座
├── demo/              # 交互式产品演示
└── main.py            # 构建入口
```

---

## 技术愿景

项目的完整形态以 **UE5 + GAS + Control Rig 混合动画管线 + 数据驱动帧窗口 + 自定义判定/回放调试 + Pixel Streaming 试玩** 为技术主线，聚焦可复现的弹反手感、高保真反馈与可扩展管线。

详见 [技术愿景与开发规划（评审版）](docs/05_技术愿景与开发规划_评审版.md)。

---

<div align="center">

**MECHA·MON 开发团队**

</div>
