import os
import sys
import time
from rag_engine import RAGEngine
from document_processor import DocumentProcessor

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.1')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')


class RAGBot:
    """Interactive RAG chatbot"""

    def __init__(self, top_k=3):
        self.engine = RAGEngine(
            llm_model=MODEL_NAME,
            embedding_model=EMBEDDING_MODEL,
            ollama_host=OLLAMA_HOST,
            top_k=top_k
        )
        self.index_loaded = False

    def connect(self, max_retries=30):
        """Connect to Ollama service"""
        print(f"Connecting to Ollama at {OLLAMA_HOST}...")

        for i in range(max_retries):
            try:
                # Test connection by getting stats
                self.engine.client.list()
                print(f"✓ Connected to Ollama")
                return True
            except Exception as e:
                if i < max_retries - 1:
                    print(f"Waiting... ({i+1}/{max_retries})")
                    time.sleep(2)
                else:
                    print(f"✗ Failed to connect: {e}")
                    return False

    def ask(self, question: str, show_context=False):
        """Ask a question using RAG"""
        if not self.index_loaded:
            print("\n⚠️  Warning: No documents indexed yet. Use /index to add documents.")
            print("Answering without context...\n")

        result = self.engine.query(
            question,
            show_context=show_context,
            show_stats=True
        )

        if result['answer']:
            print(f"\n🤖 Assistant: {result['answer']}")
        else:
            print("\n✗ Failed to generate answer")

        return result

    def index_directory(self, directory: str, pattern='*.txt'):
        """Index documents from a directory"""
        if not os.path.exists(directory):
            print(f"✗ Directory not found: {directory}")
            return False

        try:
            self.engine.index_from_directory(directory, pattern)
            self.index_loaded = True
            return True
        except Exception as e:
            print(f"✗ Error indexing documents: {e}")
            return False

    def save_index(self, filepath: str):
        """Save current index to file"""
        try:
            self.engine.save_index(filepath)
            return True
        except Exception as e:
            print(f"✗ Error saving index: {e}")
            return False

    def load_index(self, filepath: str):
        """Load index from file"""
        try:
            self.engine.load_index(filepath)
            self.index_loaded = True
            return True
        except Exception as e:
            print(f"✗ Error loading index: {e}")
            return False

    def clear_index(self):
        """Clear the current index"""
        self.engine.clear_index()
        self.index_loaded = False

    def show_stats(self):
        """Show RAG system statistics"""
        self.engine.print_stats()


def print_help():
    """Print help message"""
    print("\n" + "=" * 70)
    print("Available Commands:")
    print("=" * 70)
    print("  /help              - Show this help message")
    print("  /stats             - Show RAG system statistics")
    print("  /index <dir>       - Index documents from directory")
    print("  /index <dir> <pat> - Index documents matching pattern (e.g., *.md)")
    print("  /save <file>       - Save index to file")
    print("  /load <file>       - Load index from file")
    print("  /clear             - Clear current index")
    print("  /context on|off    - Toggle context display")
    print("  /topk <n>          - Set number of documents to retrieve (default: 3)")
    print("  /sample <dir>      - Create sample documents in directory")
    print("  /quit or /exit     - Exit the chatbot")
    print("=" * 70 + "\n")


def main():
    print("=" * 70)
    print("🤖 RAG Chatbot")
    print(f"LLM Model: {MODEL_NAME}")
    print(f"Embedding Model: {EMBEDDING_MODEL}")
    print(f"Host: {OLLAMA_HOST}")
    print("=" * 70)
    print("This bot uses Retrieval-Augmented Generation to answer questions")
    print("based on your indexed documents.")
    print("=" * 70)

    bot = RAGBot(top_k=3)

    if not bot.connect():
        sys.exit(1)

    print("\nType '/help' for available commands")
    print("=" * 70 + "\n")

    show_context = False

    while True:
        try:
            user_input = input("👤 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye! 👋")
            break

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith('/'):
            parts = user_input.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd in ['/quit', '/exit', '/q']:
                print("\nGoodbye! 👋")
                break

            elif cmd == '/help':
                print_help()

            elif cmd == '/stats':
                bot.show_stats()

            elif cmd == '/index':
                if len(parts) < 2:
                    print("Usage: /index <directory> [pattern]")
                    print("Example: /index ./documents")
                    print("Example: /index ./documents *.md")
                else:
                    directory = parts[1]
                    pattern = parts[2] if len(parts) > 2 else '*.txt'
                    bot.index_directory(directory, pattern)

            elif cmd == '/save':
                if len(parts) < 2:
                    print("Usage: /save <filepath>")
                    print("Example: /save my_index.pkl")
                else:
                    bot.save_index(parts[1])

            elif cmd == '/load':
                if len(parts) < 2:
                    print("Usage: /load <filepath>")
                    print("Example: /load my_index.pkl")
                else:
                    bot.load_index(parts[1])

            elif cmd == '/clear':
                bot.clear_index()
                print("✓ Index cleared")

            elif cmd == '/context':
                if len(parts) < 2:
                    print(f"Context display is currently: {'ON' if show_context else 'OFF'}")
                    print("Usage: /context on|off")
                else:
                    setting = parts[1].lower()
                    if setting == 'on':
                        show_context = True
                        print("✓ Context display enabled")
                    elif setting == 'off':
                        show_context = False
                        print("✓ Context display disabled")
                    else:
                        print("Usage: /context on|off")

            elif cmd == '/topk':
                if len(parts) < 2:
                    print(f"Current top-k: {bot.engine.top_k}")
                    print("Usage: /topk <number>")
                else:
                    try:
                        k = int(parts[1])
                        if k > 0:
                            bot.engine.top_k = k
                            print(f"✓ Top-k set to {k}")
                        else:
                            print("✗ Top-k must be positive")
                    except ValueError:
                        print("✗ Invalid number")

            elif cmd == '/sample':
                if len(parts) < 2:
                    print("Usage: /sample <directory>")
                    print("Example: /sample ./sample_docs")
                else:
                    processor = DocumentProcessor()
                    processor.create_sample_documents(parts[1])

            else:
                print(f"Unknown command: {cmd}")
                print("Type '/help' for available commands")

            continue

        # Ask question with RAG
        bot.ask(user_input, show_context=show_context)


if __name__ == "__main__":
    main()
