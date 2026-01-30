# coding:utf-8
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..common.mysql_manager import mysql_manager


class RegisterDialog(QDialog):
    """ 用户注册对话框 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """ 初始化用户界面 """
        self.setWindowTitle("用户注册")
        self.setModal(True)
        self.resize(400, 350)
        self.setMinimumSize(380, 320)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title_label = QLabel("用户注册", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # 输入表单布局
        form_layout = QGridLayout()
        
        # 用户名输入
        self.username_label = QLabel("用户名:", self)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("3-20个字符，支持字母、数字、下划线")
        form_layout.addWidget(self.username_label, 0, 0)
        form_layout.addWidget(self.username_input, 0, 1, 1, 2)
        
        # 密码输入
        self.password_label = QLabel("密码:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("至少6个字符")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1, 1, 2)
        
        # 确认密码输入
        self.confirm_password_label = QLabel("确认密码:", self)
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setPlaceholderText("请再次输入密码")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.confirm_password_label, 2, 0)
        form_layout.addWidget(self.confirm_password_input, 2, 1, 1, 2)
        
        # 邮箱输入
        self.email_label = QLabel("邮箱:", self)
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("请输入有效的邮箱地址")
        form_layout.addWidget(self.email_label, 3, 0)
        form_layout.addWidget(self.email_input, 3, 1, 1, 2)
        
        # 角色选择（固定为普通用户）
        self.role_label = QLabel("角色:", self)
        self.role_input = QComboBox(self)
        self.role_input.addItems(["user"])
        self.role_input.setEnabled(False)  # 禁用角色选择
        form_layout.addWidget(self.role_label, 4, 0)
        form_layout.addWidget(self.role_input, 4, 1, 1, 2)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 注册按钮
        self.register_btn = QPushButton("注册", self)
        self.register_btn.clicked.connect(self.register_user)
        self.register_btn.setDefault(True)
        
        # 取消按钮
        self.cancel_btn = QPushButton("取消", self)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.register_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # 提示标签
        hint_label = QLabel("注意：用户名和密码区分大小写", self)
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_label.setStyleSheet("color: gray; font-size: 12px;")
        
        # 添加到主布局
        main_layout.addWidget(title_label)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(hint_label)
        
        # 连接回车键注册
        self.username_input.returnPressed.connect(self.register_user)
        self.password_input.returnPressed.connect(self.register_user)
        self.confirm_password_input.returnPressed.connect(self.register_user)
        self.email_input.returnPressed.connect(self.register_user)

    def validate_input(self):
        """ 验证输入信息 """
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        email = self.email_input.text().strip()
        
        # 检查用户名
        if not username:
            QMessageBox.warning(self, "输入错误", "请输入用户名")
            return False
        
        if len(username) < 3 or len(username) > 20:
            QMessageBox.warning(self, "输入错误", "用户名长度必须在3-20个字符之间")
            return False
        
        # 检查密码
        if not password:
            QMessageBox.warning(self, "输入错误", "请输入密码")
            return False
        
        if len(password) < 6:
            QMessageBox.warning(self, "输入错误", "密码长度至少6个字符")
            return False
        
        # 检查确认密码
        if password != confirm_password:
            QMessageBox.warning(self, "输入错误", "两次输入的密码不一致")
            return False
        
        # 检查邮箱
        if not email:
            QMessageBox.warning(self, "输入错误", "请输入邮箱地址")
            return False
        
        # 简单的邮箱格式验证
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "输入错误", "请输入有效的邮箱地址")
            return False
        
        return True

    def register_user(self):
        """ 注册用户 """
        if not self.validate_input():
            return
        
        username = self.username_input.text().strip()
        password = self.password_input.text()
        email = self.email_input.text().strip()
        role = self.role_input.currentText()
        
        try:
            # 从数据库注册用户
            success, message = mysql_manager.register_user(username, password, email, role)
            
            if success:
                # 注册成功
                QMessageBox.information(self, "注册成功", f"用户 '{username}' 注册成功！\n\n请使用此账号登录系统。")
                self.accept()
            else:
                # 注册失败，显示错误消息
                QMessageBox.warning(self, "注册失败", message)
                
        except Exception as e:
            QMessageBox.critical(self, "注册异常", f"注册异常：\n{str(e)}")
