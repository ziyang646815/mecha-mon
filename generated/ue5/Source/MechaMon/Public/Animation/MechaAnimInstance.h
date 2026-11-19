// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "MechaAnimInstance.generated.h"

class UCombatFrameData;

/** 机甲动画实例：动捕基础姿态 + Control Rig 机甲化 + 程序化二级运动 */
UCLASS(Transient, Blueprintable)
class MECHAMON_API UMechaAnimInstance : public UAnimInstance
{
    GENERATED_BODY()

public:
    virtual void NativeUpdateAnimation(float DeltaSeconds) override;

    /** 由战斗帧调度同步当前招式与帧号 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Animation")
    void SetCombatState(const UCombatFrameData* InFrameData, int32 InFrame);

    UPROPERTY(BlueprintReadOnly, Category = "Combat|Animation")
    TObjectPtr<const UCombatFrameData> ActiveFrameData;

    UPROPERTY(BlueprintReadOnly, Category = "Combat|Animation")
    int32 CurrentFrame = 0;

    /** hitstop 期间保持姿态，强化打击停顿 */
    UPROPERTY(BlueprintReadOnly, Category = "Combat|Animation")
    bool bHitstopActive = false;

    /** Control Rig 混合权重：机甲化姿态占比 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Animation")
    float ControlRigAlpha = 1.f;

    /** 二级运动强度：推进器抖动/受击抖动 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Animation")
    float SecondaryMotionIntensity = 1.f;
};
