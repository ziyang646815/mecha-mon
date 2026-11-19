// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Subsystems/HitstopSubsystem.h"
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
