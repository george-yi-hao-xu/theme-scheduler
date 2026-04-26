#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Scheduler - Windows Theme Auto Switcher
主程序入口
"""

import sys
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QMessageBox, QSystemTrayIcon, QMenu, QAction, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal

# 导入自定义模块
from src.functions.config import load_config, save_config
from src.functions.theme import get_current_theme, set_theme
from src.components.ManualSwitchGroup import ManualSwitchGroup
from src.components.ScheduleGroup import ScheduleGroup


class ThemeSwitchWorker(QThread):
    """后台主题切换工作线程"""
    switch_complete = pyqtSignal(bool, bool)  # (success, light)
    
    def __init__(self, light):
        super().__init__()
        self.light = light
        
    def run(self):
        """执行主题切换"""
        result = set_theme(self.light)
        self.switch_complete.emit(result, self.light)


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
        self.manual_switch_group = ManualSwitchGroup()
        self.manual_switch_group.update_theme_display(self.current_theme)
        self.manual_switch_group.theme_switched.connect(self.manual_switch)
        main_layout.addWidget(self.manual_switch_group)
        
        # 定时切换区域
        self.schedule_group = ScheduleGroup(self.config)
        self.schedule_group.load_settings()
        self.schedule_group.schedule_set.connect(self.set_schedule)
        self.schedule_group.schedule_cancel.connect(self.cancel_schedule)
        self.schedule_group.schedule_disable.connect(self.disable_schedule)
        main_layout.addWidget(self.schedule_group)

        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 系统托盘
        self.create_tray_icon()

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

    def manual_switch(self, light):
        """手动切换主题 - 先立即更新UI，再在后台执行切换"""
        # 立即更新UI显示
        self.current_theme = light
        self.update_status()
        
        # 在后台线程执行实际的主题切换
        self.switch_worker = ThemeSwitchWorker(light)
        self.switch_worker.switch_complete.connect(self.on_switch_complete)
        self.switch_worker.start()
        
    def on_switch_complete(self, success, light):
        """主题切换完成后的回调"""
        theme_text = "浅色模式" if light else "深色模式"
        if success:
            # 移除系统通知，避免通知堆积
            pass
        else:
            # 切换失败，恢复UI显示
            self.current_theme = not light
            self.update_status()
            QMessageBox.warning(self, "切换失败", "无法切换主题，请检查权限")

    def set_schedule(self, dark_time, light_time):
        """设置定时切换"""
        self.config["dark_time"] = dark_time
        self.config["light_time"] = light_time
        self.config["auto_schedule"] = True
        
        if save_config(self.config):
            self.schedule_group.update_status(True)
            self.status_bar.showMessage(f"定时已设置: {dark_time} 深色 / {light_time} 浅色", 3000)
            QMessageBox.information(self, "设置成功", f"定时已启用\n深色模式: {dark_time}\n浅色模式: {light_time}")
        else:
            QMessageBox.warning(self, "保存失败", "无法保存设置")

    def cancel_schedule(self):
        """取消当前修改"""
        self.schedule_group.reset_time_edits()
        self.status_bar.showMessage("已取消修改", 2000)

    def disable_schedule(self):
        """禁用定时切换"""
        self.config["auto_schedule"] = False
        if save_config(self.config):
            self.schedule_group.update_status(False)
            self.status_bar.showMessage("已禁用定时切换", 3000)
            QMessageBox.information(self, "已禁用", "已取消自动设置颜色模式")
        else:
            QMessageBox.warning(self, "操作失败", "无法禁用定时设置")

    def check_schedule(self):
        """检查定时任务"""
        if not self.config["auto_schedule"]:
            return
        
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
            # 移除系统通知，避免通知堆积
            # self.tray_icon.showMessage("主题切换器", f"定时切换至{theme_text}", QSystemTrayIcon.Information, 3000)
            self.status_bar.showMessage(f"定时切换至{theme_text}", 3000)

    def update_status(self):
        """更新状态显示"""
        theme_text = "浅色模式" if self.current_theme else "深色模式"
        self.status_bar.showMessage(f"当前主题: {theme_text}")
        self.manual_switch_group.update_theme_display(self.current_theme)

    def closeEvent(self, event):
        """关闭窗口"""
        self.schedule_timer.stop()
        # 清理系统托盘图标，避免图标堆积
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
            self.tray_icon.deleteLater()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())
