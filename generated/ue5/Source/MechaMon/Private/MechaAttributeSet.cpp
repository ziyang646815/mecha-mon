// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "MechaAttributeSet.h"
#include "Net/UnrealNetwork.h"
#include "GameplayEffectExtension.h"

UMechaAttributeSet::UMechaAttributeSet()
{
    // 与 config/game_data.py BATTLE_RULES 保持一致
    InitHealth(1000.f);
    InitMaxHealth(1000.f);
    InitMeter(0.f);
    InitMaxMeter(100.f);
    InitGuard(100.f);
    InitMaxGuard(100.f);
    InitAttack(80.f);
    InitDefense(70.f);
    InitSpeed(70.f);
    InitArmor(0.f);
}

void UMechaAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Health, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, MaxHealth, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Meter, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Guard, COND_None, REPNOTIFY_Always);
}

void UMechaAttributeSet::PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data)
{
    Super::PostGameplayEffectExecute(Data);

    // [扩展点] 接入属性克制倍率、连招衰减与 Counter Hit 修正
    if (Data.EvaluatedData.Attribute == GetHealthAttribute())
    {
        SetHealth(FMath::Clamp(GetHealth(), 0.f, GetMaxHealth()));
    }
    else if (Data.EvaluatedData.Attribute == GetMeterAttribute())
    {
        SetMeter(FMath::Clamp(GetMeter(), 0.f, GetMaxMeter()));
    }
    else if (Data.EvaluatedData.Attribute == GetGuardAttribute())
    {
        // [扩展点] 防御槽清空时写入破防状态并触发长硬直
        SetGuard(FMath::Clamp(GetGuard(), 0.f, GetMaxGuard()));
    }
}

void UMechaAttributeSet::OnRep_Health(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Health, OldValue);
}

void UMechaAttributeSet::OnRep_MaxHealth(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, MaxHealth, OldValue);
}

void UMechaAttributeSet::OnRep_Meter(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Meter, OldValue);
}

void UMechaAttributeSet::OnRep_Guard(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Guard, OldValue);
}
