# -*- coding: utf-8 -*-
"""UE5 GAS 实时格斗 C++ 生产级代码基座生成器。

输出一套结构完整、命名规范、符合 GAS 工程标准的 C++ 代码基座：
帧数据驱动招式、hitbox/hurtbox 判定、弹反窗口、霸体、命中停顿、
Control Rig 混合动画与战斗回放调试。核心接入点以 [扩展点] 标注。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.game_data import MECHAS, ELEMENTS, all_moves_flat
from config.game_data import BATTLE_RULES
from config.project_config import UE5_DIR


HEADER_NOTE = """// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
"""


def _write(path: Path, content: str, header: bool = True):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((HEADER_NOTE if header else "") + content, encoding="utf-8")


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
            "GameplayAbilities", "GameplayTags", "GameplayTasks",
            "AnimGraphRuntime"
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

/** 机甲属性集：生命/能量/防御槽与战斗数值集中管理，便于平衡调整与网络复制 */
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

    // ---- 能量（必杀/超必杀消耗资源） ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Meter", ReplicatedUsing = OnRep_Meter)
    FGameplayAttributeData Meter;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Meter)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Meter")
    FGameplayAttributeData MaxMeter;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxMeter)

    // ---- 防御槽（清空即破防） ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Guard", ReplicatedUsing = OnRep_Guard)
    FGameplayAttributeData Guard;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Guard)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Guard")
    FGameplayAttributeData MaxGuard;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxGuard)

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

    /** 霸体等级：0 无 / 1 抗轻击 / 2 完全霸体 */
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Armor;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Armor)

protected:
    UFUNCTION()
    void OnRep_Health(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_MaxHealth(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_Meter(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_Guard(const FGameplayAttributeData& OldValue);
};
"""


def generate_attribute_set_cpp() -> str:
    return """#include "MechaAttributeSet.h"
#include "Net/UnrealNetwork.h"
#include "GameplayEffectExtension.h"

UMechaAttributeSet::UMechaAttributeSet()
{
    // 与 config/game_data.py BATTLE_RULES 保持一致
    InitHealth(1000.f);
    InitMaxHealth(1000.f);
    InitMeter(0.f);
    InitMaxMeter(100.f);
    InitGuard(100.f);
    InitMaxGuard(100.f);
    InitAttack(80.f);
    InitDefense(70.f);
    InitSpeed(70.f);
    InitArmor(0.f);
}

void UMechaAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Health, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, MaxHealth, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Meter, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Guard, COND_None, REPNOTIFY_Always);
}

void UMechaAttributeSet::PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data)
{
    Super::PostGameplayEffectExecute(Data);

    // [扩展点] 接入属性克制倍率、连招衰减与 Counter Hit 修正
    if (Data.EvaluatedData.Attribute == GetHealthAttribute())
    {
        SetHealth(FMath::Clamp(GetHealth(), 0.f, GetMaxHealth()));
    }
    else if (Data.EvaluatedData.Attribute == GetMeterAttribute())
    {
        SetMeter(FMath::Clamp(GetMeter(), 0.f, GetMaxMeter()));
    }
    else if (Data.EvaluatedData.Attribute == GetGuardAttribute())
    {
        // [扩展点] 防御槽清空时写入破防状态并触发长硬直
        SetGuard(FMath::Clamp(GetGuard(), 0.f, GetMaxGuard()));
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

void UMechaAttributeSet::OnRep_Meter(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Meter, OldValue);
}

void UMechaAttributeSet::OnRep_Guard(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Guard, OldValue);
}
"""


def generate_frame_data_h() -> str:
    example = all_moves_flat()[0]
    example_note = (
        f"// 示例：{example.name_en} 起手 {example.startup} / 判定 {example.active} / "
        f"收招 {example.recovery} / 伤害 {example.damage}（源自 config/game_data.py）"
    )
    return """#pragma once

#include "CoreMinimal.h"
#include "DataAsset.h"
#include "GameplayTagContainer.h"
#include "CombatFrameData.generated.h"

/** 招式帧数据：判定规则与动画表现解耦，策划在编辑器中即可调校手感 */
UCLASS(BlueprintType)
class MECHAMON_API UCombatFrameData : public UDataAsset
{
    GENERATED_BODY()

public:
    // __EXAMPLE_NOTE__

    /** 起手帧：无 hitbox 判定，可被弹反 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 StartupFrames = 4;

    /** 判定帧：hitbox 有效窗口 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 ActiveFrames = 3;

    /** 收招帧：后摇，此阶段被命中触发 Counter Hit */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 RecoveryFrames = 8;

    /** 弹反有效帧（仅系统弹反招式使用） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 ParryWindow = 0;

    /** 霸体等级：0 无 / 1 抗轻击 / 2 完全霸体 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 ArmorLevel = 0;

    /** 取消窗口：从判定结束到收招结束的可取消帧数 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 CancelWindow = 0;

    /** 可取消到的招式类别（轻击 / 重击 / 必杀 / 超必杀） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    FGameplayTagContainer CancelRoutes;

    /** 命中停顿帧 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 HitstopFrames = 4;

    /** 基础伤害与硬直 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 Damage = 0;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 HitstunFrames = 14;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 BlockstunFrames = 8;

    /** 能量消耗与收益 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Meter")
    int32 MeterCost = 0;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Meter")
    int32 MeterGain = 0;

    /** 有效距离与击退 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    float Reach = 60.f;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    float Knockback = 0.f;

    /** 招式标签（Ability.Mecha.*） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Identity")
    FGameplayTag AbilityTag;

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetTotalFrames() const { return StartupFrames + ActiveFrames + RecoveryFrames; }

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetActiveStartFrame() const { return StartupFrames; }

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetRecoveryStartFrame() const { return StartupFrames + ActiveFrames; }
};
""".replace("__EXAMPLE_NOTE__", example_note)


def generate_frame_data_cpp() -> str:
    return """#include "Abilities/CombatFrameData.h"

// 帧数据为纯配置资产，所有行为由 UCombatAbility 与判定组件驱动。
// [扩展点] 在此接入 DataAsset 校验：起手/判定/收招不得为负，取消路线标签需已注册。
"""


def generate_combat_ability_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Abilities/GameplayAbility.h"
#include "CombatAbility.generated.h"

class UCombatFrameData;
class UHitboxComponent;
class AActor;

/** 帧数据驱动招式：以固定逻辑帧推进起手/判定/收招，管理命中、取消与能量 */
UCLASS(Abstract, Blueprintable)
class MECHAMON_API UCombatAbility : public UGameplayAbility
{
    GENERATED_BODY()

public:
    UCombatAbility();

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

    /** 每个逻辑帧由战斗调度推进一次 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Frames")
    void AdvanceFrame();

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    const UCombatFrameData* GetFrameData() const { return FrameData; }

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetCurrentFrame() const { return CurrentFrame; }

protected:
    /** 帧数据资产（DataAsset 驱动） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    TObjectPtr<const UCombatFrameData> FrameData;

    /** 招式身份标签 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Identity")
    FGameplayTag AbilityTag;

    /** 命中时应用的 GameplayEffect */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    TSubclassOf<class UGameplayEffect> HitEffectClass;

    int32 CurrentFrame = 0;
    bool bHitboxEnabled = false;

    void OnActiveFramesBegin();
    void OnActiveFramesEnd();
    void ResolveHit(AActor* Target);
    bool CanCancelInto(const FGameplayTag& NextAbilityTag) const;
};
"""


def generate_combat_ability_cpp() -> str:
    return """#include "Abilities/CombatAbility.h"
#include "Abilities/CombatFrameData.h"
#include "Combat/HitboxComponent.h"
#include "MechaAttributeSet.h"
#include "AbilitySystemComponent.h"
#include "Tags/MechaGameplayTags.h"

UCombatAbility::UCombatAbility()
{
    bReplicateWhenActivated = true;
    // 客户端预测 + 服务器权威校验，配合输入回放支撑回滚
    NetExecutionPolicy = EGameplayAbilityNetExecutionPolicy::Predictable;
    InstancingPolicy = EGameplayAbilityInstancingPolicy::InstancedPerActor;
}

bool UCombatAbility::CanActivateAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayTagContainer* SourceTags,
    const FGameplayTagContainer* TargetTags,
    FGameplayTagContainer* OptionalRelevantTags) const
{
    if (!Super::CanActivateAbility(Handle, ActorInfo, SourceTags, TargetTags, OptionalRelevantTags))
    {
        return false;
    }

    const UAbilitySystemComponent* ASC = ActorInfo ? ActorInfo->AbilitySystemComponent.Get() : nullptr;
    if (!ASC || !FrameData)
    {
        return false;
    }

    // 命中/防御硬直期间禁止起手
    const FMechaGameplayTags& Tags = FMechaGameplayTags::Get();
    if (ASC->HasMatchingGameplayTag(Tags.Status_HitStun) ||
        ASC->HasMatchingGameplayTag(Tags.Status_BlockStun))
    {
        return false;
    }

    // [扩展点] 校验能量消耗、取消窗口与霸体状态
    return true;
}

void UCombatAbility::ActivateAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayAbilityActivationInfo ActivationInfo,
    const FGameplayEventData* TriggerEventData)
{
    if (!CommitAbility(Handle, ActorInfo, ActivationInfo))
    {
        EndAbility(Handle, ActorInfo, ActivationInfo, true, true);
        return;
    }

    CurrentFrame = 0;
    bHitboxEnabled = false;

    // [扩展点] 通知 UMechaAnimInstance 播放起手表现，并注册到逻辑帧调度
}

void UCombatAbility::AdvanceFrame()
{
    if (!FrameData)
    {
        return;
    }

    ++CurrentFrame;
    const int32 ActiveStart = FrameData->GetActiveStartFrame();
    const int32 RecoveryStart = FrameData->GetRecoveryStartFrame();

    if (!bHitboxEnabled && CurrentFrame >= ActiveStart && CurrentFrame < RecoveryStart)
    {
        OnActiveFramesBegin();
    }
    else if (bHitboxEnabled && CurrentFrame >= RecoveryStart)
    {
        OnActiveFramesEnd();
    }

    // [扩展点] 判定帧内每逻辑帧查询 hitbox，命中去重后进入 ResolveHit
    if (CurrentFrame >= FrameData->GetTotalFrames())
    {
        // [扩展点] 依据 CancelWindow 等待取消输入，否则正常结束
    }
}

void UCombatAbility::OnActiveFramesBegin()
{
    bHitboxEnabled = true;
    // [扩展点] UHitboxComponent::EnableHitbox(FrameData) 并广播判定开始事件
}

void UCombatAbility::OnActiveFramesEnd()
{
    bHitboxEnabled = false;
    // [扩展点] UHitboxComponent::DisableHitbox() 并清空本帧命中集合
}

void UCombatAbility::ResolveHit(AActor* Target)
{
    // [扩展点] 依次判定弹反窗口 / 霸体等级 / 防御槽，
    // 再请求 UHitstopSubsystem 命中停顿，写入 HitStun 与伤害。
}

bool UCombatAbility::CanCancelInto(const FGameplayTag& NextAbilityTag) const
{
    // [扩展点] 检查 CancelWindow 与 CancelRoutes（轻→重→必杀→超必杀）
    return FrameData && FrameData->CancelRoutes.HasTag(NextAbilityTag);
}

void UCombatAbility::EndAbility(const FGameplayAbilitySpecHandle Handle,
    const FGameplayAbilityActorInfo* ActorInfo,
    const FGameplayAbilityActivationInfo ActivationInfo,
    bool bReplicateEndAbility, bool bWasCancelled)
{
    Super::EndAbility(Handle, ActorInfo, ActivationInfo, bReplicateEndAbility, bWasCancelled);
    CurrentFrame = 0;
    bHitboxEnabled = false;
}
"""


def generate_hitbox_component_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HitboxComponent.generated.h"

class UCombatFrameData;
class AActor;

/** 判定组件：自定义 hitbox/hurtbox 查询，判定与动画表现完全解耦 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class MECHAMON_API UHitboxComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UHitboxComponent();

    /** 进入判定帧：开启 hitbox 并重置本窗口命中集合 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitbox")
    void EnableHitbox(const UCombatFrameData* InFrameData);

    /** 退出判定帧：关闭 hitbox */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitbox")
    void DisableHitbox();

    /** 当前判定帧内的重叠目标（已按 hitbox/hurtbox 过滤） */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitbox")
    bool QueryOverlaps(TArray<AActor*>& OutTargets) const;

    UFUNCTION(BlueprintPure, Category = "Combat|Hitbox")
    bool IsHitboxActive() const { return bHitboxActive; }

    /** 判定盒尺寸与偏移，随招式帧数据可覆盖 */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Hitbox")
    FVector HitboxExtent = FVector(60.f, 40.f, 80.f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Hitbox")
    FVector HitboxOffset = FVector(80.f, 0.f, 0.f);

private:
    bool bHitboxActive = false;
    TObjectPtr<const UCombatFrameData> ActiveFrameData;
    TSet<TObjectPtr<AActor>> HitActorsThisWindow;
};
"""


def generate_hitbox_component_cpp() -> str:
    return """#include "Combat/HitboxComponent.h"
#include "Abilities/CombatFrameData.h"
#include "Engine/World.h"

UHitboxComponent::UHitboxComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UHitboxComponent::EnableHitbox(const UCombatFrameData* InFrameData)
{
    ActiveFrameData = InFrameData;
    bHitboxActive = true;
    HitActorsThisWindow.Reset();

    // [扩展点] 用 FrameData->Reach 覆盖 HitboxExtent/HitboxOffset，按招式切换判定形状
}

void UHitboxComponent::DisableHitbox()
{
    bHitboxActive = false;
    ActiveFrameData = nullptr;
    HitActorsThisWindow.Reset();
}

bool UHitboxComponent::QueryOverlaps(TArray<AActor*>& OutTargets) const
{
    OutTargets.Reset();
    if (!bHitboxActive || !GetOwner() || !GetWorld())
    {
        return false;
    }

    const FVector Center = GetOwner()->GetActorLocation() +
        GetOwner()->GetActorRotation().RotateVector(HitboxOffset);
    const FCollisionShape Shape = FCollisionShape::MakeBox(HitboxExtent);
    FCollisionQueryParams Params(SCENE_QUERY_STAT(MechaHitboxQuery), false, GetOwner());

    TArray<FOverlapResult> Overlaps;
    GetWorld()->OverlapMultiByObjectType(
        Overlaps, Center, GetOwner()->GetActorQuat(),
        FCollisionObjectQueryParams(ECC_Pawn), Shape, Params);

    for (const FOverlapResult& Result : Overlaps)
    {
        AActor* Target = Result.GetActor();
        if (Target && !HitActorsThisWindow.Contains(Target))
        {
            OutTargets.Add(Target);
        }
    }

    // [扩展点] 过滤友军、已命中目标与无敌帧；读取目标 hurtbox 尺寸做精确相交
    return OutTargets.Num() > 0;
}
"""


def generate_parry_component_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ParryComponent.generated.h"

class UAbilitySystemComponent;
class AActor;

/** 弹反组件：管理 4 帧弹反窗口、成功硬直反馈与能量奖励 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class MECHAMON_API UParryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UParryComponent();

    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void Initialize(UAbilitySystemComponent* InOwnerASC);

    /** 按下防御键：开启弹反窗口 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void OpenParryWindow(int32 InWindowFrames);

    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void CloseParryWindow();

    /** 每个逻辑帧推进窗口计时 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void TickParryWindow();

    /** 受击时尝试弹反，成功返回 true */
    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    bool TryParry(AActor* Attacker, UAbilitySystemComponent* SourceASC);

    UFUNCTION(BlueprintPure, Category = "Combat|Parry")
    bool IsParryWindowOpen() const { return RemainingWindowFrames > 0; }

protected:
    /** 4 帧弹反窗口（源自 BATTLE_RULES） */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Parry")
    int32 ParryWindowFrames = 4;

    /** 弹反成功使对手陷入 36 帧硬直 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Parry")
    int32 PunishFrames = 36;

    /** 弹反成功获得 30 点能量 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Parry")
    int32 MeterReward = 30;

private:
    int32 RemainingWindowFrames = 0;
    TObjectPtr<UAbilitySystemComponent> OwnerASC;
};
"""


def generate_parry_component_cpp() -> str:
    return """#include "Combat/ParryComponent.h"
#include "AbilitySystemComponent.h"
#include "Tags/MechaGameplayTags.h"

UParryComponent::UParryComponent()
{
    PrimaryComponentTick.bCanEverTick = false;
}

void UParryComponent::Initialize(UAbilitySystemComponent* InOwnerASC)
{
    OwnerASC = InOwnerASC;
}

void UParryComponent::OpenParryWindow(int32 InWindowFrames)
{
    RemainingWindowFrames = InWindowFrames > 0 ? InWindowFrames : ParryWindowFrames;
}

void UParryComponent::CloseParryWindow()
{
    RemainingWindowFrames = 0;
}

void UParryComponent::TickParryWindow()
{
    if (RemainingWindowFrames > 0)
    {
        --RemainingWindowFrames;
    }
}

bool UParryComponent::TryParry(AActor* Attacker, UAbilitySystemComponent* SourceASC)
{
    if (RemainingWindowFrames <= 0 || !Attacker || !SourceASC || !OwnerASC)
    {
        return false;
    }

    // [扩展点] 对攻击方施加 Status.HitStun（PunishFrames 帧），
    // 为自身增加 MeterReward 点能量，并广播 Event.Parry 供表现层响应。
    const FMechaGameplayTags& Tags = FMechaGameplayTags::Get();
    (void)Tags.Event_Parry;
    (void)PunishFrames;
    (void)MeterReward;

    RemainingWindowFrames = 0;
    return true;
}
"""


def generate_anim_instance_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "MechaAnimInstance.generated.h"

class UCombatFrameData;

/** 机甲动画实例：动捕基础姿态 + Control Rig 机甲化 + 程序化二级运动 */
UCLASS(Transient, Blueprintable)
class MECHAMON_API UMechaAnimInstance : public UAnimInstance
{
    GENERATED_BODY()

public:
    virtual void NativeUpdateAnimation(float DeltaSeconds) override;

    /** 由战斗帧调度同步当前招式与帧号 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Animation")
    void SetCombatState(const UCombatFrameData* InFrameData, int32 InFrame);

    UPROPERTY(BlueprintReadOnly, Category = "Combat|Animation")
    TObjectPtr<const UCombatFrameData> ActiveFrameData;

    UPROPERTY(BlueprintReadOnly, Category = "Combat|Animation")
    int32 CurrentFrame = 0;

    /** hitstop 期间保持姿态，强化打击停顿 */
    UPROPERTY(BlueprintReadOnly, Category = "Combat|Animation")
    bool bHitstopActive = false;

    /** Control Rig 混合权重：机甲化姿态占比 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Animation")
    float ControlRigAlpha = 1.f;

    /** 二级运动强度：推进器抖动/受击抖动 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Animation")
    float SecondaryMotionIntensity = 1.f;
};
"""


def generate_anim_instance_cpp() -> str:
    return """#include "Animation/MechaAnimInstance.h"
#include "Abilities/CombatFrameData.h"

void UMechaAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
    Super::NativeUpdateAnimation(DeltaSeconds);

    // [扩展点] 根据 ActiveFrameData 的 Startup/Active/Recovery 推进 Control Rig 姿态混合，
    // 叠加程序化二级运动（推进器抖动、受击抖动）。hitstop 期间冻结姿态更新。
    (void)CurrentFrame;
    (void)ControlRigAlpha;
    (void)SecondaryMotionIntensity;
}

void UMechaAnimInstance::SetCombatState(const UCombatFrameData* InFrameData, int32 InFrame)
{
    ActiveFrameData = InFrameData;
    CurrentFrame = InFrame;
}
"""


def generate_hitstop_subsystem_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "HitstopSubsystem.generated.h"

/** 命中停顿子系统：统一调度双方冻结帧，保证打击节奏一致 */
UCLASS()
class MECHAMON_API UHitstopSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    /** 命中时请求冻结指定逻辑帧 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitstop")
    void RequestHitstop(int32 Frames);

    /** 每个逻辑帧推进命中停顿计时 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitstop")
    void TickHitstop();

    UFUNCTION(BlueprintPure, Category = "Combat|Hitstop")
    bool IsHitstopActive() const { return RemainingFrames > 0; }

    UFUNCTION(BlueprintPure, Category = "Combat|Hitstop")
    int32 GetRemainingFrames() const { return RemainingFrames; }

private:
    int32 RemainingFrames = 0;
    float CachedTimeDilation = 1.f;
};
"""


def generate_hitstop_subsystem_cpp() -> str:
    return """#include "Subsystems/HitstopSubsystem.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"

void UHitstopSubsystem::RequestHitstop(int32 Frames)
{
    if (Frames <= 0)
    {
        return;
    }

    RemainingFrames = FMath::Max(RemainingFrames, Frames);

    // [扩展点] 用 GlobalTimeDilation 或自定义时间膨胀冻结表现层，
    // 逻辑帧判定不受影响，保证弹反窗口精确。
    if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
    {
        CachedTimeDilation = UGameplayStatics::GetGlobalTimeDilation(World);
        UGameplayStatics::SetGlobalTimeDilation(World, 0.05f);
    }
}

void UHitstopSubsystem::TickHitstop()
{
    if (RemainingFrames <= 0)
    {
        return;
    }

    --RemainingFrames;
    if (RemainingFrames == 0)
    {
        if (UWorld* World = GetGameInstance() ? GetGameInstance()->GetWorld() : nullptr)
        {
            UGameplayStatics::SetGlobalTimeDilation(World, CachedTimeDilation);
        }
    }
}
"""


def generate_replay_subsystem_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "CombatReplaySubsystem.generated.h"

/** 单帧输入快照：用于帧步进调试、输入回放与服务器校验 */
USTRUCT(BlueprintType)
struct MECHAMON_API FCombatInputFrame
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "Combat|Replay")
    int32 FrameNumber = 0;

    /** 位掩码：方向/轻击/重击/必杀/超必杀/防御/跳跃/冲刺 */
    UPROPERTY(BlueprintReadOnly, Category = "Combat|Replay")
    uint32 ButtonMask = 0;
};

/** 战斗回放子系统：帧步进、输入回放与可量化复盘 */
UCLASS()
class MECHAMON_API UCombatReplaySubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "Combat|Replay")
    void RecordInputFrame(const FCombatInputFrame& Frame);

    UFUNCTION(BlueprintCallable, Category = "Combat|Replay")
    void SetFrameStepMode(bool bEnabled);

    UFUNCTION(BlueprintCallable, Category = "Combat|Replay")
    bool AdvanceOneFrame();

    UFUNCTION(BlueprintCallable, Category = "Combat|Replay")
    void ReplayFromFrame(int32 StartFrame);

    UFUNCTION(BlueprintCallable, Category = "Combat|Replay")
    FString DumpBattleLog() const;

private:
    TArray<FCombatInputFrame> RecordedFrames;
    bool bFrameStepMode = false;
    int32 ReplayCursor = 0;
};
"""


def generate_replay_subsystem_cpp() -> str:
    return """#include "Subsystems/CombatReplaySubsystem.h"

void UCombatReplaySubsystem::RecordInputFrame(const FCombatInputFrame& Frame)
{
    RecordedFrames.Add(Frame);

    // [扩展点] 输入缓冲窗口为 6 帧；按帧号排序后上传服务器做权威校验
}

void UCombatReplaySubsystem::SetFrameStepMode(bool bEnabled)
{
    bFrameStepMode = bEnabled;
    ReplayCursor = 0;
}

bool UCombatReplaySubsystem::AdvanceOneFrame()
{
    if (!bFrameStepMode || ReplayCursor >= RecordedFrames.Num())
    {
        return false;
    }

    // [扩展点] 只推进一帧输入到战斗调度，并在编辑器中可视化判定盒
    ++ReplayCursor;
    return true;
}

void UCombatReplaySubsystem::ReplayFromFrame(int32 StartFrame)
{
    ReplayCursor = FMath::Clamp(StartFrame, 0, RecordedFrames.Num());

    // [扩展点] 从分歧帧重演，配合服务器权威结果实现回滚校正
}

FString UCombatReplaySubsystem::DumpBattleLog() const
{
    FString Log;
    for (const FCombatInputFrame& Frame : RecordedFrames)
    {
        Log += FString::Printf(TEXT("F%04d mask=0x%08x\\n"), Frame.FrameNumber, Frame.ButtonMask);
    }
    return Log;
}
"""


def _tag_member(key: str, comment: str) -> str:
    return f"    // {comment}\n    FGameplayTag {key};"


def generate_tags_h() -> str:
    elements = "\n".join(
        _tag_member(f"Type_{e.key}", e.name_cn) for e in ELEMENTS
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
    FGameplayTag Status_HitStun;
    FGameplayTag Status_BlockStun;
    FGameplayTag Status_Armor;
    FGameplayTag Status_GuardBreak;

    // ---- 事件 ----
    FGameplayTag Event_Parry;
    FGameplayTag Event_CounterHit;
    FGameplayTag Event_Hit;
    FGameplayTag Event_Knockout;

    // ---- 数值 SetByCaller ----
    FGameplayTag Data_Damage;
    FGameplayTag Data_MeterCost;

private:
    static FMechaGameplayTags Instance;
    FMechaGameplayTags();
}};
"""


def generate_tags_cpp() -> str:
    element_inits = "\n".join(
        f'    Type_{e.key} = FGameplayTag::RequestGameplayTag(FName("{e.tag}"));' for e in ELEMENTS
    )
    return f"""#include "Tags/MechaGameplayTags.h"

FMechaGameplayTags FMechaGameplayTags::Instance;

FMechaGameplayTags::FMechaGameplayTags()
{{
{element_inits}

    Status_HitStun    = FGameplayTag::RequestGameplayTag(FName("Status.HitStun"));
    Status_BlockStun  = FGameplayTag::RequestGameplayTag(FName("Status.BlockStun"));
    Status_Armor      = FGameplayTag::RequestGameplayTag(FName("Status.Armor"));
    Status_GuardBreak = FGameplayTag::RequestGameplayTag(FName("Status.GuardBreak"));

    Event_Parry      = FGameplayTag::RequestGameplayTag(FName("Event.Parry"));
    Event_CounterHit = FGameplayTag::RequestGameplayTag(FName("Event.CounterHit"));
    Event_Hit        = FGameplayTag::RequestGameplayTag(FName("Event.Hit"));
    Event_Knockout   = FGameplayTag::RequestGameplayTag(FName("Event.Knockout"));

    Data_Damage    = FGameplayTag::RequestGameplayTag(FName("Data.Damage"));
    Data_MeterCost = FGameplayTag::RequestGameplayTag(FName("Data.MeterCost"));
}}
"""


def generate_battle_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameStateBase.h"
#include "BattleManager.generated.h"

class AMechaCharacter;

/** 对局管理器：负责 1v1 BO3 回合流程、计时、胜负结算与服务器权威校验 */
UCLASS()
class MECHAMON_API ABattleManager : public AGameStateBase
{
    GENERATED_BODY()

public:
    ABattleManager();

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void StartMatch(AMechaCharacter* InPlayerOne, AMechaCharacter* InPlayerTwo);

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void TickRound(float DeltaSeconds);

    /** 单局结束时由服务器调用 */
    UFUNCTION(BlueprintCallable, Category = "Battle")
    void NotifyRoundFinished(AMechaCharacter* Winner);

    UFUNCTION(BlueprintPure, Category = "Battle")
    int32 GetRoundTimeRemaining() const { return FMath::CeilToInt(RoundTimeRemaining); }

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 PlayerRoundsWon = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 OpponentRoundsWon = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 CurrentRound = 1;

private:
    float RoundTimeRemaining = 99.f;
    static constexpr int32 RoundsToWin = 2;
    TObjectPtr<AMechaCharacter> PlayerOne;
    TObjectPtr<AMechaCharacter> PlayerTwo;

    void CheckMatchEnd();
    void ResetRound();
};
"""


def generate_battle_cpp() -> str:
    return """#include "Battle/BattleManager.h"
#include "MechaCharacter.h"
#include "Net/UnrealNetwork.h"

ABattleManager::ABattleManager()
{
    bReplicates = true;
}

void ABattleManager::StartMatch(AMechaCharacter* InPlayerOne, AMechaCharacter* InPlayerTwo)
{
    PlayerOne = InPlayerOne;
    PlayerTwo = InPlayerTwo;
    PlayerRoundsWon = 0;
    OpponentRoundsWon = 0;
    CurrentRound = 1;
    ResetRound();

    // [扩展点] 广播对局开始事件，驱动 Ban/Pick 结果与战斗 HUD
}

void ABattleManager::TickRound(float DeltaSeconds)
{
    if (RoundTimeRemaining <= 0.f)
    {
        return;
    }

    RoundTimeRemaining -= DeltaSeconds;
    if (RoundTimeRemaining <= 0.f)
    {
        RoundTimeRemaining = 0.f;
        // [扩展点] 时间耗尽按剩余生命比例判定胜方
    }
}

void ABattleManager::NotifyRoundFinished(AMechaCharacter* Winner)
{
    if (Winner == PlayerOne)
    {
        ++PlayerRoundsWon;
    }
    else if (Winner == PlayerTwo)
    {
        ++OpponentRoundsWon;
    }

    CheckMatchEnd();
    if (PlayerRoundsWon < RoundsToWin && OpponentRoundsWon < RoundsToWin)
    {
        ++CurrentRound;
        ResetRound();
    }
}

void ABattleManager::CheckMatchEnd()
{
    // [扩展点] BO3 结束：写入天梯结果、战斗日志与观战数据
}

void ABattleManager::ResetRound()
{
    RoundTimeRemaining = 99.f;
    // [扩展点] 重置双方生命/能量/防御槽与位置，清空输入缓冲
}

void ABattleManager::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(ABattleManager, PlayerRoundsWon);
    DOREPLIFETIME(ABattleManager, OpponentRoundsWon);
    DOREPLIFETIME(ABattleManager, CurrentRound);
}
"""


def generate_character_h() -> str:
    return """#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MechaCharacter.generated.h"

class UAbilitySystemComponent;
class UMechaAttributeSet;
class UHitboxComponent;
class UParryComponent;
class UMechaAnimInstance;
class UCombatFrameData;

/** 机甲角色：挂载 ASC、属性集与实时格斗组件，是 1v1 对战中的基本单位 */
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

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UHitboxComponent* GetHitboxComponent() const { return HitboxComponent; }

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UParryComponent* GetParryComponent() const { return ParryComponent; }

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

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat")
    TObjectPtr<UHitboxComponent> HitboxComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat")
    TObjectPtr<UParryComponent> ParryComponent;

    /** 初始招式列表（帧数据 DataAsset 驱动） */
    UPROPERTY(EditDefaultsOnly, Category = "Combat")
    TArray<TSubclassOf<class UCombatAbility>> StartingAbilities;

    /** 输入回放记录的按键位掩码 */
    uint32 CurrentInputMask = 0;
};
"""


def generate_character_cpp() -> str:
    return """#include "MechaCharacter.h"
#include "MechaAttributeSet.h"
#include "Combat/HitboxComponent.h"
#include "Combat/ParryComponent.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"

AMechaCharacter::AMechaCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
    AbilitySystemComponent->SetIsReplicated(true);
    AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);

    AttributeSet = CreateDefaultSubobject<UMechaAttributeSet>(TEXT("AttributeSet"));
    HitboxComponent = CreateDefaultSubobject<UHitboxComponent>(TEXT("HitboxComponent"));
    ParryComponent = CreateDefaultSubobject<UParryComponent>(TEXT("ParryComponent"));

    // [扩展点] 在 BeginPlay / PossessedBy 中：
    // for (TSubclassOf<UCombatAbility> Ability : StartingAbilities)
    // {
    //     AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(Ability, 1, INDEX_NONE, this));
    // }
    // AbilitySystemComponent->InitAbilityActorInfo(this, this);
    // ParryComponent->Initialize(AbilitySystemComponent);
}
"""


def generate_readme() -> str:
    move_count = len(all_moves_flat())
    mecha_count = len(MECHAS)
    element_count = len(ELEMENTS)
    return f"""# MECHA·MON · UE5 实时格斗战斗系统代码基座

本目录由 MECHA·MON 数据驱动构建系统导出，面向 **实时 1v1 硬核机甲格斗**，
符合 UE5 / GAS 工程规范，可直接导入工程的 `Source/` 目录作为战斗系统的核心模块。

全部招式以固定 60Hz 逻辑帧描述，判定与动画表现解耦；核心接入点以 `[扩展点]` 标注。

## 核心类清单

| 类 | 文件 | 职责 |
|---|---|---|
| `AMechaCharacter` | `Public/MechaCharacter.h` | 机甲角色，挂载 ASC、属性集与格斗组件 |
| `UMechaAttributeSet` | `Public/MechaAttributeSet.h` | 生命 / 能量 / 防御槽 / 攻防速 / 霸体 |
| `UCombatAbility` | `Public/Abilities/CombatAbility.h` | 帧数据驱动招式，推进起手/判定/收招 |
| `UCombatFrameData` | `Public/Abilities/CombatFrameData.h` | 招式帧数据 DataAsset（{move_count} 个招式的配置模板） |
| `UHitboxComponent` | `Public/Combat/HitboxComponent.h` | hitbox / hurtbox 查询 |
| `UParryComponent` | `Public/Combat/ParryComponent.h` | 弹反窗口、成功硬直与能量奖励 |
| `UMechaAnimInstance` | `Public/Animation/MechaAnimInstance.h` | Control Rig 混合动画与二级运动 |
| `UHitstopSubsystem` | `Public/Subsystems/HitstopSubsystem.h` | 命中停顿调度 |
| `UCombatReplaySubsystem` | `Public/Subsystems/CombatReplaySubsystem.h` | 帧步进、输入回放与战斗日志 |
| `FMechaGameplayTags` | `Public/Tags/MechaGameplayTags.h` | {element_count} 种属性 + 格斗状态/事件标签 |
| `ABattleManager` | `Public/Battle/BattleManager.h` | 1v1 BO3 回合流程与胜负结算 |

## 数据规模

- {mecha_count} 台机甲 / {move_count} 个招式（轻击 / 重击 / 必杀 / 超必杀）
- 4 类操作系统动作：防御、弹反、推进跳跃、瞬时冲刺
- 属性克制：{element_count} × {element_count} 关系表

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
"""


def generate_all():
    files = {
        "MechaMon.Build.cs": generate_build_cs(),
        "Public/MechaCharacter.h": generate_character_h(),
        "Private/MechaCharacter.cpp": generate_character_cpp(),
        "Public/MechaAttributeSet.h": generate_attribute_set_h(),
        "Private/MechaAttributeSet.cpp": generate_attribute_set_cpp(),
        "Public/Abilities/CombatAbility.h": generate_combat_ability_h(),
        "Private/Abilities/CombatAbility.cpp": generate_combat_ability_cpp(),
        "Public/Abilities/CombatFrameData.h": generate_frame_data_h(),
        "Private/Abilities/CombatFrameData.cpp": generate_frame_data_cpp(),
        "Public/Combat/HitboxComponent.h": generate_hitbox_component_h(),
        "Private/Combat/HitboxComponent.cpp": generate_hitbox_component_cpp(),
        "Public/Combat/ParryComponent.h": generate_parry_component_h(),
        "Private/Combat/ParryComponent.cpp": generate_parry_component_cpp(),
        "Public/Animation/MechaAnimInstance.h": generate_anim_instance_h(),
        "Private/Animation/MechaAnimInstance.cpp": generate_anim_instance_cpp(),
        "Public/Subsystems/HitstopSubsystem.h": generate_hitstop_subsystem_h(),
        "Private/Subsystems/HitstopSubsystem.cpp": generate_hitstop_subsystem_cpp(),
        "Public/Subsystems/CombatReplaySubsystem.h": generate_replay_subsystem_h(),
        "Private/Subsystems/CombatReplaySubsystem.cpp": generate_replay_subsystem_cpp(),
        "Public/Tags/MechaGameplayTags.h": generate_tags_h(),
        "Private/Tags/MechaGameplayTags.cpp": generate_tags_cpp(),
        "Public/Battle/BattleManager.h": generate_battle_h(),
        "Private/Battle/BattleManager.cpp": generate_battle_cpp(),
    }
    for rel, content in files.items():
        _write(UE5_DIR / rel, content)

    # 清理早期目录中的旧文件，确保产物与实时格斗架构一致
    for legacy in (
        "Public/Abilities/MechaAbilityBase.h",
        "Private/Abilities/MechaAbilityBase.cpp",
    ):
        legacy_path = UE5_DIR / legacy
        if legacy_path.exists():
            legacy_path.unlink()

    _write(UE5_DIR / "README.md", generate_readme(), header=False)
    return list(files.keys()) + ["README.md"]
