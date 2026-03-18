# AnythingLLM + Bright Data Web MCP 演示代码

配合视频脚本 `视频脚本_AnythingLLM_BrightData_MCP测评.md` 使用。

## 文件说明

| 文件 | 用途 | 何时使用 |
|------|------|----------|
| `01_traditional_scraper_fail.py` | 传统爬虫失败对比演示 | 视频片头录制 |
| `02_env_check.py` | 环境一键检查 | 录制前预检 |
| `03_generate_mcp_config.py` | MCP 配置文件生成器 | 安装配置环节 |
| `04_test_prompts.md` | AnythingLLM 测试提示词 | 实战演示环节 |
| `05_mcp_standalone_test.py` | MCP 独立连接测试 | 排查问题时 |
| `06_demo_runner.py` | 全流程引导器（导演提词） | 正式录制时 |

## 快速开始

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 环境检查
python 02_env_check.py

# 3. 生成 MCP 配置（交互式）
python 03_generate_mcp_config.py

# 4. 正式录制（全流程引导）
python 06_demo_runner.py
```

## 前置条件

- Python 3.8+
- Node.js 18+
- AnythingLLM 桌面版
- Bright Data 账号 + API Token
