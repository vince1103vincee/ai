# 快速开始

## 前置条件

1. **API Server** 运行中
   ```bash
   cd ../api-server-mcp-demo
   python app.py
   ```

2. **Ollama** 运行中
   ```bash
   ollama serve
   ollama pull llama2
   ```

## 运行

```bash
pip install -r requirements.txt
python main.py
```

## 示例

```
You: 有哪些产品？
Assistant: 根据数据库...

You: Apple 的产品有哪些？
Assistant: Apple 产品包括...

You: 用户 u001 的订单
Assistant: 用户 u001 的订单...
```

## 命令

- `help` - 帮助
- `status` - 状态
- `tools` - 工具列表
- `history` - 历史
- `clear` - 清除
- `exit` - 退出
