// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
# MechaMon UE5 代码骨架

本目录由 Python 生成器自动导出，可直接拷贝到 UE5 工程的 `Source/` 下作为 GAS 框架起点。

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

> 注意：骨架中的 `TODO` 为需要按项目需求填充的核心逻辑（克制倍率、状态检查、结算等）。
