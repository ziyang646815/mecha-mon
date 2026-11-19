// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Animation/MechaAnimInstance.h"
#include "Abilities/CombatFrameData.h"

void UMechaAnimInstance::NativeUpdateAnimation(float DeltaSeconds)
{
    Super::NativeUpdateAnimation(DeltaSeconds);

    // [扩展点] 根据 ActiveFrameData 的 Startup/Active/Recovery 推进 Control Rig 姿态混合，
    // 叠加程序化二级运动（推进器抖动、受击抖动）。hitstop 期间冻结姿态更新。
    (void)CurrentFrame;
    (void)ControlRigAlpha;
    (void)SecondaryMotionIntensity;
}

void UMechaAnimInstance::SetCombatState(const UCombatFrameData* InFrameData, int32 InFrame)
{
    ActiveFrameData = InFrameData;
    CurrentFrame = InFrame;
}
