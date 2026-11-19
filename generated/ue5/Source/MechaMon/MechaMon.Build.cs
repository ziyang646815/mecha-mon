// ============================================================================
// MECHA·MON - UE5 Real-time Combat System (GAS)
// 由 MECHA·MON 数据驱动构建系统生成 · 生产级代码基座
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
            "GameplayAbilities", "GameplayTags", "GameplayTasks",
            "AnimGraphRuntime"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "UMG", "Slate", "SlateCore", "NetCore"
        });
    }
}
