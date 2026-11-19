// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

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
