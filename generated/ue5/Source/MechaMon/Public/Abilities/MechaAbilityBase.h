// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#pragma once

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
