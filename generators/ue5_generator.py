# -*- coding: utf-8 -*-
"""UE5 GAS C++ 代码骨架生成器。

生成的不是可直接编译的完整游戏，而是一套**结构正确、命名规范、可直接导入
UE5 工程并继续填充**的 GAS 框架骨架，用于技术演示与快速起步。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.game_data import MECHAS, ELEMENTS, all_abilities_flat
from config.project_config import UE5_DIR


HEADER_NOTE = """// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
"""


def _write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER_NOTE + content, encoding="utf-8")


def generate_build_cs() -> str:
    return """using UnrealBuildTool;

public class MechaMon : ModuleRules
{
    public MechaMon(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core", "CoreUObject", "Engine", "InputCore",
            "GameplayAbilities", "GameplayTags", "GameplayTasks"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "UMG", "Slate", "SlateCore", "NetCore"
        });
    }
}
"""


def generate_attribute_set_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "AttributeSet.h"
#include "AbilitySystemComponent.h"
#include "MechaAttributeSet.generated.h"

#define ATTRIBUTE_ACCESSORS(ClassName, PropertyName) \\
    GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \\
    GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \\
    GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \\
    GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName)

/** 机甲属性集：所有可修改数值集中在此，便于平衡调整与网络复制 */
UCLASS()
class MECHAMON_API UMechaAttributeSet : public UAttributeSet
{
    GENERATED_BODY()

public:
    UMechaAttributeSet();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
    virtual void PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data) override;

    // ---- 生命 / 装甲 ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Vitals", ReplicatedUsing = OnRep_Health)
    FGameplayAttributeData Health;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Health)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Vitals", ReplicatedUsing = OnRep_MaxHealth)
    FGameplayAttributeData MaxHealth;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxHealth)

    // ---- 能量（技能消耗资源） ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Energy", ReplicatedUsing = OnRep_Energy)
    FGameplayAttributeData Energy;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Energy)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Energy")
    FGameplayAttributeData MaxEnergy;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxEnergy)

    // ---- 战斗属性 ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Attack;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Attack)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Defense;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Defense)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Speed;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Speed)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData CritRate;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, CritRate)

    // ---- 临时护盾 ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Shield;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Shield)

protected:
    UFUNCTION()
    void OnRep_Health(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_MaxHealth(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_Energy(const FGameplayAttributeData& OldValue);
};
"""


def generate_attribute_set_cpp() -> str:
    return """#include "MechaAttributeSet.h"
#include "Net/UnrealNetwork.h"
#include "GameplayEffectExtension.h"

UMechaAttributeSet::UMechaAttributeSet()
{
    InitHealth(100.f);
    InitMaxHealth(100.f);
    InitEnergy(100.f);
    InitMaxEnergy(120.f);
    InitAttack(80.f);
    InitDefense(70.f);
    InitSpeed(70.f);
    InitCritRate(0.05f);
    InitShield(0.f);
}

void UMechaAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Health, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, MaxHealth, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Energy, COND_None, REPNOTIFY_Always);
}

void UMechaAttributeSet::PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data)
{
    Super::PostGameplayEffectExecute(Data);

    // TODO: 接入属性克制倍率（读取 Mecha.Type.* 标签）与 GameplayCue 表现
    if (Data.EvaluatedData.Attribute == GetHealthAttribute())
    {
        SetHealth(FMath::Clamp(GetHealth(), 0.f, GetMaxHealth()));
    }
    else if (Data.EvaluatedData.Attribute == GetEnergyAttribute())
    {
        SetEnergy(FMath::Clamp(GetEnergy(), 0.f, GetMaxEnergy()));
    }
}

void UMechaAttributeSet::OnRep_Health(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Health, OldValue);
}

void UMechaAttributeSet::OnRep_MaxHealth(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, MaxHealth, OldValue);
}

void UMechaAttributeSet::OnRep_Energy(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Energy, OldValue);
}
"""


def generate_ability_base_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Abilities/GameplayAbility.h"
#include "MechaAbilityBase.generated.h"

/** 所有机甲技能的基类，封装能量消耗、冷却与共同表现 */
UCLASS(Abstract, Blueprintable)
class MECHAMON_API UMechaAbilityBase : public UGameplayAbility
{
    GENERATED_BODY()

public:
    UMechaAbilityBase();

    virtual bool CanActivateAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayTagContainer* SourceTags = nullptr,
        const FGameplayTagContainer* TargetTags = nullptr,
        FGameplayTagContainer* OptionalRelevantTags = nullptr) const override;

    virtual void ActivateAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        const FGameplayEventData* TriggerEventData) override;

    virtual void EndAbility(const FGameplayAbilitySpecHandle Handle,
        const FGameplayAbilityActorInfo* ActorInfo,
        const FGameplayAbilityActivationInfo ActivationInfo,
        bool bReplicateEndAbility, bool bWasCancelled) override;

protected:
    /** 技能威力，由 DataAsset 配置 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha|Ability")
    float BasePower = 0.f;

    /** 技能属性标签（Mecha.Type.*） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha|Ability")
    FGameplayTagContainer AbilityTags;

    /** 命中时应用的 GameplayEffect */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha|Ability")
    TSubclassOf<class UGameplayEffect> HitEffectClass;
};
"""


def generate_ability_base_cpp() -> str:
    return """#include "MechaAbilityBase.h"
#include "MechaAttributeSet.h"
#include "AbilitySystemComponent.h"
#include "Abilities/Tasks/AbilityTask_PlayMontageAndWait.h"

UMechaAbilityBase::UMechaAbilityBase()
{
    bReplicateWhenActivated = true;
    NetExecutionPolicy = EGameplayAbilityNetExecutionPolicy::ServerInitiated;
    InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

bool UMechaAbilityBase::CanActivateAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayTagContainer* SourceTags,
    const FGameplayTagContainer* TargetTags,
    FGameplayTagContainer* OptionalRelevantTags) const
{
    if (!Super::CanActivateAbility(Handle, ActorInfo, SourceTags, TargetTags, OptionalRelevantTags))
    {
        return false;
    }

    // TODO: 检查冻结/眩晕状态标签，被控制时禁止释放
    // const FGameplayTag StunnedTag = FGameplayTag::RequestGameplayTag("Status.Stunned");
    return true;
}

void UMechaAbilityBase::ActivateAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayAbilityActivationInfo ActivationInfo,
    const FGameplayEventData* TriggerEventData)
{
    if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
    {
        EndAbility(Handle, ActorInfo, ActivationInfo, true, true);
        return;
    }

    // TODO: 构造 EffectSpec → 应用属性克制倍率 → ApplyGameplayEffectToTarget
    // FGameplayEffectSpecHandle Spec = MakeOutgoingSpec(HitEffectClass, GetAbilityLevel(), MakeEffectContext());
    // Spec.Data.Get()->SetSetByCallerMagnitude(FGameplayTag::RequestGameplayTag("Data.Power"), BasePower);

    EndAbility(Handle, ActorInfo, ActivationInfo, true, false);
}

void UMechaAbilityBase::EndAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayAbilityActivationInfo ActivationInfo,
    bool bReplicateEndAbility, bool bWasCancelled)
{
    Super::EndAbility(Handle, ActorInfo, ActivationInfo, bReplicateEndAbility, bWasCancelled);
}
"""


def generate_character_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MechaCharacter.generated.h"

class UAbilitySystemComponent;
class UMechaAttributeSet;

/** 机甲角色基类：挂载 ASC 与属性集，是战斗中的基本单位 */
UCLASS()
class MECHAMON_API AMechaCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMechaCharacter();

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UAbilitySystemComponent* GetMechaASC() const { return AbilitySystemComponent; }

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UMechaAttributeSet* GetMechaAttributes() const { return AttributeSet; }

    /** 机甲编号，如 MF-01 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha")
    FName MechaId;

    /** 属性标签，如 Mecha.Type.Fire */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha")
    struct FGameplayTag MechaTypeTag;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mecha")
    TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mecha")
    TObjectPtr<UMechaAttributeSet> AttributeSet;

    /** 初始技能列表（DataAsset 驱动） */
    UPROPERTY(EditDefaultsOnly, Category = "Mecha")
    TArray<TSubclassOf<class UMechaAbilityBase>> StartingAbilities;
};
"""


def generate_character_cpp() -> str:
    return """#include "MechaCharacter.h"
#include "MechaAttributeSet.h"
#include "MechaAbilityBase.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"

AMechaCharacter::AMechaCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
    AbilitySystemComponent->SetIsReplicated(true);
    AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);

    AttributeSet = CreateDefaultSubobject<UMechaAttributeSet>(TEXT("AttributeSet"));
}

// 在 BeginPlay 或 PossessedBy 中授予初始技能：
// for (TSubclassOf<UMechaAbilityBase> Ability : StartingAbilities)
// {
//     AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(Ability, 1, INDEX_NONE, this));
// }
// AbilitySystemComponent->InitAbilityActorInfo(this, this);
"""


def generate_tags_h() -> str:
    elements = "\n".join(
        f'    // {e.name_cn}\n    FGameplayTag Type_{e.key};' for e in ELEMENTS
    )
    return f"""#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "MechaGameplayTags.generated.h"

/** 集中声明项目中使用的 GameplayTag，避免字符串硬编码 */
USTRUCT(BlueprintType)
struct MECHAMON_API FMechaGameplayTags
{{
    GENERATED_BODY()

    static const FMechaGameplayTags& Get() {{ return Instance; }}

    // ---- 机甲属性 ----
{elements}

    // ---- 状态 ----
    FGameplayTag Status_Burning;
    FGameplayTag Status_Frozen;
    FGameplayTag Status_Shielded;
    FGameplayTag Status_Stunned;
    FGameplayTag Status_Overdrive;
    FGameplayTag Status_Slowed;

    // ---- 事件 ----
    FGameplayTag Event_Hit;
    FGameplayTag Event_Switch;
    FGameplayTag Event_Knockout;

    // ---- 数值 SetByCaller ----
    FGameplayTag Data_Power;

private:
    static FMechaGameplayTags Instance;
    FMechaGameplayTags();
}};
"""


def generate_tags_cpp() -> str:
    element_inits = "\n".join(
        f'    Type_{e.key} = FGameplayTag::RequestGameplayTag(FName("{e.tag}"));' for e in ELEMENTS
    )
    return f"""#include "MechaGameplayTags.h"

FMechaGameplayTags FMechaGameplayTags::Instance;

FMechaGameplayTags::FMechaGameplayTags()
{{
{element_inits}

    Status_Burning   = FGameplayTag::RequestGameplayTag(FName("Status.Burning"));
    Status_Frozen    = FGameplayTag::RequestGameplayTag(FName("Status.Frozen"));
    Status_Shielded  = FGameplayTag::RequestGameplayTag(FName("Status.Shielded"));
    Status_Stunned   = FGameplayTag::RequestGameplayTag(FName("Status.Stunned"));
    Status_Overdrive = FGameplayTag::RequestGameplayTag(FName("Status.Overdrive"));
    Status_Slowed    = FGameplayTag::RequestGameplayTag(FName("Status.Slowed"));

    Event_Hit      = FGameplayTag::RequestGameplayTag(FName("Event.Hit"));
    Event_Switch   = FGameplayTag::RequestGameplayTag(FName("Event.Switch"));
    Event_Knockout = FGameplayTag::RequestGameplayTag(FName("Event.Knockout"));

    Data_Power = FGameplayTag::RequestGameplayTag(FName("Data.Power"));
}}
"""


def generate_battle_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameStateBase.h"
#include "BattleManager.generated.h"

class AMechaCharacter;

/** 回合调度器：负责先手计算、行动顺序、换人与胜负判定 */
UCLASS()
class MECHAMON_API ABattleManager : public AGameStateBase
{
    GENERATED_BODY()

public:
    ABattleManager();

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void StartBattle(const TArray<AMechaCharacter*>& PlayerTeam, const TArray<AMechaCharacter*>& EnemyTeam);

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void EndTurn();

    UFUNCTION(BlueprintPure, Category = "Battle")
    int32 GetCurrentTurn() const { return CurrentTurn; }

    /** 服务器使用可复现种子保证战斗回放可校验 */
    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 RandomSeed;

private:
    UPROPERTY()
    TArray<TObjectPtr<AMechaCharacter>> PlayerTeam;

    UPROPERTY()
    TArray<TObjectPtr<AMechaCharacter>> EnemyTeam;

    UPROPERTY()
    TArray<TObjectPtr<AMechaCharacter>> TurnOrder;

    int32 CurrentTurn = 0;
    int32 CurrentActorIndex = 0;

    void ComputeTurnOrder();
    void CheckBattleEnd();
};
"""


def generate_battle_cpp() -> str:
    return """#include "BattleManager.h"
#include "MechaCharacter.h"
#include "MechaAttributeSet.h"
#include "Net/UnrealNetwork.h"

ABattleManager::ABattleManager()
{
    bReplicates = true;
}

void ABattleManager::StartBattle(const TArray<AMechaCharacter*>& InPlayerTeam,
                                 const TArray<AMechaCharacter*>& InEnemyTeam)
{
    PlayerTeam = InPlayerTeam;
    EnemyTeam = InEnemyTeam;
    CurrentTurn = 1;
    CurrentActorIndex = 0;
    ComputeTurnOrder();
    // TODO: 广播战斗开始事件，驱动 UI
}

void ABattleManager::ComputeTurnOrder()
{
    TurnOrder.Reset();
    TurnOrder.Append(PlayerTeam);
    TurnOrder.Append(EnemyTeam);

    // 按速度属性降序排列
    TurnOrder.Sort([](const AMechaCharacter& A, const AMechaCharacter& B)
    {
        return A.GetMechaAttributes()->GetSpeed() > B.GetMechaAttributes()->GetSpeed();
    });
}

void ABattleManager::EndTurn()
{
    CurrentActorIndex++;
    if (CurrentActorIndex >= TurnOrder.Num())
    {
        CurrentActorIndex = 0;
        CurrentTurn++;
        // TODO: 回合结束回复 12 点能量、结算 DoT、检查回合上限
    }
    CheckBattleEnd();
}

void ABattleManager::CheckBattleEnd()
{
    // TODO: 任一方全部生命归零则结算胜负
}

void ABattleManager::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(ABattleManager, RandomSeed);
}
"""


def generate_readme() -> str:
    ability_count = len(all_abilities_flat())
    return f"""# MechaMon UE5 代码骨架

本目录由 Python 生成器自动导出，可直接拷贝到 UE5 工程的 `Source/` 下作为 GAS 框架起点。

## 文件清单

| 文件 | 说明 |
|---|---|
| `MechaMon.Build.cs` | 模块依赖（Core / GameplayAbilities / GameplayTags / GameplayTasks） |
| `MechaCharacter.h/.cpp` | 机甲角色基类，挂载 ASC 与 AttributeSet |
| `MechaAttributeSet.h/.cpp` | 生命 / 能量 / 攻防速 / 暴击 / 护盾属性 |
| `MechaAbilityBase.h/.cpp` | 技能基类，能耗校验与 CommitAbility |
| `MechaGameplayTags.h/.cpp` | {len(ELEMENTS)} 种属性 + 状态 + 事件标签集中声明 |
| `BattleManager.h/.cpp` | 回合调度、先手计算、胜负判定 |

## 接入步骤

1. 新建 UE5 C++ 工程，模块名设为 `MechaMon`
2. 将本目录内容拷贝到 `Source/MechaMon/`
3. 在 `DefaultGame.ini` 中注册 GameplayTag（标签名见 `MechaGameplayTags.cpp`）
4. 创建 GameplayEffect DataAsset 配置伤害/护盾/状态
5. 为每台机甲创建继承 `UMechaAbilityBase` 的技能蓝图（共 {ability_count} 个）

> 注意：骨架中的 `TODO` 为需要按项目需求填充的核心逻辑（克制倍率、状态检查、结算等）。
"""


def generate_all():
    files = {
        "MechaMon.Build.cs": generate_build_cs(),
        "Public/MechaAttributeSet.h": generate_attribute_set_h(),
        "Private/MechaAttributeSet.cpp": generate_attribute_set_cpp(),
        "Public/Abilities/MechaAbilityBase.h": generate_ability_base_h(),
        "Private/Abilities/MechaAbilityBase.cpp": generate_ability_base_cpp(),
        "Public/MechaCharacter.h": generate_character_h(),
        "Private/MechaCharacter.cpp": generate_character_cpp(),
        "Public/Tags/MechaGameplayTags.h": generate_tags_h(),
        "Private/Tags/MechaGameplayTags.cpp": generate_tags_cpp(),
        "Public/Battle/BattleManager.h": generate_battle_h(),
        "Private/Battle/BattleManager.cpp": generate_battle_cpp(),
        "README.md": generate_readme(),
    }
    for rel, content in files.items():
        _write(UE5_DIR / rel, content)
    return list(files.keys())
