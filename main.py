# coding:utf-8
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common.config import cfg
from app.view.login_window import LoginWindow
from app.view.main_window import MainWindow


# PyQt6中不需要显式设置高DPI缩放，这些功能已经自动启用
# enable dpi scale (PyQt6中这些属性已被移除)
if cfg.get(cfg.dpiScale) == "Auto":
    pass  # PyQt6中默认启用高DPI缩放
else:
    # 对于固定缩放因子，可能需要其他处理方式
    pass

# create application
app = QApplication(sys.argv)

# internationalization
locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)

app.installTranslator(translator)

# 启动登录流程
def main():
    """ 主程序入口 """
    # 显示登录窗口
    login_window = LoginWindow()
    result = login_window.exec()
    
    if result == 1:  # QDialog.DialogCode.Accepted.value = 1
        # 登录成功，显示主窗口
        w = MainWindow()
        w.show()
        app.exec()
    else:
        # 登录失败，退出程序
        sys.exit(0)

if __name__ == "__main__":
    main()
