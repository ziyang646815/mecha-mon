// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
# MECHA·MON · UE5 战斗系统代码基座

本目录由 MECHA·MON 数据驱动构建系统导出，符合 UE5 / GAS 工程规范，
可直接导入工程的 `Source/` 目录作为战斗系统的核心模块。

## 文件清单

| 文件 | 说明 |
|---|---|
| `MechaMon.Build.cs` | 模块依赖（Core / GameplayAbilities / GameplayTags / GameplayTasks） |
| `MechaCharacter.h/.cpp` | 机甲角色基类，挂载 ASC 与 AttributeSet |
| `MechaAttributeSet.h/.cpp` | 生命 / 能量 / 攻防速 / 暴击 / 护盾属性 |
| `MechaAbilityBase.h/.cpp` | 技能基类，能耗校验与 CommitAbility |
| `MechaGameplayTags.h/.cpp` | 8 种属性 + 状态 + 事件标签集中声明 |
| `BattleManager.h/.cpp` | 回合调度、先手计算、胜负判定 |

## 接入步骤

1. 新建 UE5 C++ 工程，模块名设为 `MechaMon`
2. 将本目录内容拷贝到 `Source/MechaMon/`
3. 在 `DefaultGame.ini` 中注册 GameplayTag（标签名见 `MechaGameplayTags.cpp`）
4. 创建 GameplayEffect DataAsset 配置伤害/护盾/状态
5. 为每台机甲创建继承 `UMechaAbilityBase` 的技能蓝图（共 32 个）

> 代码中以 `[扩展点]` 标注的位置为项目特定的战斗规则接入处（克制倍率、状态判定、结算管线），
> 基座已完成模块划分、属性定义、标签体系与回合调度等通用能力。
