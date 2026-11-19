// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

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
