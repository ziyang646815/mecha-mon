// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MechaCharacter.generated.h"

class UAbilitySystemComponent;
class UMechaAttributeSet;
class UHitboxComponent;
class UParryComponent;
class UMechaAnimInstance;
class UCombatFrameData;

/** 机甲角色：挂载 ASC、属性集与实时格斗组件，是 1v1 对战中的基本单位 */
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

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UHitboxComponent* GetHitboxComponent() const { return HitboxComponent; }

    UFUNCTION(BlueprintCallable, Category = "Mecha")
    UParryComponent* GetParryComponent() const { return ParryComponent; }

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

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat")
    TObjectPtr<UHitboxComponent> HitboxComponent;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Combat")
    TObjectPtr<UParryComponent> ParryComponent;

    /** 初始招式列表（帧数据 DataAsset 驱动） */
    UPROPERTY(EditDefaultsOnly, Category = "Combat")
    TArray<TSubclassOf<class UCombatAbility>> StartingAbilities;

    /** 输入回放记录的按键位掩码 */
    uint32 CurrentInputMask = 0;
};
