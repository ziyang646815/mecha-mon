// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#include "MechaAttributeSet.h"
#include "Net/UnrealNetwork.h"
#include "GameplayEffectExtension.h"

UMechaAttributeSet::UMechaAttributeSet()
{
    InitHealth(100.f);
    InitMaxHealth(100.f);
    InitEnergy(100.f);
    InitMaxEnergy(120.f);
    InitAttack(80.f);
    InitDefense(70.f);
    InitSpeed(70.f);
    InitCritRate(0.05f);
    InitShield(0.f);
}

void UMechaAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Health, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, MaxHealth, COND_None, REPNOTIFY_Always);
    DOREPLIFETIME_CONDITION_NOTIFY(UMechaAttributeSet, Energy, COND_None, REPNOTIFY_Always);
}

void UMechaAttributeSet::PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data)
{
    Super::PostGameplayEffectExecute(Data);

    // TODO: 接入属性克制倍率（读取 Mecha.Type.* 标签）与 GameplayCue 表现
    if (Data.EvaluatedData.Attribute == GetHealthAttribute())
    {
        SetHealth(FMath::Clamp(GetHealth(), 0.f, GetMaxHealth()));
    }
    else if (Data.EvaluatedData.Attribute == GetEnergyAttribute())
    {
        SetEnergy(FMath::Clamp(GetEnergy(), 0.f, GetMaxEnergy()));
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

void UMechaAttributeSet::OnRep_Energy(const FGameplayAttributeData& OldValue)
{
    GAMEPLAYATTRIBUTE_REPNOTIFY(UMechaAttributeSet, Energy, OldValue);
}
