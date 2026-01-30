#!/usr/bin/env python3
"""
MySQL数据库设置脚本
"""

import mysql.connector
from mysql.connector import Error
import sys
import os

def test_mysql_connection():
    """测试MySQL连接"""
    try:
        # 尝试连接到MySQL服务器
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='lipper',  # 使用用户提供的密码
            connect_timeout=5
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL连接成功!")
            print(f"版本: {version[0]}")
            
            # 检查数据库
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"现有数据库: {[db[0] for db in databases]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ MySQL连接失败: {e}")
        return False

def create_bidding_database():
    """创建投标管理数据库"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='lipper'
        )
        
        cursor = connection.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS bidding_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ 数据库 'bidding_management' 创建成功")
        
        # 使用数据库
        cursor.execute("USE bidding_management")
        
        # 创建用户表
        users_table = """
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
        """
        
        cursor.execute(users_table)
        print("✅ 用户表创建成功")
        
        # 创建项目表
        projects_table = """
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
        """
        
        cursor.execute(projects_table)
        print("✅ 项目表创建成功")
        
        # 插入测试数据
        test_users = [
            ("admin", "admin@example.com", "password_hash", "管理员", "123456789", "管理公司", "admin"),
            ("user1", "user1@example.com", "password_hash", "用户1", "123456789", "投标公司", "user")
        ]
        
        for user in test_users:
            try:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, full_name, phone, company, role) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, user)
            except Error:
                pass  # 用户已存在
        
        connection.commit()
        print("✅ 测试数据插入成功")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ 创建数据库失败: {e}")
        return False

def main():
    """主函数"""
    print("=== MySQL数据库设置 ===")
    
    # 测试连接
    if not test_mysql_connection():
        print("请确保MySQL服务正在运行")
        return False
    
    # 创建数据库
    if create_bidding_database():
        print("✅ 数据库设置完成!")
        print("现在可以运行应用程序了")
        return True
    else:
        print("❌ 数据库设置失败")
        return False

if __name__ == "__main__":
    main()