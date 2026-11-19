# -*- coding: utf-8 -*-
"""MECHA·MON 核心游戏数据。

单一数据源（Single Source of Truth）：文档生成器、UE5 骨架生成器、
HTML 演示原型全部从本文件读取数据，避免"文档和演示对不上"。
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

# 克制关系：攻击方 -> (2倍克制, 0.5倍抵抗, 0倍免疫)
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
# 技能（对应 UE5 的 UGameplayAbility）
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Ability:
    id: str
    name_cn: str
    name_en: str
    type: str
    category: str        # Damage / Shield / Dot / Buff / Control / Heal
    power: int
    cost: int
    cooldown: int
    gameplay_tag: str
    description: str


def _a(aid, cn, en, typ, cat, power, cost, cd, tag, desc) -> Ability:
    return Ability(aid, cn, en, typ, cat, power, cost, cd, tag, desc)


ABILITIES: Dict[str, List[Ability]] = {
    "BLAZE": [
        _a("BLAZE_01", "烈焰冲撞", "Flame Ram", "FIRE", "Damage", 42, 18, 0,
           "Ability.Mecha.FlameRam", "高热的肩甲冲撞，命中后附带 1 层灼烧。"),
        _a("BLAZE_02", "熔核护盾", "Magma Shield", "FIRE", "Shield", 0, 22, 2,
           "Ability.Mecha.MagmaShield", "展开熔融护盾，吸收 35 点伤害并反弹 20%。"),
        _a("BLAZE_03", "灼烧飞弹", "Incendiary Pod", "FIRE", "Dot", 26, 20, 1,
           "Ability.Mecha.IncendiaryPod", "3 回合持续灼烧，每回合 12 点伤害。"),
        _a("BLAZE_04", "超频过载", "Overdrive", "FIRE", "Buff", 0, 25, 3,
           "Ability.Mecha.Overdrive", "牺牲 10% 生命，提升 40% 攻击持续 3 回合。"),
    ],
    "TIDAL": [
        _a("TIDAL_01", "深水炮击", "Hydro Cannon", "WATER", "Damage", 45, 20, 1,
           "Ability.Mecha.HydroCannon", "压缩水炮，对钢甲额外造成 20% 伤害。"),
        _a("TIDAL_02", "潮汐壁垒", "Tidal Bulwark", "WATER", "Shield", 0, 18, 2,
           "Ability.Mecha.TidalBulwark", "生成水幕护盾并恢复 15 点生命。"),
        _a("TIDAL_03", "漩涡禁锢", "Vortex Lock", "WATER", "Control", 15, 24, 2,
           "Ability.Mecha.VortexLock", "降低目标 30% 速度，持续 2 回合。"),
        _a("TIDAL_04", "再生装甲", "Regen Plating", "WATER", "Heal", 0, 26, 3,
           "Ability.Mecha.RegenPlating", "修复 40 点装甲值。"),
    ],
    "VOLT": [
        _a("VOLT_01", "雷光突袭", "Volt Rush", "ELECTRIC", "Damage", 40, 16, 0,
           "Ability.Mecha.VoltRush", "高速电磁突进，先手概率 +30%。"),
        _a("VOLT_02", "电磁脉冲", "EMP Burst", "ELECTRIC", "Control", 20, 22, 2,
           "Ability.Mecha.EMPBurst", "使敌方下一次技能能量消耗翻倍。"),
        _a("VOLT_03", "静电场", "Static Field", "ELECTRIC", "Dot", 18, 20, 1,
           "Ability.Mecha.StaticField", "每回合 15 点雷伤，并降低目标 10% 防御。"),
        _a("VOLT_04", "电容超载", "Capacitor Overload", "ELECTRIC", "Buff", 0, 24, 3,
           "Ability.Mecha.CapacitorOverload", "下次攻击必定暴击。"),
    ],
    "VERDANT": [
        _a("VERDANT_01", "藤蔓束缚", "Vine Snare", "LEAF", "Damage", 32, 16, 1,
           "Ability.Mecha.VineSnare", "有机藤蔓抽打并束缚目标 1 回合。"),
        _a("VERDANT_02", "光合修复", "Photosyn Heal", "LEAF", "Heal", 0, 22, 2,
           "Ability.Mecha.PhotosynHeal", "恢复 45 点生命并清除 1 个负面效果。"),
        _a("VERDANT_03", "孢子迷雾", "Spore Fog", "LEAF", "Control", 12, 20, 2,
           "Ability.Mecha.SporeFog", "降低敌方命中率 25%，持续 3 回合。"),
        _a("VERDANT_04", "森罗领域", "Verdant Field", "LEAF", "Buff", 0, 28, 3,
           "Ability.Mecha.VerdantField", "全队每回合恢复 12 点生命，持续 4 回合。"),
    ],
    "BASTION": [
        _a("BASTION_01", "攻城铁拳", "Siege Fist", "STEEL", "Damage", 48, 22, 1,
           "Ability.Mecha.SiegeFist", "重型液压拳，对防御型目标额外 15% 伤害。"),
        _a("BASTION_02", "绝对壁垒", "Aegis Wall", "STEEL", "Shield", 0, 20, 2,
           "Ability.Mecha.AegisWall", "吸收 60 点伤害，持续 2 回合。"),
        _a("BASTION_03", "反冲装甲", "Reactive Armor", "STEEL", "Buff", 0, 24, 3,
           "Ability.Mecha.ReactiveArmor", "反弹 30% 所受伤害，持续 3 回合。"),
        _a("BASTION_04", "磁轨重炮", "Railgun", "STEEL", "Damage", 55, 30, 3,
           "Ability.Mecha.Railgun", "蓄力一击，无视 50% 防御。"),
    ],
    "ASTRO": [
        _a("ASTRO_01", "星轨射线", "Astral Ray", "QUANTUM", "Damage", 44, 21, 1,
           "Ability.Mecha.AstralRay", "空间折叠射线，对暗影系必定 2 倍克制。"),
        _a("ASTRO_02", "相位跃迁", "Phase Shift", "QUANTUM", "Buff", 0, 20, 2,
           "Ability.Mecha.PhaseShift", "闪避下一次攻击，并提升 20% 速度。"),
        _a("ASTRO_03", "引力奇点", "Gravity Singularity", "QUANTUM", "Control", 25, 26, 3,
           "Ability.Mecha.GravitySingularity", "封锁目标换人 2 回合。"),
        _a("ASTRO_04", "时隙回溯", "Time Rewind", "QUANTUM", "Heal", 0, 30, 4,
           "Ability.Mecha.TimeRewind", "回溯至 3 回合前的生命值（不超过上限）。"),
    ],
    "SHADOW": [
        _a("SHADOW_01", "暗刃斩击", "Shadow Slash", "SHADOW", "Damage", 46, 18, 0,
           "Ability.Mecha.ShadowSlash", "高速近战，暴击率 +20%。"),
        _a("SHADOW_02", "影分身", "Shadow Clone", "SHADOW", "Buff", 0, 22, 2,
           "Ability.Mecha.ShadowClone", "生成 2 个分身，首次受击必定闪避。"),
        _a("SHADOW_03", "蚀魂之触", "Soul Drain", "SHADOW", "Dot", 24, 24, 2,
           "Ability.Mecha.SoulDrain", "吸取造成伤害的 40% 转化为自身生命。"),
        _a("SHADOW_04", "夜幕降临", "Nightfall", "SHADOW", "Control", 18, 28, 3,
           "Ability.Mecha.Nightfall", "全场命中率 -20%，暗影系免疫。"),
    ],
    "FROST": [
        _a("FROST_01", "冰棱飞射", "Ice Lance", "ICE", "Damage", 38, 17, 0,
           "Ability.Mecha.IceLance", "冻结弹头，30% 概率使目标冻结 1 回合。"),
        _a("FROST_02", "寒霜装甲", "Frost Plating", "ICE", "Shield", 0, 19, 2,
           "Ability.Mecha.FrostPlating", "护盾值 45，接触攻击者速度 -20%。"),
        _a("FROST_03", "极寒风暴", "Blizzard Core", "ICE", "Dot", 28, 25, 2,
           "Ability.Mecha.BlizzardCore", "每回合 18 点冰伤，持续 3 回合。"),
        _a("FROST_04", "绝对零度", "Absolute Zero", "ICE", "Control", 35, 32, 4,
           "Ability.Mecha.AbsoluteZero", "必定冻结目标 1 回合，并降低其 25% 防御。"),
    ],
}


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
    abilities: List[Ability] = field(default_factory=list)
    lore: str = ""

    def to_dict(self):
        d = asdict(self)
        d["element_name"] = TYPE_MAP[self.element].name_cn
        d["color"] = TYPE_MAP[self.element].color
        d["accent"] = TYPE_MAP[self.element].accent
        d["abilities"] = [asdict(a) for a in self.abilities]
        return d


MECHAS: List[Mecha] = [
    Mecha("BLAZE", "炎狱·赤焰", "Blaze Ignis", "MF-01", "FIRE", "强攻型", 78, 92, 70, 85, 100,
          ABILITIES["BLAZE"], "第一代量产型火系机甲，以高输出与灼烧叠加著称，是竞技场最受欢迎的先发机体。"),
    Mecha("TIDAL", "潮汐·沧澜", "Tidal Abyss", "MF-02", "WATER", "耐久型", 95, 75, 90, 60, 110,
          ABILITIES["TIDAL"], "深海勘探机甲改造而来，拥有全游戏最高的护盾成长，擅长持久消耗战。"),
    Mecha("VOLT", "雷鸣·疾风", "Volt Tempest", "MF-03", "ELECTRIC", "速攻型", 65, 88, 60, 110, 95,
          ABILITIES["VOLT"], "磁悬浮竞速机体，速度属性顶尖，先手压制战术的核心。"),
    Mecha("VERDANT", "苍翠·森灵", "Verdant Grove", "MF-04", "LEAF", "辅助型", 88, 70, 85, 70, 105,
          ABILITIES["VERDANT"], "生态修复机甲，搭载光合反应堆，是高端局不可或缺的续航核心。"),
    Mecha("BASTION", "玄铁·壁垒", "Iron Bastion", "MF-05", "STEEL", "防御型", 100, 80, 110, 40, 100,
          ABILITIES["BASTION"], "要塞级重装甲，正面防御无可匹敌，但转向迟缓是其致命弱点。"),
    Mecha("ASTRO", "星轨·幻境", "Astro Mirage", "MF-06", "QUANTUM", "特攻型", 70, 95, 65, 95, 100,
          ABILITIES["ASTRO"], "轨道空间站实验机体，能够干涉局部时空，操作上限极高。"),
    Mecha("SHADOW", "夜影·幽刃", "Night Shade", "MF-07", "SHADOW", "刺客型", 68, 100, 55, 100, 90,
          ABILITIES["SHADOW"], "军用潜入机甲，爆发伤害顶尖，但装甲薄弱，容错率极低。"),
    Mecha("FROST", "霜寒·极地", "Frost Permafrost", "MF-08", "ICE", "控制型", 82, 85, 80, 65, 105,
          ABILITIES["FROST"], "极地科考机甲，以冻结与减速构筑节奏封锁，是控场体系的核心。"),
]


# ---------------------------------------------------------------------------
# 竞技规则与数值
# ---------------------------------------------------------------------------
BATTLE_RULES = {
    "team_size": 3,
    "battle_format": "3v3 单败淘汰 / 天梯排位",
    "turn_limit": 30,
    "energy_regen": 12,
    "max_energy": 120,
    "crit_rate_base": 0.05,
    "crit_multiplier": 1.5,
    "switch_cost": 8,
    "ban_phase": "双方各禁用 2 台机甲（BO3 起）",
    "ranking": "青铜 → 白银 → 黄金 → 铂金 → 钻石 → 大师 → 王者",
}

PHASES = [
    {"id": "P0", "name": "概念验证", "duration": "4 周", "goal": "跑通 GAS 回合制战斗闭环",
     "deliverables": ["UE5 工程模板", "ASC + AttributeSet 原型", "1v1 可战斗 Demo", "属性克制表"],
     "status": "当前阶段"},
    {"id": "P1", "name": "核心战斗", "duration": "8 周", "goal": "完成 3v3 战斗与全部机甲",
     "deliverables": ["8 台机甲 + 32 个技能", "换人/能量/状态系统", "AI 对手", "战斗回放"],
     "status": "规划中"},
    {"id": "P2", "name": "竞技系统", "duration": "6 周", "goal": "上线天梯与匹配",
     "deliverables": ["匹配服务", "段位与排行榜", "Ban/Pick", "反作弊与战斗校验"],
     "status": "规划中"},
    {"id": "P3", "name": "内容运营", "duration": "持续", "goal": "赛季更新与电竞化",
     "deliverables": ["新机甲/技能", "赛季通行证", "观战系统", "赛事工具包"],
     "status": "规划中"},
]

GAS_ARCHITECTURE = [
    ("AbilitySystemComponent (ASC)", "挂载于每台机甲，统一驱动技能、属性与状态"),
    ("MechaAttributeSet", "Health / Energy / Attack / Defense / Speed / CritRate"),
    ("UGameplayAbility", "32 个机甲技能，DataAsset 配置 + 冷却/消耗校验"),
    ("UGameplayEffect", "伤害、护盾、灼烧、冻结、增益等即时与持续效果"),
    ("FGameplayTag", "Mecha.Type.* / Ability.* / Status.* 三层标签体系"),
    ("BattleManager (GameState)", "回合调度、先手计算、换人判定、胜负结算"),
    ("AbilityTask", "PlayMontageAndWait / WaitForTarget / 动画与镜头表现"),
    ("GameplayCue", "命中特效、音效、屏幕震动等表现层通知"),
]


def all_abilities_flat() -> List[Ability]:
    return [a for abilities in ABILITIES.values() for a in abilities]


def demo_data() -> dict:
    """导出给 HTML 原型使用的数据（JSON 可序列化）。"""
    return {
        "elements": [asdict(e) for e in ELEMENTS],
        "type_chart": TYPE_CHART,
        "mechas": [m.to_dict() for m in MECHAS],
        "rules": BATTLE_RULES,
        "phases": PHASES,
        "gas": [{"name": n, "desc": d} for n, d in GAS_ARCHITECTURE],
    }
