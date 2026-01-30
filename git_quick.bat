@echo off
chcp 65001 >nul
title Git 快速提交工具

echo.
echo ========================================
echo        Git 快速提交工具
echo ========================================
echo.

:: 检查Git是否安装
where git >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Git，请确保Git已安装并在PATH中
    pause
    exit /b 1
)

:: 检查是否在Git仓库中
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 当前目录不是Git仓库
    pause
    exit /b 1
)

:: 获取当前分支
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set "current_branch=%%i"
if "%current_branch%"=="" set "current_branch=main"

echo 📍 当前分支: %current_branch%
echo.

:: 显示修改状态
echo 📋 检查变更状态...
echo.
git status --porcelain

:: 检查是否有变更
git diff --quiet
if errorlevel 1 (
    set "has_staged=1"
    echo 📝 发现未暂存的变更
) else (
    set "has_staged=0"
    echo ✅ 没有未暂存的变更
)

git diff --cached --quiet
if errorlevel 1 (
    set "has_cached=1"
    echo 📦 发现已暂存的变更
) else (
    set "has_cached=0"
    echo ✅ 没有已暂存的变更
)

echo.

:: 如果没有变更，显示菜单
if "%has_staged%"=="0" if "%has_cached%"=="0" (
    echo 📋 没有发现变更，请选择操作:
    echo.
    echo [1] 查看提交历史
    echo [2] 拉取远程更新
    echo [3] 查看状态详情
    echo [4] 退出
    echo.
    set /p "choice=请输入选项 [1-4]: "
    
    if "%choice%"=="1" (
        echo.
        echo 📜 最近的提交历史:
        git log --oneline -5
        pause
        goto :eof
    )
    if "%choice%"=="2" (
        echo.
        echo ⬇️ 正在拉取远程更新...
        git pull origin %current_branch%
        pause
        goto :eof
    )
    if "%choice%"=="3" (
        echo.
        git status
        pause
        goto :eof
    )
    if "%choice%"=="4" (
        goto :eof
    )
    echo 无效选项
    pause
    goto :eof
)

:: 有变更时的快速提交菜单
echo 📋 发现变更，请选择操作:
echo.
echo [1] 快速提交 (add + commit + push)
echo [2] 分步骤提交
echo [3] 查看变更详情
echo [4] 取消
echo.
set /p "choice=请输入选项 [1-4]: "

if "%choice%"=="1" goto :quick_commit
if "%choice%"=="2" goto :step_by_step
if "%choice%"=="3" goto :show_changes
if "%choice%"=="4" goto :eof

echo 无效选项
pause
goto :eof

:quick_commit
echo.
echo 🚀 快速提交模式
echo.
set /p "msg=请输入提交信息: "
if "%msg%"=="" (
    echo ❌ 提交信息不能为空
    pause
    goto :eof
)

echo.
echo 📦 正在暂存所有变更...
git add .
if errorlevel 1 (
    echo ❌ 暂存失败
    pause
    goto :eof
)

echo.
echo 💾 正在提交...
git commit -m "%msg%"
if errorlevel 1 (
    echo ❌ 提交失败
    pause
    goto :eof
)

echo.
echo ⬆️ 正在推送到远程...
git push origin %current_branch%
if errorlevel 1 (
    echo ⚠️ 推送失败，但提交成功
    pause
    goto :eof
)

echo ✅ 提交成功！
pause
goto :eof

:step_by_step
echo.
echo 🔄 分步骤提交模式
echo.

echo 📋 步骤 1: 检查状态
git status
echo.

set /p "continue1=是否继续? (y/n): "
if /i not "%continue1%"=="y" goto :eof

echo.
echo 📦 步骤 2: 暂存变更
echo 选择暂存方式:
echo [1] 暂存所有文件
echo [2] 暂存特定文件
echo.
set /p "stage_choice=请选择 [1-2]: "

if "%stage_choice%"=="1" (
    echo 暂存所有文件...
    git add .
) else if "%stage_choice%"=="2" (
    echo 请输入要暂存的文件 (空格分隔):
    set /p "files=文件名: "
    git add %files%
) else (
    echo 无效选项
    pause
    goto :eof
)

if errorlevel 1 (
    echo ❌ 暂存失败
    pause
    goto :eof
)

echo.
echo 💾 步骤 3: 提交
set /p "msg=请输入提交信息: "
if "%msg%"=="" (
    echo ❌ 提交信息不能为空
    pause
    goto :eof
)

git commit -m "%msg%"
if errorlevel 1 (
    echo ❌ 提交失败
    pause
    goto :eof
)

echo.
set /p "push_now=是否立即推送到远程? (y/n): "
if /i "%push_now%"=="y" (
    echo ⬆️ 正在推送到远程...
    git push origin %current_branch%
    if errorlevel 1 (
        echo ⚠️ 推送失败，但提交成功
    ) else (
        echo ✅ 推送成功！
    )
)

echo ✅ 分步骤提交完成！
pause
goto :eof

:show_changes
echo.
echo 📋 变更详情:
echo.
git status
echo.
git diff --stat
pause
goto :eof

:eof
echo.
echo 感谢使用 Git 快速提交工具！
pause