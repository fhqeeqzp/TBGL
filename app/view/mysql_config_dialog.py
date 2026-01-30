# coding:utf-8
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, 
                           QLabel, QLineEdit, QSpinBox, QPushButton, QGroupBox,
                           QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt

from ..common.config import cfg
from ..common.mysql_manager import mysql_manager


class MySQLConfigDialog(QDialog):
    """ MySQL配置对话框 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mysql_manager = mysql_manager
        self.config = self.mysql_manager.config_manager.get_config()
        self.is_admin = False  # 是否为管理员权限
        self.is_configured = self.config.get('is_configured', False)
        self.is_initialized = self.config.get('is_initialized', False)
        self.initUI()
        self.load_config()
        self.update_ui_state()

    def initUI(self):
        """ 初始化用户界面 """
        self.setWindowTitle("MySQL数据库配置")
        self.setModal(True)
        self.resize(550, 450)
        self.setMinimumSize(500, 400)
        
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 权限提示
        self.permission_label = QLabel("当前权限: 普通用户", self)
        self.permission_label.setStyleSheet("color: red; font-weight: bold;")
        
        # 数据库连接配置组
        connection_group = QGroupBox("数据库连接配置", self)
        connection_layout = QGridLayout(connection_group)
        
        # 主机地址
        self.host_label = QLabel("主机地址:", self)
        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText("localhost 或 IP地址")
        connection_layout.addWidget(self.host_label, 0, 0)
        connection_layout.addWidget(self.host_input, 0, 1)
        
        # 端口
        self.port_label = QLabel("端口:", self)
        self.port_input = QSpinBox(self)
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(3306)
        connection_layout.addWidget(self.port_label, 0, 2)
        connection_layout.addWidget(self.port_input, 0, 3)
        
        # 用户名
        self.username_label = QLabel("用户名:", self)
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("数据库用户名")
        connection_layout.addWidget(self.username_label, 1, 0)
        connection_layout.addWidget(self.username_input, 1, 1, 1, 2)
        
        # 密码
        self.password_label = QLabel("密码:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("数据库密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        connection_layout.addWidget(self.password_label, 1, 3)
        connection_layout.addWidget(self.password_input, 1, 4)
        
        # 字符集
        self.charset_label = QLabel("字符集:", self)
        self.charset_input = QLineEdit(self)
        self.charset_input.setPlaceholderText("utf8mb4")
        self.charset_input.setText("utf8mb4")
        connection_layout.addWidget(self.charset_label, 2, 0)
        connection_layout.addWidget(self.charset_input, 2, 1)
        
        # 测试连接按钮
        self.test_btn = QPushButton("测试连接", self)
        self.test_btn.clicked.connect(self.test_connection)
        connection_layout.addWidget(self.test_btn, 2, 2, 1, 2)
        
        # 数据库配置组
        database_group = QGroupBox("数据库配置", self)
        database_layout = QGridLayout(database_group)
        
        # 数据库名
        self.database_label = QLabel("数据库名:", self)
        self.database_input = QLineEdit(self)
        self.database_input.setPlaceholderText("数据库名称")
        database_layout.addWidget(self.database_label, 0, 0)
        database_layout.addWidget(self.database_input, 0, 1, 1, 3)
        
        # 初始化按钮
        self.init_btn = QPushButton("初始化数据库", self)
        self.init_btn.clicked.connect(self.initialize_database)
        self.init_btn.setEnabled(False)  # 初始时禁用
        database_layout.addWidget(self.init_btn, 0, 4)
        
        # 状态标签
        self.status_label = QLabel("状态: 未配置", self)
        self.status_label.setStyleSheet("color: gray;")
        database_layout.addWidget(self.status_label, 1, 0, 1, 5)
        
        # 系统配置组
        system_group = QGroupBox("系统配置", self)
        system_layout = QGridLayout(system_group)
        
        # 连接超时
        self.timeout_label = QLabel("连接超时(秒):", self)
        self.timeout_input = QSpinBox(self)
        self.timeout_input.setRange(1, 300)
        self.timeout_input.setValue(30)
        system_layout.addWidget(self.timeout_label, 0, 0)
        system_layout.addWidget(self.timeout_input, 0, 1)
        
        # 自动重连
        self.reconnect_label = QLabel("自动重连:", self)
        self.reconnect_input = QCheckBox("启用", self)
        self.reconnect_input.setChecked(True)
        system_layout.addWidget(self.reconnect_label, 0, 2)
        system_layout.addWidget(self.reconnect_input, 0, 3)
        
        # 编辑按钮
        self.edit_btn = QPushButton("编辑配置", self)
        self.edit_btn.clicked.connect(self.toggle_edit_mode)
        system_layout.addWidget(self.edit_btn, 0, 4)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 保存按钮
        self.save_btn = QPushButton("保存", self)
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setEnabled(False)  # 初始时禁用
        
        # 取消按钮
        self.cancel_btn = QPushButton("取消", self)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # 添加到主布局
        main_layout.addWidget(self.permission_label)
        main_layout.addWidget(connection_group)
        main_layout.addWidget(database_group)
        main_layout.addWidget(system_group)
        main_layout.addLayout(button_layout)

    def load_config(self):
        """ 加载配置 """
        if self.config:
            self.host_input.setText(self.config.get('host', 'localhost'))
            self.port_input.setValue(self.config.get('port', 3306))
            self.username_input.setText(self.config.get('user', 'root'))
            self.password_input.setText(self.config.get('password', ''))
            self.database_input.setText(self.config.get('database', 'bidding_system'))
            self.charset_input.setText(self.config.get('charset', 'utf8mb4'))
            self.timeout_input.setValue(self.config.get('connect_timeout', 30))
            self.reconnect_input.setChecked(self.config.get('auto_reconnect', True))

    def test_connection(self):
        """ 测试数据库连接（不指定数据库名） """
        try:
            # 先更新临时配置用于测试
            test_config = self.get_current_config()
            self.mysql_manager.config_manager.update_config(test_config)
            
            # 测试连接
            success, message = self.mysql_manager.test_connection_excluding_database()
            
            if success:
                # 连接成功，设置为已配置状态
                self.mysql_manager.config_manager.set_configured(True)
                self.is_configured = True
                QMessageBox.information(self, "连接成功", message)
                
                # 禁用测试连接按钮（因为已经成功）
                self.test_btn.setEnabled(False)
                self.test_btn.setText("连接已测试")
                self.update_ui_state()
            else:
                QMessageBox.warning(self, "连接失败", message)
                
        except Exception as e:
            QMessageBox.critical(self, "连接异常", f"连接测试异常：\n{str(e)}")

    def initialize_database(self):
        """ 初始化数据库 """
        database_name = self.database_input.text().strip()
        if not database_name:
            QMessageBox.warning(self, "警告", "请输入数据库名称")
            return
        
        try:
            # 第一步：创建数据库
            success, message = self.mysql_manager.create_database(database_name)
            if not success:
                QMessageBox.warning(self, "创建失败", message)
                return
            
            # 第二步：初始化数据库结构
            success, message = self.mysql_manager.initialize_database()
            if not success:
                QMessageBox.warning(self, "初始化失败", message)
                return
            
            # 第三步：确保管理员用户存在（使用正确的插入方法）
            success, message = self.ensure_admin_user_exists()
            if not success:
                QMessageBox.warning(self, "管理员用户创建失败", message)
                return
            
            # 初始化完成
            QMessageBox.information(self, "初始化成功", 
                f"数据库 '{database_name}' 初始化成功！\n\n" +
                "默认管理员账号已创建：\n" +
                "用户名: admin\n" +
                "密码: lipper")
            self.is_initialized = True
            self.update_ui_state()  # 更新UI状态，包括禁用数据库名输入框
            
        except Exception as e:
            QMessageBox.critical(self, "初始化异常", f"数据库初始化异常：\n{str(e)}")

    def ensure_admin_user_exists(self):
        """ 确保管理员用户存在 """
        try:
            import pymysql
            
            # 获取数据库连接参数
            config = self.mysql_manager.config_manager.get_connection_params(exclude_database=False)
            
            # 直接连接数据库执行插入操作
            with pymysql.connect(**config) as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    
                    # 检查管理员用户是否存在
                    cursor.execute("SELECT id FROM users WHERE username = %s", ('admin',))
                    existing_admin = cursor.fetchone()
                    
                    if existing_admin:
                        # 用户存在，更新密码为lipper（加密）
                        hashed_password = self.mysql_manager.hash_password('lipper')
                        cursor.execute("UPDATE users SET password = %s, email = %s, role = %s, is_active = %s WHERE username = %s", 
                                     (hashed_password, 'admin@example.com', 'admin', True, 'admin'))
                        message = "管理员用户已存在，密码已更新为 lipper"
                    else:
                        # 用户不存在，插入新用户（加密密码）
                        hashed_password = self.mysql_manager.hash_password('lipper')
                        cursor.execute("INSERT INTO users (username, password, email, role, is_active) VALUES (%s, %s, %s, %s, %s)", 
                                     ('admin', hashed_password, 'admin@example.com', 'admin', True))
                        message = "管理员用户创建成功"
                    
                    conn.commit()
                    return True, message
                    
        except Exception as e:
            return False, f"管理员用户操作失败: {str(e)}"

    def toggle_edit_mode(self):
        """ 切换编辑模式 """
        if self.is_admin:
            # 当前是管理员，切换到只读模式
            self.is_admin = False
            self.update_ui_state()
        else:
            # 当前是普通用户，验证管理员权限
            password, ok = self.get_admin_password()
            
            if not ok:
                return  # 用户取消了
            
            # 如果数据库已初始化，验证数据库中的管理员密码
            if self.is_initialized:
                try:
                    # 验证数据库中的管理员密码
                    success, message = self.mysql_manager.verify_user("admin", password)
                    if success:
                        self.is_admin = True
                        # 管理员验证成功后，解除所有被禁用的组件
                        self.enable_all_inputs()
                        self.update_ui_state()
                    else:
                        QMessageBox.warning(self, "权限不足", "管理员密码错误")
                except Exception as e:
                    QMessageBox.critical(self, "验证异常", f"验证管理员密码时发生异常：\n{str(e)}")
            else:
                # 数据库未初始化时，使用默认管理员密码
                if password == "lipper":
                    self.is_admin = True
                    # 管理员验证成功后，解除所有被禁用的组件
                    self.enable_all_inputs()
                    self.update_ui_state()
                else:
                    QMessageBox.warning(self, "权限不足", "管理员密码错误")

    def enable_all_inputs(self):
        """ 启用所有输入组件 """
        # 启用所有输入框
        inputs = [self.host_input, self.port_input, self.username_input, 
                 self.password_input, self.database_input, self.charset_input, 
                 self.timeout_input]
        for input_widget in inputs:
            if hasattr(input_widget, 'setReadOnly'):
                input_widget.setReadOnly(False)
            if hasattr(input_widget, 'setEnabled'):
                input_widget.setEnabled(True)

    def get_admin_password(self):
        """ 获取管理员密码 """
        from PyQt6.QtWidgets import QInputDialog, QLineEdit
        
        password, ok = QInputDialog.getText(
            self, 
            "管理员验证", 
            "请输入管理员密码:", 
            QLineEdit.EchoMode.Password
        )
        return password, ok

    def update_ui_state(self):
        """ 更新界面状态 """
        # 更新权限标签
        if self.is_admin:
            self.permission_label.setText("当前权限: 管理员")
            self.permission_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.permission_label.setText("当前权限: 普通用户")
            self.permission_label.setStyleSheet("color: red; font-weight: bold;")
        
        # 更新编辑按钮文本
        self.edit_btn.setText("只读模式" if self.is_admin else "编辑配置")
        
        # 根据权限和配置状态设置输入框状态
        if self.is_configured and not self.is_admin:
            # 已配置且不是管理员时，锁定除数据库名外的所有输入框
            inputs_to_lock = [self.host_input, self.port_input, self.username_input, 
                            self.password_input, self.charset_input, self.timeout_input]
            for input_widget in inputs_to_lock:
                input_widget.setReadOnly(True)
                if hasattr(input_widget, 'setEnabled'):
                    input_widget.setEnabled(False)
            
            # 根据初始化状态设置数据库输入框
            if self.is_initialized:
                # 已初始化时，禁用数据库名输入框和初始化按钮
                self.database_input.setReadOnly(True)
                self.database_input.setEnabled(False)
                self.init_btn.setEnabled(False)
            else:
                # 未初始化时，启用数据库名输入框和初始化按钮
                self.database_input.setReadOnly(False)
                self.database_input.setEnabled(True)
                self.init_btn.setEnabled(True)
            
            # 更新状态标签
            if self.is_initialized:
                self.status_label.setText("状态: 已配置并初始化")
                self.status_label.setStyleSheet("color: green;")
            else:
                self.status_label.setText("状态: 已配置，未初始化")
                self.status_label.setStyleSheet("color: orange;")
        else:
            # 未配置或管理员模式时，所有输入框都可以编辑
            inputs = [self.host_input, self.port_input, self.username_input, 
                     self.password_input, self.database_input, self.charset_input, 
                     self.timeout_input]
            for input_widget in inputs:
                if hasattr(input_widget, 'setReadOnly'):
                    input_widget.setReadOnly(False)
                if hasattr(input_widget, 'setEnabled'):
                    input_widget.setEnabled(True)
            
            # 初始化按钮状态
            if self.is_configured:
                self.init_btn.setEnabled(True)
            else:
                self.init_btn.setEnabled(False)
            
            self.status_label.setText("状态: 未配置")
            self.status_label.setStyleSheet("color: gray;")

    def get_current_config(self):
        """ 获取当前配置 """
        return {
            'host': self.host_input.text() or 'localhost',
            'port': self.port_input.value(),
            'user': self.username_input.text() or 'root',
            'password': self.password_input.text(),
            'database': self.database_input.text() or 'bidding_system',
            'charset': self.charset_input.text() or 'utf8mb4',
            'connect_timeout': self.timeout_input.value(),
            'auto_reconnect': self.reconnect_input.isChecked()
        }

    def save_config(self):
        """ 保存配置 """
        try:
            config = self.get_current_config()
            self.mysql_manager.config_manager.update_config(config)
            QMessageBox.information(self, "保存成功", "配置已保存")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "保存失败", f"配置保存失败：\n{str(e)}")
