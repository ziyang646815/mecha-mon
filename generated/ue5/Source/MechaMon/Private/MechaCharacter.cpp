// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
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
