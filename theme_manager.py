import sys
import os
import platform
from typing import Dict, Any
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication


class ThemeManager(QObject):
    """主题管理器 - 检测和适应系统主题变化"""
    
    theme_changed = Signal()
    
    def __init__(self):
        super().__init__()
        self.system = platform.system()
        self.current_theme = self.detect_system_theme()
        self.last_checked_theme = self.current_theme
        
    def detect_system_theme(self) -> str:
        """检测当前系统主题"""
        try:
            if self.system == "Windows":
                return self._detect_windows_theme()
            elif self.system == "Darwin":  # macOS
                return self._detect_macos_theme()
            elif self.system == "Linux":
                return self._detect_linux_theme()
            else:
                return "light"  # 默认浅色主题
        except Exception:
            return "light"
    
    def _detect_windows_theme(self) -> str:
        """检测Windows主题"""
        try:
            import winreg
            
            # 检查注册表中的主题设置
            try:
                # Windows 10/11 主题设置
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                
                # AppsUseLightTheme 值
                apps_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                winreg.CloseKey(key)
                winreg.CloseKey(registry)
                
                if apps_light_theme == 0:
                    return "dark"
                else:
                    return "light"
            except FileNotFoundError:
                # 如果注册表项不存在，尝试其他方法
                return self._detect_windows_theme_fallback()
                
        except ImportError:
            # 如果无法导入winreg，使用备用方法
            return self._detect_windows_theme_fallback()
        except Exception:
            return "light"
    
    def _detect_windows_theme_fallback(self) -> str:
        """Windows主题检测的备用方法"""
        try:
            # 检查系统颜色设置
            import ctypes
            from ctypes import wintypes
            
            # 获取系统颜色值
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
            
            # 检查是否为深色模式（通过检查系统颜色）
            # 这是一个简化的检测方法
            return "light"  # 默认返回浅色主题
        except Exception:
            return "light"
    
    def _detect_macos_theme(self) -> str:
        """检测macOS主题"""
        try:
            import subprocess
            # 使用defaults命令检查macOS主题
            result = subprocess.run([
                'defaults', 'read', '-g', 'AppleInterfaceStyle'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return "dark"
            else:
                return "light"
        except Exception:
            return "light"
    
    def _detect_linux_theme(self) -> str:
        """检测Linux主题"""
        try:
            # 检查GTK主题设置
            gtk_settings = self._check_gtk_theme()
            if gtk_settings:
                return gtk_settings
            
            # 检查Qt主题设置
            qt_theme = self._check_qt_theme()
            if qt_theme:
                return qt_theme
                
            return "light"
        except Exception:
            return "light"
    
    def _check_gtk_theme(self) -> str:
        """检查GTK主题"""
        try:
            import subprocess
            
            # 检查当前GTK主题
            result = subprocess.run([
                'gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                theme_name = result.stdout.strip().strip("'\"")
                # 简单判断是否为深色主题
                if 'dark' in theme_name.lower():
                    return "dark"
                else:
                    return "light"
        except Exception:
            pass
        return None
    
    def _check_qt_theme(self) -> str:
        """检查Qt主题"""
        try:
            # 检查Qt应用程序的主题设置
            app = QApplication.instance()
            if app:
                palette = app.palette()
                
                # 检查窗口文本颜色来判断主题
                window_text_color = palette.color(QPalette.ColorRole.WindowText)
                
                # 如果窗口文本颜色较暗，可能是深色主题
                if window_text_color.lightness() < 128:
                    return "dark"
                else:
                    return "light"
        except Exception:
            pass
        return None
    
    def get_theme_colors(self, theme_type: str) -> Dict[str, str]:
        """获取主题颜色配置"""
        colors = {
            "light": {
                "window_bg": "#F5F5F5",
                "content_bg": "#FFFFFF",
                "title_bar_bg": "#E8E8E8",
                "text_color": "#333333",
                "border_color": "#CCCCCC",
                "button_bg": "#F0F0F0",
                "button_text": "#333333",
                "button_hover": "#E0E0E0",
                "button_pressed": "#D0D0D0",
                "close_button_bg": "#E74C3C",
                "close_button_text": "#FFFFFF",
                "close_button_hover": "#C0392B"
            },
            "dark": {
                "window_bg": "#2C2C2C",
                "content_bg": "#3C3C3C",
                "title_bar_bg": "#404040",
                "text_color": "#FFFFFF",
                "border_color": "#555555",
                "button_bg": "#555555",
                "button_text": "#FFFFFF",
                "button_hover": "#666666",
                "button_pressed": "#777777",
                "close_button_bg": "#E74C3C",
                "close_button_text": "#FFFFFF",
                "close_button_hover": "#C0392B"
            }
        }
        
        return colors.get(theme_type, colors["light"])
    
    def get_current_theme(self) -> Dict[str, str]:
        """获取当前主题颜色配置"""
        return self.get_theme_colors(self.current_theme)
    
    def check_theme_change(self) -> bool:
        """检查主题是否发生变化"""
        new_theme = self.detect_system_theme()
        
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            self.theme_changed.emit()
            return True
        
        return False
    
    def set_theme(self, theme_type: str):
        """手动设置主题"""
        if theme_type in ["light", "dark"]:
            self.current_theme = theme_type
            self.theme_changed.emit()
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        return {
            "platform": self.system,
            "theme": self.current_theme,
            "is_dark_mode": self.current_theme == "dark"
        }