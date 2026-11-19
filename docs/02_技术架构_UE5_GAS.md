# MECHA·MON 技术架构设计（UE5 + GAS）

> 引擎：Unreal Engine 5 · 框架：Gameplay Ability System (GAS) · 版本 0.1.0-Prototype

## 1. 为什么选择 GAS

Gameplay Ability System 天然契合回合制竞技游戏的需求：

- **统一能力模型**：技能、道具、状态均抽象为 Ability + Effect，规则一致
- **属性与效果解耦**：AttributeSet 管理数值，GameplayEffect 负责修改，便于平衡调整
- **标签驱动逻辑**：GameplayTag 描述状态与克制关系，避免布尔标志地狱
- **网络同步**：内置客户端预测与服务器权威校验，适合竞技对战
- **数据驱动**：技能配置可放在 DataAsset，策划可独立迭代

## 2. 核心架构分层

| 组件 | 职责 |
| --- | --- |
| AbilitySystemComponent (ASC) | 挂载于每台机甲，统一驱动技能、属性与状态 |
| MechaAttributeSet | Health / Energy / Attack / Defense / Speed / CritRate |
| UGameplayAbility | 32 个机甲技能，DataAsset 配置 + 冷却/消耗校验 |
| UGameplayEffect | 伤害、护盾、灼烧、冻结、增益等即时与持续效果 |
| FGameplayTag | Mecha.Type.* / Ability.* / Status.* 三层标签体系 |
| BattleManager (GameState) | 回合调度、先手计算、换人判定、胜负结算 |
| AbilityTask | PlayMontageAndWait / WaitForTarget / 动画与镜头表现 |
| GameplayCue | 命中特效、音效、屏幕震动等表现层通知 |

## 3. 类图（概念）

```text
AMechaCharacter (ACharacter)
  ├── UAbilitySystemComponent  ──→ 技能/效果/标签的统一入口
  ├── UMechaAttributeSet       ──→ Health / Energy / Attack / Defense / Speed
  └── UMechaAbilityBase        ──→ 继承自 UGameplayAbility
                                    ├── UFlameRamAbility
                                    ├── UMagmaShieldAbility
                                    └── ... (共 32 个)

ABattleManager (AGameStateBase)
  ├── 回合调度与先手计算
  ├── 换人判定（消耗能量）
  └── 胜负结算与回放记录
```

## 4. 标签体系（GameplayTag）

```text
Mecha.Type.Fire / Water / Electric / Leaf / Steel / Quantum / Shadow / Ice
Ability.Mecha.*        # 32 个技能标签
Status.Burning         # 灼烧（DoT）
Status.Frozen          # 冻结（跳过回合）
Status.Shielded        # 护盾
Status.Stunned         # 眩晕
Status.Overdrive       # 攻击提升
Event.Hit / Event.Switch / Event.Knockout
```

## 5. 伤害结算管线

```text
1. 技能激活 → CanActivateAbility() 校验能量/CD/控制状态
2. 构造 FGameplayEffectSpec → 设置 SetByCaller 威力系数
3. 应用 GameplayEffect → AttributeSet::PostGameplayEffectExecute()
4. 计算属性克制倍率（读取 Mecha.Type.* 标签）
5. 扣除生命 → 触发 GameplayCue 表现（特效/音效/震动）
6. 广播 Event.Hit → 战斗日志与 UI 更新
```

## 6. 网络架构

- **权威模型**：服务器全权判定伤害、命中与随机数（防作弊）
- **客户端预测**：技能释放即时播放动画，服务器回包后校正
- **随机数同步**：使用可复现的种子（战斗 ID + 回合数），支持回放校验
- **状态复制**：仅复制 ASC 的必要属性与标签，降低带宽

## 7. 目录结构（UE5 工程）

```text
Source/MechaMon/
├── Public/
│   ├── MechaCharacter.h        # 机甲角色基类
│   ├── MechaAttributeSet.h     # 属性集
│   ├── Abilities/MechaAbilityBase.h
│   ├── Effects/MechaEffects.h  # GameplayEffect 定义
│   ├── Battle/BattleManager.h  # 回合调度
│   └── Tags/MechaGameplayTags.h
└── Private/                   # 对应 .cpp 实现
```

## 8. 性能与扩展

- 首批 32 个技能，单场战斗最多 6 台机甲同时存在，性能压力可控
- GameplayCue 采用对象池，避免频繁创建特效
- DataAsset 热重载，支持策划在不重编译的情况下调整数值
- 预留部位破坏、天气场地等扩展点（通过额外标签实现）
