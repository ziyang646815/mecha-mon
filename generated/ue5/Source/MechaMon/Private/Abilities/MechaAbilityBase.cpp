// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "MechaAbilityBase.h"
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

    // [扩展点] 检查冻结/眩晕状态标签，被控制时禁止释放
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

    // [扩展点] 构造 EffectSpec → 应用属性克制倍率 → ApplyGameplayEffectToTarget
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
