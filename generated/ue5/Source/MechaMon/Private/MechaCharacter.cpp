// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "MechaCharacter.h"
#include "MechaAttributeSet.h"
#include "MechaAbilityBase.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"

AMechaCharacter::AMechaCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
    AbilitySystemComponent->SetIsReplicated(true);
    AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);

    AttributeSet = CreateDefaultSubobject<UMechaAttributeSet>(TEXT("AttributeSet"));
}

// 在 BeginPlay 或 PossessedBy 中授予初始技能：
// for (TSubclassOf<UMechaAbilityBase> Ability : StartingAbilities)
// {
//     AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(Ability, 1, INDEX_NONE, this));
// }
// AbilitySystemComponent->InitAbilityActorInfo(this, this);
