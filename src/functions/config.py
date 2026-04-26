#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import json
from pathlib import Path

DEFAULT_CONFIG = {
    "dark_time": "19:00",
    "light_time": "07:00",
    "auto_schedule": False,
}


def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent.parent / "config.json"
    config = DEFAULT_CONFIG.copy()
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception:
            pass
    return config


def save_config(config):
    """保存配置文件"""
    config_path = Path(__file__).parent.parent.parent / "config.json"
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False
