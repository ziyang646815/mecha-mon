# -*- coding: utf-8 -*-
"""HTML 演示原型生成器：把游戏数据注入自包含模板。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.game_data import demo_data
from config.project_config import PROJECT, TEMPLATES_DIR, DEMO_DIR


def generate_demo() -> Path:
    template = (TEMPLATES_DIR / "demo_template.html").read_text(encoding="utf-8")
    data_json = json.dumps(demo_data(), ensure_ascii=False, separators=(",", ":"))
    proj_json = json.dumps(PROJECT, ensure_ascii=False, separators=(",", ":"))

    html = template.replace("__GAME_DATA__", data_json).replace("__PROJECT_JSON__", proj_json)
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    out = DEMO_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    return out
