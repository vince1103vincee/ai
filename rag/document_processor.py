import os
from typing import List, Dict
from pathlib import Path

class DocumentProcessor:
    """Process documents for RAG system - chunking and loading"""

    def __init__(self, chunk_size=500, chunk_overlap=50):
        """
        Initialize document processor

        Args:
            chunk_size: Target size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into chunks with overlap

        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk

        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        if metadata is None:
            metadata = {}

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings
                sentence_end = max(
                    text.rfind('. ', start, end),
                    text.rfind('! ', start, end),
                    text.rfind('? ', start, end),
                    text.rfind('\n', start, end)
                )

                if sentence_end > start:
                    end = sentence_end + 1

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_metadata = metadata.copy()
                chunk_metadata['chunk_index'] = len(chunks)
                chunk_metadata['start_char'] = start
                chunk_metadata['end_char'] = end

                chunks.append({
                    'text': chunk_text,
                    'metadata': chunk_metadata
                })

            # Move to next chunk with overlap
            start = end - self.chunk_overlap

        return chunks

    def load_text_file(self, filepath: str) -> str:
        """Load text from a file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def load_directory(self, directory: str, pattern='*.txt') -> List[Dict]:
        """
        Load all files matching pattern from directory

        Args:
            directory: Directory path
            pattern: File pattern (e.g., '*.txt', '*.md')

        Returns:
            List of dicts with 'text' and 'metadata' keys
        """
        documents = []
        dir_path = Path(directory)

        for filepath in dir_path.glob(pattern):
            if filepath.is_file():
                try:
                    text = self.load_text_file(str(filepath))
                    metadata = {
                        'source': str(filepath),
                        'filename': filepath.name
                    }
                    documents.append({
                        'text': text,
                        'metadata': metadata
                    })
                    print(f"  Loaded: {filepath.name}")
                except Exception as e:
                    print(f"  Error loading {filepath.name}: {e}")

        return documents

    def process_documents(self, documents: List[Dict]) -> tuple[List[str], List[Dict]]:
        """
        Process documents into chunks

        Args:
            documents: List of dicts with 'text' and 'metadata' keys

        Returns:
            Tuple of (chunk_texts, chunk_metadata)
        """
        all_chunks = []

        for doc in documents:
            text = doc['text']
            metadata = doc.get('metadata', {})

            chunks = self.chunk_text(text, metadata)
            all_chunks.extend(chunks)

        # Separate texts and metadata
        chunk_texts = [chunk['text'] for chunk in all_chunks]
        chunk_metadata = [chunk['metadata'] for chunk in all_chunks]

        return chunk_texts, chunk_metadata

    def load_and_process_directory(self, directory: str, pattern='*.txt') -> tuple[List[str], List[Dict]]:
        """
        Convenience method to load and process all files in a directory

        Args:
            directory: Directory path
            pattern: File pattern

        Returns:
            Tuple of (chunk_texts, chunk_metadata)
        """
        print(f"Loading documents from {directory} (pattern: {pattern})")
        documents = self.load_directory(directory, pattern)
        print(f"Found {len(documents)} documents")

        print(f"Processing documents into chunks...")
        chunk_texts, chunk_metadata = self.process_documents(documents)
        print(f"Created {len(chunk_texts)} chunks")

        return chunk_texts, chunk_metadata

    def create_sample_documents(self, output_dir: str):
        """Create sample documents for testing"""
        os.makedirs(output_dir, exist_ok=True)

        samples = {
            'python_basics.txt': """
Python is a high-level, interpreted programming language known for its simplicity and readability.
It was created by Guido van Rossum and first released in 1991. Python emphasizes code readability
with its use of significant indentation.

Python supports multiple programming paradigms, including procedural, object-oriented, and functional
programming. It has a comprehensive standard library that supports many common programming tasks.

Common use cases for Python include web development, data analysis, artificial intelligence,
scientific computing, and automation. Popular frameworks include Django and Flask for web development,
NumPy and Pandas for data analysis, and TensorFlow and PyTorch for machine learning.
""",
            'machine_learning.txt': """
Machine Learning is a subset of artificial intelligence that enables systems to learn and improve
from experience without being explicitly programmed. It focuses on developing computer programs
that can access data and use it to learn for themselves.

There are three main types of machine learning: supervised learning, unsupervised learning, and
reinforcement learning. Supervised learning uses labeled data to train models. Unsupervised learning
finds patterns in unlabeled data. Reinforcement learning learns through trial and error.

Popular machine learning algorithms include linear regression, decision trees, random forests,
support vector machines, and neural networks. Deep learning, a subset of machine learning, uses
neural networks with multiple layers to process complex patterns.
""",
            'rag_systems.txt': """
Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with
text generation. It enhances large language models by providing them with relevant context
from a knowledge base before generating responses.

A RAG system typically consists of three main components: a document processor that chunks
and prepares documents, a vector store that stores and retrieves embeddings, and a generation
model that produces answers based on retrieved context.

RAG systems are particularly useful for question-answering systems, chatbots, and applications
that require up-to-date or domain-specific knowledge. They allow models to access information
beyond their training data, reducing hallucinations and improving factual accuracy.
"""
        }

        for filename, content in samples.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content.strip())

        print(f"✓ Created {len(samples)} sample documents in {output_dir}")
