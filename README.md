# Theme Scheduler

Windows 主题定时切换器 - 根据设定的时间自动切换系统深色/浅色模式。

## 功能特性

- **手动切换**：一键切换浅色/深色模式
- **定时自动切换**：设置两个时间点，自动在深色和浅色模式之间切换
- **系统托盘支持**：最小化到托盘，右键菜单快速操作
- **通知提醒**：切换主题时显示系统通知

## 使用方法

### 运行程序

直接双击 `dist/ThemeScheduler.exe` 即可运行。

### 手动切换

1. 点击「切换到浅色模式」按钮切换到浅色主题
2. 点击「切换到深色模式」按钮切换到深色主题

### 定时自动切换

1. 设置「深色模式时间」（如 19:00）
2. 设置「浅色模式时间」（如 07:00）
3. 点击「自动设置」按钮启用定时切换
4. 点击「取消自动设置颜色模式」按钮禁用定时切换

### 开机自启

将 `ThemeScheduler.exe` 的快捷方式放入 `shell:startup` 文件夹。

## 配置文件

配置文件 `config.json` 与程序放在同一目录：

```json
{
    "dark_time": "19:00",
    "light_time": "07:00",
    "auto_schedule": false
}
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| dark_time | 切换到深色模式的时间 | "19:00" |
| light_time | 切换到浅色模式的时间 | "07:00" |
| auto_schedule | 是否启用定时切换 | false |

## 项目结构

```
theme-scheduler/
├── main.py              # 主程序入口
├── config.json          # 配置文件
├── setup.py             # 打包脚本
├── README.md            # 项目说明
├── .gitignore           # Git 忽略配置
├── .gitattributes       # Git 属性配置
└── src/
    └── functions/
        ├── config.py    # 配置管理模块
        ├── theme.py     # 主题切换模块
        └── schedule.py  # 定时任务模块
```

## 构建说明

### 依赖安装

```bash
pip install pyinstaller pyqt5
```

### 打包成 EXE

```bash
python setup.py
```

打包后的文件位于 `dist/ThemeScheduler.exe`。

## 注意事项

1. 程序需要修改 Windows 注册表的权限
2. 建议以普通用户身份运行，不需要管理员权限
3. 定时切换每分钟检查一次时间

## License

MIT License
