# -*- coding: utf-8 -*-
"""项目元数据与路径配置。"""
from pathlib import Path

PROJECT = {
    "codename": "MECHA·MON",
    "name_cn": "机甲兽竞技场",
    "name_en": "MechaMon Arena",
    "tagline": "机甲觉醒 · 帧级博弈 · 硬核格斗",
    "engine": "Unreal Engine 5",
    "framework": "Gameplay Ability System (GAS)",
    "version": "v1.0 · Vertical Slice",
    "genre": "实时 1v1 机甲格斗 / 操作竞技",
    "platform": "PC (首发) / 主机 (后续)",
    "author": "MECHA·MON 开发团队",
}

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
DEMO_DIR = ROOT / "demo"
GENERATED_DIR = ROOT / "generated"
TEMPLATES_DIR = ROOT / "templates"
UE5_DIR = GENERATED_DIR / "ue5" / "Source" / "MechaMon"
