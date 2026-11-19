# -*- coding: utf-8 -*-
"""MECHA·MON 一键推送到 GitHub。

用法：
  1. 生成 Personal Access Token (classic)：
     GitHub 右上角头像 → Settings → Developer settings →
     Personal access tokens → Tokens (classic) → Generate new token
     勾选 repo 权限（完整仓库读写），生成后复制 token（只显示一次）。
  2. 设置环境变量并运行：
       Windows PowerShell:  $env:GH_TOKEN="你的token"; python push_to_github.py
       Git Bash / macOS / Linux:  GH_TOKEN="你的token" python push_to_github.py
     也可以直接把 token 填到下面的 TOKEN 变量里（不推荐，会留在文件里）。
"""
import os, subprocess, pathlib, shutil, sys

REPO_DIR = pathlib.Path(__file__).resolve().parent
OWNER = "ziyang646815"
REPO = "mecha-mon"
BRANCH = "main"
TOKEN = os.environ.get("GH_TOKEN", "").strip()  # 也可在此处直接填 token

if not TOKEN:
    print("✗ 未找到 GH_TOKEN。请先按文件顶部说明生成 token 并设置环境变量。")
    sys.exit(1)

# 1) 配置远程（带 token 的 HTTPS，不会落盘到 .git/config）
remote = f"https://{TOKEN}@github.com/{OWNER}/{REPO}.git"
subprocess.run(["git", "remote", "remove", "origin"], cwd=REPO_DIR, capture_output=True)
subprocess.run(["git", "remote", "add", "origin", remote], cwd=REPO_DIR, check=True)

# 2) 确保分支名为 main
subprocess.run(["git", "branch", "-M", BRANCH], cwd=REPO_DIR, check=True)

# 3) 推送（--force 仅用于首次空仓库建立引用）
print(f"→ 推送到 https://github.com/{OWNER}/{REPO} ...")
r = subprocess.run(["git", "push", "-u", "origin", BRANCH], cwd=REPO_DIR,
                   capture_output=True, text=True)
# 清理输出里的 token
safe_out = r.stdout.replace(TOKEN, "***")
safe_err = r.stderr.replace(TOKEN, "***")
print(safe_out)
print(safe_err)

# 4) 移除带 token 的远程，避免泄露
subprocess.run(["git", "remote", "remove", "origin"], cwd=REPO_DIR, capture_output=True)

if r.returncode == 0:
    print(f"\n✓ 推送成功！仓库地址：https://github.com/{OWNER}/{REPO}")
else:
    print("\n✗ 推送失败，请检查 token 权限（需勾选 repo）或仓库是否已存在。"
          "\n  如果是远端已有初始提交导致冲突，可改用：git pull --rebase origin main 后再推。")
    sys.exit(1)
