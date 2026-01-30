# coding:utf-8
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .mysql_config_dialog import MySQLConfigDialog
from .register_dialog import RegisterDialog
from ..common.mysql_manager import mysql_manager


class LoginWindow(QDialog):
    """ 登录窗口类 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """ 初始化用户界面 """
        self.setWindowTitle("系统登录")
        self.setModal(True)
        self.resize(400, 300)
        self.setMinimumSize(350, 280)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 40, 30, 30)
        
        # 标题
        title_label = QLabel("投标管理系统", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # 副标题
        subtitle_label = QLabel("请输入登录信息", self)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 用户名输入
        username_layout = QHBoxLayout()
        username_label = QLabel("用户名:", self)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("请输入用户名")
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # MySQL配置按钮
        self.mysql_config_btn = QPushButton("MySQL配置", self)
        self.mysql_config_btn.clicked.connect(self.open_mysql_config)
        
        # 注册按钮
        self.register_btn = QPushButton("注册", self)
        self.register_btn.clicked.connect(self.open_register)
        
        # 登录按钮
        self.login_btn = QPushButton("登录", self)
        self.login_btn.clicked.connect(self.check_login)
        self.login_btn.setDefault(True)
        
        button_layout.addWidget(self.mysql_config_btn)
        button_layout.addWidget(self.register_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.login_btn)
        
        # 提示标签
        hint_label = QLabel("请使用数据库中的用户名和密码登录", self)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_label.setStyleSheet("color: gray; font-size: 12px;")
        
        # 添加到主布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(subtitle_label)
        main_layout.addLayout(username_layout)
        main_layout.addLayout(password_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(hint_label)
        
        # 连接回车键登录
        self.username_input.returnPressed.connect(self.check_login)
        self.password_input.returnPressed.connect(self.check_login)

    def check_login(self):
        """ 检查登录信息 """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "输入错误", "请输入用户名和密码")
            return
        
        try:
            # 从数据库验证用户信息
            success, message = mysql_manager.verify_user(username, password)
            
            if success:
                # 登录成功，关闭对话框
                QMessageBox.information(self, "登录成功", message)
                self.accept()
            else:
                # 登录失败，显示错误消息
                QMessageBox.warning(self, "登录失败", message)
                
        except Exception as e:
            QMessageBox.critical(self, "登录异常", f"登录验证异常：\n{str(e)}")

    def open_mysql_config(self):
        """ 打开MySQL配置对话框 """
        try:
            dialog = MySQLConfigDialog(self)
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted.value:
                QMessageBox.information(self, "配置成功", "MySQL配置已保存")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开MySQL配置时出错: {str(e)}")

    def open_register(self):
        """ 打开注册对话框 """
        try:
            dialog = RegisterDialog(self)
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted.value:
                QMessageBox.information(self, "注册成功", "注册成功！请使用新账号登录。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开注册对话框时出错: {str(e)}")
