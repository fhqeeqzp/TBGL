#!/bin/bash

echo "🚀 Git 快速提交别名配置"
echo "======================================"
echo ""

# 设置Git别名
echo "📦 配置Git别名..."

git config --global alias.st status
echo "✅ git st -> git status"

git config --global alias.co checkout
echo "✅ git co -> git checkout"

git config --global alias.br branch
echo "✅ git br -> git branch"

git config --global alias.ci commit
echo "✅ git ci -> git commit"

git config --global alias.lg "log --oneline --graph --decorate --all"
echo "✅ git lg -> git log --oneline --graph --decorate --all"

# 设置快速提交别名
git config --global alias.quick '!f() { git add .; git commit -m "$1"; git push origin main; }; f'
echo "✅ git quick '消息' -> 快速提交并推送"

# 设置拉取别名
git config --global alias.pull-all '!f() { git fetch origin; git merge origin/main; }; f'
echo "✅ git pull-all -> 拉取并合并远程main分支"

# 设置检查别名
git config --global alias.check '!f() { echo "=== Git状态 ==="; git st; echo ""; echo "=== 最近提交 ==="; git lg -5; }; f'
echo "✅ git check -> 检查状态和最近提交"

echo ""
echo "🎯 使用方法:"
echo "  git quick '提交信息'      # 快速提交"
echo "  git st                   # 查看状态"
echo "  git lg                   # 查看提交历史"
echo "  git pull-all             # 拉取更新"
echo "  git check                # 检查状态"
echo ""
echo "💡 建议将这些别名保存在 ~/.bashrc 或 ~/.zshrc 中"
echo ""
echo "✨ Git别名配置完成！"