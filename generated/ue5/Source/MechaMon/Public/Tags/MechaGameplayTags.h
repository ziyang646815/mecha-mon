// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameplayTagContainer.h"
#include "MechaGameplayTags.generated.h"

/** 集中声明项目中使用的 GameplayTag，避免字符串硬编码 */
USTRUCT(BlueprintType)
struct MECHAMON_API FMechaGameplayTags
{
    GENERATED_BODY()

    static const FMechaGameplayTags& Get() { return Instance; }

    // ---- 机甲属性 ----
    // 烈焰
    FGameplayTag Type_FIRE;
    // 涌流
    FGameplayTag Type_WATER;
    // 雷霆
    FGameplayTag Type_ELECTRIC;
    // 森绿
    FGameplayTag Type_LEAF;
    // 钢甲
    FGameplayTag Type_STEEL;
    // 星轨
    FGameplayTag Type_QUANTUM;
    // 暗影
    FGameplayTag Type_SHADOW;
    // 冰晶
    FGameplayTag Type_ICE;

    // ---- 状态 ----
    FGameplayTag Status_Burning;
    FGameplayTag Status_Frozen;
    FGameplayTag Status_Shielded;
    FGameplayTag Status_Stunned;
    FGameplayTag Status_Overdrive;
    FGameplayTag Status_Slowed;

    // ---- 事件 ----
    FGameplayTag Event_Hit;
    FGameplayTag Event_Switch;
    FGameplayTag Event_Knockout;

    // ---- 数值 SetByCaller ----
    FGameplayTag Data_Power;

private:
    static FMechaGameplayTags Instance;
    FMechaGameplayTags();
};
