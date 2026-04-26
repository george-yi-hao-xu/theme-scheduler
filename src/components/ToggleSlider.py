#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToggleSlider - 双选项切换滑块组件
选中的选项有紫色背景，未选中的是白色背景
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal


class ToggleSlider(QWidget):
    """双选项切换滑块组件"""
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
        layout.setSpacing(0)
        
        # 设置固定大小
        self.setFixedSize(120, 32)
        
        # 创建两个选项标签
        self.label1 = QLabel(self.option1)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFixedSize(60, 32)
        self.label1.setStyleSheet("""
            QLabel {
                background-color: #9b59b6;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px 0 0 6px;
            }
            QLabel:hover {
                background-color: #8e44ad;
            }
        """)
        self.label1.mousePressEvent = self.on_label1_clicked
        
        self.label2 = QLabel(self.option2)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFixedSize(60, 32)
        self.label2.setStyleSheet("""
            QLabel {
                background-color: white;
                color: #555;
                font-size: 14px;
                font-weight: bold;
                border-radius: 0 6px 6px 0;
                border: 1px solid #ddd;
            }
            QLabel:hover {
                background-color: #f5f5f5;
            }
        """)
        self.label2.mousePressEvent = self.on_label2_clicked
        
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        
    def on_label1_clicked(self, event):
        """点击第一个选项"""
        if not self.checked:
            self.checked = True
            self.update_styles()
            self.clicked.emit(True)
        
    def on_label2_clicked(self, event):
        """点击第二个选项"""
        if self.checked:
            self.checked = False
            self.update_styles()
            self.clicked.emit(False)
        
    def update_styles(self):
        """更新样式"""
        if self.checked:
            # 选中第一个选项（浅色）
            self.label1.setStyleSheet("""
                QLabel {
                    background-color: #9b59b6;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 6px 0 0 6px;
                }
                QLabel:hover {
                    background-color: #8e44ad;
                }
            """)
            self.label2.setStyleSheet("""
                QLabel {
                    background-color: white;
                    color: #555;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 0 6px 6px 0;
                    border: 1px solid #ddd;
                }
                QLabel:hover {
                    background-color: #f5f5f5;
                }
            """)
        else:
            # 选中第二个选项（深色）
            self.label1.setStyleSheet("""
                QLabel {
                    background-color: white;
                    color: #555;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 6px 0 0 6px;
                    border: 1px solid #ddd;
                }
                QLabel:hover {
                    background-color: #f5f5f5;
                }
            """)
            self.label2.setStyleSheet("""
                QLabel {
                    background-color: #9b59b6;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 0 6px 6px 0;
                }
                QLabel:hover {
                    background-color: #8e44ad;
                }
            """)
        
    def setChecked(self, value):
        """设置选中状态"""
        if self.checked != value:
            self.checked = value
            self.update_styles()
        
    def isChecked(self):
        """获取选中状态"""
        return self.checked
