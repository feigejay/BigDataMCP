"""
=============================================================
演示脚本 2：环境检查 —— 一键验证所有前置条件
=============================================================
用途：录制视频前 / 正式演示前，快速确认环境是否 Ready。

运行：python 02_env_check.py
=============================================================
"""

import subprocess
import os
import sys
import json
import platform

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

PASS = f"{GREEN}PASS{RESET}"
FAIL = f"{RED}FAIL{RESET}"
WARN = f"{YELLOW}WARN{RESET}"


def check_command(cmd, name, min_version=None):
    """检查命令是否可用"""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10, shell=True
        )
        version = result.stdout.strip() or result.stderr.strip()
        version_line = version.split("\n")[0]
        print(f"  [{PASS}] {name}: {version_line}")
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
        print(f"  [{FAIL}] {name}: 未安装或不可用 ({e})")
        return False


def check_mcp_package():
    """检查 @brightdata/mcp 包"""
    try:
        result = subprocess.run(
            "npm list -g @brightdata/mcp",
            capture_output=True, text=True, timeout=10, shell=True
        )
        if "@brightdata/mcp" in result.stdout:
            print(f"  [{PASS}] @brightdata/mcp: 已全局安装")
            return True
        else:
            print(f"  [{WARN}] @brightdata/mcp: 未全局安装（npx 会在首次运行时自动下载）")
            print(f"         可运行: npm install -g @brightdata/mcp 提前安装")
            return True  # npx will handle it
    except Exception as e:
        print(f"  [{WARN}] @brightdata/mcp: 检查失败 ({e})，npx 首次运行时会自动下载")
        return True


def check_anythingllm_config():
    """检查 AnythingLLM MCP 配置文件"""
    system = platform.system()
    user = os.path.expanduser("~")

    if system == "Windows":
        config_path = os.path.join(
            user, "AppData", "Roaming", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )
    elif system == "Darwin":  # macOS
        config_path = os.path.join(
            user, "Library", "Application Support", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )
    else:  # Linux
        config_path = os.path.join(
            user, ".config", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )

    print(f"\n  配置文件路径: {config_path}")

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            servers = config.get("mcpServers", {})
            if "bright-data" in servers:
                bd = servers["bright-data"]
                env = bd.get("env", {})
                token = env.get("API_TOKEN", "")

                if token and token != "替换成你的Bright Data API Token" and not token.startswith("<"):
                    print(f"  [{PASS}] Bright Data MCP 已配置，API Token 已设置")
                    pro = env.get("PRO_MODE", "false")
                    print(f"         Pro 模式: {'开启' if pro == 'true' else '关闭（免费版）'}")
                    return True
                else:
                    print(f"  [{FAIL}] Bright Data MCP 已配置，但 API Token 未设置（还是占位符）")
                    return False
            else:
                print(f"  [{FAIL}] 配置文件存在，但未配置 Bright Data MCP 服务器")
                return False
        except json.JSONDecodeError:
            print(f"  [{FAIL}] 配置文件格式错误（JSON 解析失败）")
            return False
    else:
        print(f"  [{WARN}] 配置文件不存在")
        print(f"         请先打开 AnythingLLM → 设置 → Agent Skills 页面以生成配置文件")
        return False


def check_api_token_env():
    """检查环境变量中的 API Token"""
    token = os.environ.get("API_TOKEN", "")
    bright_token = os.environ.get("BRIGHT_DATA_API_TOKEN", "")

    if token:
        print(f"  [{PASS}] 环境变量 API_TOKEN 已设置 (长度: {len(token)})")
        return True
    elif bright_token:
        print(f"  [{PASS}] 环境变量 BRIGHT_DATA_API_TOKEN 已设置 (长度: {len(bright_token)})")
        return True
    else:
        print(f"  [{WARN}] 未检测到 API Token 环境变量（如果已在配置文件中设置则无需关心）")
        return True


def main():
    print(f"""
{BOLD}{CYAN}
 ╔══════════════════════════════════════════════════════════╗
 ║     AnythingLLM + Bright Data MCP 环境检查               ║
 ╚══════════════════════════════════════════════════════════╝
{RESET}""")

    all_pass = True

    # 1. 基础环境
    print(f"{BOLD}[1/4] 基础环境{RESET}")
    ok1 = check_command("node --version", "Node.js")
    ok2 = check_command("npm --version", "npm")
    ok3 = check_command("npx --version", "npx")
    if not (ok1 and ok2):
        all_pass = False
        print(f"\n  {RED}Node.js 是必需的！请先安装：https://nodejs.org/{RESET}")

    # 2. MCP 包
    print(f"\n{BOLD}[2/4] Bright Data MCP 包{RESET}")
    ok4 = check_mcp_package()

    # 3. AnythingLLM 配置
    print(f"\n{BOLD}[3/4] AnythingLLM MCP 配置{RESET}")
    ok5 = check_anythingllm_config()
    if not ok5:
        all_pass = False

    # 4. API Token
    print(f"\n{BOLD}[4/4] API Token{RESET}")
    check_api_token_env()

    # 汇总
    print(f"\n{'='*60}")
    if all_pass:
        print(f"""
{GREEN}{BOLD}  所有检查通过！环境已就绪，可以开始演示。{RESET}

  下一步：
  1. 打开 AnythingLLM
  2. 在聊天框输入 @agent
  3. 使用 04_test_prompts.md 中的提示词开始测试
""")
    else:
        print(f"""
{YELLOW}{BOLD}  部分检查未通过，请按上面的提示修复后再试。{RESET}

  快速修复：
  1. 安装 Node.js：https://nodejs.org/
  2. 运行配置生成器：python 03_generate_mcp_config.py
  3. 重新运行本脚本验证
""")


if __name__ == "__main__":
    main()
