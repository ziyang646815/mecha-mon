# -*- coding: utf-8 -*-
"""MECHA·MON 核心战斗数据。

单一数据源（Single Source of Truth）：文档生成器、UE5 代码基座生成器、
官方交互演示全部从本文件读取数据，确保策划、工程与展示三者完全一致。

战斗模型：实时帧驱动的 1v1 机甲格斗（KOF 式操作竞技）。
所有招式以 60Hz 逻辑帧描述，动画表现与判定规则解耦。
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Dict, List


# ---------------------------------------------------------------------------
# 属性（对应 UE5 中的 FGameplayTag: Mecha.Type.*）
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ElementType:
    key: str
    name_cn: str
    name_en: str
    color: str
    accent: str
    tag: str
    description: str


ELEMENTS: List[ElementType] = [
    ElementType("FIRE", "烈焰", "FIRE", "#ff5a2a", "#ffb347",
                "Mecha.Type.Fire", "高温武装，克制机械与冰晶，畏惧涌流。"),
    ElementType("WATER", "涌流", "WATER", "#2b8cff", "#67e8f9",
                "Mecha.Type.Water", "高耐久水装甲，克制烈焰与钢甲。"),
    ElementType("ELECTRIC", "雷霆", "ELECTRIC", "#ffd429", "#fff08a",
                "Mecha.Type.Electric", "极速突袭，克制涌流与钢甲，畏惧森绿。"),
    ElementType("LEAF", "森绿", "LEAF", "#3fbf5f", "#9be28a",
                "Mecha.Type.Leaf", "生态装甲，克制雷霆与暗影。"),
    ElementType("STEEL", "钢甲", "STEEL", "#9aa7bd", "#d7e0ef",
                "Mecha.Type.Steel", "重甲防御，克制冰晶，畏惧烈焰与雷霆。"),
    ElementType("QUANTUM", "星轨", "QUANTUM", "#a855f7", "#d8b4fe",
                "Mecha.Type.Quantum", "空间干涉，克制暗影与森绿。"),
    ElementType("SHADOW", "暗影", "SHADOW", "#6c3fd8", "#b39ddb",
                "Mecha.Type.Shadow", "高爆发刺客，克制星轨，畏惧森绿与星轨。"),
    ElementType("ICE", "冰晶", "ICE", "#4dd0e1", "#b2ebf2",
                "Mecha.Type.Ice", "控制冻阻，克制森绿，畏惧烈焰与钢甲。"),
]

TYPE_MAP: Dict[str, ElementType] = {t.key: t for t in ELEMENTS}

TYPE_CHART: Dict[str, Dict[str, List[str]]] = {
    "FIRE":     {"strong": ["LEAF", "ICE", "STEEL"], "weak": ["WATER", "FIRE"],        "none": []},
    "WATER":    {"strong": ["FIRE", "STEEL"],        "weak": ["LEAF", "ELECTRIC", "WATER"], "none": []},
    "ELECTRIC": {"strong": ["WATER", "STEEL"],       "weak": ["LEAF", "ELECTRIC"],     "none": []},
    "LEAF":     {"strong": ["ELECTRIC", "SHADOW", "WATER"], "weak": ["FIRE", "ICE", "LEAF", "QUANTUM"], "none": []},
    "STEEL":    {"strong": ["ICE"],                   "weak": ["FIRE", "WATER", "ELECTRIC", "STEEL"], "none": []},
    "QUANTUM":  {"strong": ["SHADOW", "LEAF"],       "weak": ["SHADOW", "QUANTUM"],    "none": []},
    "SHADOW":   {"strong": ["QUANTUM"],              "weak": ["LEAF", "SHADOW"],       "none": []},
    "ICE":      {"strong": ["LEAF"],                 "weak": ["FIRE", "STEEL", "ICE"], "none": []},
}


# ---------------------------------------------------------------------------
# 招式帧数据（对应 UE5 的 FCombatFrameData DataAsset + UCombatAbility）
# ---------------------------------------------------------------------------
# 帧语义：
#   startup      前摇帧，期间不可取消、无判定
#   active       判定帧，hitbox 有效
#   recovery     后摇帧，被击中可触发 Counter Hit
#   hitstun      命中后防守方硬直帧（僵直）
#   blockstun    防御后防守方硬直帧
#   hitstop      命中瞬间双方冻结帧（打击感）
#   parry_window 弹反有效帧（仅 System.Parry，在 startup 之后）
#   armor        霸体等级：0 无 / 1 抵消单次轻击 / 2 完全霸体
#   cancel       可取消到的招式类别，构成连招路线
#   input        指令（J 轻击 / K 重击 / L 必杀 / U 超必杀 / S 防御弹反）
@dataclass(frozen=True)
class Move:
    id: str
    name_cn: str
    name_en: str
    type: str
    input: str
    cls: str            # Light / Heavy / Special / Ultimate / System
    damage: int
    startup: int
    active: int
    recovery: int
    hitstun: int
    blockstun: int
    hitstop: int
    parry_window: int
    armor: int
    cancel: str
    reach: int          # 有效距离（演示坐标单位）
    knockback: int
    meter_cost: int
    meter_gain: int
    gameplay_tag: str
    description: str

    @property
    def total_frames(self) -> int:
        return self.startup + self.active + self.recovery


def _mv(mid, cn, en, typ, inp, cls, dmg, su, ac, rc, hs, bs, hstop,
        pw, armor, cancel, reach, kb, mc, mg, tag, desc) -> Move:
    return Move(mid, cn, en, typ, inp, cls, dmg, su, ac, rc, hs, bs, hstop,
                pw, armor, cancel, reach, kb, mc, mg, tag, desc)


# 每台机甲 4 招：轻击 / 重击 / 必杀 / 超必杀。
# 数值差异体现机体定位：速攻型前摇短，防御型伤害高但后摇长。
MOVES: Dict[str, List[Move]] = {
    "BLAZE": [
        _mv("BLZ_L", "烈焰直拳", "Flame Jab", "FIRE", "J", "Light", 7, 4, 3, 8, 14, 8, 4,
            0, 0, "Heavy / Special", 62, 6, 0, 6, "Ability.Mecha.FlameJab", "高热直拳，出招快，可取消接重击。"),
        _mv("BLZ_H", "熔岩重锤", "Magma Hammer", "FIRE", "K", "Heavy", 15, 9, 4, 16, 20, 12, 7,
            0, 0, "Special / Ultimate", 78, 14, 0, 11, "Ability.Mecha.MagmaHammer", "液压重锤，命中造成长时间僵直。"),
        _mv("BLZ_S", "灼热上勾", "Blazing Upper", "FIRE", "L", "Special", 23, 12, 6, 22, 26, 16, 9,
            0, 1, "Ultimate", 96, 22, 25, 16, "Ability.Mecha.BlazingUpper", "带 1 级霸体的上勾拳，可穿过轻击。"),
        _mv("BLZ_U", "超新星爆燃", "Supernova Burst", "FIRE", "U", "Ultimate", 40, 16, 10, 30, 34, 22, 14,
            0, 2, "—", 130, 34, 100, 0, "Ability.Mecha.Supernova", "全身过热爆发，完全霸体，命中即触发大硬直。"),
    ],
    "TIDAL": [
        _mv("TDL_L", "水刃切", "Hydro Slice", "WATER", "J", "Light", 6, 5, 3, 9, 14, 8, 4,
            0, 0, "Heavy / Special", 64, 5, 0, 6, "Ability.Mecha.HydroSlice", "高压水刃，射程略远。"),
        _mv("TDL_H", "潮汐重掌", "Tidal Palm", "WATER", "K", "Heavy", 16, 10, 4, 17, 21, 13, 7,
            0, 1, "Special / Ultimate", 80, 16, 0, 11, "Ability.Mecha.TidalPalm", "带 1 级霸体的重掌，抗轻击压制。"),
        _mv("TDL_S", "深水牢笼", "Abyss Trap", "WATER", "L", "Special", 22, 13, 6, 23, 28, 17, 9,
            0, 1, "Ultimate", 100, 20, 25, 16, "Ability.Mecha.AbyssTrap", "水流禁锢，命中后僵直极长。"),
        _mv("TDL_U", "沧海怒涛", "Ocean Surge", "WATER", "U", "Ultimate", 38, 17, 10, 31, 36, 23, 14,
            0, 2, "—", 132, 30, 100, 0, "Ability.Mecha.OceanSurge", "巨浪冲击，完全霸体并击退。"),
    ],
    "VOLT": [
        _mv("VLT_L", "雷光刺", "Volt Jab", "ELECTRIC", "J", "Light", 6, 3, 3, 7, 13, 7, 3,
            0, 0, "Heavy / Special", 60, 6, 0, 7, "Ability.Mecha.VoltJab", "3 帧前摇，全机甲最快起手。"),
        _mv("VLT_H", "电磁回旋", "EMP Spin", "ELECTRIC", "K", "Heavy", 13, 8, 4, 14, 19, 11, 6,
            0, 0, "Special / Ultimate", 74, 13, 0, 12, "Ability.Mecha.EMPSpin", "回旋踢，收招快，适合连段。"),
        _mv("VLT_S", "瞬闪突进", "Flash Step", "ELECTRIC", "L", "Special", 21, 10, 5, 20, 24, 15, 8,
            0, 0, "Ultimate", 110, 26, 25, 18, "Ability.Mecha.FlashStep", "瞬移突进，射程远但后摇短。"),
        _mv("VLT_U", "雷霆万钧", "Thunderfall", "ELECTRIC", "U", "Ultimate", 36, 14, 9, 27, 32, 21, 13,
            0, 1, "—", 140, 32, 100, 0, "Ability.Mecha.Thunderfall", "高空落雷，1 级霸体，压制力极强。"),
    ],
    "VERDANT": [
        _mv("VRD_L", "藤鞭抽击", "Vine Whip", "LEAF", "J", "Light", 7, 5, 3, 9, 15, 8, 4,
            0, 0, "Heavy / Special", 70, 6, 0, 6, "Ability.Mecha.VineWhip", "藤蔓抽打，射程优于普通轻击。"),
        _mv("VRD_H", "森罗重击", "Verdant Crash", "LEAF", "K", "Heavy", 14, 10, 4, 17, 20, 12, 7,
            0, 0, "Special / Ultimate", 80, 14, 0, 11, "Ability.Mecha.VerdantCrash", "重心下沉的重击。"),
        _mv("VRD_S", "孢子束缚", "Spore Snare", "LEAF", "L", "Special", 20, 12, 6, 22, 30, 18, 9,
            0, 0, "Ultimate", 104, 18, 25, 17, "Ability.Mecha.SporeSnare", "命中后附加强僵直，便于接续。"),
        _mv("VRD_U", "生命之树", "World Tree", "LEAF", "U", "Ultimate", 34, 16, 10, 30, 38, 24, 14,
            0, 2, "—", 128, 28, 100, 0, "Ability.Mecha.WorldTree", "根系爆发，完全霸体，长僵直。"),
    ],
    "BASTION": [
        _mv("BST_L", "液压铁拳", "Iron Jab", "STEEL", "J", "Light", 9, 6, 3, 10, 15, 9, 5,
            0, 1, "Heavy", 60, 8, 0, 5, "Ability.Mecha.IronJab", "带 1 级霸体的轻击，硬碰硬不亏。"),
        _mv("BST_H", "攻城铁锤", "Siege Hammer", "STEEL", "K", "Heavy", 19, 12, 5, 20, 24, 15, 9,
            0, 1, "Special", 80, 20, 0, 10, "Ability.Mecha.SiegeHammer", "全机甲单发伤害最高，后摇也最长。"),
        _mv("BST_S", "磁轨冲撞", "Rail Charge", "STEEL", "L", "Special", 26, 15, 7, 26, 30, 19, 11,
            0, 2, "Ultimate", 108, 28, 25, 14, "Ability.Mecha.RailCharge", "完全霸体冲撞，正面无解。"),
        _mv("BST_U", "要塞崩落", "Fortress Fall", "STEEL", "U", "Ultimate", 44, 20, 11, 34, 40, 26, 16,
            0, 2, "—", 124, 40, 100, 0, "Ability.Mecha.FortressFall", "整机砸落，完全霸体，一击决定胜负。"),
    ],
    "ASTRO": [
        _mv("AST_L", "星轨斩", "Astral Slash", "QUANTUM", "J", "Light", 7, 4, 3, 8, 14, 8, 4,
            0, 0, "Heavy / Special", 68, 7, 0, 6, "Ability.Mecha.AstralSlash", "空间刃，判定距离远。"),
        _mv("AST_H", "重力拳", "Gravity Fist", "QUANTUM", "K", "Heavy", 16, 10, 4, 17, 22, 13, 8,
            0, 0, "Special / Ultimate", 82, 17, 0, 11, "Ability.Mecha.GravityFist", "重力压缩拳，击退明显。"),
        _mv("AST_S", "相位突刺", "Phase Thrust", "QUANTUM", "L", "Special", 24, 12, 6, 21, 27, 16, 10,
            0, 1, "Ultimate", 116, 24, 25, 16, "Ability.Mecha.PhaseThrust", "穿相位突刺，1 级霸体。"),
        _mv("AST_U", "时空断裂", "Time Rift", "QUANTUM", "U", "Ultimate", 39, 16, 10, 29, 36, 23, 15,
            0, 2, "—", 136, 33, 100, 0, "Ability.Mecha.TimeRift", "撕裂局部时空，完全霸体。"),
    ],
    "SHADOW": [
        _mv("SHD_L", "影刃", "Shadow Blade", "SHADOW", "J", "Light", 8, 3, 3, 8, 14, 8, 4,
            0, 0, "Heavy / Special", 64, 7, 0, 7, "Ability.Mecha.ShadowBlade", "极快出刀，压制起手。"),
        _mv("SHD_H", "断魂斩", "Soul Cutter", "SHADOW", "K", "Heavy", 17, 8, 4, 15, 21, 12, 7,
            0, 0, "Special / Ultimate", 78, 15, 0, 12, "Ability.Mecha.SoulCutter", "收招快，连段核心。"),
        _mv("SHD_S", "瞬影连刺", "Phantom Rush", "SHADOW", "L", "Special", 22, 11, 7, 19, 25, 15, 9,
            0, 0, "Ultimate", 112, 20, 25, 18, "Ability.Mecha.PhantomRush", "多段突刺，命中能量收益高。"),
        _mv("SHD_U", "永夜葬送", "Eternal Night", "SHADOW", "U", "Ultimate", 37, 15, 10, 27, 34, 21, 13,
            0, 1, "—", 138, 30, 100, 0, "Ability.Mecha.EternalNight", "潜入本体消失后突袭，1 级霸体。"),
    ],
    "FROST": [
        _mv("FST_L", "冰刺", "Ice Spike", "ICE", "J", "Light", 7, 5, 3, 9, 16, 9, 5,
            0, 0, "Heavy / Special", 72, 7, 0, 6, "Ability.Mecha.IceSpike", "冰刺射程远，适合牵制。"),
        _mv("FST_H", "寒霜重击", "Frost Crush", "ICE", "K", "Heavy", 15, 11, 4, 18, 24, 14, 8,
            0, 0, "Special / Ultimate", 82, 16, 0, 11, "Ability.Mecha.FrostCrush", "命中附带冻阻僵直。"),
        _mv("FST_S", "冰封锁", "Ice Lock", "ICE", "L", "Special", 21, 13, 6, 23, 32, 19, 10,
            0, 1, "Ultimate", 106, 20, 25, 16, "Ability.Mecha.IceLock", "冻结锁定，僵直时间极长。"),
        _mv("FST_U", "绝对零度", "Absolute Zero", "ICE", "U", "Ultimate", 35, 17, 11, 31, 42, 25, 15,
            0, 2, "—", 130, 30, 100, 0, "Ability.Mecha.AbsoluteZero", "全场冻结，完全霸体，最长僵直。"),
    ],
}


# ---------------------------------------------------------------------------
# 通用操作系统招式（所有机甲共享）
# ---------------------------------------------------------------------------
SYSTEM_MOVES: List[Move] = [
    _mv("SYS_GUARD", "防御", "Guard", "SYSTEM", "S(按住)", "System", 0, 1, 0, 0, 0, 0, 0,
        0, 0, "—", 0, 0, 0, 0, "Ability.System.Guard", "按住减伤 80%，消耗防御槽，防御槽清空则破防。"),
    _mv("SYS_PARRY", "弹反", "Parry", "SYSTEM", "S(瞬间)", "System", 0, 1, 0, 20, 0, 0, 0,
        4, 0, "—", 0, 0, 0, 30, "Ability.System.Parry", "按下 S 的前 4 帧为弹反窗口，成功使对手陷入 36 帧硬直。"),
    _mv("SYS_JUMP", "推进跳跃", "Boost Jump", "SYSTEM", "Space", "System", 0, 3, 0, 0, 0, 0, 0,
        0, 0, "—", 0, 0, 0, 0, "Ability.System.BoostJump", "推进器跃起，可规避地面判定。"),
    _mv("SYS_DASH", "瞬时冲刺", "Boost Dash", "SYSTEM", "Shift", "System", 0, 2, 0, 0, 0, 0, 0,
        0, 0, "—", 0, 0, 0, 0, "Ability.System.BoostDash", "快速拉近或拉开距离。"),
]


# ---------------------------------------------------------------------------
# 机甲（对应 UE5 中的 AMechaCharacter + ASC + AttributeSet）
# ---------------------------------------------------------------------------
@dataclass
class Mecha:
    id: str
    name_cn: str
    name_en: str
    codename: str
    element: str
    role: str
    hp: int
    atk: int
    dfn: int
    spd: int
    energy: int
    moves: List[Move] = field(default_factory=list)
    lore: str = ""

    def to_dict(self):
        d = asdict(self)
        d["element_name"] = TYPE_MAP[self.element].name_cn
        d["color"] = TYPE_MAP[self.element].color
        d["accent"] = TYPE_MAP[self.element].accent
        d["moves"] = [asdict(m) for m in self.moves]
        d["total_frames"] = [m.total_frames for m in self.moves]
        return d


MECHAS: List[Mecha] = [
    Mecha("BLAZE", "炎狱·赤焰", "Blaze Ignis", "MF-01", "FIRE", "强攻型", 78, 92, 70, 85, 100,
          MOVES["BLAZE"], "第一代量产型火系机甲，以高输出与灼烧叠加著称，是竞技场最受欢迎的先发机体。"),
    Mecha("TIDAL", "潮汐·沧澜", "Tidal Abyss", "MF-02", "WATER", "耐久型", 95, 75, 90, 60, 110,
          MOVES["TIDAL"], "深海勘探机甲改造而来，拥有全游戏最高的护盾成长，擅长持久消耗战。"),
    Mecha("VOLT", "雷鸣·疾风", "Volt Tempest", "MF-03", "ELECTRIC", "速攻型", 65, 88, 60, 110, 95,
          MOVES["VOLT"], "磁悬浮竞速机体，速度属性顶尖，先手压制战术的核心。"),
    Mecha("VERDANT", "苍翠·森灵", "Verdant Grove", "MF-04", "LEAF", "辅助型", 88, 70, 85, 70, 105,
          MOVES["VERDANT"], "生态修复机甲，搭载光合反应堆，是高端局不可或缺的续航核心。"),
    Mecha("BASTION", "玄铁·壁垒", "Iron Bastion", "MF-05", "STEEL", "防御型", 100, 80, 110, 40, 100,
          MOVES["BASTION"], "要塞级重装甲，正面防御无可匹敌，但转向迟缓是其致命弱点。"),
    Mecha("ASTRO", "星轨·幻境", "Astro Mirage", "MF-06", "QUANTUM", "特攻型", 70, 95, 65, 95, 100,
          MOVES["ASTRO"], "轨道空间站实验机体，能够干涉局部时空，操作上限极高。"),
    Mecha("SHADOW", "夜影·幽刃", "Night Shade", "MF-07", "SHADOW", "刺客型", 68, 100, 55, 100, 90,
          MOVES["SHADOW"], "军用潜入机甲，爆发伤害顶尖，但装甲薄弱，容错率极低。"),
    Mecha("FROST", "霜寒·极地", "Frost Permafrost", "MF-08", "ICE", "控制型", 82, 85, 80, 65, 105,
          MOVES["FROST"], "极地科考机甲，以冻结与减速构筑节奏封锁，是控场体系的核心。"),
]


# ---------------------------------------------------------------------------
# 对战规则（实时格斗）
# ---------------------------------------------------------------------------
BATTLE_RULES = {
    "logic_tick_hz": 60,
    "render_mode": "固定 60Hz 逻辑帧 + 渲染插值，判定与表现解耦",
    "round_time_sec": 99,
    "rounds_to_win": 2,
    "battle_format": "1v1 单挑 · BO3（三局两胜）",
    "team_size": 1,
    "health": 1000,
    "meter_max": 100,
    "guard_max": 100,
    "parry_window_frames": 4,
    "parry_punish_frames": 36,
    "parry_meter_reward": 30,
    "combo_scaling": "100% → 90% → 80% → 70% → 60% → 50%（最低）",
    "input_buffer_frames": 6,
    "cancel_route": "轻击 → 重击 → 必杀 → 超必杀",
    "hitbox_policy": "自定义 hitbox/hurtbox 查询，不依赖物理引擎硬判",
    "counter_hit": "对手后摇/起手阶段被命中，伤害 ×1.25 且僵直增加 8 帧",
    "ranking": "青铜 → 白银 → 黄金 → 铂金 → 钻石 → 大师 → 王者",
    "ban_phase": "双方各禁用 2 台机甲（BO3 起）",
}


PHASES = [
    {"id": "P0", "name": "核心战斗验证", "duration": "4 周", "goal": "构建实时帧驱动 1v1 格斗核心闭环",
     "deliverables": ["UE5 工程基座", "帧数据 DataAsset 工具链", "弹反/僵直/霸体/取消系统", "1v1 可操作版本"],
     "status": "进行中"},
    {"id": "P1", "name": "完整格斗系统", "duration": "8 周", "goal": "完成 8 台机甲与全部招式、AI 对手",
     "deliverables": ["8 台机甲 + 32 个招式", "Control Rig 混合动画管线", "自适应 AI 对手", "帧步进/回放调试工具"],
     "status": "规划中"},
    {"id": "P2", "name": "竞技系统", "duration": "6 周", "goal": "上线匹配、天梯与观战",
     "deliverables": ["匹配服务", "段位与排行榜", "Ban/Pick", "服务器权威校验与反作弊"],
     "status": "规划中"},
    {"id": "P3", "name": "内容运营", "duration": "持续", "goal": "赛季更新与电竞化",
     "deliverables": ["新机甲/招式", "赛季通行证", "观战系统", "赛事工具包"],
     "status": "规划中"},
]

GAS_ARCHITECTURE = [
    ("AbilitySystemComponent (ASC)", "挂载于每台机甲，统一驱动招式、属性与状态"),
    ("MechaAttributeSet", "Health / Meter / Guard / Attack / Defense / Speed / Armor"),
    ("UCombatAbility", "32 个招式，帧数据驱动 + 能量消耗与取消规则校验"),
    ("FCombatFrameData (DataAsset)", "startup / active / recovery / parryWindow / armor / cancelWindow / hitstop"),
    ("UHitboxComponent", "自定义 hitbox/hurtbox 查询，判定与动画表现解耦"),
    ("UParryComponent", "弹反窗口判定、成功硬直反馈与能量奖励"),
    ("UHitstopSubsystem", "命中停顿帧调度，统一控制打击节奏"),
    ("UMechaAnimInstance", "动捕基础姿态 + Control Rig 机甲化 + 程序化二级运动"),
    ("CombatReplaySubsystem", "帧步进调试、输入回放与战斗日志（Perforce 构建流水线）"),
    ("GameplayCue", "命中特效、分层音效、镜头震动等表现层通知"),
]


def all_moves_flat() -> List[Move]:
    return [m for moves in MOVES.values() for m in moves]


# 兼容旧调用方
all_abilities_flat = all_moves_flat


def demo_data() -> dict:
    """导出给官方交互演示使用的数据（JSON 可序列化）。"""
    return {
        "elements": [asdict(e) for e in ELEMENTS],
        "type_chart": TYPE_CHART,
        "mechas": [m.to_dict() for m in MECHAS],
        "system_moves": [asdict(m) for m in SYSTEM_MOVES],
        "rules": BATTLE_RULES,
        "phases": PHASES,
        "gas": [{"name": n, "desc": d} for n, d in GAS_ARCHITECTURE],
    }
