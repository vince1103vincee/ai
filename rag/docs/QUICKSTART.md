# RAG System - Quick Start Guide

## Method 1: Interactive RAG Bot (Easiest)

### Step 1: Start the bot
```bash
cd /Users/tingchu.chen/code/ai/rag
python rag_bot.py
```

### Step 2: Create sample documents (for testing)
```
/sample ./my_docs
```

### Step 3: Index the documents
```
/index ./my_docs
```

### Step 4: Ask questions!
```
What is Python?
What are the types of machine learning?
How does RAG work?
```

### Step 5: View retrieved context (optional)
```
/context on
What is Python used for?
```

### Step 6: Save your index (so you don't have to re-index next time)
```
/save my_index.pkl
```

### Next time: Load the saved index
```
/load my_index.pkl
```

---

## Method 2: Index Your Own Documents

### Prepare your documents
1. Create a directory with your text files:
```bash
mkdir ~/my_knowledge
echo "Your content here..." > ~/my_knowledge/doc1.txt
echo "More content..." > ~/my_knowledge/doc2.txt
```

2. Start the bot and index:
```
python rag_bot.py
/index ~/my_knowledge
```

3. For markdown files:
```
/index ~/my_knowledge *.md
```

---

## Method 3: Use RAG Programmatically (Python Script)

### Example script:
```python
from rag_engine import RAGEngine

# Initialize
rag = RAGEngine()

# Index documents
rag.index_from_directory('./my_docs', pattern='*.txt')

# Query
result = rag.query("What is Python?", show_context=True)
print(result['answer'])

# Save for later
rag.save_index('my_index.pkl')
```

---

## All Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/help` | Show help | `/help` |
| `/sample <dir>` | Create sample docs | `/sample ./test_docs` |
| `/index <dir> [pattern]` | Index documents | `/index ./docs *.md` |
| `/save <file>` | Save index | `/save my_index.pkl` |
| `/load <file>` | Load index | `/load my_index.pkl` |
| `/clear` | Clear index | `/clear` |
| `/context on\|off` | Toggle context display | `/context on` |
| `/topk <n>` | Set retrieval count | `/topk 5` |
| `/stats` | Show statistics | `/stats` |
| `/quit` | Exit | `/quit` |

---

## Tips for Best Results

1. **Chunk Size**: Default is 500 characters. Good for most use cases.

2. **Top-K**: Default is 3 documents. Increase for more context:
   ```
   /topk 5
   ```

3. **File Organization**: Group related documents in directories:
   ```
   /index ./python_docs *.md
   /index ./ml_docs *.txt
   ```

4. **Save Your Index**: Always save after indexing to avoid re-processing:
   ```
   /save project_knowledge.pkl
   ```

5. **Context Display**: Turn on to debug what's being retrieved:
   ```
   /context on
   ```

---

## Common Workflows

### Workflow 1: Quick Test
```bash
cd rag
python rag_bot.py
/sample ./test
/index ./test
What is RAG?
/quit
```

### Workflow 2: Index Project Documentation
```bash
python rag_bot.py
/index ~/projects/myproject/docs *.md
/save myproject_index.pkl
Tell me about the authentication system
/quit
```

### Workflow 3: Daily Use (with saved index)
```bash
python rag_bot.py
/load myproject_index.pkl
How do I configure the database?
/quit
```

---

## Troubleshooting

**Q: "No documents indexed" warning**
- Run `/index <directory>` first to add documents

**Q: Indexing is slow**
- This is normal for large document sets
- Save the index with `/save` to avoid re-indexing

**Q: Poor answers**
- Try `/topk 5` to retrieve more documents
- Check `/context on` to see what's being retrieved
- Improve document quality and organization

**Q: "Error getting embedding"**
- Make sure `nomic-embed-text` is installed:
  ```bash
  ollama pull nomic-embed-text
  ```
