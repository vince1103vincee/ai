# MCP Demo - API Data Assistant with Ollama

通过自然语言查询 API 数据的 MCP 服务器

## 功能

- 🤖 自然语言查询产品、用户、订单等数据
- 🦙 使用 Ollama 本地 LLM
- 🛠️ 14 个数据查询工具
- 💬 多轮对话支持

## 项目结构

```
mcp-demo/
├── api_client/          # API 客户端
├── ollama_client/       # Ollama 客户端
├── mcp_server/          # MCP 服务器
├── config/              # 配置
├── main.py             # 主入口
└── requirements.txt    # 依赖
```

## 快速开始

### 1. 启动依赖服务

```bash
# API Server (需要 Flask 运行)
cd ../api-server-mcp-demo
python app.py

# Ollama (在另一个终端)
ollama serve
ollama pull llama2
```

### 2. 安装并运行

```bash
cd mcp-demo
pip install -r requirements.txt
python main.py
```

### 3. 开始查询

```
You: 有哪些 Apple 产品？
You: iPhone 的库存是多少？
You: 用户 u001 买过什么？
```

## 可用命令

- `help` - 帮助
- `status` - 检查状态
- `tools` - 列出工具
- `history` - 对话历史
- `clear` - 清除历史
- `exit` - 退出

## 配置

编辑 `config/settings.py` 中的硬编码值：

```python
API_SERVER_URL = 'http://localhost:8000'
OLLAMA_BASE_URL = 'http://localhost:11434'
OLLAMA_MODEL = 'llama2'
OLLAMA_TEMPERATURE = 0.7
```

## 可用工具

**产品**: get_all_products, get_product, search_products_by_name, get_products_by_category, get_products_by_brand, get_inventory

**用户**: get_all_users, get_user, search_users_by_name

**订单**: get_all_orders, get_order, get_user_orders

**系统**: get_stats, api_health_check