// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MechaCharacter.generated.h"

class UAbilitySystemComponent;
class UMechaAttributeSet;

/** 机甲角色基类：挂载 ASC 与属性集，是战斗中的基本单位 */
UCLASS()
class MECHAMON_API AMechaCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AMechaCharacter();

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UAbilitySystemComponent* GetMechaASC() const { return AbilitySystemComponent; }

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UMechaAttributeSet* GetMechaAttributes() const { return AttributeSet; }

    /** 机甲编号，如 MF-01 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha")
    FName MechaId;

    /** 属性标签，如 Mecha.Type.Fire */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Mecha")
    struct FGameplayTag MechaTypeTag;

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mecha")
    TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Mecha")
    TObjectPtr<UMechaAttributeSet> AttributeSet;

    /** 初始技能列表（DataAsset 驱动） */
    UPROPERTY(EditDefaultsOnly, Category = "Mecha")
    TArray<TSubclassOf<class UMechaAbilityBase>> StartingAbilities;
};
