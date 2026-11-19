// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Combat/HitboxComponent.h"
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
