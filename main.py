#!/usr/bin/env python3
"""
投标管理软件 - 主入口程序
使用PyQt6 + MySQL开发的现代化无边框窗口应用
"""

import sys
import os
import logging
import traceback
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMessageBox, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QIcon

from main_window import MainWindow
from theme_manager import ThemeManager
from database_manager import DatabaseManager


class Application:
    """应用程序主类"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.theme_manager = None
        self.database_manager = None
        self.splash = None
        
        # 设置日志
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志系统"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler('bidding_management.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_splash_screen(self):
        """创建启动画面"""
        try:
            # 创建一个简单的启动画面
            splash_pixmap = QPixmap(400, 300)
            splash_pixmap.fill(Qt.GlobalColor.white)
            
            self.splash = QSplashScreen(splash_pixmap)
            self.splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
            
            # 设置启动画面文字
            font = QFont()
            font.setPointSize(16)
            self.splash.setFont(font)
            
            self.splash.showMessage("正在启动投标管理软件...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
            self.splash.show()
            
            # 强制刷新显示
            self.app.processEvents()
            
        except Exception as e:
            self.logger.warning(f"创建启动画面失败: {e}")
    
    def setup_application(self):
        """设置应用程序"""
        # 创建QApplication实例
        self.app = QApplication(sys.argv)
        
        # 设置应用程序信息
        self.app.setApplicationName("投标管理软件")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Company")
        self.app.setOrganizationDomain("company.com")
        
        # 设置应用程序图标
        try:
            icon_path = os.path.join(project_root, "resources", "icon.ico")
            if os.path.exists(icon_path):
                self.app.setWindowIcon(QIcon(icon_path))
        except Exception as e:
            self.logger.warning(f"设置应用图标失败: {e}")
        
        # 创建启动画面
        self.create_splash_screen()
        
        # 初始化组件
        self.initialize_components()
        
        # 关闭启动画面
        if self.splash:
            self.splash.finish(self.main_window)
    
    def initialize_components(self):
        """初始化应用程序组件"""
        try:
            if self.splash:
                self.splash.showMessage("正在初始化主题管理器...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
                self.app.processEvents()
            
            # 初始化主题管理器
            self.theme_manager = ThemeManager()
            
            # 数据库连接延迟到主窗口创建时进行
            # 这避免了在GUI启动前阻塞
            
            if self.splash:
                self.splash.showMessage("正在创建主窗口...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
                self.app.processEvents()
            
            # 创建主窗口
            self.main_window = MainWindow()
            
            # 延迟初始化数据库管理器
            self.database_manager = None
            # 数据库连接由MainWindow内部处理
            
            # 连接主题变化信号
            self.theme_manager.theme_changed.connect(self.main_window.apply_theme)
            
            self.logger.info("应用程序组件初始化完成")
            
        except Exception as e:
            self.logger.error(f"初始化组件失败: {e}")
            self.logger.error(traceback.format_exc())
            raise
    
    def show_welcome_message(self):
        """显示欢迎消息"""
        try:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("欢迎使用")
            msg.setText("投标管理软件已成功启动！\n\n"
                       "功能特性：\n"
                       "• 无边框现代化界面\n"
                       "• 智能主题适配\n"
                       "• MySQL数据库支持\n"
                       "• 完整的投标管理功能")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        except Exception as e:
            self.logger.warning(f"显示欢迎消息失败: {e}")
    
    def run(self):
        """运行应用程序"""
        try:
            # 设置应用程序
            self.setup_application()
            
            # 显示主窗口
            self.main_window.show()
            
            # 显示欢迎消息
            QTimer.singleShot(1000, self.show_welcome_message)
            
            self.logger.info("应用程序启动成功")
            
            # 运行事件循环
            return self.app.exec()
            
        except Exception as e:
            self.logger.error(f"应用程序运行失败: {e}")
            self.logger.error(traceback.format_exc())
            
            if self.app:
                QMessageBox.critical(None, "启动错误", f"应用程序启动失败:\n{e}")
            
            return 1
        
        finally:
            # 清理资源
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        try:
            self.logger.info("正在清理应用程序资源...")
            
            if self.database_manager:
                self.database_manager.close_connection()
            
            if self.splash:
                self.splash.close()
            
            self.logger.info("资源清理完成")
            
        except Exception as e:
            self.logger.error(f"清理资源失败: {e}")


def main():
    """主函数"""
    try:
        # 检查Python版本
        if sys.version_info < (3, 8):
            print("错误：需要Python 3.8或更高版本")
            return 1
        
        # 检查依赖
        required_modules = [
            'PyQt6', 'mysql.connector', 'dotenv'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            print(f"错误：缺少必要的依赖模块: {', '.join(missing_modules)}")
            print("请运行: pip install -r requirements.txt")
            return 1
        
        # 创建并运行应用程序
        app = Application()
        return app.run()
        
    except KeyboardInterrupt:
        print("\n用户中断程序")
        return 0
    except Exception as e:
        print(f"未处理的异常: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)