import subprocess
import datetime
import os

def run_command(command):
    """运行终端命令并返回结果"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 运行失败: {command}")
        print(f"错误详情: {result.stderr}")
        return False
    return True

def sync_to_github():
    print("🚀 开始同步菜单到 GitHub...")

    # 1. 确保在正确的文件夹路径（当前脚本所在目录）
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 2. 先拉取远程最新内容，避免冲突
    print("🔄 正在拉取远程最新内容...")
    if not run_command("git pull origin main --allow-unrelated-histories"):
        print("❌ 拉取失败，请检查网络或手动解决冲突。")
        return

    # 3. 添加文件到暂存区
    print("📦 正在整理文件...")
    run_command("git add index.html admin.html menu.json server.py push_menu.py images/*")

    # 4. 提交修改，备注加上当前时间
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Update menu at {now}"
    has_changes = run_command(f'git commit -m "{commit_message}"')

    if has_changes:
        print(f"✅ 已生成提交记录: {commit_message}")
    else:
        print("ℹ️ 没有发现新改动，无需提交。")
        print("✅ 本地已是最新状态，无需上传。")
        return

    # 5. 推送到 GitHub
    print("☁️ 正在上传到远程仓库...")
    if run_command("git push origin main"):
        print("\n🎉 同步成功！菜单已飞向云端。")
        print("请等待 1 分钟左右，手机刷新网址即可看到更新。")
    else:
        print("❌ 上传失败，请检查网络或 Git 配置。")

if __name__ == "__main__":
    sync_to_github()
    # 保持窗口开启，方便查看结果
    input("\n按下回车键关闭窗口...")
