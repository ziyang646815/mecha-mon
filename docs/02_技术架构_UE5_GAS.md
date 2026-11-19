# MECHA·MON 技术架构设计（UE5 + GAS）

> 引擎：Unreal Engine 5 · 框架：Gameplay Ability System (GAS) · 版本 v1.0 · Vertical Slice

## 1. 为什么选择 GAS

Gameplay Ability System 天然契合实时帧驱动格斗的需求：

- **统一能力模型**：招式、弹反、防御、跳跃、冲刺均抽象为 Ability，规则一致、可复用。
- **标签驱动状态**：HitStun / BlockStun / Armor 等以 GameplayTag 描述，避免布尔标志地狱，并且天然支持取消规则与 Counter Hit 判定。
- **属性与效果解耦**：AttributeSet 管理生命/能量/防御槽，GameplayEffect 负责修改，便于平衡调整。
- **帧数据可配置**：招式的起手/判定/收招封装为 FCombatFrameData DataAsset，策划可独立迭代手感。
- **网络同步**：内置客户端预测与服务器权威校验，配合输入回放与回滚，满足竞技对战低延迟要求。
- **表现与判定解耦**：命中产生 GameplayCue 与 hitstop，动画仅负责表现，不影响判定结果。

## 2. 核心架构分层

| 组件 | 职责 |
| --- | --- |
| AbilitySystemComponent (ASC) | 挂载于每台机甲，统一驱动招式、属性与状态 |
| MechaAttributeSet | Health / Meter / Guard / Attack / Defense / Speed / Armor |
| UCombatAbility | 32 个招式，帧数据驱动 + 能量消耗与取消规则校验 |
| FCombatFrameData (DataAsset) | startup / active / recovery / parryWindow / armor / cancelWindow / hitstop |
| UHitboxComponent | 自定义 hitbox/hurtbox 查询，判定与动画表现解耦 |
| UParryComponent | 弹反窗口判定、成功硬直反馈与能量奖励 |
| UHitstopSubsystem | 命中停顿帧调度，统一控制打击节奏 |
| UMechaAnimInstance | 动捕基础姿态 + Control Rig 机甲化 + 程序化二级运动 |
| CombatReplaySubsystem | 帧步进调试、输入回放与战斗日志（Perforce 构建流水线） |
| GameplayCue | 命中特效、分层音效、镜头震动等表现层通知 |

## 3. 类图（概念）

```text
AMechaCharacter (ACharacter)
  ├── UAbilitySystemComponent        ──→ 招式/效果/标签的统一入口
  ├── UMechaAttributeSet             ──→ Health / Meter / Guard / Attack / Defense / Speed
  ├── UCombatAbility                 ──→ 帧数据驱动招式（继承 UGameplayAbility）
  │     └── FCombatFrameData         ──→ Startup/Active/Recovery/ParryWindow/Armor/Cancel/Hitstop (DataAsset)
  ├── UHitboxComponent               ──→ 自定义 hitbox / hurtbox 查询
  ├── UParryComponent                ──→ 弹反窗口判定与硬直反馈
  └── UMechaAnimInstance             ──→ Control Rig 混合动画与程序化二级运动

UHitstopSubsystem (UGameInstanceSubsystem)
  └── 命中停顿帧调度，统一控制打击节奏

CombatReplaySubsystem (UGameInstanceSubsystem)
  ├── 帧步进调试 / 输入回放 / 战斗日志
  └── 服务器权威校验与回滚数据支撑
```

## 4. 标签体系（GameplayTag）

```text
Mecha.Type.Fire / Water / Electric / Leaf / Steel / Quantum / Shadow / Ice
Ability.Mecha.*        # 32 个招式标签
Ability.System.*       # Guard / Parry / BoostJump / BoostDash
Status.HitStun         # 命中硬直
Status.BlockStun       # 防御硬直
Status.Armor           # 霸体等级
Event.Parry            # 弹反成功
Event.CounterHit       # 反击命中（对手起手/后摇被击中）
Event.Hit / Event.Knockout
```

## 5. 命中判定管线（帧驱动）

```text
1. 起手帧  → UCombatAbility 激活，播放动捕+Control Rig 表现，此时无判定
2. 判定帧  → UHitboxComponent 每逻辑帧查询 hitbox/hurtbox 重叠
3. 命中查询 → 读取防守方标签：Status.Armor（霸体抵消）/ Event.Parry（4 帧窗口）
4. 防御判定 → 若按住防御且防御槽充足，进入 BlockStun 并消耗防御槽；清空则破防
5. hitstop  → UHitstopSubsystem 冻结双方指定帧，制造打击停顿
6. 僵直     → 写入 Status.HitStun / Status.BlockStun，防守方进入硬直
7. 取消     → 检查 CancelWindow 与取消路线（轻→重→必杀→超必杀），允许则接续下一招
8. 表现     → 广播 GameplayCue（特效/音效/镜头震动）与战斗日志
```

## 6. 网络架构

- **权威模型**：服务器以固定逻辑帧全权判定命中、弹反、僵直与伤害（防作弊）。
- **客户端预测**：本地输入立即播放动画与 hitstop，服务器回包后校正，保证操作跟手。
- **输入回放**：客户端按帧上传输入序列（含输入缓冲），服务器可逐帧重演校验结果。
- **Rollback 思路**：预测偏差时回退到分歧帧并重演，最大限度降低网络延迟对格斗手感的影响。
- **状态复制**：仅复制 ASC 必要属性与标签，GameplayCue 使用预测 Key 去重，降低带宽。

## 7. 目录结构（UE5 工程）

```text
Source/MechaMon/
├── Public/
│   ├── MechaCharacter.h            # 机甲角色基类（ASC + AttributeSet + 判定组件）
│   ├── MechaAttributeSet.h         # 属性集
│   ├── Abilities/CombatAbility.h   # 帧数据驱动招式基类
│   ├── Abilities/CombatFrameData.h # FCombatFrameData DataAsset
│   ├── Combat/HitboxComponent.h    # hitbox/hurtbox 查询
│   ├── Combat/ParryComponent.h     # 弹反窗口
│   ├── Animation/MechaAnimInstance.h # Control Rig 混合动画
│   ├── Subsystems/HitstopSubsystem.h # 命中停顿
│   ├── Subsystems/CombatReplaySubsystem.h # 帧步进/回放
│   └── Tags/MechaGameplayTags.h
└── Private/                       # 对应 .cpp 实现
```

## 8. 性能与扩展

- 首批 32 个招式，单场 1v1 仅两台机甲，判定查询与 hitstop 调度开销可控
- GameplayCue 采用对象池，避免命中高频触发时频繁创建特效
- FCombatFrameData 支持热重载，策划无需重编译即可调整帧窗口与伤害
- 判定与表现解耦，新增机甲复用帧数据模板与 Control Rig 管线，边际成本递减
