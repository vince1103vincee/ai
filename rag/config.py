import os

# Ollama Configuration
# Default to K8s service if in cluster, otherwise localhost
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

# Model Configuration
LLM_MODEL = os.getenv('MODEL_NAME', 'llama3.1')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')

# RAG Configuration
DEFAULT_CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '500'))
DEFAULT_CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '50'))
DEFAULT_TOP_K = int(os.getenv('TOP_K', '3'))

print(f"RAG Config:")
print(f"  Ollama Host: {OLLAMA_HOST}")
print(f"  LLM Model: {LLM_MODEL}")
print(f"  Embedding Model: {EMBEDDING_MODEL}")
