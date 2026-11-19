// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Subsystems/CombatReplaySubsystem.h"

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
        Log += FString::Printf(TEXT("F%04d mask=0x%08x\n"), Frame.FrameNumber, Frame.ButtonMask);
    }
    return Log;
}
