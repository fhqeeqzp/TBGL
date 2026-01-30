# 投标管理软件

一个基于PyQt6 + MySQL的现代化投标管理应用程序，支持无边框窗口和智能主题适配。

## 功能特性

- 🖥️ **无边框现代化界面** - 采用自定义标题栏和圆角设计
- 🎨 **智能主题适配** - 自动检测并跟随系统主题（浅色/深色）
- 🗄️ **MySQL数据库支持** - 完整的数据库架构和管理功能
- 📁 **文件管理** - 支持投标文档的上传和管理
- 👥 **用户管理** - 多角色用户权限系统
- 📊 **项目管理** - 完整的投标项目管理功能
- 📋 **投标管理** - 投标提交和评审功能
- 🔍 **审计日志** - 完整的操作日志记录

## 技术栈

- **GUI框架**: PyQt6
- **数据库**: MySQL 8.0+
- **数据库连接器**: mysql-connector-python
- **配置管理**: python-dotenv
- **开发语言**: Python 3.8+

## 项目结构

```
投标管理软件/
├── main.py                 # 应用程序主入口
├── main_window.py          # 主窗口类
├── theme_manager.py        # 主题管理器
├── database_manager.py     # 数据库管理器
├── test_app.py            # 应用程序测试
├── requirements.txt       # Python依赖包
├── .env.example           # 环境变量模板
├── start.bat              # Windows快速启动脚本
├── resources/             # 资源文件夹
│   └── icon.ico           # 应用程序图标
└── README.md              # 项目说明文档
```

## 快速开始

### 1. 环境要求

- Python 3.8 或更高版本
- MySQL 8.0 或更高版本
- Windows 10/11（推荐）

### 2. 数据库设置

1. 安装MySQL服务器
2. 创建数据库：
```sql
CREATE DATABASE bidding_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 创建用户（可选）：
```sql
CREATE USER 'bidding_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON bidding_management.* TO 'bidding_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

1. 复制环境变量模板：
```bash
copy .env.example .env
```

2. 编辑 `.env` 文件，配置数据库连接信息：
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bidding_management
DB_USER=root
DB_PASSWORD=your_password_here
```

### 5. 运行应用程序

#### 方法一：使用启动脚本（推荐）
双击运行 `start.bat` 文件

#### 方法二：命令行运行
```bash
python main.py
```

### 6. 测试应用程序

```bash
python test_app.py
```

## 主题系统

应用程序支持自动检测和跟随系统主题：

- **浅色主题** - 适用于白天使用
- **深色主题** - 适用于夜间使用
- **自动检测** - 每秒检查一次系统主题变化
- **实时切换** - 主题变化时立即应用新主题

## 数据库架构

### 主要表结构

1. **users** - 用户表
   - 用户信息、权限角色
   - 支持管理员、用户、查看者三种角色

2. **projects** - 项目表
   - 投标项目信息
   - 支持建设、服务、货物三种项目类型

3. **bids** - 投标表
   - 投标提交和状态管理
   - 支持技术标和商务标

4. **documents** - 文档表
   - 项目和投标相关文档
   - 支持文件上传和管理

5. **audit_logs** - 审计日志表
   - 完整的操作日志记录
   - 支持数据变更追踪

### 特性

- **自动表创建** - 应用程序启动时自动创建必要的表结构
- **字符集支持** - 完整支持UTF-8字符集
- **外键约束** - 保持数据完整性
- **索引优化** - 提高查询性能

## 开发指南

### 添加新功能

1. **数据库扩展**
   - 在 `database_manager.py` 中的 `_create_tables()` 方法添加新的表
   - 添加相应的CRUD方法

2. **UI组件**
   - 继承PyQt6的标准组件
   - 在 `main_window.py` 中添加新的界面元素
   - 确保主题样式的一致性

3. **主题样式**
   - 在 `theme_manager.py` 中添加新的颜色配置
   - 使用一致的命名约定

### 代码规范

- 遵循PEP 8 Python编码规范
- 使用类型注解
- 添加适当的文档字符串
- 保持函数和类的单一职责原则

## 常见问题

### Q: 应用程序无法启动
A: 检查以下几点：
1. Python版本是否为3.8+
2. 所有依赖包是否正确安装
3. MySQL服务是否正在运行
4. `.env`文件中的数据库配置是否正确

### Q: 数据库连接失败
A: 验证以下配置：
1. MySQL服务器是否启动
2. 主机地址和端口是否正确
3. 用户名和密码是否有效
4. 数据库是否存在

### Q: 主题不自动切换
A: 检查以下几点：
1. 系统是否支持主题检测（Windows 10/11）
2. 系统主题是否已更改
3. 应用程序是否在系统托盘外运行

### Q: 窗口无法拖拽
A: 确认以下设置：
1. 是否在窗口的非控制按钮区域拖拽
2. 窗口是否处于最大化状态

## 技术支持

如果遇到问题，请检查：

1. 应用程序日志文件：`bidding_management.log`
2. 运行测试脚本：`python test_app.py`
3. 确认系统要求和依赖安装

## 版本历史

### v1.0.0
- 初始版本发布
- 实现无边框窗口界面
- 支持主题自动适配
- 集成MySQL数据库
- 完整的投标管理功能框架

## 许可证

本项目仅供学习和演示使用。