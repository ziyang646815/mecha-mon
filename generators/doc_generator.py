# -*- coding: utf-8 -*-
"""文档生成器：输出 GDD / 技术架构 / 竞技规则 / 项目路线图。

所有文档均从 config/game_data.py 的帧驱动战斗数据读取，确保策划、工程与展示三者一致。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.game_data import (
    ELEMENTS, TYPE_CHART, TYPE_MAP, MECHAS, SYSTEM_MOVES, BATTLE_RULES,
    PHASES, GAS_ARCHITECTURE, all_moves_flat,
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
        f"**{PROJECT['name_cn']}**（{PROJECT['name_en']}）是一款以帧级操作为核心的 "
        "**实时 1v1 机甲格斗**竞技产品。玩家以单机甲身份进入战场，在固定 60Hz 逻辑帧上"
        "通过起手、判定、收招的精确博弈，配合弹反、防御、霸体与取消路线击败对手。",
        "",
        f"- **一句话定位**：{PROJECT['tagline']}",
        f"- **游戏类型**：{PROJECT['genre']}",
        f"- **目标平台**：{PROJECT['platform']}",
        f"- **核心体验**：匹配 → Ban/Pick → 实时对战 → 段位结算",
        "",
        "## 2. 核心玩法循环",
        "",
        "```text",
        "进入匹配 → Ban/Pick（各禁用 2 台） → 选定机甲 → BO3 实时对战 → 结算段位/奖励",
        "     ↑                                                              ↓",
        "     └──────────── 复盘帧数据 → 调整打法与取消路线 ←────────────────┘",
        "```",
        "",
        f"对战采用 **{BATTLE_RULES['battle_format']}**，单局 {BATTLE_RULES['round_time_sec']} 秒，"
        f"先胜 {BATTLE_RULES['rounds_to_win']} 局者获胜。全部判定运行在 "
        f"{BATTLE_RULES['logic_tick_hz']}Hz 固定逻辑帧上：{BATTLE_RULES['render_mode']}。",
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

    lines += [
        "",
        "## 4. 机甲图鉴与招式帧数据",
        "",
        f"首批 **{len(MECHAS)}** 台机甲，每台配备 4 个专属招式（轻击 / 重击 / 必杀 / 超必杀），"
        f"合计 **{len(all_moves_flat())}** 个招式。帧数据决定手感与博弈，动画表现与判定完全解耦。",
        "",
    ]
    rows = []
    for m in MECHAS:
        rows.append([m.codename, m.name_cn, TYPE_MAP[m.element].name_cn, m.role,
                     f"{m.hp}/{m.atk}/{m.dfn}/{m.spd}"])
    lines.append(_table(["编号", "名称", "属性", "定位", "HP/攻/防/速"], rows))
    lines += [
        "",
        "> 帧数据列含义：**起手**（无判定前摇）/ **判定**（hitbox 有效帧）/ **收招**（后摇，"
        "被命中触发 Counter Hit）/ **霸体**（0 无、1 抗轻击、2 完全）/ **取消**（可接续的招式类别）。"
        "总帧数 = 起手 + 判定 + 收招。",
        "",
    ]
    for m in MECHAS:
        lines += [f"### 4.{MECHAS.index(m) + 1} {m.name_cn} · {TYPE_MAP[m.element].name_cn}", "", m.lore, ""]
        lines.append(_table(
            ["招式", "类型", "指令", "起手", "判定", "收招", "总帧", "伤害", "霸体", "取消路线"],
            [[mv.name_cn, mv.cls, mv.input, mv.startup, mv.active, mv.recovery,
              mv.total_frames, mv.damage, mv.armor, mv.cancel] for mv in m.moves],
        ))
        lines.append("")

    lines += [
        "## 5. 操作系统",
        "",
        "所有机甲共享一套操作系统，构成实时格斗的底层博弈：防御与弹反共享 S 键，"
        "长按与瞬间输入对应完全不同的风险收益。",
        "",
    ]
    lines.append(_table(
        ["操作", "指令", "起手", "有效/收招", "关键参数", "说明"],
        [[mv.name_cn, mv.input, mv.startup,
          f"{mv.active}/{mv.recovery}",
          f"弹反窗口 {mv.parry_window} 帧" if mv.parry_window else "—",
          mv.description] for mv in SYSTEM_MOVES],
    ))
    lines += [
        "",
        f"- **弹反**：按下 S 的前 {BATTLE_RULES['parry_window_frames']} 帧为弹反窗口；成功弹反使对手陷入 "
        f"{BATTLE_RULES['parry_punish_frames']} 帧硬直，并获得 {BATTLE_RULES['parry_meter_reward']} 点能量。",
        "- **防御**：按住 S 持续减伤，消耗防御槽；防御槽清空即破防，随后进入长硬直。",
        "- **跳跃 / 冲刺**：推进跳跃可规避地面判定，瞬时冲刺用于拉近或拉开距离，均可在取消窗口中使用。",
        "",
        "## 6. 竞技模式",
        "",
        f"- **对战形式**：{BATTLE_RULES['battle_format']}",
        f"- **队伍规模**：{BATTLE_RULES['team_size']} 台机甲（单挑）",
        f"- **单局时长**：{BATTLE_RULES['round_time_sec']} 秒",
        f"- **禁用阶段**：{BATTLE_RULES['ban_phase']}",
        f"- **逻辑帧率**：{BATTLE_RULES['logic_tick_hz']}Hz（{BATTLE_RULES['render_mode']}）",
        f"- **段位体系**：{BATTLE_RULES['ranking']}",
        "",
        "## 7. 差异化设计",
        "",
        "1. **帧级操作深度**：起手/判定/收招逐帧可调，配合输入缓冲与取消窗口，形成可钻研的操作上限。",
        "2. **弹反博弈**：4 帧弹反窗口带来高风险高回报的读招对抗，是高端局的核心心理战。",
        "3. **霸体与取消**：霸体等级抵消压制，取消路线（轻→重→必杀→超必杀）构筑连段与资源管理。",
        "4. **Control Rig 混合动画**：动捕基础姿态叠加程序化机甲化与二级运动，兼顾重量感与判定精度。",
        "5. **电竞观赏性**：1v1 单挑、帧数据可读、hitstop 打击感强，观赛门槛低且回放可量化复盘。",
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
        "Gameplay Ability System 天然契合实时帧驱动格斗的需求：",
        "",
        "- **统一能力模型**：招式、弹反、防御、跳跃、冲刺均抽象为 Ability，规则一致、可复用。",
        "- **标签驱动状态**：HitStun / BlockStun / Armor 等以 GameplayTag 描述，避免布尔标志地狱，"
        "并且天然支持取消规则与 Counter Hit 判定。",
        "- **属性与效果解耦**：AttributeSet 管理生命/能量/防御槽，GameplayEffect 负责修改，便于平衡调整。",
        "- **帧数据可配置**：招式的起手/判定/收招封装为 FCombatFrameData DataAsset，策划可独立迭代手感。",
        "- **网络同步**：内置客户端预测与服务器权威校验，配合输入回放与回滚，满足竞技对战低延迟要求。",
        "- **表现与判定解耦**：命中产生 GameplayCue 与 hitstop，动画仅负责表现，不影响判定结果。",
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
        "  ├── UAbilitySystemComponent        ──→ 招式/效果/标签的统一入口",
        "  ├── UMechaAttributeSet             ──→ Health / Meter / Guard / Attack / Defense / Speed",
        "  ├── UCombatAbility                 ──→ 帧数据驱动招式（继承 UGameplayAbility）",
        "  │     └── FCombatFrameData         ──→ Startup/Active/Recovery/ParryWindow/Armor/Cancel/Hitstop (DataAsset)",
        "  ├── UHitboxComponent               ──→ 自定义 hitbox / hurtbox 查询",
        "  ├── UParryComponent                ──→ 弹反窗口判定与硬直反馈",
        "  └── UMechaAnimInstance             ──→ Control Rig 混合动画与程序化二级运动",
        "",
        "UHitstopSubsystem (UGameInstanceSubsystem)",
        "  └── 命中停顿帧调度，统一控制打击节奏",
        "",
        "CombatReplaySubsystem (UGameInstanceSubsystem)",
        "  ├── 帧步进调试 / 输入回放 / 战斗日志",
        "  └── 服务器权威校验与回滚数据支撑",
        "```",
        "",
        "## 4. 标签体系（GameplayTag）",
        "",
        "```text",
        "Mecha.Type.Fire / Water / Electric / Leaf / Steel / Quantum / Shadow / Ice",
        "Ability.Mecha.*        # 32 个招式标签",
        "Ability.System.*       # Guard / Parry / BoostJump / BoostDash",
        "Status.HitStun         # 命中硬直",
        "Status.BlockStun       # 防御硬直",
        "Status.Armor           # 霸体等级",
        "Event.Parry            # 弹反成功",
        "Event.CounterHit       # 反击命中（对手起手/后摇被击中）",
        "Event.Hit / Event.Knockout",
        "```",
        "",
        "## 5. 命中判定管线（帧驱动）",
        "",
        "```text",
        "1. 起手帧  → UCombatAbility 激活，播放动捕+Control Rig 表现，此时无判定",
        "2. 判定帧  → UHitboxComponent 每逻辑帧查询 hitbox/hurtbox 重叠",
        "3. 命中查询 → 读取防守方标签：Status.Armor（霸体抵消）/ Event.Parry（4 帧窗口）",
        "4. 防御判定 → 若按住防御且防御槽充足，进入 BlockStun 并消耗防御槽；清空则破防",
        "5. hitstop  → UHitstopSubsystem 冻结双方指定帧，制造打击停顿",
        "6. 僵直     → 写入 Status.HitStun / Status.BlockStun，防守方进入硬直",
        "7. 取消     → 检查 CancelWindow 与取消路线（轻→重→必杀→超必杀），允许则接续下一招",
        "8. 表现     → 广播 GameplayCue（特效/音效/镜头震动）与战斗日志",
        "```",
        "",
        "## 6. 网络架构",
        "",
        "- **权威模型**：服务器以固定逻辑帧全权判定命中、弹反、僵直与伤害（防作弊）。",
        "- **客户端预测**：本地输入立即播放动画与 hitstop，服务器回包后校正，保证操作跟手。",
        "- **输入回放**：客户端按帧上传输入序列（含输入缓冲），服务器可逐帧重演校验结果。",
        "- **Rollback 思路**：预测偏差时回退到分歧帧并重演，最大限度降低网络延迟对格斗手感的影响。",
        "- **状态复制**：仅复制 ASC 必要属性与标签，GameplayCue 使用预测 Key 去重，降低带宽。",
        "",
        "## 7. 目录结构（UE5 工程）",
        "",
        "```text",
        "Source/MechaMon/",
        "├── Public/",
        "│   ├── MechaCharacter.h            # 机甲角色基类（ASC + AttributeSet + 判定组件）",
        "│   ├── MechaAttributeSet.h         # 属性集",
        "│   ├── Abilities/CombatAbility.h   # 帧数据驱动招式基类",
        "│   ├── Abilities/CombatFrameData.h # FCombatFrameData DataAsset",
        "│   ├── Combat/HitboxComponent.h    # hitbox/hurtbox 查询",
        "│   ├── Combat/ParryComponent.h     # 弹反窗口",
        "│   ├── Animation/MechaAnimInstance.h # Control Rig 混合动画",
        "│   ├── Subsystems/HitstopSubsystem.h # 命中停顿",
        "│   ├── Subsystems/CombatReplaySubsystem.h # 帧步进/回放",
        "│   └── Tags/MechaGameplayTags.h",
        "└── Private/                       # 对应 .cpp 实现",
        "```",
        "",
        "## 8. 性能与扩展",
        "",
        f"- 首批 {len(all_moves_flat())} 个招式，单场 1v1 仅两台机甲，判定查询与 hitstop 调度开销可控",
        "- GameplayCue 采用对象池，避免命中高频触发时频繁创建特效",
        "- FCombatFrameData 支持热重载，策划无需重编译即可调整帧窗口与伤害",
        "- 判定与表现解耦，新增机甲复用帧数据模板与 Control Rig 管线，边际成本递减",
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
            ["制作人/策划", "1", "整体设计、帧数据与数值平衡、进度把控"],
            ["UE5 程序", "2", "GAS 战斗系统、判定/弹反、网络同步与回滚"],
            ["技术美术", "1", "Control Rig 混合动画、机甲材质、GameplayCue"],
            ["3D 美术", "2", "机甲建模、动捕精修、战场场景"],
            ["UI/UX", "1", "战斗 HUD、帧数据监视器、图鉴与排位界面"],
            ["QA", "1", "手感测试、帧数据验证与平衡性测试"],
        ]),
        "",
        "## 3. 风险与对策",
        "",
        _table(["风险", "影响", "对策"], [
            ["弹反手感调校难度高", "操作体验受损", "用帧步进工具 + 判定盒可视化 + 输入回放量化调参"],
            ["GAS 学习曲线陡峭", "开发延期", "先做垂直切片，建立内部 Ability 与帧数据模板库"],
            ["帧数据与动画不同步", "判定失真", "判定与表现解耦，帧数据单一数据源驱动"],
            ["网络延迟影响格斗手感", "竞技体验下降", "客户端预测 + 输入回放 + 回滚，服务器权威校验"],
        ]),
        "",
        "## 4. 本期交付清单",
        "",
        "- [x] 游戏设计文档（GDD）",
        "- [x] UE5 + GAS 技术架构文档",
        "- [x] 竞技规则与数值框架",
        "- [x] UE5 C++ 生产级代码基座（可直接导入工程）",
        "- [x] Python 数据驱动构建系统（单一数据源）",
        "- [x] 官方交互式产品演示（实时操作格斗 / 帧数据监视器 / 机甲图鉴 / 技术架构 / 路线图）",
        "",
        "## 5. 下一步",
        "",
        "1. 导入 `generated/ue5/Source/MechaMon` 生产级代码基座，搭建 UE5 工程",
        "2. 在编辑器中配置帧数据 DataAsset（起手 / 判定 / 收招 / 弹反窗口 / 霸体 / 取消）",
        "3. 实现弹反—僵直垂直切片，跑通单机甲对单机甲的实时操作闭环",
        "4. 接入帧步进调试与判定盒可视化，逐帧验证手感与数值",
        "",
    ]
    return "\n".join(lines)


def generate_rules_doc() -> str:
    lines = [
        f"# {PROJECT['codename']} 竞技规则与数值框架",
        "",
        "> 本文档定义实时格斗的规则层，所有数值由 Python 配置驱动，可快速调整。",
        "",
        "## 1. 对战基础规则",
        "",
        _table(["项目", "数值/规则"], [[k, v] for k, v in BATTLE_RULES.items()]),
        "",
        "## 2. 招式帧数据表",
        "",
        "全部招式运行在 60Hz 逻辑帧上。列含义：起手（前摇）/ 判定（hitbox 有效）/ 收招（后摇）/ "
        "命中硬直 / 防御硬直 / 命中停顿 / 霸体 / 取消路线。",
        "",
    ]
    for m in MECHAS:
        lines += [f"### {m.name_cn} · {TYPE_MAP[m.element].name_cn}", ""]
        lines.append(_table(
            ["招式", "指令", "起手", "判定", "收招", "命中硬直", "防御硬直", "命中停顿", "霸体", "取消路线"],
            [[mv.name_cn, mv.input, mv.startup, mv.active, mv.recovery, mv.hitstun,
              mv.blockstun, mv.hitstop, mv.armor, mv.cancel] for mv in m.moves],
        ))
        lines.append("")

    lines += [
        "## 3. 伤害与修正规则",
        "",
        "```text",
        "命中伤害 = 招式伤害 × 属性克制倍率 × 连招衰减 × Counter Hit 修正",
        "属性克制倍率 = 2.0 (克制) / 1.0 (中性) / 0.5 (抵抗) / 0.0 (免疫)",
        f"连招衰减   = {BATTLE_RULES['combo_scaling']}",
        f"Counter Hit = {BATTLE_RULES['counter_hit']}",
        "最终伤害 = max(1, floor(命中伤害))",
        "```",
        "",
        f"- **连招伤害递减**：{BATTLE_RULES['combo_scaling']}，抑制无限连，鼓励重新起手。",
        f"- **Counter Hit**：{BATTLE_RULES['counter_hit']}。",
        f"- **取消路线**：{BATTLE_RULES['cancel_route']}，仅可在取消窗口内衔接。",
        f"- **输入缓冲**：{BATTLE_RULES['input_buffer_frames']} 帧，提升操作容错。",
        "",
        "## 4. 弹反与防御规则",
        "",
        f"- **弹反窗口**：按下 S 的前 {BATTLE_RULES['parry_window_frames']} 帧。",
        f"- **弹反成功**：对手陷入 {BATTLE_RULES['parry_punish_frames']} 帧硬直，"
        f"弹反方获得 {BATTLE_RULES['parry_meter_reward']} 点能量（上限 {BATTLE_RULES['meter_max']}）。",
        f"- **普通防御**：按住 S 持续减伤，消耗防御槽（上限 {BATTLE_RULES['guard_max']}）；"
        "防御槽清空即破防，进入长硬直。",
        "- **风险收益**：弹反失败会暴露于对手的完整起手，防御虽稳但无法反击，构成读招博弈。",
        "",
        "## 5. 霸体与命中判定",
        "",
        "- **霸体等级**：0 无霸体；1 抵消单次轻击；2 完全霸体（超必杀级）。",
        f"- **判定策略**：{BATTLE_RULES['hitbox_policy']}。",
        "- **命中停顿（hitstop）**：命中瞬间双方冻结指定帧，强化打击感且不影响逻辑帧判定。",
        "",
        "## 6. 属性克制表",
        "",
    ]
    lines.append(_table(
        ["属性", "2× 克制", "0.5× 抵抗"],
        [[f"{e.name_cn} `{e.key}`",
          "、".join(TYPE_MAP[x].name_cn for x in TYPE_CHART[e.key]["strong"]) or "—",
          "、".join(TYPE_MAP[x].name_cn for x in TYPE_CHART[e.key]["weak"]) or "—"]
         for e in ELEMENTS],
    ))
    lines += [
        "",
        "## 7. 平衡性约束",
        "",
        f"- 共 {len(MECHAS)} 台机甲、{len(all_moves_flat())} 个招式，每台 4 招覆盖轻/重/必杀/超必杀。",
        "- 速攻型机体起手短、伤害低；防御型伤害高但后摇长，机体定位由帧数据体现。",
        "- 属性克制闭环确保无绝对强势属性；超必杀需消耗满能量，资源博弈决定爆发时机。",
        "- 竞技场采用标准化数值，养成仅影响有限区间，保证公平对战。",
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
