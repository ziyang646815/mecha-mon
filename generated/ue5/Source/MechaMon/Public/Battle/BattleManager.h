// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameStateBase.h"
#include "BattleManager.generated.h"

class AMechaCharacter;

/** 对局管理器：负责 1v1 BO3 回合流程、计时、胜负结算与服务器权威校验 */
UCLASS()
class MECHAMON_API ABattleManager : public AGameStateBase
{
    GENERATED_BODY()

public:
    ABattleManager();

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void StartMatch(AMechaCharacter* InPlayerOne, AMechaCharacter* InPlayerTwo);

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void TickRound(float DeltaSeconds);

    /** 单局结束时由服务器调用 */
    UFUNCTION(BlueprintCallable, Category = "Battle")
    void NotifyRoundFinished(AMechaCharacter* Winner);

    UFUNCTION(BlueprintPure, Category = "Battle")
    int32 GetRoundTimeRemaining() const { return FMath::CeilToInt(RoundTimeRemaining); }

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 PlayerRoundsWon = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 OpponentRoundsWon = 0;

    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 CurrentRound = 1;

private:
    float RoundTimeRemaining = 99.f;
    static constexpr int32 RoundsToWin = 2;
    TObjectPtr<AMechaCharacter> PlayerOne;
    TObjectPtr<AMechaCharacter> PlayerTwo;

    void CheckMatchEnd();
    void ResetRound();
};
