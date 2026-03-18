"""
=============================================================
演示脚本 1：传统爬虫 vs Bright Data MCP —— 反爬对比实测
=============================================================
用途：视频录制时，先运行这个脚本展示传统爬虫的惨状，
      形成和后续 MCP 方案的鲜明对比。

运行：python 01_traditional_scraper_fail.py
=============================================================
"""

import requests
import time
import json

# ========== 配色输出 ==========
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def divider(title):
    print(f"\n{CYAN}{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}{RESET}\n")


def test_basic_request(url, site_name):
    """最基础的 requests 请求"""
    print(f"{YELLOW}[测试] 基础 requests 请求 {site_name}{RESET}")
    print(f"  URL: {url}")
    try:
        resp = requests.get(url, timeout=15)
        print(f"  状态码: {RED if resp.status_code != 200 else GREEN}{resp.status_code}{RESET}")
        content_len = len(resp.text)
        print(f"  响应长度: {content_len} 字符")

        # 检查是否被反爬拦截
        blocked_signs = [
            "captcha", "challenge", "blocked", "access denied",
            "robot", "verify", "cf-browser", "distil",
            "perimeterx", "datadome", "cloudflare"
        ]
        body_lower = resp.text[:3000].lower()
        detected = [s for s in blocked_signs if s in body_lower]

        if resp.status_code == 403:
            print(f"  结果: {RED}{BOLD}403 被拒绝访问！网站直接把我们拦了{RESET}")
        elif resp.status_code == 503:
            print(f"  结果: {RED}{BOLD}503 服务不可用！触发了反爬机制{RESET}")
        elif detected:
            print(f"  结果: {RED}{BOLD}虽然返回200，但内容是反爬页面！{RESET}")
            print(f"  检测到反爬关键词: {', '.join(detected)}")
        elif content_len < 5000:
            print(f"  结果: {RED}{BOLD}返回内容过短，很可能是空壳页面{RESET}")
        else:
            print(f"  结果: {GREEN}看起来拿到了内容（但不一定是完整数据）{RESET}")

        # 展示前500字符
        print(f"\n  {YELLOW}--- 响应内容前 500 字符 ---{RESET}")
        preview = resp.text[:500].replace("\n", "\n  ")
        print(f"  {preview}")
        print(f"  {YELLOW}--- 截断 ---{RESET}")

        return resp.status_code == 200 and not detected

    except requests.exceptions.Timeout:
        print(f"  结果: {RED}{BOLD}请求超时！{RESET}")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"  结果: {RED}{BOLD}连接被拒绝！{RESET}")
        print(f"  错误: {e}")
        return False
    except Exception as e:
        print(f"  结果: {RED}{BOLD}请求失败: {e}{RESET}")
        return False


def test_with_headers(url, site_name):
    """带伪装 Headers 的请求"""
    print(f"\n{YELLOW}[测试] 带 User-Agent 伪装请求 {site_name}{RESET}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        print(f"  状态码: {RED if resp.status_code != 200 else GREEN}{resp.status_code}{RESET}")
        content_len = len(resp.text)
        print(f"  响应长度: {content_len} 字符")

        blocked_signs = [
            "captcha", "challenge", "blocked", "access denied",
            "robot", "verify", "cf-browser", "distil",
            "perimeterx", "datadome"
        ]
        body_lower = resp.text[:3000].lower()
        detected = [s for s in blocked_signs if s in body_lower]

        if resp.status_code != 200:
            print(f"  结果: {RED}{BOLD}加了 Headers 也没用，照样被拦！{RESET}")
        elif detected:
            print(f"  结果: {RED}{BOLD}加了 Headers 还是触发了反爬！{RESET}")
            print(f"  检测到: {', '.join(detected)}")
        elif content_len < 5000:
            print(f"  结果: {RED}{BOLD}内容太短，大概率是反爬页面{RESET}")
        else:
            print(f"  结果: {YELLOW}拿到了一些内容，但可能不完整（JS渲染内容缺失）{RESET}")

        return resp.status_code == 200 and not detected

    except Exception as e:
        print(f"  结果: {RED}{BOLD}失败: {e}{RESET}")
        return False


def main():
    print(f"""
{BOLD}{CYAN}
 ╔══════════════════════════════════════════════════════════╗
 ║     传统爬虫 vs Bright Data MCP —— 反爬对比实测          ║
 ║                                                          ║
 ║  本脚本演示：用传统 Python 爬虫请求反爬严格的网站        ║
 ║  后续在 AnythingLLM 中用 Bright Data MCP 抓取同样的页面  ║
 ╚══════════════════════════════════════════════════════════╝
{RESET}""")

    # ========== 测试目标 ==========
    targets = [
        {
            "name": "Zillow（房产网站，反爬极严）",
            "url": "https://www.zillow.com/homedetails/104-69-88th-Ave-2R-Richmond-Hill-NY-11418/458388893_zpid/",
        },
        {
            "name": "Amazon（电商平台，反爬机制复杂）",
            "url": "https://www.amazon.com/dp/B0D1XD1ZV3",
        },
        {
            "name": "LinkedIn（社交平台，强制登录+反爬）",
            "url": "https://www.linkedin.com/company/openai/",
        },
    ]

    results = []

    for target in targets:
        divider(f"目标: {target['name']}")

        # 测试1: 裸请求
        ok1 = test_basic_request(target["url"], target["name"])
        time.sleep(1)

        # 测试2: 带Headers
        ok2 = test_with_headers(target["url"], target["name"])
        time.sleep(1)

        results.append({
            "site": target["name"],
            "basic": ok1,
            "with_headers": ok2,
        })

    # ========== 汇总 ==========
    divider("汇总：传统爬虫测试结果")

    print(f"  {'网站':<35} {'裸请求':<12} {'伪装Headers':<12}")
    print(f"  {'-'*59}")
    for r in results:
        s1 = f"{GREEN}成功{RESET}" if r["basic"] else f"{RED}失败{RESET}"
        s2 = f"{GREEN}成功{RESET}" if r["with_headers"] else f"{RED}失败{RESET}"
        print(f"  {r['site']:<30} {s1:<20} {s2:<20}")

    fail_count = sum(1 for r in results if not r["basic"] and not r["with_headers"])

    print(f"""
{BOLD}{RED}
  结论：{fail_count}/{len(results)} 个网站用传统爬虫方式无法正常获取数据！
{RESET}
{YELLOW}  这些网站的反爬手段包括：
  - Cloudflare / PerimeterX 等 WAF 防护
  - JavaScript 渲染（数据不在初始 HTML 中）
  - 验证码（CAPTCHA）
  - 设备指纹检测
  - IP 频率限制与封禁

  接下来，我们在 AnythingLLM 中用 Bright Data Web MCP 抓取同样的页面，
  看看效果有什么不同……
{RESET}""")


if __name__ == "__main__":
    main()
