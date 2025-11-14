# RAG System Deep Dive - Part 2

## Part 2 (Continued): Document Processing

### 2.3 Metadata Tracking

```python
chunk_metadata = metadata.copy()
chunk_metadata['chunk_index'] = len(chunks)
chunk_metadata['start_char'] = start
chunk_metadata['end_char'] = end

chunks.append({
    'text': chunk_text,
    'metadata': chunk_metadata
})
```

**Why track metadata?**

```python
# Example metadata structure:
{
    'source': '/Users/you/docs/python_guide.txt',
    'filename': 'python_guide.txt',
    'chunk_index': 2,           # This is the 3rd chunk (0-indexed)
    'start_char': 1000,         # Starts at character 1000
    'end_char': 1500            # Ends at character 1500
}
```

**Use cases:**

1. **Citation**: "Found in python_guide.txt, chunk 2"
2. **Debugging**: "Why did this chunk match?"
3. **Re-ranking**: Prefer chunks from certain files
4. **Deduplication**: Skip similar chunks from same source

---

### 2.4 Loading from Directories

```python
def load_directory(self, directory: str, pattern='*.txt') -> List[Dict]:
    documents = []
    dir_path = Path(directory)

    for filepath in dir_path.glob(pattern):
        if filepath.is_file():
            text = self.load_text_file(str(filepath))
            metadata = {
                'source': str(filepath),
                'filename': filepath.name
            }
            documents.append({'text': text, 'metadata': metadata})

    return documents
```

**Flow diagram:**

```
Directory: ./docs/
├─ python.txt
├─ django.md
└─ flask.txt

Call: load_directory('./docs', '*.txt')
  ↓
Glob matches: python.txt, flask.txt (django.md skipped - not .txt)
  ↓
For each file:
  1. Read content
  2. Create metadata
  3. Add to documents list
  ↓
Return:
[
  {
    'text': "Python is...",
    'metadata': {'source': './docs/python.txt', 'filename': 'python.txt'}
  },
  {
    'text': "Flask is...",
    'metadata': {'source': './docs/flask.txt', 'filename': 'flask.txt'}
  }
]
```

---

### 2.5 Complete Document Processing Pipeline

```python
def load_and_process_directory(self, directory: str, pattern='*.txt'):
    # Step 1: Load files
    documents = self.load_directory(directory, pattern)

    # Step 2: Chunk each document
    chunk_texts, chunk_metadata = self.process_documents(documents)

    return chunk_texts, chunk_metadata
```

**End-to-end example:**

```
Input: Directory with 2 files
┌─────────────────────────────────────┐
│ docs/python.txt (1000 chars):       │
│ "Python is a programming language..." │
│                                     │
│ docs/ml.txt (800 chars):            │
│ "Machine learning uses algorithms..." │
└─────────────────────────────────────┘

Step 1: load_directory()
├─ Load python.txt → doc1
└─ Load ml.txt → doc2

Step 2: process_documents()
├─ Chunk doc1 (1000 chars, size=500, overlap=50)
│   ├─ chunk_0: chars 0-500
│   └─ chunk_1: chars 450-1000
│
└─ Chunk doc2 (800 chars)
    ├─ chunk_0: chars 0-500
    └─ chunk_1: chars 450-800

Output:
chunk_texts = [
  "Python is a programming language...",  # doc1, chunk 0
  "...created in 1991. Python is used...", # doc1, chunk 1
  "Machine learning uses algorithms...",   # doc2, chunk 0
  "...neural networks and deep learning."  # doc2, chunk 1
]

chunk_metadata = [
  {'source': 'docs/python.txt', 'filename': 'python.txt', 'chunk_index': 0},
  {'source': 'docs/python.txt', 'filename': 'python.txt', 'chunk_index': 1},
  {'source': 'docs/ml.txt', 'filename': 'ml.txt', 'chunk_index': 0},
  {'source': 'docs/ml.txt', 'filename': 'ml.txt', 'chunk_index': 1}
]
```

---

## Part 3: RAG Engine - Bringing It All Together

### 3.1 The RAG Query Flow

```python
def query(self, question: str, show_context=False, show_stats=True) -> Dict:
    # Step 1: Retrieve relevant documents
    context_docs = self.retrieve(question)

    # Step 2: Create prompt with context
    prompt = self._create_rag_prompt(question, context_docs)

    # Step 3: Generate answer
    response = self.client.chat(
        model=self.llm_model,
        messages=[{'role': 'user', 'content': prompt}]
    )

    return {
        'answer': response['message']['content'],
        'context': context_docs,
        'response_data': response
    }
```

**Complete flow visualization:**

```
User Question: "How does Django work?"
        │
        ↓
┌───────────────────────────────────────────────────────┐
│ STEP 1: RETRIEVAL (retrieve method)                  │
├───────────────────────────────────────────────────────┤
│                                                       │
│ 1a. Convert question to embedding                    │
│     "How does Django work?"                           │
│     → [0.15, 0.72, 0.31, ..., 0.42]                  │
│                                                       │
│ 1b. Search vector store                              │
│     Compare with all stored document embeddings      │
│                                                       │
│ 1c. Top 3 results (top_k=3):                         │
│     ┌───────────────────────────────────────┐        │
│     │ [1] "Django is a Python web            │        │
│     │      framework..." (score: 0.93)       │        │
│     │                                        │        │
│     │ [2] "Django uses MTV pattern..."       │        │
│     │      (score: 0.87)                     │        │
│     │                                        │        │
│     │ [3] "Python frameworks like Django..." │        │
│     │      (score: 0.79)                     │        │
│     └───────────────────────────────────────┘        │
│                                                       │
└───────────────────────────────────────────────────────┘
        │
        ↓
┌───────────────────────────────────────────────────────┐
│ STEP 2: PROMPT CONSTRUCTION                          │
├───────────────────────────────────────────────────────┤
│                                                       │
│ Build context-aware prompt:                          │
│                                                       │
│ ╔═══════════════════════════════════════════════╗    │
│ ║ You are a helpful assistant. Use the          ║    │
│ ║ following context to answer the question.     ║    │
│ ║                                               ║    │
│ ║ Context:                                      ║    │
│ ║ [Document 1 - django.txt (relevance: 0.93)]:  ║    │
│ ║ Django is a Python web framework...           ║    │
│ ║                                               ║    │
│ ║ [Document 2 - patterns.txt (relevance: 0.87)]:║    │
│ ║ Django uses MTV pattern...                    ║    │
│ ║                                               ║    │
│ ║ [Document 3 - python.txt (relevance: 0.79)]:  ║    │
│ ║ Python frameworks like Django...              ║    │
│ ║                                               ║    │
│ ║ Question: How does Django work?               ║    │
│ ║                                               ║    │
│ ║ Answer:                                       ║    │
│ ╚═══════════════════════════════════════════════╝    │
│                                                       │
└───────────────────────────────────────────────────────┘
        │
        ↓
┌───────────────────────────────────────────────────────┐
│ STEP 3: LLM GENERATION                               │
├───────────────────────────────────────────────────────┤
│                                                       │
│ Send to llama3.1:                                    │
│   model: "llama3.1"                                  │
│   messages: [{'role': 'user', 'content': prompt}]    │
│                                                       │
│ LLM reads context + question → Generates answer      │
│                                                       │
│ Response:                                            │
│ "Django works as a Python web framework that         │
│  follows the MTV (Model-Template-View) pattern.      │
│  Based on the provided context..."                   │
│                                                       │
└───────────────────────────────────────────────────────┘
        │
        ↓
    Return to user
```

---

### 3.2 Prompt Engineering - The Secret Sauce

Let's examine the prompt construction in detail:

```python
def _create_rag_prompt(self, query: str, context_docs: List[Tuple[str, float, Dict]]) -> str:
    if not context_docs:
        # Fallback: no context available
        return f"""You are a helpful assistant. Answer the following question:

Question: {query}

Answer:"""

    # Build context from retrieved documents
    context_parts = []
    for i, (doc, score, metadata) in enumerate(context_docs, 1):
        source = metadata.get('filename', metadata.get('source', 'Unknown'))
        context_parts.append(f"[Document {i} - {source} (relevance: {score:.2f})]:\n{doc}")

    context = "\n\n".join(context_parts)

    # Create prompt with instructions + context + question
    prompt = f"""You are a helpful assistant. Use the following context to answer the question. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {query}

Answer:"""

    return prompt
```

**Why this prompt structure works:**

1. **Clear Instructions**: "Use the following context..."
   - Tells LLM where to look
   - Reduces hallucinations

2. **Numbered Documents**: "[Document 1]", "[Document 2]"
   - Easy to reference
   - Allows citation

3. **Relevance Scores**: "(relevance: 0.93)"
   - Helps LLM weight information
   - More relevant = more important

4. **Escape Hatch**: "If answer cannot be found, say so"
   - Prevents making up answers
   - Improves honesty

**Example of final prompt sent to LLM:**

```
You are a helpful assistant. Use the following context to answer the question. If the answer cannot be found in the context, say so.

Context:
[Document 1 - django.txt (relevance: 0.93)]:
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

[Document 2 - patterns.txt (relevance: 0.87)]:
Django follows the Model-Template-View (MTV) architectural pattern. The Model defines the data structure, the Template handles the presentation layer, and the View contains the business logic that processes requests and returns responses.

[Document 3 - python_frameworks.txt (relevance: 0.79)]:
Python frameworks like Django and Flask provide tools and libraries for building web applications. Django is known as a "batteries-included" framework, offering many built-in features out of the box.

Question: How does Django work?

Answer:
```

**LLM then generates** (example):

```
Django works by following the Model-Template-View (MTV) architectural pattern. As a high-level Python web framework, it handles much of the complexity of web development automatically. The Model layer defines your data structure, the Template layer manages how data is presented to users, and the View layer contains the business logic that processes incoming requests and returns appropriate responses. Django is known as a "batteries-included" framework, meaning it provides many built-in features that help developers build applications rapidly without reinventing common functionality.
```

**Notice**:
- ✓ Answer is grounded in provided context
- ✓ Combines information from multiple documents
- ✓ Uses proper terminology from the docs
- ✓ Doesn't add information not in context

---

### 3.3 Index Management

```python
def index_from_directory(self, directory: str, pattern='*.txt',
                         chunk_size=500, chunk_overlap=50):
    # Create document processor
    processor = DocumentProcessor(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Load and chunk documents
    chunk_texts, chunk_metadata = processor.load_and_process_directory(
        directory, pattern
    )

    # Add to vector store (convert to embeddings)
    self.vector_store.add_documents(chunk_texts, chunk_metadata)
```

**Complete indexing flow:**

```
Directory: ./docs/
├─ python.txt (2KB)
├─ django.txt (3KB)
└─ ml.txt (2.5KB)

Call: index_from_directory('./docs', '*.txt', chunk_size=500, chunk_overlap=50)
        │
        ↓
┌─────────────────────────────────────────┐
│ 1. Create DocumentProcessor             │
│    chunk_size=500, overlap=50           │
└─────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────┐
│ 2. Load files (load_and_process)        │
│    ├─ Read python.txt                   │
│    ├─ Read django.txt                   │
│    └─ Read ml.txt                       │
└─────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────┐
│ 3. Chunk documents                      │
│    ├─ python.txt → 4 chunks             │
│    ├─ django.txt → 6 chunks             │
│    └─ ml.txt → 5 chunks                 │
│    Total: 15 chunks                     │
└─────────────────────────────────────────┘
        │
        ↓
┌─────────────────────────────────────────┐
│ 4. Generate embeddings                  │
│    For each chunk (15 total):           │
│    ├─ Call nomic-embed-text API         │
│    ├─ Get 768-dim vector                │
│    └─ Store in vector_store             │
│                                         │
│    Progress: "Processed 10/15..."      │
└─────────────────────────────────────────┘
        │
        ↓
    ✓ Index ready!
    15 chunks embedded and searchable
```

---

(Continued in DEEP_DIVE_PART3.md...)
