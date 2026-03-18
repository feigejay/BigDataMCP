"""
=============================================================
演示脚本 6：一键运行全部演示流程
=============================================================
用途：视频录制时，按顺序引导执行每个演示环节。
      充当一个"导演提词器"，告诉你现在该做什么。

运行：python 06_demo_runner.py
=============================================================
"""

import subprocess
import sys
import os
import time

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause(msg="按 Enter 继续..."):
    input(f"\n  {DIM}{msg}{RESET}")


def run_script(script_name):
    """运行指定的 Python 脚本"""
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"  {RED}脚本不存在: {script_path}{RESET}")


def show_prompt(title, prompt_text):
    """展示要在 AnythingLLM 中输入的 Prompt"""
    print(f"""
{BOLD}{CYAN}{'='*60}
  {title}
{'='*60}{RESET}

{YELLOW}  请在 AnythingLLM 中输入以下 Prompt：{RESET}
{DIM}  （先输入 @agent 进入 Agent 模式）{RESET}

{GREEN}┌────────────────────────────────────────────────────┐{RESET}
""")
    for line in prompt_text.strip().split("\n"):
        print(f"{GREEN}│{RESET}  {line}")
    print(f"""
{GREEN}└────────────────────────────────────────────────────┘{RESET}
""")


def main():
    clear_screen()
    print(f"""
{BOLD}{CYAN}
 ╔══════════════════════════════════════════════════════════╗
 ║                                                          ║
 ║   AnythingLLM + Bright Data MCP 演示流程引导器           ║
 ║                                                          ║
 ║   本脚本会按视频脚本顺序，引导你完成每个演示环节        ║
 ║   按 Enter 进入下一步                                    ║
 ║                                                          ║
 ╚══════════════════════════════════════════════════════════╝
{RESET}

  {DIM}提示：请先打开录屏软件（OBS 等），准备好后按 Enter 开始{RESET}
""")
    pause("准备好了？按 Enter 开始演示流程...")

    # ================================================
    # 环节 1: 环境检查
    # ================================================
    clear_screen()
    print(f"""
{BOLD}{CYAN}
 ┌──────────────────────────────────────┐
 │  环节 0 / 预检：环境检查             │
 └──────────────────────────────────────┘
{RESET}
  {DIM}这个环节不需要录制，只是确认环境就绪{RESET}
""")
    pause("按 Enter 运行环境检查...")
    run_script("02_env_check.py")
    pause("环境检查完成。确认无误后按 Enter 进入正式演示...")

    # ================================================
    # 环节 2: 传统爬虫失败演示
    # ================================================
    clear_screen()
    print(f"""
{BOLD}{CYAN}
 ┌──────────────────────────────────────┐
 │  环节 1 / 片头素材：传统爬虫失败     │
 │                                      │
 │  对应视频：0:20-0:35                 │
 └──────────────────────────────────────┘
{RESET}
  {YELLOW}操作说明：{RESET}
  1. 开始录屏
  2. 运行传统爬虫脚本，展示请求反爬网站的失败画面
  3. 这段素材用于视频片头的"痛点引入"

  {DIM}录制要点：终端画面要清晰，失败信息用红色高亮{RESET}
""")
    pause("按 Enter 运行传统爬虫演示...")
    run_script("01_traditional_scraper_fail.py")
    pause("传统爬虫演示完成。按 Enter 继续...")

    # ================================================
    # 环节 3: AnythingLLM 安装（提示）
    # ================================================
    clear_screen()
    print(f"""
{BOLD}{CYAN}
 ┌──────────────────────────────────────┐
 │  环节 2 / 安装配置：AnythingLLM      │
 │                                      │
 │  对应视频：1:50-2:50                 │
 └──────────────────────────────────────┘
{RESET}
  {YELLOW}操作说明：{RESET}
  1. 录制打开 AnythingLLM 官网 → 下载页面
  2. 展示安装过程（如果已安装，可以展示打开后的界面）
  3. 展示选择 LLM 模型的过程（Gemini / OpenAI / Ollama）
  4. 创建工作区

  {DIM}如果 AnythingLLM 已安装好，快速展示界面即可{RESET}
""")
    pause("录完 AnythingLLM 安装后按 Enter 继续...")

    # ================================================
    # 环节 4: Bright Data MCP 配置
    # ================================================
    clear_screen()
    print(f"""
{BOLD}{CYAN}
 ┌──────────────────────────────────────┐
 │  环节 3 / 安装配置：Bright Data MCP  │
 │                                      │
 │  对应视频：2:50-4:20                 │
 └──────────────────────────────────────┘
{RESET}
  {YELLOW}操作说明（按顺序录制）：{RESET}

  Step A: 展示 Bright Data 控制台，获取 API Token
  Step B: 终端运行验证命令（下面会提供）
  Step C: 编辑 MCP 配置文件（可用配置生成器自动完成）
  Step D: 在 AnythingLLM 中点 Refresh 验证连接

  {DIM}如果配置已经做好了，可以展示最终效果即可{RESET}
""")
    pause("按 Enter 显示终端验证命令...")

    print(f"""
  {YELLOW}在终端运行以下命令验证 MCP：{RESET}

  {GREEN}# Linux / Mac:{RESET}
  API_TOKEN="你的Token" npx -y @brightdata/mcp

  {GREEN}# Windows PowerShell:{RESET}
  $Env:API_TOKEN="你的Token"; npx -y @brightdata/mcp

  {DIM}看到启动日志后 Ctrl+C 退出，然后用配置生成器写入配置文件{RESET}
""")
    pause("需要运行配置生成器吗？按 Enter 运行（或 Ctrl+C 跳过）...")

    try:
        run_script("03_generate_mcp_config.py")
    except KeyboardInterrupt:
        print(f"\n  {DIM}已跳过{RESET}")

    pause("MCP 配置完成后按 Enter 继续...")

    # ================================================
    # 环节 5: 场景一
    # ================================================
    clear_screen()
    show_prompt(
        "环节 4 / 场景一：GitHub 开源项目调研（免费版）\n  对应视频：4:20-5:15",
        """帮我在 Google 上搜索"2026年3月最值得关注的AI开源项目推荐"，
从搜索结果中挑出最相关的 3 篇文章，
逐个抓取它们的完整正文内容。

然后基于这些文章的内容，帮我整理一份"本周AI开源项目推荐清单"。
每个项目包含：
1. 项目名称
2. GitHub 地址（如果文章提到了的话）
3. 一句话介绍它是干什么的
4. 适合什么人使用

最后用表格形式输出。"""
    )
    print(f"""
  {YELLOW}录制要点：{RESET}
  - 展示 Agent 调用 search_engine → scrape_as_markdown 的完整过程
  - 注意展示工具调用的日志（展开 Agent 详情下拉菜单）
  - 最终表格输出要完整展示
""")
    pause("场景一录制完成后按 Enter 继续...")

    # ================================================
    # 环节 6: 场景二
    # ================================================
    clear_screen()
    show_prompt(
        "环节 5 / 场景二：反爬硬骨头实测 — Zillow 房源抓取\n  对应视频：5:15-6:10",
        """请帮我抓取这个 Zillow 房源页面的详细信息：
https://www.zillow.com/homedetails/104-69-88th-Ave-2R-Richmond-Hill-NY-11418/458388893_zpid/

我想知道：
1. 房屋价格
2. 地址
3. 面积（平方英尺）
4. 卧室和卫生间数量
5. 房源描述
6. 上市时间

请用清晰的列表格式输出。"""
    )
    print(f"""
  {YELLOW}录制要点：{RESET}
  - 开头插入之前录制的"传统爬虫失败"画面作为对比
  - 重点展示：同样的 URL，MCP 直接拿到数据
  - Pro 版会调用 web_data_zillow_properties_listing 专用工具
  - 免费版会用 scrape_as_markdown 通用抓取
""")
    pause("场景二录制完成后按 Enter 继续...")

    # ================================================
    # 环节 7: 场景三
    # ================================================
    clear_screen()
    show_prompt(
        "环节 6 / 场景三：跨平台信息聚合分析\n  对应视频：6:10-7:10",
        """我想深入了解 MCP（Model Context Protocol）这个技术的最新发展情况。
请帮我做以下调研：

第一步：用英文搜索 "MCP Model Context Protocol 2026 latest developments"，
挑选 2 篇最有价值的英文文章并抓取全文。

第二步：再用中文搜索 "MCP协议 2026 最新进展 社区评价"，
挑选 1 篇中文社区讨论并抓取内容。

第三步：基于你抓取到的全部内容，给我写一份综合分析报告，包含：
1. MCP 目前发展到什么阶段（用通俗语言说明）
2. 社区的主流正面评价（3条）
3. 社区的主流负面评价或担忧（3条）
4. 你认为 MCP 的未来发展趋势

报告控制在 500 字以内，重点突出核心观点。"""
    )
    print(f"""
  {YELLOW}录制要点：{RESET}
  - 这是最复杂的场景，Agent 需要多轮工具调用
  - 重点展示 Agent 的自主编排能力（中英文搜索切换）
  - 最终报告要完整展示，体现 AI 的分析能力
""")
    pause("场景三录制完成后按 Enter 继续...")

    # ================================================
    # 完成
    # ================================================
    clear_screen()
    print(f"""
{BOLD}{GREEN}
 ╔══════════════════════════════════════════════════════════╗
 ║                                                          ║
 ║           所有演示环节录制完成！                          ║
 ║                                                          ║
 ╚══════════════════════════════════════════════════════════╝
{RESET}

  {BOLD}录制素材清单：{RESET}

  {GREEN}[1]{RESET} 传统爬虫失败画面（终端录屏）
  {GREEN}[2]{RESET} AnythingLLM 安装配置画面
  {GREEN}[3]{RESET} Bright Data 控制台 + MCP 配置画面
  {GREEN}[4]{RESET} 场景一：GitHub 项目调研（AnythingLLM 录屏）
  {GREEN}[5]{RESET} 场景二：Zillow 反爬实测（AnythingLLM 录屏）
  {GREEN}[6]{RESET} 场景三：跨平台信息聚合（AnythingLLM 录屏）

  {BOLD}后期制作提醒：{RESET}
  - 别忘了录制竞品对比表格的画外音
  - 片头片尾用模板生成
  - 视频发布时添加时间戳章节标记

  {CYAN}辛苦了！去剪片吧 :){RESET}
""")


if __name__ == "__main__":
    main()
