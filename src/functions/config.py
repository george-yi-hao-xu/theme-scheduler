#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
"""

import json
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "dark_time": "19:00",
    "light_time": "07:00",
    "auto_schedule": False,
}


def get_config_path():
    """获取配置文件路径（支持脚本和 EXE 两种运行方式）"""
    if getattr(sys, 'frozen', False):
        # 打包成 EXE 后，使用 EXE 所在目录
        return Path(sys.executable).parent / "config.json"
    else:
        # 作为脚本运行时，使用项目根目录
        return Path(__file__).parent.parent.parent / "config.json"


def load_config():
    """加载配置文件"""
    config_path = get_config_path()
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
    config_path = get_config_path()
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False
