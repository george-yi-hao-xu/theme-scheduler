#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Scheduler - Windows Theme Auto Switcher
主程序入口
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTimeEdit, QMessageBox, QSystemTrayIcon, QMenu, QAction,
    QGroupBox, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer, QTime

# 导入自定义模块
from src.functions.config import load_config, save_config
from src.functions.theme import get_current_theme, set_theme


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.current_theme = get_current_theme()
        
        # 定时检查器 (每分钟检查一次)
        self.schedule_timer = QTimer()
        self.schedule_timer.timeout.connect(self.check_schedule)
        self.schedule_timer.start(60000)
        
        self.init_ui()
        self.load_schedule_settings()

    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("主题定时切换器")
        self.setMinimumSize(380, 320)

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 手动切换区域
        main_layout.addWidget(self.create_manual_switch_group())
        
        # 定时切换区域
        main_layout.addWidget(self.create_schedule_group())

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 系统托盘
        self.create_tray_icon()

    def create_manual_switch_group(self):
        """创建手动切换区域"""
        group = QGroupBox("手动切换")
        layout = QVBoxLayout(group)
        
        # 切换按钮
        button_row = QHBoxLayout()
        
        self.light_button = QPushButton("切换到浅色模式")
        self.light_button.clicked.connect(lambda: self.manual_switch(True))
        self.light_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white;
                padding: 12px 24px; border: none; border-radius: 8px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        button_row.addWidget(self.light_button)

        self.dark_button = QPushButton("切换到深色模式")
        self.dark_button.clicked.connect(lambda: self.manual_switch(False))
        self.dark_button.setStyleSheet("""
            QPushButton {
                background-color: #555; color: white;
                padding: 12px 24px; border: none; border-radius: 8px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background-color: #444; }
        """)
        button_row.addWidget(self.dark_button)
        
        layout.addLayout(button_row)
        
        # 当前主题显示
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("当前主题:"))
        self.current_theme_label = QLabel("浅色模式" if self.current_theme else "深色模式")
        self.current_theme_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        theme_row.addWidget(self.current_theme_label)
        theme_row.addStretch()
        layout.addLayout(theme_row)
        
        return group

    def create_schedule_group(self):
        """创建定时切换区域"""
        group = QGroupBox("定时自动切换")
        layout = QVBoxLayout(group)
        
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
        
        self.auto_button = QPushButton("自动设置")
        self.auto_button.clicked.connect(self.set_schedule)
        self.auto_button.setStyleSheet("""
            QPushButton { background-color: #2196F3; color: white;
                padding: 10px 20px; border: none; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #1976D2; }
        """)
        button_row.addWidget(self.auto_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_schedule)
        self.cancel_button.setStyleSheet("""
            QPushButton { background-color: #FF9800; color: white;
                padding: 10px 20px; border: none; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #F57C00; }
        """)
        button_row.addWidget(self.cancel_button)

        self.disable_button = QPushButton("取消自动设置颜色模式")
        self.disable_button.clicked.connect(self.disable_schedule)
        self.disable_button.setStyleSheet("""
            QPushButton { background-color: #f44336; color: white;
                padding: 10px 16px; border: none; border-radius: 6px; font-size: 13px; }
            QPushButton:hover { background-color: #d32f2f; }
        """)
        button_row.addWidget(self.disable_button)
        
        layout.addLayout(button_row)

        # 状态显示
        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("定时状态:"))
        self.schedule_status_label = QLabel("未启用" if not self.config["auto_schedule"] else "已启用")
        self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        status_row.addWidget(self.schedule_status_label)
        status_row.addStretch()
        layout.addLayout(status_row)
        
        return group

    def create_tray_icon(self):
        """创建系统托盘图标"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(1))
        
        tray_menu = QMenu()
        tray_menu.addAction("切换浅色", lambda: self.manual_switch(True))
        tray_menu.addAction("切换深色", lambda: self.manual_switch(False))
        tray_menu.addSeparator()
        tray_menu.addAction("显示窗口", self.show)
        tray_menu.addAction("退出", self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(lambda r: self.show() if r == QSystemTrayIcon.DoubleClick else None)

    def load_schedule_settings(self):
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

    def manual_switch(self, light):
        """手动切换主题"""
        if set_theme(light):
            self.current_theme = light
            self.update_status()
            theme_text = "浅色模式" if light else "深色模式"
            self.tray_icon.showMessage("主题切换器", f"已切换至{theme_text}", QSystemTrayIcon.Information, 3000)
        else:
            QMessageBox.warning(self, "切换失败", "无法切换主题，请检查权限")

    def set_schedule(self):
        """设置定时切换"""
        dark_time = self.dark_time_edit.time().toString("HH:mm")
        light_time = self.light_time_edit.time().toString("HH:mm")
        
        self.config["dark_time"] = dark_time
        self.config["light_time"] = light_time
        self.config["auto_schedule"] = True
        
        if save_config(self.config):
            self.schedule_status_label.setText("已启用")
            self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #28a745;")
            self.status_bar.showMessage(f"定时已设置: {dark_time} 深色 / {light_time} 浅色", 3000)
            QMessageBox.information(self, "设置成功", f"定时已启用\n深色模式: {dark_time}\n浅色模式: {light_time}")
        else:
            QMessageBox.warning(self, "保存失败", "无法保存设置")

    def cancel_schedule(self):
        """取消当前修改"""
        self.dark_time_edit.setTime(QTime.fromString(self.config["dark_time"], "HH:mm"))
        self.light_time_edit.setTime(QTime.fromString(self.config["light_time"], "HH:mm"))
        self.status_bar.showMessage("已取消修改", 2000)

    def disable_schedule(self):
        """禁用定时切换"""
        self.config["auto_schedule"] = False
        if save_config(self.config):
            self.schedule_status_label.setText("未启用")
            self.schedule_status_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #666;")
            self.status_bar.showMessage("已禁用定时切换", 3000)
            QMessageBox.information(self, "已禁用", "已取消自动设置颜色模式")
        else:
            QMessageBox.warning(self, "操作失败", "无法禁用定时设置")

    def check_schedule(self):
        """检查定时任务"""
        if not self.config["auto_schedule"]:
            return
        
        from datetime import datetime
        
        now = datetime.now().time()
        dark_time = datetime.strptime(self.config["dark_time"], "%H:%M").time()
        light_time = datetime.strptime(self.config["light_time"], "%H:%M").time()
        
        should_be_dark = False
        
        if dark_time > light_time:
            if now >= dark_time or now < light_time:
                should_be_dark = True
        else:
            if now >= dark_time and now < light_time:
                should_be_dark = True
        
        if should_be_dark and self.current_theme:
            self.auto_switch(False)
        elif not should_be_dark and not self.current_theme:
            self.auto_switch(True)

    def auto_switch(self, light):
        """自动切换主题"""
        if set_theme(light):
            self.current_theme = light
            self.update_status()
            theme_text = "浅色模式" if light else "深色模式"
            self.tray_icon.showMessage("主题切换器", f"定时切换至{theme_text}", QSystemTrayIcon.Information, 3000)
            self.status_bar.showMessage(f"定时切换至{theme_text}", 3000)

    def update_status(self):
        """更新状态显示"""
        theme_text = "浅色模式" if self.current_theme else "深色模式"
        self.current_theme_label.setText(theme_text)
        self.status_bar.showMessage(f"当前主题: {theme_text}")

    def closeEvent(self, event):
        """关闭窗口"""
        self.schedule_timer.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
