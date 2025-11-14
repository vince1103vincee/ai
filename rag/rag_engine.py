import ollama
from typing import List, Dict, Tuple
from vector_store import VectorStore
from document_processor import DocumentProcessor

class RAGEngine:
    """RAG Engine that combines retrieval and generation"""

    def __init__(
        self,
        llm_model='llama3.1',
        embedding_model='nomic-embed-text',
        ollama_host='http://localhost:11434',
        top_k=3
    ):
        """
        Initialize RAG Engine

        Args:
            llm_model: Model to use for generation
            embedding_model: Model to use for embeddings
            ollama_host: Ollama server host
            top_k: Number of documents to retrieve
        """
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.ollama_host = ollama_host
        self.top_k = top_k

        # Initialize components
        self.vector_store = VectorStore(
            embedding_model=embedding_model,
            ollama_host=ollama_host
        )
        self.client = ollama.Client(host=ollama_host)

        # Statistics
        self.total_queries = 0
        self.total_tokens = 0

    def index_documents(self, documents: List[str], metadata: List[Dict] = None):
        """Add documents to the vector store"""
        self.vector_store.add_documents(documents, metadata)

    def index_from_directory(
        self,
        directory: str,
        pattern='*.txt',
        chunk_size=500,
        chunk_overlap=50
    ):
        """
        Load and index documents from a directory

        Args:
            directory: Directory containing documents
            pattern: File pattern to match
            chunk_size: Size of document chunks
            chunk_overlap: Overlap between chunks
        """
        processor = DocumentProcessor(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        chunk_texts, chunk_metadata = processor.load_and_process_directory(
            directory, pattern
        )

        self.vector_store.add_documents(chunk_texts, chunk_metadata)

    def retrieve(self, query: str) -> List[Tuple[str, float, Dict]]:
        """
        Retrieve relevant documents for a query

        Returns:
            List of (document, score, metadata) tuples
        """
        return self.vector_store.search(query, top_k=self.top_k)

    def _create_rag_prompt(self, query: str, context_docs: List[Tuple[str, float, Dict]]) -> str:
        """Create a prompt with retrieved context"""
        if not context_docs:
            return f"""You are a helpful assistant. Answer the following question:

Question: {query}

Answer:"""

        # Build context from retrieved documents
        context_parts = []
        for i, (doc, score, metadata) in enumerate(context_docs, 1):
            source = metadata.get('filename', metadata.get('source', 'Unknown'))
            context_parts.append(f"[Document {i} - {source} (relevance: {score:.2f})]:\n{doc}")

        context = "\n\n".join(context_parts)

        prompt = f"""You are a helpful assistant. Use the following context to answer the question. If the answer cannot be found in the context, say so.

Context:
{context}

Question: {query}

Answer:"""

        return prompt

    def query(
        self,
        question: str,
        show_context=False,
        show_stats=True
    ) -> Dict:
        """
        Query the RAG system

        Args:
            question: User's question
            show_context: Whether to print retrieved context
            show_stats: Whether to print statistics

        Returns:
            Dict with 'answer', 'context', 'response_data'
        """
        self.total_queries += 1

        # Retrieve relevant documents
        context_docs = self.retrieve(question)

        if show_context and context_docs:
            print("\n" + "─" * 70)
            print("📚 Retrieved Context:")
            print("─" * 70)
            for i, (doc, score, metadata) in enumerate(context_docs, 1):
                source = metadata.get('filename', metadata.get('source', 'Unknown'))
                print(f"\n[{i}] {source} (score: {score:.3f})")
                print(f"{doc[:200]}..." if len(doc) > 200 else doc)
            print("─" * 70)

        # Create prompt with context
        prompt = self._create_rag_prompt(question, context_docs)

        # Generate answer
        try:
            response = self.client.chat(
                model=self.llm_model,
                messages=[{'role': 'user', 'content': prompt}]
            )

            answer = response['message']['content']

            # Update statistics
            if 'eval_count' in response:
                self.total_tokens += response['eval_count']

            if show_stats:
                self._print_stats(response, len(context_docs))

            return {
                'answer': answer,
                'context': context_docs,
                'response_data': response
            }

        except Exception as e:
            print(f"\n✗ Error generating response: {e}")
            return {
                'answer': None,
                'context': context_docs,
                'response_data': None
            }

    def _print_stats(self, response: Dict, num_context_docs: int):
        """Print query statistics"""
        print("\n" + "─" * 70)
        print("📊 Query Statistics:")
        print("─" * 70)

        print(f"Context documents retrieved: {num_context_docs}")

        if 'prompt_eval_count' in response:
            print(f"Prompt tokens: {response['prompt_eval_count']}")

        if 'eval_count' in response:
            print(f"Response tokens: {response['eval_count']}")

        if 'eval_duration' in response:
            duration_sec = response['eval_duration'] / 1_000_000_000
            print(f"Generation time: {duration_sec:.2f}s")

            if 'eval_count' in response:
                tokens_per_sec = response['eval_count'] / duration_sec
                print(f"Generation speed: {tokens_per_sec:.2f} tokens/sec")

        print("─" * 70)

    def save_index(self, filepath: str):
        """Save the vector store index"""
        self.vector_store.save(filepath)

    def load_index(self, filepath: str):
        """Load a vector store index"""
        self.vector_store.load(filepath)

    def clear_index(self):
        """Clear all indexed documents"""
        self.vector_store.clear()

    def get_stats(self) -> Dict:
        """Get RAG engine statistics"""
        vs_stats = self.vector_store.stats()
        return {
            'total_queries': self.total_queries,
            'total_tokens_generated': self.total_tokens,
            'num_indexed_documents': vs_stats['num_documents'],
            'embedding_model': vs_stats['embedding_model'],
            'llm_model': self.llm_model,
            'top_k': self.top_k
        }

    def print_stats(self):
        """Print RAG engine statistics"""
        stats = self.get_stats()

        print("\n" + "=" * 70)
        print("📈 RAG Engine Statistics")
        print("=" * 70)
        print(f"Indexed documents: {stats['num_indexed_documents']}")
        print(f"Total queries: {stats['total_queries']}")
        print(f"Total tokens generated: {stats['total_tokens_generated']}")
        print(f"LLM model: {stats['llm_model']}")
        print(f"Embedding model: {stats['embedding_model']}")
        print(f"Top-K retrieval: {stats['top_k']}")
        print("=" * 70 + "\n")
