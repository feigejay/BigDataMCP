"""
=============================================================
演示脚本 3：MCP 配置生成器
=============================================================
用途：交互式生成 AnythingLLM 的 MCP 配置文件，
      自动写入正确的路径，省去手动查路径、编辑 JSON 的麻烦。

运行：python 03_generate_mcp_config.py
=============================================================
"""

import os
import sys
import json
import platform
import shutil
from datetime import datetime

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def get_config_path():
    """获取 AnythingLLM MCP 配置文件路径"""
    system = platform.system()
    user = os.path.expanduser("~")

    if system == "Windows":
        return os.path.join(
            user, "AppData", "Roaming", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )
    elif system == "Darwin":
        return os.path.join(
            user, "Library", "Application Support", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )
    else:
        return os.path.join(
            user, ".config", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )


def main():
    print(f"""
{BOLD}{CYAN}
 ╔══════════════════════════════════════════════════════════╗
 ║     AnythingLLM × Bright Data MCP 配置生成器             ║
 ╚══════════════════════════════════════════════════════════╝
{RESET}""")

    config_path = get_config_path()
    print(f"  目标配置文件: {CYAN}{config_path}{RESET}\n")

    # 检查目录是否存在
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        print(f"  {YELLOW}配置目录不存在: {config_dir}{RESET}")
        print(f"  请先打开 AnythingLLM → 设置 → Agent Skills 页面，让它自动创建目录。")
        print(f"  或者手动创建目录后重新运行本脚本。\n")

        create = input(f"  是否手动创建目录？(y/n): ").strip().lower()
        if create == "y":
            os.makedirs(config_dir, exist_ok=True)
            print(f"  {GREEN}目录已创建{RESET}\n")
        else:
            print(f"  {YELLOW}已取消{RESET}")
            return

    # 检查是否已有配置文件
    if os.path.exists(config_path):
        print(f"  {YELLOW}配置文件已存在！{RESET}")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
            print(f"  当前内容:")
            print(f"  {json.dumps(existing, indent=2, ensure_ascii=False)}\n")
        except Exception:
            print(f"  （无法读取当前内容）\n")

        overwrite = input(f"  是否覆盖？会先备份原文件 (y/n): ").strip().lower()
        if overwrite != "y":
            print(f"  {YELLOW}已取消{RESET}")
            return

        # 备份
        backup_path = config_path + f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(config_path, backup_path)
        print(f"  {GREEN}原文件已备份到: {backup_path}{RESET}\n")

    # 获取 API Token
    print(f"  {BOLD}请输入你的 Bright Data API Token:{RESET}")
    print(f"  （获取方式：登录 brightdata.com → 控制台 → MCP 区块 → 生成 Token）\n")
    api_token = input(f"  API Token: ").strip()

    if not api_token:
        print(f"\n  {RED}Token 不能为空！{RESET}")
        return

    # Pro 模式选择
    print(f"\n  {BOLD}是否启用 Pro 模式？{RESET}")
    print(f"  - 免费版: search_engine + scrape_as_markdown（够日常使用）")
    print(f"  - Pro 版: 60+ 专用工具（Amazon/YouTube/LinkedIn 等，按量付费）\n")
    pro_mode = input(f"  启用 Pro 模式？(y/n, 默认 n): ").strip().lower()

    # 生成配置
    env = {"API_TOKEN": api_token}
    if pro_mode == "y":
        env["PRO_MODE"] = "true"

    config = {
        "mcpServers": {
            "bright-data": {
                "command": "npx",
                "args": ["-y", "@brightdata/mcp"],
                "env": env
            }
        }
    }

    # 写入文件
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"""
{GREEN}{BOLD}  配置文件已生成！{RESET}

  文件路径: {CYAN}{config_path}{RESET}

  文件内容:
{json.dumps(config, indent=2, ensure_ascii=False)}

{BOLD}  下一步操作:{RESET}
  1. 打开（或重启）AnythingLLM
  2. 进入 设置 → Agent Skills
  3. 点击 Refresh 按钮
  4. 你应该能看到 "Bright Data" 出现在 MCP Servers 列表中
  5. 在聊天框输入 @agent 开始使用！

  Pro 模式: {GREEN + '已开启' if pro_mode == 'y' else YELLOW + '未开启（免费版）'}{RESET}
""")

    # 同时生成一份到当前目录作为备用
    local_copy = os.path.join(os.path.dirname(__file__), "mcp_config_backup.json")
    with open(local_copy, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"  {CYAN}配置副本已保存到: {local_copy}{RESET}")


if __name__ == "__main__":
    main()
