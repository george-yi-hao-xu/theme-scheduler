#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManualSwitchGroup - 手动切换区域组件
"""

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from src.components.ToggleSwitch import ToggleSwitch


class ManualSwitchGroup(QGroupBox):
    """手动切换区域组件"""
    theme_switched = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__("手动切换", parent)
        self.current_theme = True
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # Apple 风格的 toggle 开关
        toggle_row = QHBoxLayout()
        toggle_row.setAlignment(Qt.AlignCenter)
        
        # 浅色标签
        light_label = QLabel("浅色")
        light_label.setStyleSheet("font-size: 14px; color: #555;")
        toggle_row.addWidget(light_label)
        
        # Toggle 开关
        self.theme_toggle = ToggleSwitch()
        self.theme_toggle.setChecked(self.current_theme)
        self.theme_toggle.clicked.connect(self.on_toggle_changed)
        toggle_row.addWidget(self.theme_toggle)
        
        # 深色标签
        dark_label = QLabel("深色")
        dark_label.setStyleSheet("font-size: 14px; color: #555;")
        toggle_row.addWidget(dark_label)
        
        layout.addLayout(toggle_row)
        
        # 当前主题显示
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("当前主题:"))
        self.current_theme_label = QLabel("浅色模式")
        self.current_theme_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #555;")
        theme_row.addWidget(self.current_theme_label)
        theme_row.addStretch()
        layout.addLayout(theme_row)
        
    def on_toggle_changed(self, checked):
        """Toggle 状态改变时触发信号"""
        # 滑块在左边(checked=False) → 浅色模式
        # 滑块在右边(checked=True) → 深色模式
        self.current_theme = not checked
        self.theme_switched.emit(not checked)
        
    def update_theme_display(self, light):
        """更新主题显示"""
        self.current_theme = light
        self.current_theme_label.setText("浅色模式" if light else "深色模式")
        # 浅色模式 → 滑块在左边(checked=False)
        # 深色模式 → 滑块在右边(checked=True)
        self.theme_toggle.setChecked(not light)
        
    def get_current_theme(self):
        """获取当前主题"""
        return self.current_theme
