# -*- coding: utf-8 -*-
"""文档生成器：输出 GDD / 技术架构 / 竞技规则 / 项目路线图。"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.game_data import (
    ELEMENTS, TYPE_CHART, TYPE_MAP, MECHAS, BATTLE_RULES,
    PHASES, GAS_ARCHITECTURE, all_abilities_flat,
)
from config.project_config import PROJECT


def _table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def generate_gdd() -> str:
    lines = [
        f"# {PROJECT['codename']} 游戏设计文档（GDD）",
        "",
        f"> 版本 {PROJECT['version']} · 引擎 {PROJECT['engine']} · 技术框架 {PROJECT['framework']}",
        "",
        "## 1. 产品概述",
        "",
        f"**{PROJECT['name_cn']}**（{PROJECT['name_en']}）是一款以机甲收集与回合制策略对战为核心的竞技游戏。"
        "玩家扮演机甲指挥官，组建 3 台机甲的作战小队，通过属性克制、技能组合与能量管理击败对手。",
        "",
        f"- **一句话定位**：{PROJECT['tagline']}",
        f"- **游戏类型**：{PROJECT['genre']}",
        f"- **目标平台**：{PROJECT['platform']}",
        f"- **核心体验**：收集 → 养成 → 构筑 → 竞技",
        "",
        "## 2. 核心玩法循环",
        "",
        "```text",
        "登录 → 选择机甲小队 → 匹配对手 → Ban/Pick → 3v3 回合制对战 → 结算段位/奖励",
        "        ↑                                                              ↓",
        "        └──────────── 获得零件 → 改装机甲 → 解锁新技能 ←──────────────┘",
        "```",
        "",
        "## 3. 属性克制体系",
        "",
        f"当前共 **{len(ELEMENTS)}** 种属性，形成循环克制关系。克制伤害为 2 倍，被抵抗为 0.5 倍。",
        "",
    ]
    rows = []
    for e in ELEMENTS:
        c = TYPE_CHART[e.key]
        rows.append([
            f"{e.name_cn} `{e.key}`",
            "、".join(TYPE_MAP[x].name_cn for x in c["strong"]) or "—",
            "、".join(TYPE_MAP[x].name_cn for x in c["weak"]) or "—",
            e.description,
        ])
    lines.append(_table(["属性", "2× 克制", "0.5× 抵抗", "定位描述"], rows))
    lines += ["", "## 4. 机甲图鉴", "", f"首批 **{len(MECHAS)}** 台机甲，每台配备 4 个专属技能。", ""]
    rows = []
    for m in MECHAS:
        rows.append([m.codename, m.name_cn, TYPE_MAP[m.element].name_cn, m.role,
                     f"{m.hp}/{m.atk}/{m.dfn}/{m.spd}", m.abilities[0].name_cn])
    lines.append(_table(["编号", "名称", "属性", "定位", "HP/攻/防/速", "代表技能"], rows))
    lines += ["", "### 4.1 技能清单（按机甲）", ""]
    for m in MECHAS:
        lines += [f"#### {m.name_cn} · {TYPE_MAP[m.element].name_cn}", "", m.lore, ""]
        lines.append(_table(
            ["技能", "类型", "威力", "耗能", "CD", "GameplayTag", "说明"],
            [[a.name_cn, a.category, a.power or "—", a.cost, a.cooldown, a.gameplay_tag, a.description]
             for a in m.abilities],
        ))
        lines.append("")
    lines += [
        "## 5. 养成系统",
        "",
        "- **核心模块**：机甲等级、装甲强化、武器精通、能源核心（4 条养成线）",
        "- **改装槽位**：每台机甲 3 个模块槽（攻击/防御/功能），通过竞技获得零件",
        "- **技能解锁**：等级 5/10/15/20 依次解锁 4 个技能，避免新手信息过载",
        "- **平衡原则**：养成仅影响数值上限的 ±10%，竞技场采用标准化数值（公平对战）",
        "",
        "## 6. 竞技模式",
        "",
        f"- **对战形式**：{BATTLE_RULES['battle_format']}",
        f"- **队伍规模**：{BATTLE_RULES['team_size']} 台机甲",
        f"- **回合上限**：{BATTLE_RULES['turn_limit']} 回合，超时按剩余装甲百分比判定",
        f"- **禁用阶段**：{BATTLE_RULES['ban_phase']}",
        f"- **段位体系**：{BATTLE_RULES['ranking']}",
        "",
        "## 7. 与非机甲IP的差异化",
        "",
        "1. **能量管理**：技能消耗能量而非传统 PP，引入资源博弈",
        "2. **部位破坏**：重击可破坏机甲部位，降低对应属性（开发中）",
        "3. **换人代价**：换人消耗能量，抑制无脑轮换",
        "4. **电竞友好**：回合制 + 明确克制关系，观赛门槛低、可读性强",
        "",
    ]
    return "\n".join(lines)


def generate_tech_doc() -> str:
    lines = [
        f"# {PROJECT['codename']} 技术架构设计（UE5 + GAS）",
        "",
        f"> 引擎：{PROJECT['engine']} · 框架：{PROJECT['framework']} · 版本 {PROJECT['version']}",
        "",
        "## 1. 为什么选择 GAS",
        "",
        "Gameplay Ability System 天然契合回合制竞技游戏的需求：",
        "",
        "- **统一能力模型**：技能、道具、状态均抽象为 Ability + Effect，规则一致",
        "- **属性与效果解耦**：AttributeSet 管理数值，GameplayEffect 负责修改，便于平衡调整",
        "- **标签驱动逻辑**：GameplayTag 描述状态与克制关系，避免布尔标志地狱",
        "- **网络同步**：内置客户端预测与服务器权威校验，适合竞技对战",
        "- **数据驱动**：技能配置可放在 DataAsset，策划可独立迭代",
        "",
        "## 2. 核心架构分层",
        "",
    ]
    lines.append(_table(
        ["组件", "职责"],
        [[n, d] for n, d in GAS_ARCHITECTURE],
    ))
    lines += [
        "",
        "## 3. 类图（概念）",
        "",
        "```text",
        "AMechaCharacter (ACharacter)",
        "  ├── UAbilitySystemComponent  ──→ 技能/效果/标签的统一入口",
        "  ├── UMechaAttributeSet       ──→ Health / Energy / Attack / Defense / Speed",
        "  └── UMechaAbilityBase        ──→ 继承自 UGameplayAbility",
        "                                    ├── UFlameRamAbility",
        "                                    ├── UMagmaShieldAbility",
        "                                    └── ... (共 32 个)",
        "",
        "ABattleManager (AGameStateBase)",
        "  ├── 回合调度与先手计算",
        "  ├── 换人判定（消耗能量）",
        "  └── 胜负结算与回放记录",
        "```",
        "",
        "## 4. 标签体系（GameplayTag）",
        "",
        "```text",
        "Mecha.Type.Fire / Water / Electric / Leaf / Steel / Quantum / Shadow / Ice",
        "Ability.Mecha.*        # 32 个技能标签",
        "Status.Burning         # 灼烧（DoT）",
        "Status.Frozen          # 冻结（跳过回合）",
        "Status.Shielded        # 护盾",
        "Status.Stunned         # 眩晕",
        "Status.Overdrive       # 攻击提升",
        "Event.Hit / Event.Switch / Event.Knockout",
        "```",
        "",
        "## 5. 伤害结算管线",
        "",
        "```text",
        "1. 技能激活 → CanActivateAbility() 校验能量/CD/控制状态",
        "2. 构造 FGameplayEffectSpec → 设置 SetByCaller 威力系数",
        "3. 应用 GameplayEffect → AttributeSet::PostGameplayEffectExecute()",
        "4. 计算属性克制倍率（读取 Mecha.Type.* 标签）",
        "5. 扣除生命 → 触发 GameplayCue 表现（特效/音效/震动）",
        "6. 广播 Event.Hit → 战斗日志与 UI 更新",
        "```",
        "",
        "## 6. 网络架构",
        "",
        "- **权威模型**：服务器全权判定伤害、命中与随机数（防作弊）",
        "- **客户端预测**：技能释放即时播放动画，服务器回包后校正",
        "- **随机数同步**：使用可复现的种子（战斗 ID + 回合数），支持回放校验",
        "- **状态复制**：仅复制 ASC 的必要属性与标签，降低带宽",
        "",
        "## 7. 目录结构（UE5 工程）",
        "",
        "```text",
        "Source/MechaMon/",
        "├── Public/",
        "│   ├── MechaCharacter.h        # 机甲角色基类",
        "│   ├── MechaAttributeSet.h     # 属性集",
        "│   ├── Abilities/MechaAbilityBase.h",
        "│   ├── Effects/MechaEffects.h  # GameplayEffect 定义",
        "│   ├── Battle/BattleManager.h  # 回合调度",
        "│   └── Tags/MechaGameplayTags.h",
        "└── Private/                   # 对应 .cpp 实现",
        "```",
        "",
        "## 8. 性能与扩展",
        "",
        f"- 首批 {len(all_abilities_flat())} 个技能，单场战斗最多 6 台机甲同时存在，性能压力可控",
        "- GameplayCue 采用对象池，避免频繁创建特效",
        "- DataAsset 热重载，支持策划在不重编译的情况下调整数值",
        "- 预留部位破坏、天气场地等扩展点（通过额外标签实现）",
        "",
    ]
    return "\n".join(lines)


def generate_roadmap() -> str:
    lines = [
        f"# {PROJECT['codename']} 项目规划与路线图",
        "",
        f"> 版本 {PROJECT['version']} · 当前进入核心战斗验证阶段",
        "",
        "## 1. 项目里程碑",
        "",
    ]
    lines.append(_table(
        ["阶段", "名称", "周期", "核心目标", "交付物", "状态"],
        [[p["id"], p["name"], p["duration"], p["goal"], " / ".join(p["deliverables"]), p["status"]]
         for p in PHASES],
    ))
    lines += [
        "",
        "## 2. 团队配置建议",
        "",
        _table(["角色", "人数", "职责"], [
            ["制作人/策划", "1", "整体设计、数值平衡、进度把控"],
            ["UE5 程序", "2", "GAS 框架、战斗系统、网络同步"],
            ["技术美术", "1", "机甲材质、技能特效、GameplayCue"],
            ["3D 美术", "2", "机甲建模、动画、场景"],
            ["UI/UX", "1", "战斗界面、图鉴、排位界面"],
            ["QA", "1", "功能测试、平衡性测试"],
        ]),
        "",
        "## 3. 风险与对策",
        "",
        _table(["风险", "影响", "对策"], [
            ["GAS 学习曲线陡峭", "开发延期", "先做垂直切片，建立内部 Ability 模板库"],
            ["数值平衡难度高", "竞技体验受损", "搭建自动对战模拟脚本，快速迭代"],
            ["机甲美术产能不足", "内容更新慢", "模块化拼装 + 共用骨架，降低单台成本"],
            ["竞技匹配冷启动", "玩家流失", "先做 AI 对战与好友对战，积累用户后开启排位"],
        ]),
        "",
        "## 4. 本期交付清单",
        "",
        "- [x] 游戏设计文档（GDD）",
        "- [x] UE5 + GAS 技术架构文档",
        "- [x] 竞技规则与数值框架",
        "- [x] UE5 C++ 生产级代码基座（可直接导入工程）",
        "- [x] Python 数据驱动构建系统（单一数据源）",
        "- [x] 官方交互式产品演示（战斗模拟 / 机甲图鉴 / 技术架构 / 路线图）",
        "",
        "## 5. 下一步",
        "",
        "1. 搭建 UE5 工程，导入 `generated/ue5/Source/MechaMon` 代码基座",
        "2. 在编辑器中配置 GameplayTag 与 DataAsset",
        "3. 实现首台机甲的完整战斗闭环（炎狱·赤焰 vs 潮汐·沧澜）",
        "4. 用数值模拟脚本验证克制关系与平衡性",
        "",
    ]
    return "\n".join(lines)


def generate_rules_doc() -> str:
    lines = [
        f"# {PROJECT['codename']} 竞技规则与数值框架",
        "",
        "> 本文档定义对战的规则层，所有数值由 Python 配置驱动，可快速调整。",
        "",
        "## 1. 对战基础规则",
        "",
        _table(["项目", "数值/规则"], [[k, v] for k, v in BATTLE_RULES.items()]),
        "",
        "## 2. 伤害计算公式",
        "",
        "```text",
        "基础伤害 = 技能威力 × (攻击方攻击 / 防御方防御) × 属性克制倍率 × 暴击倍率",
        "属性克制倍率 = 2.0 (克制) / 1.0 (中性) / 0.5 (抵抗) / 0.0 (免疫)",
        "暴击倍率 = 1.5 (基础) + 装备修正",
        "最终伤害 = max(1, floor(基础伤害 × 随机波动(0.95~1.05)))",
        "```",
        "",
        "## 3. 行动顺序",
        "",
        "1. 按速度属性降序排列（同速时按服务器随机数）",
        "2. 拥有先手标签的技能优先结算",
        "3. 冻结/眩晕状态跳过回合",
        "4. 每回合结束回复 12 点能量（上限 120）",
        "",
        "## 4. 状态效果表",
        "",
        _table(["状态", "GameplayTag", "效果", "持续"], [
            ["灼烧", "Status.Burning", "每回合 12 点伤害", "3 回合"],
            ["冻结", "Status.Frozen", "跳过行动", "1 回合"],
            ["护盾", "Status.Shielded", "吸收伤害", "2 回合"],
            ["眩晕", "Status.Stunned", "跳过行动", "1 回合"],
            ["超频", "Status.Overdrive", "攻击 +40%", "3 回合"],
            ["减速", "Status.Slowed", "速度 -30%", "2 回合"],
        ]),
        "",
        "## 5. 平衡性约束",
        "",
        f"- 共 {len(MECHAS)} 台机甲、{len(all_abilities_flat())} 个技能",
        "- 单台机甲 4 个技能，耗能区间 16~32，CD 区间 0~4",
        "- 属性克制闭环确保无绝对强势属性",
        "- 竞技场采用标准化数值，养成仅影响 ±10%",
        "",
    ]
    return "\n".join(lines)


def generate_all():
    DOCS = Path(__file__).resolve().parent.parent / "docs"
    DOCS.mkdir(parents=True, exist_ok=True)
    outputs = {
        "01_游戏设计文档_GDD.md": generate_gdd(),
        "02_技术架构_UE5_GAS.md": generate_tech_doc(),
        "03_项目规划_路线图.md": generate_roadmap(),
        "04_竞技规则与数值.md": generate_rules_doc(),
    }
    for name, content in outputs.items():
        (DOCS / name).write_text(content, encoding="utf-8")
    return list(outputs.keys())
