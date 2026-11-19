# -*- coding: utf-8 -*-
"""项目元数据与路径配置。"""
from pathlib import Path

PROJECT = {
    "codename": "MECHA·MON",
    "name_cn": "机甲兽竞技场",
    "name_en": "MechaMon Arena",
    "tagline": "机甲觉醒 · 策略竞技 · 属性压制",
    "engine": "Unreal Engine 5",
    "framework": "Gameplay Ability System (GAS)",
    "version": "0.1.0-Prototype",
    "genre": "回合制策略竞技 / 机甲收集养成",
    "platform": "PC (首发) / 主机 (后续)",
    "author": "Project MECHA·MON 筹备组",
}

ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
DEMO_DIR = ROOT / "demo"
GENERATED_DIR = ROOT / "generated"
TEMPLATES_DIR = ROOT / "templates"
UE5_DIR = GENERATED_DIR / "ue5" / "Source" / "MechaMon"
