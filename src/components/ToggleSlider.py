#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToggleSlider - 双选项切换组件（RadioButton 风格）
使用两个 QRadioButton，仿 iPhone 设置界面风格
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QRadioButton
from PyQt5.QtCore import Qt, pyqtSignal


class ToggleSlider(QWidget):
    """双选项切换组件（RadioButton 风格）"""
    clicked = pyqtSignal(bool)  # True 表示选中第一个选项（浅色），False 表示选中第二个选项（深色）
    
    def __init__(self, option1="浅色", option2="深色", parent=None):
        super().__init__(parent)
        self.option1 = option1
        self.option2 = option2
        self.checked = True  # True 表示选中 option1（浅色）
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(30)
        
        # 浅色选项
        light_layout = QHBoxLayout()
        light_layout.setSpacing(8)
        
        self.light_label = QLabel(self.option1)
        self.light_label.setStyleSheet("font-size: 14px;")
        
        self.light_radio = QRadioButton()
        self.light_radio.setChecked(True)
        self.light_radio.clicked.connect(self.on_light_clicked)
        
        light_layout.addWidget(self.light_label)
        light_layout.addWidget(self.light_radio)
        layout.addLayout(light_layout)
        
        # 深色选项
        dark_layout = QHBoxLayout()
        dark_layout.setSpacing(8)
        
        self.dark_label = QLabel(self.option2)
        self.dark_label.setStyleSheet("font-size: 14px;")
        
        self.dark_radio = QRadioButton()
        self.dark_radio.setChecked(False)
        self.dark_radio.clicked.connect(self.on_dark_clicked)
        
        dark_layout.addWidget(self.dark_label)
        dark_layout.addWidget(self.dark_radio)
        layout.addLayout(dark_layout)
        
    def on_light_clicked(self, checked):
        """点击浅色选项"""
        if checked and not self.checked:
            self.checked = True
            self.clicked.emit(True)
        
    def on_dark_clicked(self, checked):
        """点击深色选项"""
        if checked and self.checked:
            self.checked = False
            self.clicked.emit(False)
        
    def setChecked(self, value):
        """设置选中状态"""
        if self.checked != value:
            self.checked = value
            self.light_radio.setChecked(value)
            self.dark_radio.setChecked(not value)
        
    def isChecked(self):
        """获取选中状态"""
        return self.checked
