// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Combat/ParryComponent.h"
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
