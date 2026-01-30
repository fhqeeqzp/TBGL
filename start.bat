@echo off
chcp 65001 >nul
echo 投标管理软件 - 快速启动脚本
echo ================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python环境检测成功

REM 检查是否在虚拟环境中
if defined VIRTUAL_ENV (
    echo ✓ 检测到虚拟环境: %VIRTUAL_ENV%
) else (
    echo ⚠ 警告：建议使用虚拟环境
)

echo.
echo 正在检查依赖包...
echo.

REM 安装依赖
echo 安装Python依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ 依赖安装失败
    pause
    exit /b 1
)

echo ✓ 依赖安装完成
echo.

REM 检查.env文件
if not exist .env (
    echo 创建.env配置文件...
    copy .env.example .env
    echo ⚠ 请编辑.env文件配置数据库连接信息
    echo.
)

REM 运行测试
echo 运行应用程序测试...
python test_app.py
if errorlevel 1 (
    echo.
    echo ⚠ 测试失败，但可以尝试运行应用程序
    echo 请检查上述错误信息并解决相关问题
    echo.
)

REM 启动应用程序
echo 启动投标管理软件...
python main.py

if errorlevel 1 (
    echo.
    echo ✗ 应用程序启动失败
    echo 请检查上述错误信息
    pause
)