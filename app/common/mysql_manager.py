# coding:utf-8
"""
MySQL数据库连接和配置管理模块
"""

import pymysql
import json
import os
import bcrypt
from typing import Dict, List, Optional, Tuple


class MySQLConfig:
    """ MySQL配置管理类 """

    def __init__(self):
        """ 初始化配置管理 """
        self.config_file = "app/config/mysql_config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """ 加载配置文件 """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        
        # 默认配置
        return {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "",
            "database": "bidding_system",
            "charset": "utf8mb4",
            "connect_timeout": 30,
            "auto_reconnect": True,
            "is_configured": False,
            "is_initialized": False
        }

    def _save_config(self):
        """ 保存配置文件 """
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def get_config(self) -> Dict:
        """ 获取配置 """
        return self.config.copy()

    def update_config(self, config: Dict):
        """ 更新配置 """
        self.config.update(config)
        self._save_config()

    def get_connection_params(self, exclude_database: bool = False) -> Dict:
        """
        获取连接参数
        
        Args:
            exclude_database: 是否排除数据库名（用于测试连接）
        """
        params = {
            'host': self.config.get('host', 'localhost'),
            'port': self.config.get('port', 3306),
            'user': self.config.get('user', 'root'),
            'password': self.config.get('password', ''),
            'charset': self.config.get('charset', 'utf8mb4'),
            'connect_timeout': self.config.get('connect_timeout', 30)
        }
        
        if not exclude_database and self.config.get('database'):
            params['database'] = self.config['database']
        
        return params

    def set_configured(self, configured: bool):
        """ 设置配置状态 """
        self.config['is_configured'] = configured
        self._save_config()

    def set_initialized(self, initialized: bool):
        """ 设置初始化状态 """
        self.config['is_initialized'] = initialized
        self._save_config()

    def is_configured(self) -> bool:
        """ 检查是否已配置 """
        return self.config.get('is_configured', False)

    def is_initialized(self) -> bool:
        """ 检查是否已初始化 """
        return self.config.get('is_initialized', False)


class MySQLManager:
    """ MySQL数据库管理器 """

    def __init__(self):
        """ 初始化数据库管理器 """
        self.config_manager = MySQLConfig()
        self.connection = None
        self.cursor = None

    def hash_password(self, password: str) -> str:
        """
        使用bcrypt加密密码
        
        Args:
            password: 原始密码
            
        Returns:
            str: 加密后的密码
        """
        salt = bcrypt.gensalt(rounds=12)  # 使用12轮加密
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            password: 原始密码
            hashed_password: 加密后的密码
            
        Returns:
            bool: 密码是否匹配
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False

    def test_connection_excluding_database(self) -> Tuple[bool, str]:
        """
        测试数据库连接（不指定数据库名）
        
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        try:
            connection_params = self.config_manager.get_connection_params(exclude_database=True)
            
            # 连接到MySQL服务器（不指定数据库）
            self.connection = pymysql.connect(**connection_params)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            
            # 测试基本查询
            self.cursor.execute("SELECT VERSION()")
            version = self.cursor.fetchone()
            
            return True, f"连接成功，MySQL版本: {version.get('VERSION()', 'Unknown')}"
            
        except Exception as e:
            return False, f"连接测试失败: {str(e)}"
        finally:
            self.close()

    def test_connection_with_database(self) -> Tuple[bool, str]:
        """
        测试数据库连接（指定数据库名）
        
        Returns:
            Tuple[bool, str]: (是否成功, 错误信息)
        """
        try:
            if not self.connection:
                connection_params = self.config_manager.get_connection_params(exclude_database=False)
                self.connection = pymysql.connect(**connection_params)
                self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            
            # 测试数据库查询
            self.cursor.execute("SELECT 1")
            return True, "数据库连接测试成功"
            
        except Exception as e:
            return False, f"数据库连接测试失败: {str(e)}"
        finally:
            if self.connection and self.connection.open:
                self.close()

    def create_database(self, database_name: str) -> Tuple[bool, str]:
        """
        创建数据库
        
        Args:
            database_name: 数据库名称
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        try:
            # 首先连接到MySQL服务器（不指定数据库）
            connection_params = self.config_manager.get_connection_params(exclude_database=True)
            
            with pymysql.connect(**connection_params) as conn:
                with conn.cursor() as cursor:
                    # 创建数据库
                    create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                    cursor.execute(create_db_sql)
                    conn.commit()
                    
                    # 更新配置中的数据库名
                    config = self.config_manager.get_config()
                    config['database'] = database_name
                    self.config_manager.update_config(config)
                    
                    return True, f"数据库 '{database_name}' 创建成功"
                    
        except Exception as e:
            return False, f"创建数据库失败: {str(e)}"

    def initialize_database(self) -> Tuple[bool, str]:
        """
        初始化数据库（创建表和插入初始数据）
        
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        try:
            # 连接到指定的数据库
            connection_params = self.config_manager.get_connection_params(exclude_database=False)
            
            with pymysql.connect(**connection_params) as conn:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    # 创建表结构
                    success, message = self.create_tables_in_cursor(cursor)
                    if not success:
                        return False, message
                    
                    # 插入初始数据
                    success, message = self.insert_initial_data_in_cursor(cursor)
                    if not success:
                        return False, message
                    
                    # 提交事务
                    conn.commit()
                    
                    # 设置初始化状态
                    self.config_manager.set_initialized(True)
                    
                    return True, "数据库初始化成功"
                    
        except Exception as e:
            return False, f"数据库初始化失败: {str(e)}"

    def create_tables_in_cursor(self, cursor) -> Tuple[bool, str]:
        """ 在指定游标中创建表结构 """
        tables_sql = [
            # 用户表
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                role ENUM('admin', 'user') DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            # 项目表
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INT PRIMARY KEY AUTO_INCREMENT,
                project_name VARCHAR(255) NOT NULL,
                project_code VARCHAR(100) UNIQUE,
                description TEXT,
                budget DECIMAL(15,2),
                start_date DATE,
                end_date DATE,
                status ENUM('planning', 'open', 'in_progress', 'completed', 'cancelled') DEFAULT 'planning',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            # 投标表
            """
            CREATE TABLE IF NOT EXISTS bids (
                id INT PRIMARY KEY AUTO_INCREMENT,
                project_id INT NOT NULL,
                bidder_name VARCHAR(255) NOT NULL,
                bidder_contact VARCHAR(100),
                bid_amount DECIMAL(15,2),
                bid_date DATE,
                status ENUM('submitted', 'reviewing', 'accepted', 'rejected') DEFAULT 'submitted',
                documents TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            # 系统配置表
            """
            CREATE TABLE IF NOT EXISTS system_config (
                id INT PRIMARY KEY AUTO_INCREMENT,
                config_key VARCHAR(100) NOT NULL UNIQUE,
                config_value TEXT,
                config_type VARCHAR(20) DEFAULT 'string',
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        ]
        
        try:
            for sql in tables_sql:
                cursor.execute(sql)
            
            return True, "表结构创建成功"
            
        except Exception as e:
            return False, f"创建表失败: {str(e)}"

    def insert_initial_data_in_cursor(self, cursor) -> Tuple[bool, str]:
        """ 在指定游标中插入初始数据 """
        try:
            # 确保管理员用户存在（使用加密密码）
            admin_password = self.hash_password('lipper')
            cursor.execute("""
                INSERT INTO users (username, password, email, role, is_active) 
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                password = VALUES(password), 
                email = VALUES(email), 
                role = VALUES(role),
                is_active = VALUES(is_active)
            """, ('admin', admin_password, 'admin@example.com', 'admin', True))
            
            # 插入系统配置
            configs = [
                ('system_name', '投标管理系统', 'string', '系统名称'),
                ('version', '1.0.0', 'string', '系统版本'),
                ('max_file_size', '10485760', 'int', '最大文件上传大小(字节)'),
                ('db_initialized', 'true', 'boolean', '数据库是否已初始化')
            ]
            
            for config_key, config_value, config_type, description in configs:
                cursor.execute("""
                    INSERT INTO system_config (config_key, config_value, config_type, description) 
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                    config_value = VALUES(config_value)
                """, (config_key, config_value, config_type, description))
            
            return True, "初始数据插入成功"
            
        except Exception as e:
            return False, f"插入初始数据失败: {str(e)}"

    def connect(self) -> bool:
        """
        连接数据库
        
        Returns:
            bool: 连接是否成功
        """
        try:
            if self.connection:
                self.close()
            
            connection_params = self.config_manager.get_connection_params(exclude_database=False)
            
            self.connection = pymysql.connect(**connection_params)
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            return True
            
        except Exception as e:
            print(f"数据库连接失败: {e}")
            self.connection = None
            self.cursor = None
            return False

    def close(self):
        """ 关闭数据库连接 """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.cursor = None
        self.connection = None

    def execute_query(self, sql: str, params: Optional[Tuple] = None) -> List[Dict]:
        """
        执行查询语句
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            List[Dict]: 查询结果列表
        """
        try:
            if not self.connection:
                if not self.connect():
                    return []
            
            self.cursor.execute(sql, params)
            return self.cursor.fetchall()
            
        except Exception as e:
            print(f"查询执行失败: {e}")
            return []

    def execute_update(self, sql: str, params: Optional[Tuple] = None) -> int:
        """
        执行更新语句
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            int: 影响的行数
        """
        try:
            if not self.connection:
                if not self.connect():
                    return 0
            
            self.cursor.execute(sql, params)
            self.connection.commit()
            return self.cursor.rowcount
            
        except Exception as e:
            print(f"更新执行失败: {e}")
            if self.connection:
                self.connection.rollback()
            return 0

    def verify_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        验证用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        try:
            if not self.connection:
                if not self.connect():
                    return False, "数据库连接失败"
            
            # 查询用户
            sql = "SELECT id, username, password, role FROM users WHERE username = %s AND is_active = 1"
            self.cursor.execute(sql, (username,))
            user = self.cursor.fetchone()
            
            if user and self.verify_password(password, user['password']):
                return True, f"欢迎，{user['role']}用户 {user['username']}"
            else:
                return False, "用户名或密码错误"
                
        except Exception as e:
            return False, f"验证失败: {str(e)}"

    def register_user(self, username: str, password: str, email: str, role: str = 'user') -> Tuple[bool, str]:
        """
        注册新用户
        
        Args:
            username: 用户名
            password: 密码
            email: 邮箱
            role: 角色（默认user）
            
        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        try:
            if not self.connection:
                if not self.connect():
                    return False, "数据库连接失败"
            
            # 检查用户名是否已存在
            sql = "SELECT id FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            if self.cursor.fetchone():
                return False, "用户名已存在"
            
            # 检查邮箱是否已存在
            sql = "SELECT id FROM users WHERE email = %s"
            self.cursor.execute(sql, (email,))
            if self.cursor.fetchone():
                return False, "邮箱已被使用"
            
            # 加密密码
            hashed_password = self.hash_password(password)
            
            # 插入新用户
            sql = """
            INSERT INTO users (username, password, email, role) 
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql, (username, hashed_password, email, role))
            self.connection.commit()
            
            return True, "用户注册成功"
            
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return False, f"注册失败: {str(e)}"

    def check_user_exists(self, username: str) -> bool:
        """
        检查用户是否存在
        
        Args:
            username: 用户名
            
        Returns:
            bool: 是否存在
        """
        try:
            if not self.connection:
                if not self.connect():
                    return False
            
            sql = "SELECT id FROM users WHERE username = %s"
            self.cursor.execute(sql, (username,))
            return self.cursor.fetchone() is not None
            
        except Exception as e:
            print(f"检查用户存在性失败: {e}")
            return False


# 创建全局数据库管理器实例
mysql_manager = MySQLManager()
