// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

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
