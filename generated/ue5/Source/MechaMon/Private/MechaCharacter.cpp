// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#include "MechaCharacter.h"
#include "MechaAttributeSet.h"
#include "Combat/HitboxComponent.h"
#include "Combat/ParryComponent.h"
#include "AbilitySystemComponent.h"
#include "Abilities/GameplayAbility.h"

AMechaCharacter::AMechaCharacter()
{
    PrimaryActorTick.bCanEverTick = false;

    AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
    AbilitySystemComponent->SetIsReplicated(true);
    AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Mixed);

    AttributeSet = CreateDefaultSubobject<UMechaAttributeSet>(TEXT("AttributeSet"));
    HitboxComponent = CreateDefaultSubobject<UHitboxComponent>(TEXT("HitboxComponent"));
    ParryComponent = CreateDefaultSubobject<UParryComponent>(TEXT("ParryComponent"));

    // [扩展点] 在 BeginPlay / PossessedBy 中：
    // for (TSubclassOf<UCombatAbility> Ability : StartingAbilities)
    // {
    //     AbilitySystemComponent->GiveAbility(FGameplayAbilitySpec(Ability, 1, INDEX_NONE, this));
    // }
    // AbilitySystemComponent->InitAbilityActorInfo(this, this);
    // ParryComponent->Initialize(AbilitySystemComponent);
}
