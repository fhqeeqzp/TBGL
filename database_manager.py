import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any, List, Tuple
import logging
from contextlib import contextmanager
import threading


class DatabaseManager:
    """MySQL数据库管理器"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = self._load_config()
        self.logger = self._setup_logger()
        self._lock = threading.Lock()
        self.initialized = False
        
        # 不立即连接数据库
        # 延迟初始化以避免阻塞GUI
    
    def _load_config(self) -> Dict[str, Any]:
        """加载数据库配置"""
        # 尝试从环境变量加载配置
        import os
        from dotenv import load_dotenv
        
        # 加载.env文件（如果存在）
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
        
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'bidding_management'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'charset': 'utf8mb4',
            'autocommit': False,
            'connect_timeout': 10,
            'raise_on_warnings': False
        }
        
        return config
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('DatabaseManager')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def connect(self) -> bool:
        """连接到MySQL数据库"""
        try:
            with self._lock:
                if self.connection and self.connection.is_connected():
                    self.logger.info("数据库连接已存在")
                    return True
                
                self.logger.info("正在连接到MySQL数据库...")
                self.connection = mysql.connector.connect(**self.config)
                
                if self.connection.is_connected():
                    self.cursor = self.connection.cursor()
                    self.logger.info(f"成功连接到数据库: {self.config['host']}:{self.config['port']}")
                    
                    # 标记为已初始化
                    self.initialized = True
                    
                    # 初始化数据库（如果需要）
                    self._initialize_database()
                    return True
                    
        except Error as e:
            self.logger.error(f"连接数据库失败: {e}")
            self.connection = None
            self.cursor = None
            return False
        
        return False
    
    def _initialize_database(self):
        """初始化数据库"""
        try:
            # 创建数据库（如果不存在）
            self.create_database_if_not_exists()
            
            # 初始化表结构
            self._create_tables()
            
        except Error as e:
            self.logger.error(f"初始化数据库失败: {e}")
    
    def create_database_if_not_exists(self):
        """创建数据库（如果不存在）"""
        try:
            # 连接到MySQL服务器（不指定数据库）
            temp_config = self.config.copy()
            temp_config.pop('database', None)
            
            temp_connection = mysql.connector.connect(**temp_config)
            temp_cursor = temp_connection.cursor()
            
            temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            
            temp_cursor.close()
            temp_connection.close()
            
        except Error as e:
            self.logger.error(f"创建数据库失败: {e}")
    
    def _create_tables(self):
        """创建必要的表"""
        tables = {
            'users': """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100),
                    phone VARCHAR(20),
                    company VARCHAR(100),
                    role ENUM('admin', 'user', 'viewer') DEFAULT 'user',
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_username (username),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            'projects': """
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    project_name VARCHAR(200) NOT NULL,
                    project_code VARCHAR(50) UNIQUE NOT NULL,
                    project_type ENUM('construction', 'service', 'goods') NOT NULL,
                    description TEXT,
                    budget DECIMAL(15,2),
                    start_date DATE,
                    end_date DATE,
                    status ENUM('draft', 'active', 'completed', 'cancelled') DEFAULT 'draft',
                    created_by INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users(id),
                    INDEX idx_project_code (project_code),
                    INDEX idx_status (status),
                    INDEX idx_project_type (project_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            'bids': """
                CREATE TABLE IF NOT EXISTS bids (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    project_id INT NOT NULL,
                    bidder_name VARCHAR(100) NOT NULL,
                    bidder_company VARCHAR(100),
                    bid_amount DECIMAL(15,2),
                    bid_currency VARCHAR(3) DEFAULT 'CNY',
                    technical_proposal TEXT,
                    commercial_proposal TEXT,
                    status ENUM('draft', 'submitted', 'under_review', 'accepted', 'rejected') DEFAULT 'draft',
                    submission_date TIMESTAMP NULL,
                    review_date TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                    INDEX idx_project_id (project_id),
                    INDEX idx_status (status),
                    INDEX idx_submission_date (submission_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            'documents': """
                CREATE TABLE IF NOT EXISTS documents (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    project_id INT,
                    bid_id INT,
                    document_name VARCHAR(200) NOT NULL,
                    document_type ENUM('technical', 'commercial', 'legal', 'certificate', 'other'),
                    file_path VARCHAR(500) NOT NULL,
                    file_size INT,
                    file_hash VARCHAR(64),
                    is_confidential BOOLEAN DEFAULT FALSE,
                    uploaded_by INT,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                    FOREIGN KEY (bid_id) REFERENCES bids(id) ON DELETE CASCADE,
                    FOREIGN KEY (uploaded_by) REFERENCES users(id),
                    INDEX idx_project_id (project_id),
                    INDEX idx_bid_id (bid_id),
                    INDEX idx_document_type (document_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            
            'audit_logs': """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    action VARCHAR(50) NOT NULL,
                    table_name VARCHAR(50),
                    record_id INT,
                    old_values JSON,
                    new_values JSON,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    INDEX idx_user_id (user_id),
                    INDEX idx_action (action),
                    INDEX idx_table_name (table_name),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        }
        
        for table_name, create_sql in tables.items():
            try:
                self.cursor.execute(create_sql)
                self.connection.commit()
                self.logger.info(f"表 '{table_name}' 创建成功或已存在")
            except Error as e:
                self.logger.error(f"创建表 '{table_name}' 失败: {e}")
    
    @contextmanager
    def get_cursor(self):
        """获取数据库游标的上下文管理器"""
        cursor = None
        try:
            if not self.connection or not self.connection.is_connected():
                # 尝试重新连接
                if not self.connect():
                    raise Error("无法连接到数据库")
            cursor = self.connection.cursor(dictionary=True)
            yield cursor
        except Error as e:
            if self.connection:
                self.connection.rollback()
            self.logger.error(f"数据库操作失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
    
    def execute_query(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """执行查询语句"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                self.logger.info(f"查询执行成功，返回 {len(result)} 条记录")
                return result
        except Error as e:
            self.logger.error(f"查询执行失败: {e}")
            return []
    
    def execute_update(self, query: str, params: Optional[Tuple] = None) -> bool:
        """执行更新语句"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                affected_rows = cursor.rowcount
                self.logger.info(f"更新执行成功，影响 {affected_rows} 行")
                return True
        except Error as e:
            self.logger.error(f"更新执行失败: {e}")
            return False
    
    def execute_insert(self, query: str, params: Optional[Tuple] = None) -> Optional[int]:
        """执行插入语句，返回插入记录的ID"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                last_id = cursor.lastrowid
                self.logger.info(f"插入成功，记录ID: {last_id}")
                return last_id
        except Error as e:
            self.logger.error(f"插入失败: {e}")
            return None
    
    def execute_delete(self, query: str, params: Optional[Tuple] = None) -> bool:
        """执行删除语句"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                affected_rows = cursor.rowcount
                self.logger.info(f"删除成功，影响 {affected_rows} 行")
                return True
        except Error as e:
            self.logger.error(f"删除失败: {e}")
            return False
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result is not None
        except Error as e:
            self.logger.error(f"连接测试失败: {e}")
            return False
    
    def get_connection_status(self) -> Dict[str, Any]:
        """获取连接状态"""
        status = {
            'connected': False,
            'host': self.config.get('host'),
            'port': self.config.get('port'),
            'database': self.config.get('database'),
            'server_info': None,
            'connection_id': None
        }
        
        try:
            if self.connection and self.connection.is_connected():
                status['connected'] = True
                status['server_info'] = self.connection.get_server_info()
                status['connection_id'] = self.connection.connection_id
        except Error as e:
            self.logger.error(f"获取连接状态失败: {e}")
        
        return status
    
    def close_connection(self):
        """关闭数据库连接"""
        try:
            with self._lock:
                if self.cursor:
                    self.cursor.close()
                if self.connection and self.connection.is_connected():
                    self.connection.close()
                    self.logger.info("数据库连接已关闭")
        except Error as e:
            self.logger.error(f"关闭连接失败: {e}")
        finally:
            self.cursor = None
            self.connection = None
    
    def reconnect(self) -> bool:
        """重新连接数据库"""
        self.logger.info("尝试重新连接数据库...")
        self.close_connection()
        return self.connect()
    
    def __del__(self):
        """析构函数"""
        self.close_connection()