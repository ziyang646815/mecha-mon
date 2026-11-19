// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#include "MechaGameplayTags.h"

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

    Status_Burning   = FGameplayTag::RequestGameplayTag(FName("Status.Burning"));
    Status_Frozen    = FGameplayTag::RequestGameplayTag(FName("Status.Frozen"));
    Status_Shielded  = FGameplayTag::RequestGameplayTag(FName("Status.Shielded"));
    Status_Stunned   = FGameplayTag::RequestGameplayTag(FName("Status.Stunned"));
    Status_Overdrive = FGameplayTag::RequestGameplayTag(FName("Status.Overdrive"));
    Status_Slowed    = FGameplayTag::RequestGameplayTag(FName("Status.Slowed"));

    Event_Hit      = FGameplayTag::RequestGameplayTag(FName("Event.Hit"));
    Event_Switch   = FGameplayTag::RequestGameplayTag(FName("Event.Switch"));
    Event_Knockout = FGameplayTag::RequestGameplayTag(FName("Event.Knockout"));

    Data_Power = FGameplayTag::RequestGameplayTag(FName("Data.Power"));
}
