import ollama
import os
import sys
import time

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama3.1')

def wait_for_ollama(max_retries=30):
    """Wait for Ollama service"""
    print(f"Connecting to Ollama at {OLLAMA_HOST}...")
    
    for i in range(max_retries):
        try:
            client = ollama.Client(host=OLLAMA_HOST)
            # Simple connection test - just try to list models
            client.list()
            print(f"✓ Connected to Ollama")
            return client
        except Exception as e:
            if i < max_retries - 1:
                print(f"Waiting for Ollama... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"✗ Failed to connect: {e}")
                sys.exit(1)

def translate(text, client):
    """Translate Traditional Chinese to English"""
    prompt = f"""Translate the following Traditional Chinese to English. Only output the translation, no explanations.

Traditional Chinese: {text}

English:"""
    
    try:
        response = client.chat(
            model=MODEL_NAME,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("=" * 60)
    print("Traditional Chinese → English Translator")
    print(f"Model: {MODEL_NAME}")
    print("=" * 60)
    
    client = wait_for_ollama()
    
    print("\nType 'quit' to exit\n")
    
    while True:
        try:
            text = input("中文: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if text.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not text:
            continue
        
        print("Translating...")
        result = translate(text, client)
        print(f"English: {result}\n")

if __name__ == "__main__":
    main()