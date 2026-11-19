// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "AttributeSet.h"
#include "AbilitySystemComponent.h"
#include "MechaAttributeSet.generated.h"

#define ATTRIBUTE_ACCESSORS(ClassName, PropertyName) \
    GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \
    GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName)

/** 机甲属性集：生命/能量/防御槽与战斗数值集中管理，便于平衡调整与网络复制 */
UCLASS()
class MECHAMON_API UMechaAttributeSet : public UAttributeSet
{
    GENERATED_BODY()

public:
    UMechaAttributeSet();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
    virtual void PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data) override;

    // ---- 生命 / 装甲 ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Vitals", ReplicatedUsing = OnRep_Health)
    FGameplayAttributeData Health;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Health)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Vitals", ReplicatedUsing = OnRep_MaxHealth)
    FGameplayAttributeData MaxHealth;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxHealth)

    // ---- 能量（必杀/超必杀消耗资源） ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Meter", ReplicatedUsing = OnRep_Meter)
    FGameplayAttributeData Meter;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Meter)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Meter")
    FGameplayAttributeData MaxMeter;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxMeter)

    // ---- 防御槽（清空即破防） ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Guard", ReplicatedUsing = OnRep_Guard)
    FGameplayAttributeData Guard;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Guard)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Guard")
    FGameplayAttributeData MaxGuard;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxGuard)

    // ---- 战斗属性 ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Attack;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Attack)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Defense;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Defense)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Speed;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Speed)

    /** 霸体等级：0 无 / 1 抗轻击 / 2 完全霸体 */
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Armor;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Armor)

protected:
    UFUNCTION()
    void OnRep_Health(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_MaxHealth(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_Meter(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_Guard(const FGameplayAttributeData& OldValue);
};
