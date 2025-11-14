import ollama
import os
import sys
import time

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.1')

class SimpleBot:
    def __init__(self):
        self.client = None
        self.total_tokens = 0
        self.total_duration = 0
        self.message_count = 0
        
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
    
    def print_stats(self, response):
        """Print detailed statistics from response"""
        print("\n" + "─" * 70)
        print("📊 Response Statistics:")
        print("─" * 70)
        
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
        
        print("─" * 70)
        print(f"Session totals - Messages: {self.message_count} | Tokens: {self.total_tokens} | Duration: {self.format_duration(self.total_duration)}")
        print("─" * 70 + "\n")
    
    def ask(self, user_message):
        """Send single message and get response (no history)"""
        if not self.client:
            return "Error: Not connected to Ollama"
        
        try:
            self.message_count += 1
            
            # Send only current message (no history)
            response = self.client.chat(
                model=MODEL_NAME,
                messages=[{'role': 'user', 'content': user_message}]
            )
            
            # Extract assistant's message
            assistant_message = response['message']['content']
            
            # Print response
            print(f"\n🤖 Assistant: {assistant_message}")
            
            # Print statistics
            self.print_stats(response)
            
            return assistant_message
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            return None
    
    def show_stats(self):
        """Show session statistics"""
        print("\n" + "=" * 70)
        print("📈 Session Statistics")
        print("=" * 70)
        print(f"Total messages: {self.message_count}")
        print(f"Total tokens generated: {self.total_tokens}")
        print(f"Total duration: {self.format_duration(self.total_duration)}")
        
        if self.total_duration > 0 and self.total_tokens > 0:
            avg_speed = (self.total_tokens / self.total_duration) * 1_000_000_000
            print(f"Average speed: {avg_speed:.2f} tokens/sec")
        
        if self.message_count > 0:
            avg_tokens = self.total_tokens / self.message_count
            print(f"Average tokens per message: {avg_tokens:.2f}")
        
        print("=" * 70 + "\n")

def print_help():
    """Print help message"""
    print("\n" + "=" * 70)
    print("Available Commands:")
    print("=" * 70)
    print("  /help     - Show this help message")
    print("  /stats    - Show session statistics")
    print("  /quit     - Exit the chatbot")
    print("  /exit     - Exit the chatbot")
    print("=" * 70 + "\n")

def main():
    print("=" * 70)
    print("🤖 Simple Q&A Bot (No Memory)")
    print(f"Model: {MODEL_NAME}")
    print(f"Host: {OLLAMA_HOST}")
    print("=" * 70)
    print("Note: Each question is independent - no conversation history")
    print("=" * 70)
    
    bot = SimpleBot()
    
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
            elif cmd == '/stats':
                bot.show_stats()
            else:
                print(f"Unknown command: {user_input}")
                print("Type '/help' for available commands")
            continue
        
        # Simple Q&A (no history)
        bot.ask(user_input)

if __name__ == "__main__":
    main()