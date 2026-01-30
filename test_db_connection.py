#!/usr/bin/env python3
"""
简单数据库连接测试
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_direct_connection():
    """直接连接测试"""
    print("=== 直接MySQL连接测试 ===")
    
    config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'bidding_management',
        'user': 'root',
        'password': 'lipper',
        'charset': 'utf8mb4',
        'autocommit': False
    }
    
    try:
        print(f"尝试连接: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ 连接成功!")
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"版本: {version[0]}")
            
            cursor.execute("USE bidding_management")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"表: {[table[0] for table in tables]}")
            
            # 测试查询
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            print(f"用户数: {len(users)}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_env_connection():
    """使用环境变量的连接测试"""
    print("\n=== 环境变量连接测试 ===")
    
    print("环境变量:")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD', '***')}")
    
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_NAME', 'bidding_management'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': 'utf8mb4',
        'autocommit': False
    }
    
    try:
        print(f"尝试连接: {config['user']}@{config['host']}:{config['port']}/{config['database']}")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ 环境变量连接成功!")
            
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"版本: {version[0]}")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"❌ 环境变量连接失败: {e}")
        return False

if __name__ == "__main__":
    print("数据库连接测试\n")
    
    # 测试直接连接
    direct_success = test_direct_connection()
    
    # 测试环境变量连接
    env_success = test_env_connection()
    
    print(f"\n=== 测试结果 ===")
    print(f"直接连接: {'✅ 成功' if direct_success else '❌ 失败'}")
    print(f"环境变量连接: {'✅ 成功' if env_success else '❌ 失败'}")