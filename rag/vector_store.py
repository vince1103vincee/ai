import numpy as np
import pickle
import os
from typing import List, Tuple, Dict
import ollama

class VectorStore:
    """Simple vector store using cosine similarity for document retrieval"""

    def __init__(self, embedding_model='nomic-embed-text', ollama_host='http://localhost:11434'):
        self.embedding_model = embedding_model
        self.ollama_host = ollama_host
        self.client = ollama.Client(host=ollama_host)
        self.documents = []  # List of document texts
        self.embeddings = []  # List of embeddings
        self.metadata = []  # List of metadata dicts

    def _get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a text using Ollama"""
        try:
            response = self.client.embeddings(
                model=self.embedding_model,
                prompt=text
            )
            return np.array(response['embedding'])
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None

    def add_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector store"""
        if metadata is None:
            metadata = [{}] * len(documents)

        print(f"Adding {len(documents)} documents to vector store...")

        for i, (doc, meta) in enumerate(zip(documents, metadata)):
            embedding = self._get_embedding(doc)
            if embedding is not None:
                self.documents.append(doc)
                self.embeddings.append(embedding)
                self.metadata.append(meta)

            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1}/{len(documents)} documents")

        print(f"✓ Added {len(self.documents)} documents successfully")

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float, Dict]]:
        """
        Search for most similar documents to query
        Returns list of (document, similarity_score, metadata) tuples
        """
        if not self.documents:
            return []

        query_embedding = self._get_embedding(query)
        if query_embedding is None:
            return []

        # Calculate similarities
        similarities = []
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            similarities.append((self.documents[i], similarity, self.metadata[i]))

        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def save(self, filepath: str):
        """Save vector store to disk"""
        data = {
            'documents': self.documents,
            'embeddings': self.embeddings,
            'metadata': self.metadata,
            'embedding_model': self.embedding_model
        }

        with open(filepath, 'wb') as f:
            pickle.dump(data, f)

        print(f"✓ Vector store saved to {filepath}")

    def load(self, filepath: str):
        """Load vector store from disk"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Vector store file not found: {filepath}")

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        self.documents = data['documents']
        self.embeddings = data['embeddings']
        self.metadata = data['metadata']
        self.embedding_model = data['embedding_model']

        print(f"✓ Vector store loaded from {filepath}")
        print(f"  Documents: {len(self.documents)}")
        print(f"  Embedding model: {self.embedding_model}")

    def clear(self):
        """Clear all documents from vector store"""
        self.documents = []
        self.embeddings = []
        self.metadata = []
        print("✓ Vector store cleared")

    def stats(self):
        """Get statistics about the vector store"""
        return {
            'num_documents': len(self.documents),
            'embedding_model': self.embedding_model,
            'embedding_dim': len(self.embeddings[0]) if self.embeddings else 0
        }