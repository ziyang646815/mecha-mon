// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Abilities/CombatAbility.h"
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
