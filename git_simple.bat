@echo off
git status
echo.
echo 使用说明:
echo - git_commit.bat: 快速提交
echo - git_quick.bat: 完整功能
echo - git_quick.ps1: PowerShell版本
echo.
set /p msg=请输入提交信息: 
if "%msg%"=="" exit
git add .
git commit -m "%msg%"
git push origin main
echo 提交完成!