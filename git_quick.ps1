# Git 快速提交 PowerShell 脚本
# 使用方法: .\git_quick.ps1

param(
    [string]$Message = "",
    [switch]$Help = $false,
    [switch]$Status = $false,
    [switch]$Pull = $false
)

# 设置控制台编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Git 快速提交"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "       Git 快速提交工具 (PowerShell)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 显示帮助
if ($Help) {
    Write-Host "使用方法:" -ForegroundColor Yellow
    Write-Host "  .\git_quick.ps1                    # 交互模式" -ForegroundColor White
    Write-Host "  .\git_quick.ps1 -Message '更新'    # 快速提交" -ForegroundColor White
    Write-Host "  .\git_quick.ps1 -Status            # 查看状态" -ForegroundColor White
    Write-Host "  .\git_quick.ps1 -Pull             # 拉取更新" -ForegroundColor White
    Write-Host "  .\git_quick.ps1 -Help              # 显示帮助" -ForegroundColor White
    Write-Host ""
    return
}

# 检查Git是否安装
try {
    $gitVersion = git --version 2>$null
    if (-not $gitVersion) {
        Write-Host "❌ 错误: Git未安装或不在PATH中" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
    Write-Host "✅ $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误: 无法运行Git命令" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 检查是否在Git仓库中
try {
    $gitDir = git rev-parse --git-dir 2>$null
    if (-not $gitDir) {
        Write-Host "❌ 错误: 当前目录不是Git仓库" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
} catch {
    Write-Host "❌ 错误: 无法检测Git仓库" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 获取当前分支
try {
    $currentBranch = git branch --show-current 2>$null
    if ([string]::IsNullOrEmpty($currentBranch)) {
        $currentBranch = "main"
    }
} catch {
    $currentBranch = "main"
}

Write-Host "📍 当前分支: $currentBranch" -ForegroundColor Blue
Write-Host ""

# 检查变更状态
function Get-GitStatus {
    param()
    
    $uncommitted = git diff --quiet
    $staged = git diff --cached --quiet
    
    $hasUncommitted = -not $uncommitted
    $hasStaged = -not $staged
    
    return @{
        HasUncommitted = $hasUncommitted
        HasStaged = $hasStaged
        HasChanges = $hasUncommitted -or $hasStaged
    }
}

$status = Get-GitStatus

# 如果指定了Status参数，显示状态
if ($Status) {
    Write-Host "📋 Git 状态详情:" -ForegroundColor Yellow
    Write-Host ""
    git status
    Write-Host ""
    Read-Host "按回车键退出"
    return
}

# 如果指定了Pull参数，拉取更新
if ($Pull) {
    Write-Host "⬇️ 正在拉取远程更新..." -ForegroundColor Yellow
    git pull origin $currentBranch
    Write-Host ""
    Read-Host "按回车键退出"
    return
}

# 如果提供了提交信息，快速提交
if ($Message -ne "") {
    Write-Host "🚀 快速提交模式" -ForegroundColor Yellow
    Write-Host ""
    
    # 检查是否有变更
    if (-not $status.HasChanges) {
        Write-Host "✅ 没有发现变更，无需提交" -ForegroundColor Green
        Read-Host "按回车键退出"
        return
    }
    
    Write-Host "📦 暂存所有变更..." -ForegroundColor Cyan
    git add .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 暂存失败" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
    
    Write-Host "💾 提交变更..." -ForegroundColor Cyan
    git commit -m $Message
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 提交失败" -ForegroundColor Red
        Read-Host "按回车键退出"
        exit 1
    }
    
    Write-Host "⬆️ 推送到远程..." -ForegroundColor Cyan
    git push origin $currentBranch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️ 推送失败，但提交成功" -ForegroundColor Yellow
    } else {
        Write-Host "✅ 提交成功！" -ForegroundColor Green
    }
    
    Write-Host ""
    Read-Host "按回车键退出"
    return
}

# 交互模式
if (-not $status.HasChanges) {
    Write-Host "✅ 没有发现变更" -ForegroundColor Green
    Write-Host ""
    Write-Host "请选择操作:" -ForegroundColor Yellow
    Write-Host "[1] 查看提交历史" -ForegroundColor White
    Write-Host "[2] 拉取远程更新" -ForegroundColor White
    Write-Host "[3] 查看状态详情" -ForegroundColor White
    Write-Host "[4] 退出" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "请输入选项 [1-4]"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "📜 最近的提交历史:" -ForegroundColor Yellow
            git log --oneline -5
        }
        "2" {
            Write-Host ""
            Write-Host "⬇️ 正在拉取远程更新..." -ForegroundColor Yellow
            git pull origin $currentBranch
        }
        "3" {
            Write-Host ""
            git status
        }
        "4" {
            return
        }
        default {
            Write-Host "❌ 无效选项" -ForegroundColor Red
        }
    }
} else {
    Write-Host "📋 发现变更:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    Write-Host "请选择操作:" -ForegroundColor Yellow
    Write-Host "[1] 快速提交 (add + commit + push)" -ForegroundColor White
    Write-Host "[2] 分步骤提交" -ForegroundColor White
    Write-Host "[3] 查看变更详情" -ForegroundColor White
    Write-Host "[4] 取消" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "请输入选项 [1-4]"
    
    switch ($choice) {
        "1" {
            Write-Host ""
            $commitMessage = Read-Host "请输入提交信息"
            
            if ([string]::IsNullOrEmpty($commitMessage)) {
                Write-Host "❌ 提交信息不能为空" -ForegroundColor Red
                break
            }
            
            Write-Host ""
            Write-Host "🚀 快速提交中..." -ForegroundColor Yellow
            
            Write-Host "📦 暂存变更..." -ForegroundColor Cyan
            git add .
            
            Write-Host "💾 提交..." -ForegroundColor Cyan
            git commit -m $commitMessage
            
            Write-Host "⬆️ 推送..." -ForegroundColor Cyan
            git push origin $currentBranch
            
            Write-Host "✅ 提交完成！" -ForegroundColor Green
        }
        "2" {
            Write-Host ""
            Write-Host "🔄 分步骤提交模式" -ForegroundColor Yellow
            Write-Host ""
            
            Write-Host "📋 步骤 1: 检查状态" -ForegroundColor Cyan
            git status
            Write-Host ""
            
            $continue = Read-Host "是否继续? (y/n)"
            if ($continue -ne "y" -and $continue -ne "Y") {
                break
            }
            
            Write-Host ""
            Write-Host "📦 步骤 2: 暂存变更" -ForegroundColor Cyan
            Write-Host "[1] 暂存所有文件" -ForegroundColor White
            Write-Host "[2] 暂存特定文件" -ForegroundColor White
            Write-Host ""
            
            $stageChoice = Read-Host "请选择 [1-2]"
            
            if ($stageChoice -eq "1") {
                Write-Host "暂存所有文件..." -ForegroundColor Cyan
                git add .
            } elseif ($stageChoice -eq "2") {
                $files = Read-Host "请输入要暂存的文件 (空格分隔)"
                if (-not [string]::IsNullOrEmpty($files)) {
                    git add $files
                }
            }
            
            Write-Host ""
            Write-Host "💾 步骤 3: 提交" -ForegroundColor Cyan
            $commitMessage = Read-Host "请输入提交信息"
            
            if (-not [string]::IsNullOrEmpty($commitMessage)) {
                git commit -m $commitMessage
                
                Write-Host ""
                $pushNow = Read-Host "是否立即推送到远程? (y/n)"
                if ($pushNow -eq "y" -or $pushNow -eq "Y") {
                    Write-Host "⬆️ 正在推送到远程..." -ForegroundColor Cyan
                    git push origin $currentBranch
                }
            }
            
            Write-Host "✅ 分步骤提交完成！" -ForegroundColor Green
        }
        "3" {
            Write-Host ""
            Write-Host "📋 变更详情:" -ForegroundColor Yellow
            Write-Host ""
            git status
            Write-Host ""
            git diff --stat
        }
        "4" {
            return
        }
        default {
            Write-Host "❌ 无效选项" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "感谢使用 Git 快速提交工具！" -ForegroundColor Cyan
Read-Host "按回车键退出"