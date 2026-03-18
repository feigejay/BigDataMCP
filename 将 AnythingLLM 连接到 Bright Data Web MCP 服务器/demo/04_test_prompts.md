# AnythingLLM + Bright Data MCP 测试提示词

> 使用方式：在 AnythingLLM 聊天框中先输入 `@agent` 启动 Agent 模式，
> 然后复制下面的提示词发送。

---

## 场景一：GitHub 开源项目调研（免费版）

### Prompt（直接复制）

```
帮我在 Google 上搜索"2026年3月最值得关注的AI开源项目推荐"，
从搜索结果中挑出最相关的 3 篇文章，
逐个抓取它们的完整正文内容。

然后基于这些文章的内容，帮我整理一份"本周AI开源项目推荐清单"。
每个项目包含：
1. 项目名称
2. GitHub 地址（如果文章提到了的话）
3. 一句话介绍它是干什么的
4. 适合什么人使用

最后用表格形式输出。
```

### 预期行为
- Agent 调用 `search_engine` 搜索 Google
- Agent 调用 `scrape_as_markdown` 抓取 3 篇文章
- Agent 整理输出表格

### 录制要点
- 重点展示 Agent 自主决策过程（选择工具 → 执行 → 解析 → 总结）
- 如果搜索结果不理想，展示 Agent 如何调整策略

---

## 场景二：反爬硬骨头实测（对比传统爬虫）

### 前置演示
先运行 `01_traditional_scraper_fail.py` 展示传统爬虫失败画面。

### Prompt —— Zillow 房源抓取（直接复制）

```
请帮我抓取这个 Zillow 房源页面的详细信息：
https://www.zillow.com/homedetails/104-69-88th-Ave-2R-Richmond-Hill-NY-11418/458388893_zpid/

我想知道：
1. 房屋价格
2. 地址
3. 面积（平方英尺）
4. 卧室和卫生间数量
5. 房源描述
6. 上市时间

请用清晰的列表格式输出。
```

### 备选 Prompt —— Amazon 商品抓取

```
帮我抓取这个 Amazon 商品页面的信息：
https://www.amazon.com/dp/B0D1XD1ZV3

告诉我：
- 商品名称
- 当前价格
- 用户评分和评论数
- 主要卖点（前3条 bullet points）
```

### 预期行为
- 免费版：Agent 调用 `scrape_as_markdown`，抓取网页转 Markdown，从中提取信息
- Pro 版：Agent 自动选择 `web_data_zillow_properties_listing` 或 `web_data_amazon_product`，直接返回结构化数据

### 录制要点
- 重点对比：传统爬虫 403/验证码 vs MCP 直接出数据
- 如果用 Pro 版，强调 Agent 自动选择了"专用工具"而不是通用的 scrape

---

## 场景三：跨平台信息聚合分析（综合能力展示）

### Prompt（直接复制）

```
我想深入了解 MCP（Model Context Protocol）这个技术的最新发展情况。
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

报告控制在 500 字以内，重点突出核心观点。
```

### 预期行为
- Agent 做 2 次搜索（英文 + 中文）
- Agent 抓取 3 个不同网页
- Agent 综合分析并输出结构化报告

### 录制要点
- 重点展示多轮工具调用的自主串联能力
- 注意 Agent 在中英文搜索之间的策略切换
- 最终报告的质量（是否引用了实际抓取到的内容）

---

## 附加场景（可选，用于补充录制素材）

### Prompt A：实时新闻追踪

```
@agent
帮我搜索今天（2026年3月）最重要的 3 条 AI 行业新闻，
抓取新闻原文，然后用 100 字以内概括每条新闻的核心要点。
```

### Prompt B：技术文档速读

```
@agent
请帮我抓取这个页面的内容：
https://modelcontextprotocol.io/introduction

然后用中文帮我总结这篇文档的核心要点，
重点回答：MCP 是什么、解决什么问题、怎么用。
控制在 300 字以内。
```

### Prompt C：多商品价格对比（Pro 版）

```
@agent
我想买一副无线降噪耳机，请帮我从 Amazon 上获取以下 3 款耳机的信息：
- Sony WH-1000XM5: https://www.amazon.com/dp/B0BT35JDRQ
- Apple AirPods Max: https://www.amazon.com/dp/B0D1XD1ZV3
- Bose QuietComfort Ultra: https://www.amazon.com/dp/B0CCZ1L489

用表格对比：名称、价格、评分、评论数量。
最后给出你的购买建议。
```

---

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Agent 不调用 MCP 工具 | 没有进入 Agent 模式 | 聊天框先输入 `@agent` |
| 提示 "No MCP tools available" | 配置文件未正确设置 | 运行 `03_generate_mcp_config.py` 重新配置 |
| MCP 工具调用超时 | 首次运行 npx 需要下载包 | 先在终端手动运行一次 `npx -y @brightdata/mcp` |
| 只看到 2 个工具 | 未开启 Pro 模式 | 在配置文件中添加 `"PRO_MODE": "true"` |
| 抓取结果为空 | Token 无效或额度用完 | 检查 Bright Data 控制台余额和 Token 状态 |
