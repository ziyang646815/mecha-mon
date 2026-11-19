// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "Tags/MechaGameplayTags.h"

FMechaGameplayTags FMechaGameplayTags::Instance;

FMechaGameplayTags::FMechaGameplayTags()
{
    Type_FIRE = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Fire"));
    Type_WATER = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Water"));
    Type_ELECTRIC = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Electric"));
    Type_LEAF = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Leaf"));
    Type_STEEL = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Steel"));
    Type_QUANTUM = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Quantum"));
    Type_SHADOW = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Shadow"));
    Type_ICE = FGameplayTag::RequestGameplayTag(FName("Mecha.Type.Ice"));

    Status_HitStun    = FGameplayTag::RequestGameplayTag(FName("Status.HitStun"));
    Status_BlockStun  = FGameplayTag::RequestGameplayTag(FName("Status.BlockStun"));
    Status_Armor      = FGameplayTag::RequestGameplayTag(FName("Status.Armor"));
    Status_GuardBreak = FGameplayTag::RequestGameplayTag(FName("Status.GuardBreak"));

    Event_Parry      = FGameplayTag::RequestGameplayTag(FName("Event.Parry"));
    Event_CounterHit = FGameplayTag::RequestGameplayTag(FName("Event.CounterHit"));
    Event_Hit        = FGameplayTag::RequestGameplayTag(FName("Event.Hit"));
    Event_Knockout   = FGameplayTag::RequestGameplayTag(FName("Event.Knockout"));

    Data_Damage    = FGameplayTag::RequestGameplayTag(FName("Data.Damage"));
    Data_MeterCost = FGameplayTag::RequestGameplayTag(FName("Data.MeterCost"));
}
