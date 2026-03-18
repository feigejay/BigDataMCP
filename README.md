# 让 AI 学会"上网" AnythingLLM + Bright Data Web MCP 实战

---

**体验地址：[AnythingLLM + Bright Data Web MCP,现在注册即送25美金](https://www.bright.cn/blog/ai/anythingllm-with-web-mcp/?utm_source=brand&utm_campaign=brnd-mkt_cn_csdn_manong202603&promo=brd25)**



## 前言：我们要解决什么问题？

如果你经常使用 AI 工具，一定遇到过这两个痛点：

**痛点一：AI 无法获取实时数据**

你问 ChatGPT："今天 GitHub 上最火的开源项目是什么？" 它会告诉你——"我无法访问实时网页。"

**痛点二：自己写爬虫太痛苦**

你自己写爬虫去抓数据，requests 发出去，要么 403，要么跳验证码，要么直接封 IP。稍微复杂点的网站，光对付反爬就够你折腾一下午。

**今天介绍的方案，一次性解决这两个问题。**

---

## 方案介绍

### AnythingLLM 是什么？

AnythingLLM 是一个"万能 AI 前端"。它能接入几乎所有大模型：

- GPT、Claude、Gemini、DeepSeek
- 用 Ollama 跑本地模型
- 上传文档聊天、RAG 向量检索
- **原生支持 MCP 协议**

### Bright Data Web MCP 是什么？

做爬虫的朋友对 Bright Data 不陌生——全球 1.5 亿 IP 池，专门干代理和反反爬的老牌厂商。

他们推出了一个开源的 MCP 服务器，把网页数据采集能力封装成 AI 可以直接调用的工具：

| 版本   | 可用工具                           | 说明                                             |
| ------ | ---------------------------------- | ------------------------------------------------ |
| 免费版 | search_engine + scrape_as_markdown | 搜索引擎 + 网页抓取转 Markdown                   |
| Pro 版 | 60+ 专用工具                       | Amazon、YouTube、LinkedIn 等平台直接提结构化数据 |

---

## 连接步骤：从零到跑通（约5分钟）

### Step 1：安装 AnythingLLM

1. 访问 [anythingllm.com](https://anythingllm.com/download) 下载桌面版
2. 双击安装，一路下一步
3. 有 NVIDIA 显卡的话，建议安装 GPU 加速依赖

### Step 2：选择大模型

AnythingLLM 支持多种 LLM Provider：

- **Gemini**（推荐）：免费额度高，响应快
- **Ollama + 本地模型**：完全不花钱
- **GPT-4 / Claude**：也完全支持

> 关键点：不管你选哪个模型，后面接的 MCP 工具都一样。换模型不用重新配 MCP。

### Step 3：获取 Bright Data API Token

1. 访问 [brightdata.com](https://www.bright.cn/) 注册账号（新用户有免费额度）
2. 登录控制台，找到 MCP 引导入口
3. 按提示生成 API Token
4. **保存好这个 Token，后面要用**

### Step 4：在 AnythingLLM 中配置 MCP

1. 打开 AnythingLLM → 左下角齿轮 → **Agent Skills**
2. 找到配置文件 `anythingllm_mcp_servers.json`：
   - **Windows**：`C:\Users\你的用户名\AppData\Roaming\anythingllm-desktop\storage\plugins\`
   - **Mac**：`~/Library/Application Support/anythingllm-desktop/storage/plugins/`
3. 用编辑器打开，修改为：

```json
{
  "mcpServers": {
    "bright-data": {
      "command": "npx",
      "args": ["-y", "@brightdata/mcp"],
      "env": {
        "API_TOKEN": "替换成你的Bright Data API Token"
      }
    }
  }
}
```

> 如果要用 Pro 模式，加一行 `"PRO_MODE": "true"`

4. 保存文件，回到 AnythingLLM → Agent Skills → 点击 **Refresh**
5. 看到 **Bright Data** 出现，展开可查看所有可用工具

**连接完成！**

---

## 实战场景演示

### 场景一：GitHub 开源项目调研

在聊天框输入 `@agent` 启动 Agent，然后发送：

```
@agent
帮我在 Google 上搜索"2026年3月最值得关注的AI开源项目"，
挑出搜索结果中最相关的3篇文章，
然后逐一抓取这些文章的完整内容，
帮我总结出一份"本周AI开源项目推荐清单"，
包含项目名、GitHub地址、一句话描述、适合什么人用。
```

**执行过程**：

1. Agent 调用 `search_engine` 做 Google 搜索
2. 获取搜索结果后，自主调用 `scrape_as_markdown` 抓取每篇文章
3. 最终输出结构化的推荐清单

> 这两个工具是免费版就有的，不花一分钱。以前要手动一篇篇看或写脚本，现在一句话搞定。

---

### 场景二：反爬硬骨头实测

**传统爬虫的困境**：

```python
import requests
r = requests.get("https://www.zillow.com/homedetails/...")
print(r.status_code)  # 403
```

用 requests 直接请求 Zillow，403。加了 headers 和代理？照样被拦。

**用 Bright Data MCP**：

```
@agent
请帮我抓取这个 Zillow 房源页面的完整信息：
https://www.zillow.com/homedetails/104-69-88th-Ave-2R-Richmond-Hill-NY-11418/458388893_zpid/

告诉我这套房子的价格、面积、卧室卫生间数量、地址，以及房源描述。
```

同样的 URL，通过 Bright Data MCP 去抓，直接成功。

- **Pro 模式**：自动选用 `web_data_zillow_properties_listing` 专用工具，直接返回结构化 JSON
- **免费模式**：用 `scrape_as_markdown` 拿到 Markdown 内容，AI 自动提取信息

**原理**：Bright Data 的 Web Unlocker 自动处理验证码、JS 渲染、IP 轮换。你不用管反爬细节，直接拿数据。

---

### 场景三：跨平台信息聚合分析

```
@agent
我想深入了解 MCP（Model Context Protocol）的最新发展。请帮我完成：

1. 在 Google 搜索"MCP protocol 2026 latest update"
2. 从搜索结果中挑2篇最有价值的文章，抓取全文
3. 再搜索"MCP protocol 社区评价 优缺点"
4. 抓取其中1篇中文社区讨论的内容

最后给我一份综合分析报告：MCP 目前发展到什么阶段，
社区的主要正面和负面评价分别是什么，
你认为它未来的发展趋势如何。
```

**执行过程**：

- 两轮搜索（英文 + 中文关键词）
- 逐个抓取文章
- Agent 自主串联工具调用
- 输出有理有据的分析报告

手动做这件事要一两个小时，现在一个 Prompt 两三分钟搞定。

---

## 竞品对比

| 维度           | Bright Data MCP         | Firecrawl | Crawl4AI   |
| -------------- | ----------------------- | --------- | ---------- |
| 反爬能力       | 企业级，1.5亿IP池       | 有限      | 基本没有   |
| 免费可用工具   | 搜索 + 网页抓取         | 有限额度  | 开源免费   |
| 专用数据采集器 | 60+（Amazon/YouTube等） | 无        | 无         |
| JS 动态渲染    | 内置 Browser API        | 支持      | 部分支持   |
| MCP 接入方式   | stdio / SSE / HTTP      | stdio     | 需自行封装 |
| 上手门槛       | 低（npm一行命令）       | 低        | 中等       |
| 适合谁         | 要稳定抓数据的人        | 轻量抓取  | 学习研究   |

**结论**：

- **Crawl4AI**：完全免费开源，适合学习和简单场景，但遇到反爬要自己处理
- **Firecrawl**：轻量好用，但没有按平台定制的结构化采集器
- **Bright Data MCP**：杀手锏是 **反爬能力** 和 **60多个垂直平台专用采集器**

---

## 优缺点总结

### 优点

1. **接入简单**：改一个 JSON 文件就接通，全程不超过5分钟
2. **免费版够用**：search_engine + scrape_as_markdown 覆盖80%日常需求
3. **反爬能力强**：Zillow、Amazon 这些硬骨头都能啃
4. **模型随便换**：今天用 Gemini，明天换 GPT，MCP 配置一字不改

### 槽点

1. **Pro 模式要花钱**：60 多个高级工具按量计费，重度使用注意成本
2. **需要 Node.js 环境**：不玩前端的同学要先装一下
3. **Agent 模式才能用**：必须输 `@agent` 才能调 MCP 工具，普通聊天模式不行

---

## 快速参考

### 工具链接

- AnythingLLM 下载：https://anythingllm.com/download
- Bright Data 注册：https://www.bright.cn/
- Bright Data Web MCP（npm）：https://www.npmjs.com/package/@brightdata/mcp

### 配置文件路径

**Windows**：

```
C:\Users\你的用户名\AppData\Roaming\anythingllm-desktop\storage\plugins\anythingllm_mcp_servers.json
```

**Mac**：

```
~/Library/Application Support/anythingllm-desktop/storage/plugins/anythingllm_mcp_servers.json
```

### JSON 配置模板（复制即用）

```json
{
  "mcpServers": {
    "bright-data": {
      "command": "npx",
      "args": ["-y", "@brightdata/mcp"],
      "env": {
        "API_TOKEN": "替换成你的Token"
      }
    }
  }
}
```

---

## 总结

如果你经常需要让 AI 帮你做信息搜集和数据抓取，这套方案的性价比非常高：

- **免费版**：日常够用
- **Pro 版**：真正的"AI + 爬虫"终极形态

最关键的是，它让**完全不懂爬虫技术的人**也能拿到以前只有专业爬虫工程师才能搞到的数据。

让 AI 学会"上网"，从此实时数据随便拿。