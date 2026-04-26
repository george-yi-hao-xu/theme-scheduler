#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题切换模块
"""

import winreg
import ctypes

# Windows API constants
HWND_BROADCAST = 0xFFFF
WM_SETTINGCHANGE = 0x1A
SMTO_ABORTIFHUNG = 0x0002

# Registry paths
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
REG_NAME = "AppsUseLightTheme"


def get_current_theme() -> bool:
    """获取当前主题状态"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH) as key:
            value, _ = winreg.QueryValueEx(key, REG_NAME)
            return bool(value)
    except Exception:
        return True


def set_theme(light: bool) -> bool:
    """设置主题: True=浅色, False=深色"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, REG_NAME, 0, winreg.REG_DWORD, 1 if light else 0)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 1 if light else 0)

        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST,
            WM_SETTINGCHANGE,
            0,
            ctypes.c_wchar_p("ImmersiveColorSet"),
            SMTO_ABORTIFHUNG,
            5000,
            ctypes.byref(ctypes.c_size_t(0)),
        )
        return True
    except Exception:
        return False
