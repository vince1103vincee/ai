import ollama
import os
import sys
import time
from datetime import datetime

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.1')

class ChatBot:
    def __init__(self):
        self.client = None
        self.conversation_history = []
        self.total_tokens = 0
        self.total_duration = 0
        
    def connect(self, max_retries=30):
        """Connect to Ollama service"""
        print(f"Connecting to Ollama at {OLLAMA_HOST}...")
        
        for i in range(max_retries):
            try:
                self.client = ollama.Client(host=OLLAMA_HOST)
                self.client.list()
                print(f"✓ Connected to Ollama")
                return True
            except Exception as e:
                if i < max_retries - 1:
                    print(f"Waiting... ({i+1}/{max_retries})")
                    time.sleep(2)
                else:
                    print(f"✗ Failed to connect: {e}")
                    return False
    
    def format_duration(self, nanoseconds):
        """Convert nanoseconds to readable format"""
        if nanoseconds < 1000:
            return f"{nanoseconds}ns"
        elif nanoseconds < 1_000_000:
            return f"{nanoseconds/1000:.2f}μs"
        elif nanoseconds < 1_000_000_000:
            return f"{nanoseconds/1_000_000:.2f}ms"
        else:
            return f"{nanoseconds/1_000_000_000:.2f}s"
    
    def format_bytes(self, bytes_val):
        """Convert bytes to readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.2f}{unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.2f}TB"
    
    def print_stats(self, response):
        """Print detailed statistics from response"""
        print("\n" + "─" * 70)
        print("📊 Response Statistics:")
        print("─" * 70)
        
        # Model info
        if 'model' in response:
            print(f"Model: {response['model']}")
        
        # Timestamps
        if 'created_at' in response:
            print(f"Created: {response['created_at']}")
        
        # Token counts
        if 'prompt_eval_count' in response:
            print(f"Prompt tokens: {response['prompt_eval_count']}")
        
        if 'eval_count' in response:
            print(f"Response tokens: {response['eval_count']}")
            self.total_tokens += response['eval_count']
        
        total_tokens = response.get('prompt_eval_count', 0) + response.get('eval_count', 0)
        if total_tokens > 0:
            print(f"Total tokens (this message): {total_tokens}")
        
        # Timing
        if 'prompt_eval_duration' in response:
            prompt_time = response['prompt_eval_duration']
            print(f"Prompt processing time: {self.format_duration(prompt_time)}")
        
        if 'eval_duration' in response:
            eval_time = response['eval_duration']
            print(f"Response generation time: {self.format_duration(eval_time)}")
            self.total_duration += eval_time
        
        if 'total_duration' in response:
            total_time = response['total_duration']
            print(f"Total time: {self.format_duration(total_time)}")
        
        # Speed metrics
        if 'eval_count' in response and 'eval_duration' in response:
            eval_count = response['eval_count']
            eval_duration = response['eval_duration']
            if eval_duration > 0:
                tokens_per_sec = (eval_count / eval_duration) * 1_000_000_000
                print(f"Generation speed: {tokens_per_sec:.2f} tokens/sec")
        
        # Load duration
        if 'load_duration' in response:
            print(f"Model load time: {self.format_duration(response['load_duration'])}")
        
        # Context info
        if 'context' in response and isinstance(response['context'], list):
            context_size = len(response['context'])
            print(f"Context size: {context_size} tokens")
        
        print("─" * 70)
        print(f"Session totals - Tokens: {self.total_tokens} | Duration: {self.format_duration(self.total_duration)}")
        print("─" * 70 + "\n")
    
    def chat(self, user_message):
        """Send message and get response with stats"""
        if not self.client:
            return "Error: Not connected to Ollama"
        
        try:
            # Add user message to history
            self.conversation_history.append({
                'role': 'user',
                'content': user_message
            })
            
            # Get response
            start_time = time.time()
            response = self.client.chat(
                model=MODEL_NAME,
                messages=self.conversation_history
            )
            end_time = time.time()
            
            # Extract assistant's message
            assistant_message = response['message']['content']
            
            # Add assistant message to history
            self.conversation_history.append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            # Print response
            print(f"\n🤖 Assistant: {assistant_message}")
            
            # Print statistics
            self.print_stats(response)
            
            return assistant_message
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return None
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.total_tokens = 0
        self.total_duration = 0
        print("✓ Conversation history cleared")
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print("No conversation history")
            return
        
        print("\n" + "=" * 70)
        print("📜 Conversation History")
        print("=" * 70)
        for i, msg in enumerate(self.conversation_history, 1):
            role = "👤 You" if msg['role'] == 'user' else "🤖 Assistant"
            print(f"\n[{i}] {role}:")
            print(msg['content'])
        print("\n" + "=" * 70 + "\n")

def print_help():
    """Print help message"""
    print("\n" + "=" * 70)
    print("Available Commands:")
    print("=" * 70)
    print("  /help     - Show this help message")
    print("  /reset    - Clear conversation history")
    print("  /history  - Show conversation history")
    print("  /quit     - Exit the chatbot")
    print("  /exit     - Exit the chatbot")
    print("=" * 70 + "\n")

def main():
    print("=" * 70)
    print("🤖 Ollama ChatBot")
    print(f"Model: {MODEL_NAME}")
    print(f"Host: {OLLAMA_HOST}")
    print("=" * 70)
    
    bot = ChatBot()
    
    if not bot.connect():
        sys.exit(1)
    
    print("\nType '/help' for available commands")
    print("=" * 70 + "\n")
    
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
            cmd = user_input.lower()
            
            if cmd in ['/quit', '/exit', '/q']:
                print("\nGoodbye! 👋")
                break
            elif cmd == '/help':
                print_help()
            elif cmd == '/reset':
                bot.reset_conversation()
            elif cmd == '/history':
                bot.show_history()
            else:
                print(f"Unknown command: {user_input}")
                print("Type '/help' for available commands")
            continue
        
        # Regular chat
        bot.chat(user_input)

if __name__ == "__main__":
    main()