#!/usr/bin/env python3
"""
Example usage of the RAG system

This script demonstrates how to use the RAG components programmatically.
"""

from rag_engine import RAGEngine
from document_processor import DocumentProcessor
import os

def example_basic_usage():
    """Basic RAG usage example"""
    print("=" * 70)
    print("Example 1: Basic RAG Usage")
    print("=" * 70)

    # Initialize RAG engine
    rag = RAGEngine(
        llm_model='llama3.1',
        embedding_model='nomic-embed-text',
        top_k=3
    )

    # Create sample documents
    print("\n1. Creating sample documents...")
    processor = DocumentProcessor()
    sample_dir = './example_docs'
    processor.create_sample_documents(sample_dir)

    # Index documents
    print("\n2. Indexing documents...")
    rag.index_from_directory(sample_dir, pattern='*.txt')

    # Query the system
    print("\n3. Querying the system...")
    questions = [
        "What is Python?",
        "What are the types of machine learning?",
        "How does RAG work?"
    ]

    for question in questions:
        print(f"\n{'='*70}")
        print(f"Q: {question}")
        print(f"{'='*70}")

        result = rag.query(question, show_context=True, show_stats=False)

        if result['answer']:
            print(f"\nA: {result['answer']}")

    # Show statistics
    print("\n4. Statistics:")
    rag.print_stats()

    # Save index
    print("\n5. Saving index...")
    rag.save_index('example_index.pkl')

    # Cleanup
    print("\n6. Cleanup...")
    import shutil
    if os.path.exists(sample_dir):
        shutil.rmtree(sample_dir)
    print(f"✓ Removed {sample_dir}")


def example_custom_documents():
    """Example with custom document processing"""
    print("\n" + "=" * 70)
    print("Example 2: Custom Document Processing")
    print("=" * 70)

    # Initialize with custom settings
    rag = RAGEngine(
        llm_model='llama3.1',
        embedding_model='nomic-embed-text',
        top_k=2  # Retrieve top 2 documents
    )

    # Create custom processor with smaller chunks
    processor = DocumentProcessor(
        chunk_size=300,  # Smaller chunks
        chunk_overlap=30
    )

    # Custom documents
    documents = [
        {
            'text': """
            The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.
            It is named after the engineer Gustave Eiffel, whose company designed and built the tower.
            Constructed from 1887 to 1889, it was initially criticized by some of France's leading
            artists and intellectuals for its design, but it has become a global cultural icon of
            France and one of the most recognizable structures in the world.
            """,
            'metadata': {'source': 'eiffel_tower_facts', 'category': 'landmarks'}
        },
        {
            'text': """
            The Great Wall of China is a series of fortifications made of stone, brick, tamped earth,
            wood, and other materials. It was built along an east-to-west line across the historical
            northern borders of China to protect the Chinese states and empires against raids and
            invasions. Several walls were built from as early as the 7th century BC, with selective
            stretches later joined together by Qin Shi Huang.
            """,
            'metadata': {'source': 'great_wall_facts', 'category': 'landmarks'}
        }
    ]

    # Process documents into chunks
    print("\n1. Processing documents...")
    chunk_texts, chunk_metadata = processor.process_documents(documents)
    print(f"Created {len(chunk_texts)} chunks")

    # Index the chunks
    print("\n2. Indexing chunks...")
    rag.index_documents(chunk_texts, chunk_metadata)

    # Query
    print("\n3. Querying...")
    result = rag.query(
        "Who built the Eiffel Tower?",
        show_context=True,
        show_stats=True
    )

    if result['answer']:
        print(f"\nAnswer: {result['answer']}")


def example_load_existing_index():
    """Example of loading a saved index"""
    print("\n" + "=" * 70)
    print("Example 3: Loading Existing Index")
    print("=" * 70)

    # Check if example index exists
    if not os.path.exists('example_index.pkl'):
        print("\n⚠️  No saved index found. Run example_basic_usage() first.")
        return

    # Initialize RAG engine
    rag = RAGEngine()

    # Load saved index
    print("\n1. Loading saved index...")
    rag.load_index('example_index.pkl')

    # Query immediately (no need to re-index)
    print("\n2. Querying loaded index...")
    result = rag.query(
        "Tell me about Python frameworks",
        show_context=False,
        show_stats=True
    )

    if result['answer']:
        print(f"\nAnswer: {result['answer']}")


if __name__ == "__main__":
    import sys

    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                     RAG System Examples                              ║
╚══════════════════════════════════════════════════════════════════════╝

Available examples:
  1 - Basic RAG usage with sample documents
  2 - Custom document processing
  3 - Load existing index

""")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("Select example (1-3) or 'all': ").strip()

    if choice == '1':
        example_basic_usage()
    elif choice == '2':
        example_custom_documents()
    elif choice == '3':
        example_load_existing_index()
    elif choice.lower() == 'all':
        example_basic_usage()
        example_custom_documents()
        example_load_existing_index()
    else:
        print("Invalid choice. Use 1, 2, 3, or 'all'")
