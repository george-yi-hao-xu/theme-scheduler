#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ManualSwitchGroup - 手动切换区域组件
"""

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

from src.components.ToggleSlider import ToggleSlider


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
        
        # ToggleSlider 双选项切换滑块
        toggle_row = QHBoxLayout()
        toggle_row.setAlignment(Qt.AlignCenter)
        
        # ToggleSlider - 选中的选项有紫色背景，未选中的是白色背景
        self.theme_toggle = ToggleSlider("浅色", "深色")
        self.theme_toggle.setChecked(self.current_theme)
        self.theme_toggle.clicked.connect(self.on_toggle_changed)
        toggle_row.addWidget(self.theme_toggle)
        
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
        # checked=True → 选中浅色模式
        # checked=False → 选中深色模式
        self.current_theme = checked
        self.theme_switched.emit(checked)
        
    def update_theme_display(self, light):
        """更新主题显示"""
        self.current_theme = light
        self.current_theme_label.setText("浅色模式" if light else "深色模式")
        # 浅色模式 → 选中浅色选项
        # 深色模式 → 选中深色选项
        self.theme_toggle.setChecked(light)
        
    def get_current_theme(self):
        """获取当前主题"""
        return self.current_theme
