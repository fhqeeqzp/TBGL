import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QBrush, QColor, QPainter, QPen
from theme_manager import ThemeManager
from database_manager import DatabaseManager


class TitleBar(QFrame):
    """自定义标题栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(40)
        self.setObjectName("titleBar")
        
        # 初始化拖拽相关变量
        self.drag_position = QPoint()
        self.mouse_pressed = False
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(0)
        
        # 应用图标和标题
        icon_label = QLabel()
        icon_label.setFixedSize(24, 24)
        icon_label.setObjectName("appIcon")
        
        title_label = QLabel("投标管理软件")
        title_label.setObjectName("titleLabel")
        title_label.setMinimumWidth(200)
        
        # 弹簧
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # 控制按钮
        self.min_button = QPushButton("−")
        self.min_button.setFixedSize(30, 30)
        self.min_button.setObjectName("minButton")
        
        self.max_button = QPushButton("□")
        self.max_button.setFixedSize(30, 30)
        self.max_button.setObjectName("maxButton")
        
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("closeButton")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addItem(spacer)
        layout.addWidget(self.min_button)
        layout.addWidget(self.max_button)
        layout.addWidget(self.close_button)
    
    def connect_signals(self):
        """连接信号"""
        self.min_button.clicked.connect(self.parent_window.showMinimized)
        self.max_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.parent_window.close)
    
    def toggle_maximize(self):
        """切换最大化状态"""
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.mouse_pressed and event.buttons() == Qt.MouseButton.LeftButton:
            if not self.parent_window.isMaximized():
                self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.mouse_pressed = False
        event.accept()


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        
        # 数据库管理器（可能在初始化失败）
        self.database_manager = None
        self.database_available = False
        
        # 窗口状态
        self.is_maximized = False
        
        self.setup_ui()
        self.setup_timers()
        self.apply_theme()
        self.apply_style()
        
        # 尝试初始化数据库（在后台进行）
        self.initialize_database()
    
    def initialize_database(self):
        """初始化数据库连接"""
        try:
            from database_manager import DatabaseManager
            self.database_manager = DatabaseManager()
            
            # 测试连接
            if self.database_manager.test_connection():
                self.database_available = True
                print("✓ 数据库连接成功")
            else:
                print("⚠ 数据库连接失败，应用程序将以离线模式运行")
        except Exception as e:
            print(f"⚠ 数据库初始化失败: {e}")
            self.database_manager = None
            self.database_available = False
        
    def setup_ui(self):
        """设置UI"""
        # 设置窗口属性
        self.setWindowTitle("投标管理软件")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        self.title_bar = TitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # 内容区域
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)
        
        # 欢迎标签
        welcome_label = QLabel("欢迎使用投标管理软件")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        content_layout.addWidget(welcome_label)
        main_layout.addWidget(content_frame)
    
    def setup_timers(self):
        """设置定时器"""
        # 主题检查定时器
        self.theme_timer = QTimer()
        self.theme_timer.timeout.connect(self.check_system_theme)
        self.theme_timer.start(1000)  # 每秒检查一次
    
    def check_system_theme(self):
        """检查系统主题变化"""
        if self.theme_manager.check_theme_change():
            self.apply_theme()
            self.apply_style()
    
    def apply_theme(self):
        """应用主题"""
        theme_colors = self.theme_manager.get_current_theme()
        
        # 设置窗口颜色
        self.setStyleSheet(f"""
            MainWindow {{
                background-color: {theme_colors['window_bg']};
            }}
            #contentFrame {{
                background-color: {theme_colors['content_bg']};
                border: 1px solid {theme_colors['border_color']};
                border-radius: 8px;
            }}
            #titleBar {{
                background-color: {theme_colors['title_bar_bg']};
                border-bottom: 1px solid {theme_colors['border_color']};
            }}
            #welcomeLabel {{
                color: {theme_colors['text_color']};
                font-size: 24px;
                font-weight: bold;
            }}
        """)
    
    def apply_style(self):
        """应用样式到控件"""
        theme_colors = self.theme_manager.get_current_theme()
        
        # 设置按钮样式
        style = f"""
            QPushButton {{
                background-color: {theme_colors['button_bg']};
                color: {theme_colors['button_text']};
                border: 1px solid {theme_colors['border_color']};
                border-radius: 4px;
                padding: 5px 10px;
            }}
            QPushButton:hover {{
                background-color: {theme_colors['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {theme_colors['button_pressed']};
            }}
            #closeButton {{
                background-color: {theme_colors['close_button_bg']};
                color: {theme_colors['close_button_text']};
            }}
            #closeButton:hover {{
                background-color: {theme_colors['close_button_hover']};
            }}
            #titleLabel {{
                color: {theme_colors['text_color']};
                font-size: 14px;
                font-weight: bold;
            }}
        """
        
        self.title_bar.setStyleSheet(style)
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        
        # 检查是否最大化状态改变
        current_maximized = self.isMaximized()
        if current_maximized != self.is_maximized:
            self.is_maximized = current_maximized
            if hasattr(self.title_bar, 'max_button'):
                self.title_bar.max_button.setText("□" if not current_maximized else "◻")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 清理数据库连接
        if self.database_manager:
            self.database_manager.close_connection()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("投标管理软件")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Company")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())