#!/usr/bin/env python3
"""
登录窗口测试程序
"""

import sys
from PySide6.QtWidgets import QApplication

# 添加项目根目录到Python路径
import os
sys.path.insert(0, os.path.dirname(__file__))

from login_window import LoginWindow


def test_login_window():
    """测试登录窗口"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("登录窗口测试")
    app.setApplicationVersion("1.0.0")
    
    print("=== 登录窗口功能测试 ===")
    print("启动登录窗口...")
    
    # 创建登录窗口
    login_window = LoginWindow()
    
    # 显示窗口
    login_window.show()
    
    print("✓ 登录窗口已启动")
    print("功能说明：")
    print("- 用户名: admin")
    print("- 密码: 123")
    print("- 无边框窗口")
    print("- Web风格界面")
    print("- 支持拖拽移动")
    print("- 美观的深色主题")
    print("- 登录验证功能")
    
    # 连接登录成功信号
    def on_login_success():
        print("✓ 登录验证成功！")
        print("提示：在实际应用中，这里会显示主窗口")
        
    login_window.login_successful.connect(on_login_success)
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(test_login_window())