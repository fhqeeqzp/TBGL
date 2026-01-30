# Git 快速提交工具使用说明

## 📋 文件说明

我已经为你创建了多个Git快速提交脚本：

### 🖥️ Windows批处理文件 (.bat)
- `git_simple.bat` - 最简单的提交方式
- `git_commit.bat` - 快速提交工具  
- `git_quick.bat` - 完整功能的提交工具

### ⚡ PowerShell脚本 (.ps1)
- `git_quick.ps1` - 功能最完整的PowerShell版本

## 🚀 使用方法

### 方法1: 简单的Git命令组合
在Git Bash或命令提示符中执行：

```bash
# 快速提交当前所有变更
git add .
git commit -m "更新内容"
git push origin main

# 或者一键执行 (需要创建别名)
git config --global alias.quick '!f() { git add .; git commit -m "$1"; git push origin main; }; f'
# 然后使用: git quick "提交信息"
```

### 方法2: 使用创建的批处理文件

#### git_simple.bat (推荐新手使用)
双击运行，按照提示输入提交信息即可。

#### git_quick.ps1 (推荐有PowerShell经验的用户)
```powershell
# 交互模式
.\git_quick.ps1

# 快速提交模式
.\git_quick.ps1 -Message "更新功能"

# 查看状态
.\git_quick.ps1 -Status

# 拉取更新
.\git_quick.ps1 -Pull
```

### 方法3: IDE集成的Git功能
- **VS Code**: 按 `Ctrl+Shift+G` 打开Git面板
- **PyCharm**: 使用内置的Git工具窗口
- **Vim**: 使用vim-fugitive插件

## 📝 推荐工作流

### 日常开发工作流
```bash
# 1. 开发前先拉取最新代码
git pull origin main

# 2. 开发过程中可以随时查看状态
git status
git diff

# 3. 开发完成后快速提交
git_simple.bat
# 或手动执行:
git add .
git commit -m "描述你做了什么"
git push origin main
```

### 提交信息格式建议
```bash
git commit -m "功能: 添加用户登录功能"
git commit -m "修复: 解决数据库连接超时问题"
git commit -m "文档: 更新API使用说明"
git commit -m "重构: 优化登录窗口UI设计"
```

## ⚠️ 注意事项

1. **提交前检查**: 每次提交前运行 `git status` 检查变更
2. **提交信息**: 写清楚、简洁的提交信息
3. **分支管理**: 确保在正确的分支上工作
4. **冲突解决**: 遇到冲突时先解决再提交

## 🛠️ 自定义配置

### 创建Git别名 (推荐)
```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --decorate --all"

# 快速提交别名
git config --global alias.quick "!f() { git add .; git commit -m \"$1\"; git push origin main; }; f"

# 使用示例
git quick "快速提交信息"
```

### 设置默认分支
```bash
git branch -M main  # 重命名当前分支为main
git config --global init.defaultBranch main
```

## 🔧 故障排除

### 常见问题
1. **编码问题**: 确保文件保存为UTF-8编码
2. **权限问题**: 确保对Git仓库有写权限
3. **网络问题**: 检查Git配置和SSH密钥

### 强制推送 (谨慎使用)
```bash
git push --force-with-lease origin main  # 安全强制推送
```

## 📚 更多资源

- [Git官方文档](https://git-scm.com/docs)
- [GitHub Desktop](https://desktop.github.com/) - 图形化Git工具
- [SourceTree](https://www.sourcetreeapp.com/) - 免费Git GUI

---

💡 **提示**: 建议先熟悉基本的Git命令，然后再使用批处理脚本自动化操作。