// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Battle/BattleManager.h"
#include "MechaCharacter.h"
#include "Net/UnrealNetwork.h"

ABattleManager::ABattleManager()
{
    bReplicates = true;
}

void ABattleManager::StartMatch(AMechaCharacter* InPlayerOne, AMechaCharacter* InPlayerTwo)
{
    PlayerOne = InPlayerOne;
    PlayerTwo = InPlayerTwo;
    PlayerRoundsWon = 0;
    OpponentRoundsWon = 0;
    CurrentRound = 1;
    ResetRound();

    // [扩展点] 广播对局开始事件，驱动 Ban/Pick 结果与战斗 HUD
}

void ABattleManager::TickRound(float DeltaSeconds)
{
    if (RoundTimeRemaining <= 0.f)
    {
        return;
    }

    RoundTimeRemaining -= DeltaSeconds;
    if (RoundTimeRemaining <= 0.f)
    {
        RoundTimeRemaining = 0.f;
        // [扩展点] 时间耗尽按剩余生命比例判定胜方
    }
}

void ABattleManager::NotifyRoundFinished(AMechaCharacter* Winner)
{
    if (Winner == PlayerOne)
    {
        ++PlayerRoundsWon;
    }
    else if (Winner == PlayerTwo)
    {
        ++OpponentRoundsWon;
    }

    CheckMatchEnd();
    if (PlayerRoundsWon < RoundsToWin && OpponentRoundsWon < RoundsToWin)
    {
        ++CurrentRound;
        ResetRound();
    }
}

void ABattleManager::CheckMatchEnd()
{
    // [扩展点] BO3 结束：写入天梯结果、战斗日志与观战数据
}

void ABattleManager::ResetRound()
{
    RoundTimeRemaining = 99.f;
    // [扩展点] 重置双方生命/能量/防御槽与位置，清空输入缓冲
}

void ABattleManager::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(ABattleManager, PlayerRoundsWon);
    DOREPLIFETIME(ABattleManager, OpponentRoundsWon);
    DOREPLIFETIME(ABattleManager, CurrentRound);
}
