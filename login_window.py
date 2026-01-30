#!/usr/bin/env python3
"""
登录窗口类 - 美观的Web风格登录界面
"""

import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QSpacerItem, QSizePolicy, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPalette, QBrush, QColor, QPainter, QPen


class LoginTitleBar(QFrame):
    """登录窗口自定义标题栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(40)
        self.setObjectName("loginTitleBar")
        
        # 初始化拖拽相关变量
        self.drag_position = QPoint()
        self.mouse_pressed = False
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(0)
        
        # 应用图标和标题
        icon_label = QLabel("🏢")
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel("投标管理系统")
        title_label.setObjectName("loginTitleLabel")
        title_label.setMinimumWidth(150)
        title_label.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
        
        # 弹簧
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # 关闭按钮
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(30, 30)
        self.close_button.setObjectName("loginCloseButton")
        
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addItem(spacer)
        layout.addWidget(self.close_button)
    
    def connect_signals(self):
        """连接信号"""
        self.close_button.clicked.connect(self.parent_window.close)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mouse_pressed = True
            self.drag_position = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.mouse_pressed and event.buttons() == Qt.MouseButton.LeftButton:
            self.parent_window.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.mouse_pressed = False
        event.accept()


class LoginWindow(QWidget):
    """登录窗口类"""
    
    # 登录成功信号
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setup_window_properties()
        
        # 设置UI
        self.setup_ui()
        
        # 应用主题
        self.apply_theme()
        
        # 连接信号
        self.connect_signals()
    
    def setup_window_properties(self):
        """设置窗口属性"""
        self.setWindowTitle("投标管理系统 - 登录")
        self.setFixedSize(420, 520)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 居中显示
        screen = self.screen().geometry()
        window = self.geometry()
        self.move((screen.width() - window.width()) // 2, (screen.height() - window.height()) // 2)
    
    def setup_ui(self):
        """设置UI"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        self.title_bar = LoginTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # 内容容器
        content_frame = QFrame()
        content_frame.setObjectName("loginContentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(40, 40, 40, 40)
        content_layout.setSpacing(30)
        
        # 顶部Logo和标题
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_label = QLabel("🏢")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFont(QFont("Segoe UI Emoji", 48))
        logo_label.setObjectName("loginLogo")
        
        # 标题
        title_label = QLabel("投标管理系统")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        title_label.setObjectName("loginTitle")
        
        # 副标题
        subtitle_label = QLabel("欢迎使用 - 请登录您的账户")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setFont(QFont("Microsoft YaHei", 10))
        subtitle_label.setObjectName("loginSubtitle")
        
        logo_layout.addWidget(logo_label)
        logo_layout.addWidget(title_label)
        logo_layout.addWidget(subtitle_label)
        
        # 输入区域
        input_frame = QFrame()
        input_frame.setObjectName("loginInputFrame")
        input_layout = QVBoxLayout(input_frame)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(20)
        
        # 用户名输入
        username_layout = QVBoxLayout()
        username_label = QLabel("用户名")
        username_label.setFont(QFont("Microsoft YaHei", 10))
        username_label.setObjectName("loginLabel")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入用户名")
        self.username_input.setFont(QFont("Microsoft YaHei", 12))
        self.username_input.setObjectName("loginInput")
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # 密码输入
        password_layout = QVBoxLayout()
        password_label = QLabel("密码")
        password_label.setFont(QFont("Microsoft YaHei", 10))
        password_label.setObjectName("loginLabel")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFont(QFont("Microsoft YaHei", 12))
        self.password_input.setObjectName("loginInput")
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        input_layout.addLayout(username_layout)
        input_layout.addLayout(password_layout)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
        self.login_button.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        self.login_button.setFixedHeight(45)
        self.login_button.setObjectName("loginButton")
        
        # 记住密码选项
        remember_layout = QHBoxLayout()
        remember_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.remember_checkbox = QPushButton("记住密码")
        self.remember_checkbox.setFont(QFont("Microsoft YaHei", 9))
        self.remember_checkbox.setObjectName("rememberCheckbox")
        self.remember_checkbox.setCheckable(True)
        self.remember_checkbox.setChecked(False)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        # 忘记密码链接
        forgot_label = QLabel("忘记密码？")
        forgot_label.setFont(QFont("Microsoft YaHei", 9))
        forgot_label.setObjectName("forgotLabel")
        forgot_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addItem(spacer)
        remember_layout.addWidget(forgot_label)
        
        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Microsoft YaHei", 9))
        self.status_label.setObjectName("loginStatusLabel")
        self.status_label.setVisible(False)
        
        # 组装布局
        content_layout.addLayout(logo_layout)
        content_layout.addSpacing(20)
        content_layout.addWidget(input_frame)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.login_button)
        content_layout.addSpacing(10)
        content_layout.addLayout(remember_layout)
        content_layout.addSpacing(10)
        content_layout.addWidget(self.status_label)
        content_layout.addStretch()
        
        main_layout.addWidget(content_frame)
        
        # 保存组件引用
        self.forgot_label = forgot_label
    
    def connect_signals(self):
        """连接信号"""
        self.login_button.clicked.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        self.username_input.returnPressed.connect(self.handle_login)
        self.remember_checkbox.clicked.connect(self.toggle_remember_password)
        self.forgot_label.mousePressEvent = lambda event: self.handle_forgot_password()
    
    def apply_theme(self):
        """应用主题"""
        # 深色主题风格
        colors = {
            "window_bg": "rgba(45, 45, 48, 0.95)",
            "content_bg": "rgba(62, 62, 66, 0.9)",
            "title_bar_bg": "rgba(64, 64, 68, 0.9)",
            "border": "rgba(255, 255, 255, 0.1)",
            "text_primary": "#FFFFFF",
            "text_secondary": "#CCCCCC",
            "input_bg": "rgba(68, 68, 70, 0.8)",
            "input_border": "rgba(255, 255, 255, 0.2)",
            "button_bg": "#007ACC",
            "button_hover": "#1890FF",
            "button_pressed": "#0066CC",
            "accent": "#FF6B6B"
        }
        
        self.setStyleSheet(f"""
            LoginWindow {{
                background-color: {colors['window_bg']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
            }}
            #loginContentFrame {{
                background-color: {colors['content_bg']};
                border: none;
                border-radius: 12px 12px 0 0;
            }}
            #loginTitleBar {{
                background-color: {colors['title_bar_bg']};
                border-bottom: 1px solid {colors['border']};
                border-radius: 12px 12px 0 0;
            }}
            #loginTitle {{
                color: {colors['text_primary']};
                margin-bottom: 5px;
            }}
            #loginSubtitle {{
                color: {colors['text_secondary']};
                margin-bottom: 20px;
            }}
            #loginLogo {{
                color: {colors['accent']};
                margin-bottom: 10px;
            }}
            #loginInputFrame {{
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 20px;
            }}
            #loginLabel {{
                color: {colors['text_primary']};
                margin-bottom: 8px;
            }}
            #loginInput {{
                background-color: {colors['input_bg']};
                border: 1px solid {colors['input_border']};
                border-radius: 6px;
                padding: 12px;
                color: {colors['text_primary']};
                selection-background-color: {colors['button_bg']};
            }}
            #loginInput:focus {{
                border-color: {colors['button_bg']};
                background-color: rgba(255, 255, 255, 0.05);
            }}
            #loginButton {{
                background-color: {colors['button_bg']};
                border: none;
                border-radius: 6px;
                color: white;
                padding: 12px;
            }}
            #loginButton:hover {{
                background-color: {colors['button_hover']};
            }}
            #loginButton:pressed {{
                background-color: {colors['button_pressed']};
            }}
            #rememberCheckbox {{
                background-color: transparent;
                border: none;
                color: {colors['text_secondary']};
                padding: 8px;
            }}
            #rememberCheckbox:checked {{
                color: {colors['button_bg']};
            }}
            #forgotLabel {{
                color: {colors['text_secondary']};
                padding: 8px;
            }}
            #forgotLabel:hover {{
                color: {colors['button_bg']};
            }}
            #loginStatusLabel {{
                color: {colors['accent']};
                background-color: rgba(255, 107, 107, 0.1);
                border: 1px solid rgba(255, 107, 107, 0.3);
                border-radius: 4px;
                padding: 8px;
            }}
        """)
    
    def handle_login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        # 验证输入
        if not username:
            self.show_status("请输入用户名", True)
            self.username_input.setFocus()
            return
        
        if not password:
            self.show_status("请输入密码", True)
            self.password_input.setFocus()
            return
        
        # 显示加载状态
        self.show_status("正在验证...", False)
        self.login_button.setEnabled(False)
        
        # 模拟验证延迟
        QTimer.singleShot(1000, lambda: self.verify_credentials(username, password))
    
    def verify_credentials(self, username, password):
        """验证凭据"""
        # 硬编码验证（实际应用中应该从数据库或配置文件读取）
        if username == "admin" and password == "123":
            self.show_status("登录成功！", False)
            self.accept_login()
        else:
            self.show_status("用户名或密码错误", True)
            self.login_button.setEnabled(True)
            self.password_input.clear()
            self.password_input.setFocus()
    
    def accept_login(self):
        """接受登录"""
        # 延迟关闭窗口，让用户看到成功消息
        QTimer.singleShot(500, self.close)
        
        # 发送登录成功信号
        self.login_successful.emit()
    
    def toggle_remember_password(self):
        """切换记住密码状态"""
        is_checked = self.remember_checkbox.isChecked()
        # 这里可以实现记住密码逻辑
        print(f"记住密码: {'是' if is_checked else '否'}")
    
    def handle_forgot_password(self):
        """处理忘记密码"""
        QMessageBox.information(
            self, 
            "忘记密码", 
            "请联系系统管理员重置密码。\n\n"
            "管理员邮箱: admin@example.com"
        )
    
    def show_status(self, message, is_error=False):
        """显示状态信息"""
        self.status_label.setText(message)
        self.status_label.setVisible(True)
        
        if not is_error:
            # 成功信息自动隐藏
            QTimer.singleShot(3000, self.status_label.hide)
    
    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

