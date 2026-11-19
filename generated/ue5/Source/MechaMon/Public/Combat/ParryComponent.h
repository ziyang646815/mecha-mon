// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ParryComponent.generated.h"

class UAbilitySystemComponent;
class AActor;

/** 弹反组件：管理 4 帧弹反窗口、成功硬直反馈与能量奖励 */
UCLASS(ClassGroup = (Combat), meta = (BlueprintSpawnableComponent))
class MECHAMON_API UParryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UParryComponent();

    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void Initialize(UAbilitySystemComponent* InOwnerASC);

    /** 按下防御键：开启弹反窗口 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void OpenParryWindow(int32 InWindowFrames);

    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void CloseParryWindow();

    /** 每个逻辑帧推进窗口计时 */
    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    void TickParryWindow();

    /** 受击时尝试弹反，成功返回 true */
    UFUNCTION(BlueprintCallable, Category = "Combat|Parry")
    bool TryParry(AActor* Attacker, UAbilitySystemComponent* SourceASC);

    UFUNCTION(BlueprintPure, Category = "Combat|Parry")
    bool IsParryWindowOpen() const { return RemainingWindowFrames > 0; }

protected:
    /** 4 帧弹反窗口（源自 BATTLE_RULES） */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Parry")
    int32 ParryWindowFrames = 4;

    /** 弹反成功使对手陷入 36 帧硬直 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Parry")
    int32 PunishFrames = 36;

    /** 弹反成功获得 30 点能量 */
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Combat|Parry")
    int32 MeterReward = 30;

private:
    int32 RemainingWindowFrames = 0;
    TObjectPtr<UAbilitySystemComponent> OwnerASC;
};
