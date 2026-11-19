// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameStateBase.h"
#include "BattleManager.generated.h"

class AMechaCharacter;

/** 回合调度器：负责先手计算、行动顺序、换人与胜负判定 */
UCLASS()
class MECHAMON_API ABattleManager : public AGameStateBase
{
    GENERATED_BODY()

public:
    ABattleManager();

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void StartBattle(const TArray<AMechaCharacter*>& PlayerTeam, const TArray<AMechaCharacter*>& EnemyTeam);

    UFUNCTION(BlueprintCallable, Category = "Battle")
    void EndTurn();

    UFUNCTION(BlueprintPure, Category = "Battle")
    int32 GetCurrentTurn() const { return CurrentTurn; }

    /** 服务器使用可复现种子保证战斗回放可校验 */
    UPROPERTY(Replicated, BlueprintReadOnly, Category = "Battle")
    int32 RandomSeed;

private:
    UPROPERTY()
    TArray<TObjectPtr<AMechaCharacter>> PlayerTeam;

    UPROPERTY()
    TArray<TObjectPtr<AMechaCharacter>> EnemyTeam;

    UPROPERTY()
    TArray<TObjectPtr<AMechaCharacter>> TurnOrder;

    int32 CurrentTurn = 0;
    int32 CurrentActorIndex = 0;

    void ComputeTurnOrder();
    void CheckBattleEnd();
};
