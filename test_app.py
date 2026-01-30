#!/usr/bin/env python3
"""
测试脚本 - 验证应用程序的各个组件
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """测试模块导入"""
    print("正在测试模块导入...")
    
    try:
        from PySide6.QtWidgets import QApplication
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QPalette
        print("✓ PySide6 模块导入成功")
    except ImportError as e:
        print(f"✗ PySide6 模块导入失败: {e}")
        return False
    
    try:
        import mysql.connector
        print("✓ MySQL Connector 模块导入成功")
    except ImportError as e:
        print(f"✗ MySQL Connector 模块导入失败: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✓ python-dotenv 模块导入成功")
    except ImportError as e:
        print(f"✗ python-dotenv 模块导入失败: {e}")
        return False
    
    return True

def test_theme_manager():
    """测试主题管理器"""
    print("\n正在测试主题管理器...")
    
    try:
        from theme_manager import ThemeManager
        theme_manager = ThemeManager()
        
        # 测试主题检测
        current_theme = theme_manager.current_theme
        print(f"✓ 当前检测到的主题: {current_theme}")
        
        # 测试主题颜色配置
        colors = theme_manager.get_current_theme()
        print(f"✓ 获取主题颜色配置成功，包含 {len(colors)} 个颜色值")
        
        # 测试系统信息
        sys_info = theme_manager.get_system_info()
        print(f"✓ 系统信息: {sys_info}")
        
        return True
    except Exception as e:
        print(f"✗ 主题管理器测试失败: {e}")
        return False

def test_database_manager():
    """测试数据库管理器"""
    print("\n正在测试数据库管理器...")
    
    try:
        from database_manager import DatabaseManager
        db_manager = DatabaseManager()
        
        # 测试连接状态
        status = db_manager.get_connection_status()
        print(f"✓ 数据库连接状态: {status}")
        
        if status['connected']:
            print("✓ 数据库连接成功")
            
            # 测试简单查询
            result = db_manager.execute_query("SELECT VERSION() as version")
            if result:
                print(f"✓ 数据库版本: {result[0]['version']}")
            
            # 测试表创建
            tables = db_manager.execute_query("SHOW TABLES")
            print(f"✓ 当前数据库表: {[table for table_dict in tables for table in table_dict.values()]}")
            
        else:
            print("⚠ 数据库连接失败，但模块可正常初始化")
        
        # 清理
        db_manager.close_connection()
        return True
    except Exception as e:
        print(f"✗ 数据库管理器测试失败: {e}")
        return False

def test_main_window():
    """测试主窗口"""
    print("\n正在测试主窗口...")
    
    try:
        from main_window import MainWindow, TitleBar
        
        # 检查类是否正常定义
        print("✓ MainWindow 类定义正常")
        print("✓ TitleBar 类定义正常")
        
        return True
    except Exception as e:
        print(f"✗ 主窗口测试失败: {e}")
        return False

def test_application():
    """测试应用程序"""
    print("\n正在测试应用程序...")
    
    try:
        # 创建一个临时的QApplication实例
        from PySide6.QtWidgets import QApplication
        app = QApplication([])
        
        from main_window import MainWindow
        window = MainWindow()
        
        print("✓ 主窗口创建成功")
        print(f"✓ 窗口标题: {window.windowTitle()}")
        print(f"✓ 窗口大小: {window.size().width()}x{window.size().height()}")
        
        return True
    except Exception as e:
        print(f"✗ 应用程序测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 投标管理软件组件测试 ===\n")
    
    tests = [
        ("模块导入", test_imports),
        ("主题管理器", test_theme_manager),
        ("数据库管理器", test_database_manager),
        ("主窗口", test_main_window),
        ("应用程序", test_application)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name}测试 ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name}测试通过")
            else:
                print(f"✗ {test_name}测试失败")
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有测试通过！应用程序可以正常运行。")
        print("\n下一步:")
        print("1. 配置MySQL数据库")
        print("2. 复制.env.example为.env并配置数据库连接")
        print("3. 运行: python main.py")
    else:
        print("✗ 部分测试失败，请检查依赖和配置。")
        print("\n可能的问题:")
        print("1. 缺少Python依赖包 - 运行: pip install -r requirements.txt")
        print("2. MySQL数据库未启动或配置错误")
        print("3. 环境变量未正确配置")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)