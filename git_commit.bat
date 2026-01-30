@echo off
title Git 快速提交
echo 🚀 Git 快速提交工具
echo.

:: 检查Git
where git >nul 2>&1 || (echo ❌ Git未安装 & pause & exit /b 1)

:: 检查仓库
git rev-parse --git-dir >nul 2>&1 || (echo ❌ 不是Git仓库 & pause & exit /b 1)

:: 获取分支
for /f "tokens=*" %%i in ('git branch --show-current 2^>nul') do set "branch=%%i"
if "%branch%"=="" set "branch=main"

echo 📍 分支: %branch%
echo.

:: 检查变更
if git diff --quiet && git diff --cached --quiet (
    echo ✅ 没有变更
    echo [1] 查看历史  [2] 拉取更新  [3] 退出
    set /p "opt=选择: "
    if "%opt%"=="1" git log --oneline -5 & pause & goto end
    if "%opt%"=="2" git pull origin %branch% & pause & goto end
    goto end
)

echo 📋 发现变更:
git status --short
echo.

:: 快速提交
set /p "msg=提交信息: "
if "%msg%"=="" goto end

echo.
echo 📦 暂存... git add .
git add .

echo 💾 提交... git commit -m "%msg%"
git commit -m "%msg%"

echo ⬆️ 推送... git push origin %branch%
git push origin %branch%

echo ✅ 完成！
:end
pause