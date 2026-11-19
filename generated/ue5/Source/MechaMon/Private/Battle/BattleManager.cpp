// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#include "BattleManager.h"
#include "MechaCharacter.h"
#include "MechaAttributeSet.h"
#include "Net/UnrealNetwork.h"

ABattleManager::ABattleManager()
{
    bReplicates = true;
}

void ABattleManager::StartBattle(const TArray<AMechaCharacter*>& InPlayerTeam,
                                 const TArray<AMechaCharacter*>& InEnemyTeam)
{
    PlayerTeam = InPlayerTeam;
    EnemyTeam = InEnemyTeam;
    CurrentTurn = 1;
    CurrentActorIndex = 0;
    ComputeTurnOrder();
    // TODO: 广播战斗开始事件，驱动 UI
}

void ABattleManager::ComputeTurnOrder()
{
    TurnOrder.Reset();
    TurnOrder.Append(PlayerTeam);
    TurnOrder.Append(EnemyTeam);

    // 按速度属性降序排列
    TurnOrder.Sort([](const AMechaCharacter& A, const AMechaCharacter& B)
    {
        return A.GetMechaAttributes()->GetSpeed() > B.GetMechaAttributes()->GetSpeed();
    });
}

void ABattleManager::EndTurn()
{
    CurrentActorIndex++;
    if (CurrentActorIndex >= TurnOrder.Num())
    {
        CurrentActorIndex = 0;
        CurrentTurn++;
        // TODO: 回合结束回复 12 点能量、结算 DoT、检查回合上限
    }
    CheckBattleEnd();
}

void ABattleManager::CheckBattleEnd()
{
    // TODO: 任一方全部生命归零则结算胜负
}

void ABattleManager::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(ABattleManager, RandomSeed);
}
