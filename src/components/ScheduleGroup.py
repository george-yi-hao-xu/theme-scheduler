#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ScheduleGroup - 定时切换区域组件
"""

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTimeEdit
from PyQt5.QtCore import QTime, pyqtSignal


class ScheduleGroup(QGroupBox):
    """定时切换区域组件"""
    schedule_set = pyqtSignal(str, str)
    schedule_cancel = pyqtSignal()
    schedule_disable = pyqtSignal()
    
    def __init__(self, config, parent=None):
        super().__init__("定时自动切换", parent)
        self.config = config
        
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 深色时间设置
        dark_row = QHBoxLayout()
        dark_row.addWidget(QLabel("深色模式时间:"))
        self.dark_time_edit = QTimeEdit()
        self.dark_time_edit.setDisplayFormat("HH:mm")
        self.dark_time_edit.setTime(QTime(19, 0))
        dark_row.addWidget(self.dark_time_edit)
        layout.addLayout(dark_row)

        # 浅色时间设置
        light_row = QHBoxLayout()
        light_row.addWidget(QLabel("浅色模式时间:"))
        self.light_time_edit = QTimeEdit()
        self.light_time_edit.setDisplayFormat("HH:mm")
        self.light_time_edit.setTime(QTime(7, 0))
        light_row.addWidget(self.light_time_edit)
        layout.addLayout(light_row)

        # 操作按钮
        button_row = QHBoxLayout()
        
        self.auto_button = QPushButton("定时切换")
        self.auto_button.clicked.connect(self.on_set_schedule)
        self.auto_button.setStyleSheet("""
            QPushButton { background-color: #63b3ed; color: white;
                padding: 10px 20px; border: none; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #4299e1; }
        """)
        button_row.addWidget(self.auto_button)

        self.disable_button = QPushButton("取消定时切换")
        self.disable_button.clicked.connect(self.on_disable_schedule)
        self.disable_button.setStyleSheet("""
            QPushButton { background-color: #e53e3e; color: white;
                padding: 10px 16px; border: none; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #c53030; }
        """)
        button_row.addWidget(self.disable_button)

        self.cancel_button = QPushButton("重置")
        self.cancel_button.clicked.connect(self.on_cancel_schedule)
        self.cancel_button.setStyleSheet("""
            QPushButton { background-color: #a0aec0; color: white;
                padding: 10px 20px; border: none; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #718096; }
        """)
        button_row.addWidget(self.cancel_button)
        
        layout.addLayout(button_row)

        # 状态显示
        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("定时状态:"))
        self.schedule_status_label = QLabel("未启用" if not self.config["auto_schedule"] else "已启用")
        self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        status_row.addWidget(self.schedule_status_label)
        status_row.addStretch()
        layout.addLayout(status_row)
        
    def load_settings(self):
        """加载保存的定时设置"""
        dark_time = self.config["dark_time"].split(":")
        light_time = self.config["light_time"].split(":")
        
        self.dark_time_edit.setTime(QTime(int(dark_time[0]), int(dark_time[1])))
        self.light_time_edit.setTime(QTime(int(light_time[0]), int(light_time[1])))
        
        if self.config["auto_schedule"]:
            self.schedule_status_label.setText("已启用")
            self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #28a745;")
        else:
            self.schedule_status_label.setText("未启用")
            self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #666;")
            
    def on_set_schedule(self):
        """设置定时切换"""
        dark_time = self.dark_time_edit.time().toString("HH:mm")
        light_time = self.light_time_edit.time().toString("HH:mm")
        self.schedule_set.emit(dark_time, light_time)
        
    def on_cancel_schedule(self):
        """取消当前修改"""
        self.schedule_cancel.emit()
        
    def on_disable_schedule(self):
        """禁用定时切换"""
        self.schedule_disable.emit()
        
    def update_status(self, enabled):
        """更新定时状态显示"""
        if enabled:
            self.schedule_status_label.setText("已启用")
            self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #28a745;")
        else:
            self.schedule_status_label.setText("未启用")
            self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #666;")
            
    def reset_time_edits(self):
        """重置时间编辑框"""
        self.dark_time_edit.setTime(QTime.fromString(self.config["dark_time"], "HH:mm"))
        self.light_time_edit.setTime(QTime.fromString(self.config["light_time"], "HH:mm"))
