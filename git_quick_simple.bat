@echo off
echo 🚀 Git 快速提交工具
echo.

:: 检查Git是否可用
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git未安装或不在PATH中
    pause
    exit /b 1
)

:: 检查是否在Git仓库中
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ❌ 当前目录不是Git仓库
    pause
    exit /b 1
)

:: 检查是否有变更
git diff --quiet
if errorlevel 1 (
    echo 📝 发现未暂存的变更
) else (
    echo ✅ 没有未暂存的变更
)

git diff --cached --quiet
if errorlevel 1 (
    echo 📦 发现已暂存的变更
) else (
    echo ✅ 没有已暂存的变更
)

echo.
echo 请选择操作:
echo [1] 快速提交 (推荐)
echo [2] 查看状态
echo [3] 拉取更新
echo [4] 退出
echo.

set /p choice=请输入选项 [1-4]: 

if "%choice%"=="1" (
    echo.
    set /p msg=请输入提交信息: 
    if "%msg%"=="" (
        echo ❌ 提交信息不能为空
        pause
        exit /b 1
    )
    
    echo.
    echo 🚀 正在快速提交...
    git add .
    git commit -m "%msg%"
    git push origin main
    
    if errorlevel 1 (
        echo ⚠️ 推送可能失败，请检查
    ) else (
        echo ✅ 提交成功！
    )
)

if "%choice%"=="2" (
    git status
)

if "%choice%"=="3" (
    echo.
    echo ⬇️ 正在拉取远程更新...
    git pull origin main
)

if "%choice%"=="4" (
    exit /b 0
)

echo.
pause