# RAG System - Retrieval-Augmented Generation

一個簡單但功能完整的 RAG（檢索增強生成）系統，使用 Ollama 作為後端。

## 📁 目錄結構

```
rag/
├── rag_bot.py              # 🎯 主程序 - 互動式聊天機器人
├── rag_engine.py           # 核心引擎 - RAG 邏輯實現
├── vector_store.py         # 向量存儲 - 文檔向量化和檢索
├── document_processor.py   # 文檔處理 - 文本分塊和載入
├── config.py               # 配置文件
├── __init__.py             # Python 包初始化
│
├── data/                   # 📂 數據文件
│   └── demo_docs/          # 演示用文檔
│       ├── python_basics.txt
│       ├── machine_learning.txt
│       ├── rag_systems.txt
│       └── wovenid.txt
│
├── docs/                   # 📚 文檔
│   ├── QUICKSTART.md       # 快速開始指南
│   ├── DEEP_DIVE.md        # 深入解析 (Part 1)
│   ├── DEEP_DIVE_PART2.md  # 深入解析 (Part 2)
│   ├── DEEP_DIVE_PART3.md  # 深入解析 (Part 3)
│   ├── chunk_logic_explained.md      # 分塊邏輯詳解
│   ├── index_flow_diagram.md         # 索引流程圖
│   └── index_flow_diagram.html       # 互動式流程圖
│
├── examples/               # 💡 示例代碼
│   └── example_usage.py    # 程序化使用示例
│
├── demos/                  # 🎨 演示腳本
│   ├── chunk_demo.py       # 分塊邏輯詳細演示
│   └── chunk_simple_demo.py # 分塊邏輯簡化演示
│
└── scripts/                # 🔧 工具腳本
    ├── setup.sh            # 環境設置腳本
    ├── demo.sh             # 演示腳本
    ├── verify_k8s_models.sh # K8s 模型驗證
    └── test_k8s_connection.py # K8s 連接測試
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
# 創建虛擬環境
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
pip install ollama numpy
```

### 2. 啟動 Ollama 服務

確保 Ollama 正在運行並已安裝所需模型：

```bash
# 拉取 LLM 模型
ollama pull llama3.1

# 拉取 Embedding 模型
ollama pull nomic-embed-text
```

### 3. 運行聊天機器人

```bash
python rag_bot.py
```

### 4. 索引文檔

在聊天機器人中執行：

```
/index ./data/demo_docs
```

### 5. 開始提問

```
What is Python?
What are the types of machine learning?
How does RAG work?
```

## 📖 主要功能

### 核心命令

| 命令 | 說明 | 示例 |
|------|------|------|
| `/help` | 顯示幫助信息 | `/help` |
| `/index <dir>` | 索引目錄中的文檔 | `/index ./data/demo_docs` |
| `/index <dir> <pattern>` | 索引符合模式的文檔 | `/index ./docs *.md` |
| `/save <file>` | 保存索引到文件 | `/save my_index.pkl` |
| `/load <file>` | 從文件載入索引 | `/load my_index.pkl` |
| `/clear` | 清除當前索引 | `/clear` |
| `/stats` | 顯示統計信息 | `/stats` |
| `/context on\|off` | 切換上下文顯示 | `/context on` |
| `/topk <n>` | 設置檢索數量 | `/topk 5` |
| `/quit` | 退出程序 | `/quit` |

## 🔧 核心組件

### 1. RAGBot (rag_bot.py)

互動式聊天機器人，提供命令行界面。

**主要功能**：
- 文檔索引管理
- 問答查詢
- 索引保存/載入

### 2. RAGEngine (rag_engine.py)

RAG 系統的核心引擎。

**主要功能**：
- 文檔索引
- 向量檢索
- 答案生成
- 統計追蹤

**關鍵參數**：
```python
RAGEngine(
    llm_model='llama3.1',           # 生成模型
    embedding_model='nomic-embed-text',  # 嵌入模型
    ollama_host='http://localhost:11434',
    top_k=3  # 檢索文檔數量
)
```

### 3. VectorStore (vector_store.py)

向量存儲和檢索系統。

**主要功能**：
- 文檔向量化
- 餘弦相似度搜索
- 索引持久化

**數據結構**：
```python
self.documents   # 原始文本列表
self.embeddings  # 向量列表（NumPy 數組）
self.metadata    # 元數據列表
```

### 4. DocumentProcessor (document_processor.py)

文檔處理和分塊。

**主要功能**：
- 文件載入
- 文本分塊（智能句子邊界檢測）
- 元數據管理

**分塊參數**：
```python
DocumentProcessor(
    chunk_size=500,      # 每塊字元數
    chunk_overlap=50     # 塊間重疊字元數
)
```

## 📊 工作流程

```
1. 載入文檔
   ↓
2. 文本分塊（500 字元/塊，50 字元重疊）
   ↓
3. 向量化（Ollama nomic-embed-text）
   ↓
4. 存儲（內存中的向量存儲）
   ↓
5. 查詢時：
   - 查詢向量化
   - 餘弦相似度搜索
   - 檢索 top-k 文檔
   - 生成答案（Ollama llama3.1）
```

## 🎯 使用示例

### 程序化使用

查看 `examples/example_usage.py`：

```python
from rag_engine import RAGEngine

# 初始化
rag = RAGEngine()

# 索引文檔
rag.index_from_directory('./data/demo_docs', pattern='*.txt')

# 查詢
result = rag.query("What is Python?", show_context=True)
print(result['answer'])

# 保存索引
rag.save_index('my_index.pkl')
```

### 演示腳本

**分塊邏輯演示**：
```bash
# 簡化演示
python demos/chunk_simple_demo.py

# 詳細演示（需要修復無限循環）
# python demos/chunk_demo.py 1
```

## 📚 深入學習

### 文檔資源

1. **快速開始**: `docs/QUICKSTART.md`
2. **深入解析**:
   - `docs/DEEP_DIVE.md` (基礎概念)
   - `docs/DEEP_DIVE_PART2.md` (索引流程)
   - `docs/DEEP_DIVE_PART3.md` (查詢流程)
3. **分塊邏輯**: `docs/chunk_logic_explained.md`
4. **流程圖**:
   - `docs/index_flow_diagram.md` (Markdown)
   - `docs/index_flow_diagram.html` (互動式，在瀏覽器中打開)

### 互動式流程圖

在瀏覽器中打開：
```bash
open docs/index_flow_diagram.html
```

## 🔍 技術細節

### 向量化

- **模型**: nomic-embed-text
- **維度**: 768
- **相似度**: 餘弦相似度

### 文本分塊

- **大小**: 500 字元（可配置）
- **重疊**: 50 字元（可配置）
- **邊界檢測**: 句子邊界優先（句號、問號、驚嘆號、換行）

### 生成模型

- **模型**: llama3.1
- **上下文**: 檢索到的 top-k 文檔
- **提示**: 基於上下文的結構化提示

## ⚙️ 配置

環境變量（在 `config.py` 或命令行設置）：

```bash
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=llama3.1
export EMBEDDING_MODEL=nomic-embed-text
```

## 🐛 故障排除

### Ollama 連接失敗

```bash
# 檢查 Ollama 是否運行
curl http://localhost:11434/api/tags

# 重啟 Ollama
ollama serve
```

### 模型未找到

```bash
# 拉取所需模型
ollama pull llama3.1
ollama pull nomic-embed-text

# 驗證模型
ollama list
```

### K8s 環境

如果在 Kubernetes 環境中運行：

```bash
# 驗證 K8s 模型
bash scripts/verify_k8s_models.sh

# 測試連接
python scripts/test_k8s_connection.py
```

## 📝 開發

### 添加新功能

1. 修改核心模塊：`rag_engine.py`, `vector_store.py`, `document_processor.py`
2. 更新 CLI：`rag_bot.py`
3. 添加測試：在 `examples/` 或 `demos/` 中
4. 更新文檔：在 `docs/` 中

### 運行示例

```bash
# 基礎示例
python examples/example_usage.py

# 分塊演示
python demos/chunk_simple_demo.py

# 完整演示
bash scripts/demo.sh
```

## 💡 使用技巧

1. **Chunk Size**: 較小的塊（200-500 字元）適合具體事實，較大的塊（500-1000 字元）保留更多上下文
2. **Top-K**: 從 3-5 個文檔開始，更多不一定更好，可能稀釋相關性
3. **文檔組織**: 將相關文檔放在不同目錄中便於索引
4. **保存索引**: 建立索引後保存，避免每次重啟都重新嵌入
5. **上下文顯示**: 使用 `/context on` 查看檢索到的文檔以便調試

## 📄 授權

MIT License

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！

---

**快速鏈接**：
- 📖 [快速開始](docs/QUICKSTART.md)
- 🔬 [深入解析](docs/DEEP_DIVE.md)
- 🎨 [互動式流程圖](docs/index_flow_diagram.html)
- 💡 [使用示例](examples/example_usage.py)
