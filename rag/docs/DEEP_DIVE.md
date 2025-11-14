# RAG System Deep Dive - How Everything Works

## Part 1: Vector Embeddings - The Magic Behind RAG

### 1.1 What Happens in `_get_embedding()`

```python
def _get_embedding(self, text: str) -> np.ndarray:
    response = self.client.embeddings(
        model=self.embedding_model,  # nomic-embed-text
        prompt=text
    )
    return np.array(response['embedding'])
```

**Step-by-step breakdown:**

1. **Input**: Text string (e.g., "Python is a programming language")

2. **API Call**: Sends text to Ollama's `nomic-embed-text` model
   ```
   POST http://localhost:11434/api/embeddings
   {
     "model": "nomic-embed-text",
     "prompt": "Python is a programming language"
   }
   ```

3. **Model Processing**:
   - Neural network analyzes the text
   - Captures semantic meaning (not just keywords!)
   - Outputs a 768-dimensional vector

4. **Output**: NumPy array of 768 floating-point numbers
   ```python
   array([0.234, -0.456, 0.123, ..., 0.891])  # 768 numbers total
   ```

**Why 768 dimensions?**
- Each dimension captures a different semantic feature
- Dimension 1 might relate to "programming concepts"
- Dimension 2 might relate to "languages"
- Dimension 3 might relate to "technical vs non-technical"
- etc.

**Key insight**: Similar meanings → Similar vectors!

```python
# Example vectors (simplified to 5D for illustration)
"Python programming"     → [ 0.9,  0.8,  0.1, -0.2,  0.5]
"Coding in Python"       → [ 0.85, 0.75, 0.15, -0.15, 0.48]  # Very close!
"Cat videos"             → [-0.3, -0.2,  0.9,  0.7, -0.4]   # Very different!
```

---

### 1.2 Cosine Similarity - Measuring "Closeness"

```python
def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**What this does**: Measures the angle between two vectors

**Visual explanation:**

```
Vector Space (simplified 2D):

        Programming Concepts (dimension 1)
              ↑
              |     vector_a (Python)
              |    /
              |   / 15° angle
              |  /____vector_b (Java)
              | /
              |/________________→ Web Development (dimension 2)

Small angle = Similar meaning = High cosine similarity (close to 1.0)
```

**Mathematical breakdown:**

```python
# Given two vectors:
a = [0.9, 0.8, 0.1]  # "Python programming"
b = [0.85, 0.75, 0.15]  # "Coding in Python"

# 1. Dot product (how much vectors "agree")
dot_product = (0.9 * 0.85) + (0.8 * 0.75) + (0.1 * 0.15)
            = 0.765 + 0.6 + 0.015
            = 1.38

# 2. Vector magnitudes (lengths)
||a|| = sqrt(0.9² + 0.8² + 0.1²) = sqrt(0.81 + 0.64 + 0.01) = 1.208
||b|| = sqrt(0.85² + 0.75² + 0.15²) = sqrt(0.7225 + 0.5625 + 0.0225) = 1.147

# 3. Cosine similarity
similarity = 1.38 / (1.208 * 1.147) = 1.38 / 1.386 = 0.996

# Result: 0.996 means VERY similar! (1.0 = identical)
```

**Similarity scale:**
- 1.0 = Identical meaning
- 0.9 - 0.99 = Very similar
- 0.7 - 0.89 = Related
- 0.5 - 0.69 = Somewhat related
- 0.0 - 0.49 = Different topics
- -1.0 = Opposite meaning (rare)

---

### 1.3 The `add_documents()` Flow

```python
def add_documents(self, documents: List[str], metadata: List[Dict] = None):
    for i, (doc, meta) in enumerate(zip(documents, metadata)):
        embedding = self._get_embedding(doc)  # Convert to vector
        if embedding is not None:
            self.documents.append(doc)        # Store original text
            self.embeddings.append(embedding) # Store vector
            self.metadata.append(meta)        # Store metadata
```

**What happens when you index documents:**

```
Documents (text):
├─ "Python is a programming language"
├─ "Machine learning uses algorithms"
└─ "Django is a web framework"

    ↓ _get_embedding() for each ↓

Parallel arrays stored in memory:
┌────────────────────────────────────────────────────────┐
│ self.documents = [                                     │
│   "Python is a programming language",                  │
│   "Machine learning uses algorithms",                  │
│   "Django is a web framework"                          │
│ ]                                                      │
├────────────────────────────────────────────────────────┤
│ self.embeddings = [                                    │
│   [0.23, -0.45, 0.12, ..., 0.89],  # 768 numbers      │
│   [0.67, 0.34, -0.12, ..., 0.45],  # 768 numbers      │
│   [0.12, 0.78, 0.23, ..., 0.34]    # 768 numbers      │
│ ]                                                      │
├────────────────────────────────────────────────────────┤
│ self.metadata = [                                      │
│   {"filename": "python.txt", "chunk_index": 0},        │
│   {"filename": "ml.txt", "chunk_index": 0},            │
│   {"filename": "django.txt", "chunk_index": 0}         │
│ ]                                                      │
└────────────────────────────────────────────────────────┘

All arrays use same index:
  documents[0] ↔ embeddings[0] ↔ metadata[0]
```

**Performance note**: Progress printed every 10 documents
```python
if (i + 1) % 10 == 0:
    print(f"  Processed {i + 1}/{len(documents)} documents")
```
This prevents console spam for large document sets.

---

### 1.4 The `search()` Flow - The Heart of Retrieval

```python
def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float, Dict]]:
    # 1. Convert query to vector
    query_embedding = self._get_embedding(query)

    # 2. Compare with all stored embeddings
    similarities = []
    for i, doc_embedding in enumerate(self.embeddings):
        similarity = self._cosine_similarity(query_embedding, doc_embedding)
        similarities.append((self.documents[i], similarity, self.metadata[i]))

    # 3. Sort by similarity (highest first)
    similarities.sort(key=lambda x: x[1], reverse=True)

    # 4. Return top K results
    return similarities[:top_k]
```

**Detailed walkthrough with example:**

```
User query: "Tell me about Python web frameworks"

Step 1: Convert query to embedding
────────────────────────────────────────────────
query = "Tell me about Python web frameworks"
        ↓ _get_embedding() ↓
query_embedding = [0.15, 0.72, 0.31, ..., 0.42]  # 768 numbers

Step 2: Compare with all documents
────────────────────────────────────────────────
Stored documents (from earlier example):
[0] "Python is a programming language"    embedding: [0.23, -0.45, ...]
[1] "Machine learning uses algorithms"    embedding: [0.67, 0.34, ...]
[2] "Django is a web framework"           embedding: [0.12, 0.78, ...]

Calculate similarity for each:
  cosine_similarity(query_embedding, embedding[0]) = 0.73
  cosine_similarity(query_embedding, embedding[1]) = 0.45
  cosine_similarity(query_embedding, embedding[2]) = 0.91  ← Highest!

Create list:
similarities = [
  ("Python is a programming language", 0.73, {metadata}),
  ("Machine learning uses algorithms", 0.45, {metadata}),
  ("Django is a web framework", 0.91, {metadata})
]

Step 3: Sort by similarity (descending)
────────────────────────────────────────────────
similarities.sort(key=lambda x: x[1], reverse=True)

Result after sorting:
[
  ("Django is a web framework", 0.91, {...}),           ← Best match!
  ("Python is a programming language", 0.73, {...}),    ← 2nd best
  ("Machine learning uses algorithms", 0.45, {...})     ← 3rd
]

Step 4: Return top_k=3 results
────────────────────────────────────────────────
return similarities[:3]  # All 3 in this case

Final output:
[
  ("Django is a web framework", 0.91, {"filename": "django.txt", ...}),
  ("Python is a programming language", 0.73, {"filename": "python.txt", ...}),
  ("Machine learning uses algorithms", 0.45, {"filename": "ml.txt", ...})
]
```

**Why this works**:
- Query asked about "Python web frameworks"
- "Django" document has both "Python" and "web framework"
- Embedding captures this semantic overlap
- Cosine similarity of 0.91 indicates strong match!

---

### 1.5 Save & Load - Persistence

```python
def save(self, filepath: str):
    data = {
        'documents': self.documents,
        'embeddings': self.embeddings,
        'metadata': self.metadata,
        'embedding_model': self.embedding_model
    }
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)
```

**Why this is important:**

```
Without save/load:
├─ Every restart: Re-process all documents
├─ 100 documents × 0.5s per embedding = 50 seconds
└─ Waste of time and API calls!

With save/load:
├─ First time: 50 seconds to build index
├─ Save to file: 1 second
├─ Next time: Load from file: 0.1 seconds
└─ 500x faster! ⚡
```

**What's stored in pickle file:**

```python
{
  'documents': ["text1", "text2", ...],           # Original texts
  'embeddings': [[0.1, ...], [0.2, ...], ...],   # Pre-computed vectors!
  'metadata': [{...}, {...}, ...],                # File info, chunks
  'embedding_model': 'nomic-embed-text'           # Which model was used
}
```

**Security note**: Pickle files can execute code when loaded. Only load files you created!

---

## Part 2: Document Chunking - Breaking It Down

### 2.1 Why Chunk?

**Problem**: Large documents are hard to search effectively

```
Example document (5000 characters):
┌─────────────────────────────────────────────────┐
│ Introduction to Python... (500 chars)           │ ← Relevant!
│ History of Python... (500 chars)                │
│ Python syntax basics... (500 chars)             │ ← Relevant!
│ Advanced decorators... (500 chars)              │
│ Networking in Python... (500 chars)             │
│ Database connections... (500 chars)             │
│ Web frameworks... (500 chars)                   │ ← Relevant!
│ Testing strategies... (500 chars)               │
│ Deployment pipelines... (500 chars)             │
│ Conclusion... (500 chars)                       │
└─────────────────────────────────────────────────┘

If we embed entire document:
  - Embedding averages ALL topics
  - "Python web frameworks" query matches weakly (0.45)
  - Loses precision!

If we chunk into 10 pieces:
  - Each chunk has focused topic
  - "Web frameworks" chunk matches strongly (0.91)
  - High precision! ✓
```

---

### 2.2 The Chunking Algorithm

```python
def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + self.chunk_size  # Default: 500 chars

        # Try to break at sentence boundaries
        if end < len(text):
            sentence_end = max(
                text.rfind('. ', start, end),
                text.rfind('! ', start, end),
                text.rfind('? ', start, end),
                text.rfind('\n', start, end)
            )

            if sentence_end > start:
                end = sentence_end + 1

        chunk_text = text[start:end].strip()
        chunks.append({'text': chunk_text, 'metadata': {...}})

        # Move to next chunk with overlap
        start = end - self.chunk_overlap  # Default: 50 chars

    return chunks
```

**Visual example:**

```
Original text (simplified):
"Python is great. It was created in 1991. Python is used for web dev. Django is popular."

chunk_size = 30, chunk_overlap = 10

Chunk 1 (chars 0-30):
├─ "Python is great. It was cre"
└─ Problem: Cuts mid-sentence! ❌

Smart boundary detection:
├─ Look for '. ' before position 30
├─ Found at position 18: "Python is great."
└─ Use that instead! ✓

Result:
┌────────────────────────────────────────────────┐
│ Chunk 0: "Python is great."                   │
│   start: 0, end: 18                            │
├────────────────────────────────────────────────┤
│ Chunk 1: "It was created in 1991."            │
│   start: 8 (18-10 overlap), end: 39           │
│   Overlap: "t."                                │
├────────────────────────────────────────────────┤
│ Chunk 2: "Python is used for web dev."        │
│   start: 29, end: 67                           │
│   Overlap: "1991. "                            │
└────────────────────────────────────────────────┘

Overlap ensures context isn't lost at boundaries!
```

---

(Continued in next response due to length...)
