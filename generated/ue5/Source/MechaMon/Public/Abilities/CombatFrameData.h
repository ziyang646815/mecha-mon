// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
// ============================================================================
#pragma once

#include "CoreMinimal.h"
#include "DataAsset.h"
#include "GameplayTagContainer.h"
#include "CombatFrameData.generated.h"

/** 招式帧数据：判定规则与动画表现解耦，策划在编辑器中即可调校手感 */
UCLASS(BlueprintType)
class MECHAMON_API UCombatFrameData : public UDataAsset
{
    GENERATED_BODY()

public:
    // // 示例：Flame Jab 起手 4 / 判定 3 / 收招 8 / 伤害 7（源自 config/game_data.py）

    /** 起手帧：无 hitbox 判定，可被弹反 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 StartupFrames = 4;

    /** 判定帧：hitbox 有效窗口 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 ActiveFrames = 3;

    /** 收招帧：后摇，此阶段被命中触发 Counter Hit */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 RecoveryFrames = 8;

    /** 弹反有效帧（仅系统弹反招式使用） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 ParryWindow = 0;

    /** 霸体等级：0 无 / 1 抗轻击 / 2 完全霸体 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 ArmorLevel = 0;

    /** 取消窗口：从判定结束到收招结束的可取消帧数 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    int32 CancelWindow = 0;

    /** 可取消到的招式类别（轻击 / 重击 / 必杀 / 超必杀） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Frames")
    FGameplayTagContainer CancelRoutes;

    /** 命中停顿帧 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 HitstopFrames = 4;

    /** 基础伤害与硬直 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 Damage = 0;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 HitstunFrames = 14;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    int32 BlockstunFrames = 8;

    /** 能量消耗与收益 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Meter")
    int32 MeterCost = 0;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Meter")
    int32 MeterGain = 0;

    /** 有效距离与击退 */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    float Reach = 60.f;
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Impact")
    float Knockback = 0.f;

    /** 招式标签（Ability.Mecha.*） */
    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category = "Combat|Identity")
    FGameplayTag AbilityTag;

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetTotalFrames() const { return StartupFrames + ActiveFrames + RecoveryFrames; }

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetActiveStartFrame() const { return StartupFrames; }

    UFUNCTION(BlueprintPure, Category = "Combat|Frames")
    int32 GetRecoveryStartFrame() const { return StartupFrames + ActiveFrames; }
};
