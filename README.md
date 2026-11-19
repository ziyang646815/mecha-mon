<div align="center">

# MECHA·MON

### 机甲兽竞技场 · 实时 1v1 硬核机甲格斗

[![UE5](https://img.shields.io/badge/Engine-Unreal%20Engine%205-0a1120?style=flat-square)](https://www.unrealengine.com/)
[![GAS](https://img.shields.io/badge/Framework-Gameplay%20Ability%20System-00e5ff?style=flat-square)](https://dev.epicgames.com/documentation/)
[![60Hz](https://img.shields.io/badge/Logic-60Hz%20Frame%20Data-7c3aed?style=flat-square)](#)
[![Version](https://img.shields.io/badge/Version-v1.0%20Vertical%20Slice-ff6b1a?style=flat-square)](#)
[![Platform](https://img.shields.io/badge/Platform-PC%20%7C%20Console-33e08b?style=flat-square)](#)

**机甲觉醒 · 帧级博弈 · 硬核格斗**

</div>

---

## 项目简介

**MECHA·MON（机甲兽竞技场）** 是一款以帧级操作为核心的实时 1v1 硬核机甲格斗产品。玩家以单机甲身份进入战场，在固定 60Hz 逻辑帧上通过起手、判定、收招的精确博弈，配合弹反、防御、霸体与取消路线击败对手。

项目采用 **Unreal Engine 5 + Gameplay Ability System** 作为核心技术栈，以数据驱动架构贯穿策划、工程与展示全流程。招式的起手/判定/收招封装为帧数据资产，判定与动画表现彻底解耦，目标是打造具备电竞深度与高保真表现力的机甲格斗产品。

| 项目要素 | 说明 |
|---|---|
| 游戏类型 | 实时 1v1 机甲格斗 / 操作竞技 |
| 核心玩法 | BO3 单挑 · 帧级判定 · 弹反博弈 · Ban/Pick · 天梯排位 |
| 逻辑帧率 | 固定 60Hz，判定与渲染插值解耦 |
| 目标平台 | PC（首发）/ 主机（后续） |
| 技术引擎 | Unreal Engine 5，C++ 主程 + 蓝图工具 |
| 能力框架 | Gameplay Ability System（GAS） |

---

## 键位操作说明

| 按键 | 动作 | 说明 |
|---|---|---|
| `A` / `D` | 左右移动 | 地面位移，调整攻防距离 |
| `J` | 轻击 | 起手最快，可取消接重击 |
| `K` | 重击 | 伤害高、后摇长，命中僵直明显 |
| `L` | 必杀 | 消耗 25 点能量，带霸体与长僵直 |
| `U` | 超必杀 | 消耗 100 点能量，完全霸体，一击决定胜负 |
| `S`（按住） | 防御 | 持续减伤并消耗防御槽，防御槽清空即破防 |
| `S`（瞬间） | 弹反 | 按下前 4 帧为弹反窗口，成功使对手陷入 36 帧硬直并获得 30 点能量 |
| `Space` | 推进跳跃 | 规避地面判定，可在取消窗口中使用 |
| `Shift` | 瞬时冲刺 | 快速拉近或拉开距离 |

---

## 内容一览

### 设计文档

| 文档 | 路径 | 说明 |
|---|---|---|
| 游戏设计文档（GDD） | `docs/01_游戏设计文档_GDD.md` | 产品定位、核心循环、招式帧数据、操作系统与差异化 |
| 技术架构 | `docs/02_技术架构_UE5_GAS.md` | GAS 分层、类图、标签体系、帧驱动判定管线与网络回滚 |
| 项目规划 | `docs/03_项目规划_路线图.md` | 四阶段里程碑、团队配置、风险对策与交付清单 |
| 竞技规则与数值 | `docs/04_竞技规则与数值.md` | 帧数据表、弹反/破防规则、连招递减、Counter Hit 与克制表 |
| **技术愿景（评审版）** | `docs/05_技术愿景与开发规划_评审版.md` | 完整技术路线、混合动画管线、预算分配与交付标准 |

### UE5 代码基座清单

| 核心类 | 路径 | 说明 |
|---|---|---|
| `AMechaCharacter` | `generated/ue5/Source/MechaMon/Public/MechaCharacter.h` | 机甲角色，挂载 ASC、属性集与格斗组件 |
| `UMechaAttributeSet` | `.../Public/MechaAttributeSet.h` | 生命 / 能量 / 防御槽 / 攻防速 / 霸体 |
| `UCombatAbility` | `.../Public/Abilities/CombatAbility.h` | 帧数据驱动招式，推进起手/判定/收招 |
| `UCombatFrameData` | `.../Public/Abilities/CombatFrameData.h` | 招式帧数据 DataAsset |
| `UHitboxComponent` / `UParryComponent` | `.../Public/Combat/` | 判定查询与弹反窗口 |
| `UMechaAnimInstance` | `.../Public/Animation/MechaAnimInstance.h` | Control Rig 混合动画 |
| `UHitstopSubsystem` / `UCombatReplaySubsystem` | `.../Public/Subsystems/` | 命中停顿与帧步进回放 |
| `ABattleManager` | `.../Public/Battle/BattleManager.h` | 1v1 BO3 对局流程与胜负结算 |

### 工程资产

| 资产 | 路径 | 说明 |
|---|---|---|
| 交互式产品演示 | `demo/index.html` | 实时操作格斗 / 帧数据监视器 / 机甲图鉴 / 技术架构 / 路线图 |
| 数据驱动构建系统 | `main.py` + `generators/` | 由统一数据源自动生成全部文档与代码 |

---

## 交互式产品演示

`demo/index.html` 是一个自包含的交互式产品演示，无需安装任何依赖，直接用浏览器打开即可体验：

- **实时操作格斗** —— 以键位驱动机甲对战，含起手/判定/收招、弹反、僵直、霸体、取消与 hitstop
- **帧数据监视器** —— 逐帧查看招式状态与判定窗口，量化复盘手感
- **机甲图鉴** —— 8 台机甲、32 个招式的帧数据与五维属性雷达图
- **技术架构与路线图** —— 可视化展示 GAS 分层与四阶段规划

> 演示由统一数据源驱动，与文档、代码共享同一套帧数据模型，确保三端一致。

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
├── generated/ue5/     # UE5 实时格斗代码基座
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
