# -*- coding: utf-8 -*-
"""MECHA·MON 项目生成器 CLI。

用法：
    python main.py            # 生成全部产物
    python main.py docs       # 只生成文档
    python main.py ue5        # 只生成 UE5 GAS 代码基座
    python main.py demo       # 只生成官方交互式产品演示
    python main.py check      # 校验数据与产物
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.game_data import MECHAS, ELEMENTS, TYPE_CHART, all_moves_flat
from config.project_config import (
    PROJECT, DOCS_DIR, DEMO_DIR, UE5_DIR,
)
from generators import doc_generator, ue5_generator, demo_generator


def banner():
    print("=" * 62)
    print(f"  {PROJECT['codename']} · {PROJECT['name_cn']}  [{PROJECT['version']}]")
    print(f"  引擎 {PROJECT['engine']}  |  框架 {PROJECT['framework']}")
    print("=" * 62)


def cmd_docs():
    names = doc_generator.generate_all()
    print(f"[文档] 已生成 {len(names)} 份文档 → {DOCS_DIR}")
    for n in names:
        print(f"       - {n}")


def cmd_ue5():
    files = ue5_generator.generate_all()
    print(f"[UE5]  已生成 {len(files)} 个 C++ 基座文件 → {UE5_DIR}")
    for f in files:
        print(f"       - {f}")


def cmd_demo():
    out = demo_generator.generate_demo()
    print(f"[演示] 已生成官方交互式产品演示 → {out}")
    print(f"       大小 {out.stat().st_size / 1024:.1f} KB（自包含，可直接双击打开）")


def cmd_check():
    errors = []
    # 数据完整性
    assert len(MECHAS) == 8, "机甲数量不是 8"
    assert len(ELEMENTS) == 8, "属性数量不是 8"
    moves = all_moves_flat()
    if len(moves) != 32:
        errors.append(f"招式数量 {len(moves)} != 32")
    for m in MECHAS:
        if len(m.moves) != 4:
            errors.append(f"{m.name_cn} 招式数 {len(m.moves)} != 4")
        if m.element not in TYPE_CHART:
            errors.append(f"{m.name_cn} 属性 {m.element} 未在克制表中")
        for mv in m.moves:
            if mv.startup <= 0 or mv.active <= 0 or mv.recovery <= 0:
                errors.append(f"{m.name_cn}/{mv.name_cn} 帧数据非法")
            if mv.hitstun <= 0 or mv.hitstop <= 0:
                errors.append(f"{m.name_cn}/{mv.name_cn} 僵直/hitstop 非法")
    # 产物完整性
    for d, label in [(DOCS_DIR, "文档"), (DEMO_DIR, "演示")]:
        if not d.exists() or not any(d.iterdir()):
            errors.append(f"{label}目录为空：{d}")
    if not (UE5_DIR / "Public" / "MechaCharacter.h").exists():
        errors.append("UE5 骨架缺失 MechaCharacter.h")

    print(f"[校验] 机甲 {len(MECHAS)} 台 | 属性 {len(ELEMENTS)} 种 | 招式 {len(moves)} 个 | 帧数据 ✓")
    if errors:
        print("[校验] 发现问题：")
        for e in errors:
            print("       ✗", e)
        sys.exit(1)
    print("[校验] ✓ 数据与产物完整")


def main():
    banner()
    p = argparse.ArgumentParser(description="MECHA·MON 项目生成器")
    p.add_argument("action", nargs="?", default="all",
                   choices=["all", "docs", "ue5", "demo", "check"])
    args = p.parse_args()

    if args.action in ("all", "docs"):
        cmd_docs()
    if args.action in ("all", "ue5"):
        cmd_ue5()
    if args.action in ("all", "demo"):
        cmd_demo()
    if args.action in ("all", "check"):
        cmd_check()

    print("-" * 62)
    print("完成。交互式产品演示：demo/index.html")
    print("文档目录：docs/   UE5 代码基座：generated/ue5/Source/MechaMon/")


if __name__ == "__main__":
    main()
