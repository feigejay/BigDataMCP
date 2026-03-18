"""
=============================================================
演示脚本 5：独立测试 Bright Data MCP（不依赖 AnythingLLM）
=============================================================
用途：直接在终端与 MCP 服务器交互，验证 MCP 连接和工具可用性。
      帮助排查问题——到底是 MCP 本身的问题还是 AnythingLLM 的问题。

运行：python 05_mcp_standalone_test.py
=============================================================
"""

import subprocess
import json
import sys
import os
import time

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def get_api_token():
    """获取 API Token"""
    # 优先从环境变量获取
    token = os.environ.get("API_TOKEN", "")
    if token:
        return token

    token = os.environ.get("BRIGHT_DATA_API_TOKEN", "")
    if token:
        return token

    # 尝试从配置文件读取
    import platform
    user = os.path.expanduser("~")
    system = platform.system()

    if system == "Windows":
        config_path = os.path.join(
            user, "AppData", "Roaming", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )
    elif system == "Darwin":
        config_path = os.path.join(
            user, "Library", "Application Support", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )
    else:
        config_path = os.path.join(
            user, ".config", "anythingllm-desktop",
            "storage", "plugins", "anythingllm_mcp_servers.json"
        )

    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            token = config.get("mcpServers", {}).get("bright-data", {}).get("env", {}).get("API_TOKEN", "")
            if token and not token.startswith("<") and "替换" not in token:
                return token
        except Exception:
            pass

    # 手动输入
    print(f"  {YELLOW}未找到 API Token，请手动输入：{RESET}")
    token = input("  Bright Data API Token: ").strip()
    return token


def test_mcp_startup(token):
    """测试 MCP 服务器能否启动"""
    print(f"\n{BOLD}[测试 1] MCP 服务器启动{RESET}")

    env = os.environ.copy()
    env["API_TOKEN"] = token

    try:
        # 启动 MCP 服务器，发送 initialize 请求
        proc = subprocess.Popen(
            ["npx", "-y", "@brightdata/mcp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=True,
        )

        # 发送 MCP initialize 请求 (JSON-RPC)
        init_request = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }) + "\n"

        print(f"  发送 initialize 请求...")
        proc.stdin.write(init_request.encode())
        proc.stdin.flush()

        # 等待响应（最多 30 秒）
        import select
        start = time.time()
        response_data = b""

        while time.time() - start < 30:
            # 读取一行
            try:
                proc.stdout.timeout = 1
            except Exception:
                pass

            line = b""
            while True:
                if time.time() - start > 30:
                    break
                try:
                    char = proc.stdout.read(1)
                    if not char:
                        time.sleep(0.1)
                        continue
                    line += char
                    if char == b"\n":
                        break
                except Exception:
                    time.sleep(0.1)
                    continue

            if line:
                response_data = line
                break

        if response_data:
            try:
                resp = json.loads(response_data.decode().strip())
                if "result" in resp:
                    server_info = resp.get("result", {}).get("serverInfo", {})
                    server_name = server_info.get("name", "unknown")
                    server_version = server_info.get("version", "unknown")
                    print(f"  [{GREEN}PASS{RESET}] MCP 服务器已响应")
                    print(f"         服务器: {server_name} v{server_version}")

                    # 发送 tools/list 请求
                    tools_request = json.dumps({
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/list",
                        "params": {}
                    }) + "\n"

                    print(f"\n{BOLD}[测试 2] 获取可用工具列表{RESET}")
                    proc.stdin.write(tools_request.encode())
                    proc.stdin.flush()

                    # 读取工具列表响应
                    start2 = time.time()
                    tools_data = b""
                    while time.time() - start2 < 15:
                        line = b""
                        while True:
                            if time.time() - start2 > 15:
                                break
                            try:
                                char = proc.stdout.read(1)
                                if not char:
                                    time.sleep(0.1)
                                    continue
                                line += char
                                if char == b"\n":
                                    break
                            except Exception:
                                time.sleep(0.1)
                                continue
                        if line:
                            tools_data = line
                            break

                    if tools_data:
                        tools_resp = json.loads(tools_data.decode().strip())
                        tools = tools_resp.get("result", {}).get("tools", [])
                        print(f"  [{GREEN}PASS{RESET}] 获取到 {len(tools)} 个工具")
                        print(f"\n  可用工具列表:")
                        for i, tool in enumerate(tools, 1):
                            name = tool.get("name", "unknown")
                            desc = tool.get("description", "")[:60]
                            print(f"    {i:2d}. {CYAN}{name}{RESET}")
                            print(f"        {desc}...")
                    else:
                        print(f"  [{YELLOW}WARN{RESET}] 工具列表响应超时")

                elif "error" in resp:
                    error = resp.get("error", {})
                    print(f"  [{RED}FAIL{RESET}] MCP 返回错误: {error.get('message', 'unknown')}")
            except json.JSONDecodeError:
                print(f"  [{YELLOW}WARN{RESET}] 收到响应但无法解析 JSON")
                print(f"  原始响应: {response_data.decode()[:200]}")
        else:
            # 检查 stderr
            stderr_output = ""
            try:
                stderr_output = proc.stderr.read(2000).decode()
            except Exception:
                pass

            if stderr_output:
                if "ready" in stderr_output.lower() or "started" in stderr_output.lower():
                    print(f"  [{GREEN}PASS{RESET}] MCP 服务器已启动（通过 stderr 确认）")
                    print(f"  stderr: {stderr_output[:300]}")
                else:
                    print(f"  [{YELLOW}WARN{RESET}] MCP 服务器输出:")
                    print(f"  {stderr_output[:500]}")
            else:
                print(f"  [{RED}FAIL{RESET}] MCP 服务器无响应（30秒超时）")

        # 清理
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()

    except FileNotFoundError:
        print(f"  [{RED}FAIL{RESET}] npx 命令不可用，请先安装 Node.js")
    except Exception as e:
        print(f"  [{RED}FAIL{RESET}] 测试失败: {e}")


def main():
    print(f"""
{BOLD}{CYAN}
 ╔══════════════════════════════════════════════════════════╗
 ║     Bright Data MCP 独立测试                             ║
 ║     直接在终端验证 MCP 服务器连接和工具可用性            ║
 ╚══════════════════════════════════════════════════════════╝
{RESET}""")

    token = get_api_token()
    if not token:
        print(f"  {RED}未提供 API Token，无法测试{RESET}")
        return

    print(f"  API Token: {token[:8]}...{token[-4:]} (长度: {len(token)})")

    test_mcp_startup(token)

    print(f"""
{BOLD}
{'='*60}
  测试完成！

  如果所有测试通过：
  → MCP 服务器本身没问题，可以放心在 AnythingLLM 中使用

  如果测试失败：
  → 检查 API Token 是否正确
  → 检查 Node.js / npx 是否正常安装
  → 检查网络连接（MCP 需要访问 Bright Data API）
{'='*60}
{RESET}""")


if __name__ == "__main__":
    main()
