#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务模块
"""

from datetime import datetime


def check_schedule(config: dict) -> str | None:
    """
    检查是否需要切换主题
    返回: "dark" - 切换深色, "light" - 切换浅色, None - 不需要切换
    """
    if not config.get("auto_schedule", False):
        return None

    now = datetime.now().time()
    dark_time = datetime.strptime(config["dark_time"], "%H:%M").time()
    light_time = datetime.strptime(config["light_time"], "%H:%M").time()

    should_be_dark = False

    # 深色时间 > 浅色时间 (如 19:00 深色, 07:00 浅色)
    # 深色模式时段: dark_time 到 light_time
    if dark_time > light_time:
        if now >= dark_time or now < light_time:
            should_be_dark = True
    else:
        if now >= dark_time and now < light_time:
            should_be_dark = True

    if should_be_dark:
        return "dark"
    else:
        return "light"
