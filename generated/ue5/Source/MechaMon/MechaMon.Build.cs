// ============================================================================
// MECHA·MON - UE5 GAS Framework Skeleton
// 由 MechaMonFramework 自动生成 · 代码结构完整，逻辑需按项目需求补充
// ============================================================================
using UnrealBuildTool;

public class MechaMon : ModuleRules
{
    public MechaMon(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core", "CoreUObject", "Engine", "InputCore",
            "GameplayAbilities", "GameplayTags", "GameplayTasks"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "UMG", "Slate", "SlateCore", "NetCore"
        });
    }
}
