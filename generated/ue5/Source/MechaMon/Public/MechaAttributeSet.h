// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
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

/** 机甲属性集：所有可修改数值集中在此，便于平衡调整与网络复制 */
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

    // ---- 能量（技能消耗资源） ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Energy", ReplicatedUsing = OnRep_Energy)
    FGameplayAttributeData Energy;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Energy)

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Energy")
    FGameplayAttributeData MaxEnergy;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, MaxEnergy)

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

    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData CritRate;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, CritRate)

    // ---- 临时护盾 ----
    UPROPERTY(BlueprintReadOnly, Category = "Mecha|Combat")
    FGameplayAttributeData Shield;
    ATTRIBUTE_ACCESSORS(UMechaAttributeSet, Shield)

protected:
    UFUNCTION()
    void OnRep_Health(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_MaxHealth(const FGameplayAttributeData& OldValue);
    UFUNCTION()
    void OnRep_Energy(const FGameplayAttributeData& OldValue);
};
