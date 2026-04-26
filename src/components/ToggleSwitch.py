#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToggleSwitch - Apple 风格的 Toggle 开关组件
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QRect, pyqtSignal


class ToggleSwitch(QWidget):
    """自定义 Apple 风格的 Toggle 开关"""
    clicked = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(52, 28)
        self.checked = False
        
    def setChecked(self, value):
        self.checked = value
        self.update()
        
    def isChecked(self):
        return self.checked
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        bg_rect = QRect(0, 0, 52, 28)
        bg_color = QColor(74, 85, 104) if self.checked else QColor(160, 174, 192)
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(bg_rect, 14, 14)
        
        # 绘制滑块
        handle_x = 26 if self.checked else 2
        handle_rect = QRect(handle_x, 2, 24, 24)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRoundedRect(handle_rect, 12, 12)
        
    def mouseReleaseEvent(self, event):
        self.checked = not self.checked
        self.update()
        self.clicked.emit(self.checked)
