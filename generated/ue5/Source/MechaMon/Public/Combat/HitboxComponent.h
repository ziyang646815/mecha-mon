// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HitboxComponent.generated.h"

class UCombatFrameData;
class AActor;

/** 判定组件：自定义 hitbox/hurtbox 查询，判定与动画表现完全解耦 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class MECHAMON_API UHitboxComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UHitboxComponent();

    /** 进入判定帧：开启 hitbox 并重置本窗口命中集合 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitbox")
    void EnableHitbox(const UCombatFrameData* InFrameData);

    /** 退出判定帧：关闭 hitbox */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitbox")
    void DisableHitbox();

    /** 当前判定帧内的重叠目标（已按 hitbox/hurtbox 过滤） */
    UFUNCTION(BlueprintCallable, Category = "Combat|Hitbox")
    bool QueryOverlaps(TArray<AActor*>& OutTargets) const;

    UFUNCTION(BlueprintPure, Category = "Combat|Hitbox")
    bool IsHitboxActive() const { return bHitboxActive; }

    /** 判定盒尺寸与偏移，随招式帧数据可覆盖 */
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Hitbox")
    FVector HitboxExtent = FVector(60.f, 40.f, 80.f);

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Combat|Hitbox")
    FVector HitboxOffset = FVector(80.f, 0.f, 0.f);

private:
    bool bHitboxActive = false;
    TObjectPtr<const UCombatFrameData> ActiveFrameData;
    TSet<TObjectPtr<AActor>> HitActorsThisWindow;
};
