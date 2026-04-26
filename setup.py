#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

try:
    import PyInstaller.__main__
except ImportError:
    print("Please install dependencies first: pip install pyinstaller pyqt5")
    sys.exit(1)

def main():
    project_dir = Path(__file__).parent
    script_path = project_dir / "main.py"
    
    if not script_path.exists():
        print(f"Error: Cannot find {script_path}")
        sys.exit(1)
    
    args = [
        str(script_path),
        "--onefile",
        "--windowed",
        "--name=ThemeScheduler",
        "--add-data=config.json;.\\",
        "--add-data=src/functions/config.py;src/functions\\",
        "--add-data=src/functions/theme.py;src/functions\\",
        "--add-data=src/functions/schedule.py;src/functions\\",
        "--clean",
    ]
    
    print(f"Running PyInstaller: {' '.join(args)}")
    PyInstaller.__main__.run(args)
    
    dist_dir = project_dir / "dist"
    if dist_dir.exists():
        import shutil
        src_config = project_dir / "config.json"
        dst_config = dist_dir / "config.json"
        if src_config.exists():
            shutil.copy(src_config, dst_config)
            print(f"Copied config.json to {dst_config}")
    
    print("\nPackaging completed! Output file: dist/ThemeScheduler.exe")

if __name__ == "__main__":
    main()
