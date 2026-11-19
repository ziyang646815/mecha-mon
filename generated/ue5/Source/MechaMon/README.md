# MECHA·MON · UE5 实时格斗战斗系统代码基座

本目录由 MECHA·MON 数据驱动构建系统导出，面向 **实时 1v1 硬核机甲格斗**，
符合 UE5 / GAS 工程规范，可直接导入工程的 `Source/` 目录作为战斗系统的核心模块。

全部招式以固定 60Hz 逻辑帧描述，判定与动画表现解耦；核心接入点以 `[扩展点]` 标注。

## 核心类清单

| 类 | 文件 | 职责 |
|---|---|---|
| `AMechaCharacter` | `Public/MechaCharacter.h` | 机甲角色，挂载 ASC、属性集与格斗组件 |
| `UMechaAttributeSet` | `Public/MechaAttributeSet.h` | 生命 / 能量 / 防御槽 / 攻防速 / 霸体 |
| `UCombatAbility` | `Public/Abilities/CombatAbility.h` | 帧数据驱动招式，推进起手/判定/收招 |
| `UCombatFrameData` | `Public/Abilities/CombatFrameData.h` | 招式帧数据 DataAsset（32 个招式的配置模板） |
| `UHitboxComponent` | `Public/Combat/HitboxComponent.h` | hitbox / hurtbox 查询 |
| `UParryComponent` | `Public/Combat/ParryComponent.h` | 弹反窗口、成功硬直与能量奖励 |
| `UMechaAnimInstance` | `Public/Animation/MechaAnimInstance.h` | Control Rig 混合动画与二级运动 |
| `UHitstopSubsystem` | `Public/Subsystems/HitstopSubsystem.h` | 命中停顿调度 |
| `UCombatReplaySubsystem` | `Public/Subsystems/CombatReplaySubsystem.h` | 帧步进、输入回放与战斗日志 |
| `FMechaGameplayTags` | `Public/Tags/MechaGameplayTags.h` | 8 种属性 + 格斗状态/事件标签 |
| `ABattleManager` | `Public/Battle/BattleManager.h` | 1v1 BO3 回合流程与胜负结算 |

## 数据规模

- 8 台机甲 / 32 个招式（轻击 / 重击 / 必杀 / 超必杀）
- 4 类操作系统动作：防御、弹反、推进跳跃、瞬时冲刺
- 属性克制：8 × 8 关系表

## 接入步骤

1. 新建 UE5 C++ 工程，模块名设为 `MechaMon`。
2. 将本目录内容拷贝到 `Source/MechaMon/`（保留 `Public/` 与 `Private/` 结构）。
3. 在编辑器中创建 `UCombatFrameData` DataAsset，按 `config/game_data.py` 配置帧窗口与伤害。
4. 在 `DefaultGame.ini` 中注册 GameplayTag（标签名见 `Tags/MechaGameplayTags.cpp`）。
5. 为每台机甲创建继承 `UCombatAbility` 的招式蓝图，绑定帧数据与 GameplayEffect。
6. 在地图中放置 `ABattleManager`，配置 1v1 BO3 对局流程。

> 代码中以 `[扩展点]` 标注的位置为项目特定的战斗规则接入处（弹反判定、霸体抵消、
> 连招衰减、命中管线与回滚校验）。基座已完成模块划分、属性定义、帧数据资产、
> 标签体系与对局流程等通用能力。
