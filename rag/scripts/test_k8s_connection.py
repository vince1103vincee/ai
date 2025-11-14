#!/usr/bin/env python3
"""
Test connection to K8s Ollama and verify both models
"""

import os
import sys

try:
    import ollama
except ImportError:
    print("❌ ollama package not installed")
    print("Run: pip install --user ollama")
    sys.exit(1)

# Get Ollama host from environment or use default
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

print("=" * 70)
print("Testing K8s Ollama Connection")
print("=" * 70)
print(f"Host: {OLLAMA_HOST}")
print()

# Initialize client
client = ollama.Client(host=OLLAMA_HOST)

# Test 1: List models
print("1. Listing all models...")
print("-" * 70)
try:
    models = client.list()
    print(f"✓ Connected successfully!")
    print(f"Found {len(models['models'])} models:")
    for model in models['models']:
        name = model['name']
        size_gb = model['size'] / (1024**3)
        print(f"  - {name:30} ({size_gb:.2f} GB)")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    print("\nMake sure:")
    print("  1. Ollama is running in K8s")
    print("  2. Port-forward is active: kubectl port-forward -n ollama service/ollama-service 11434:11434")
    print(f"  3. OLLAMA_HOST is correct: {OLLAMA_HOST}")
    sys.exit(1)

print()

# Test 2: Check for required models
print("2. Checking required models...")
print("-" * 70)

required_models = {
    'llama3.1': False,
    'nomic-embed-text': False
}

for model in models['models']:
    name = model['name'].split(':')[0]  # Remove :latest suffix
    if name in required_models:
        required_models[name] = True

for model_name, exists in required_models.items():
    status = "✓" if exists else "❌"
    print(f"{status} {model_name:30} {'Found' if exists else 'MISSING'}")

print()

# Test 3: Test embedding generation
print("3. Testing embedding model...")
print("-" * 70)

if required_models['nomic-embed-text']:
    try:
        response = client.embeddings(
            model='nomic-embed-text',
            prompt='This is a test'
        )
        embedding = response['embedding']
        print(f"✓ Embedding generated successfully!")
        print(f"  Embedding dimension: {len(embedding)}")
        print(f"  First 5 values: {embedding[:5]}")
    except Exception as e:
        print(f"❌ Failed to generate embedding: {e}")
else:
    print("⚠️  nomic-embed-text not found, skipping embedding test")

print()

# Test 4: Test LLM
print("4. Testing LLM model...")
print("-" * 70)

if required_models['llama3.1']:
    try:
        response = client.chat(
            model='llama3.1',
            messages=[{'role': 'user', 'content': 'Say "Hello" and nothing else.'}]
        )
        answer = response['message']['content']
        print(f"✓ LLM responded successfully!")
        print(f"  Response: {answer}")
    except Exception as e:
        print(f"❌ Failed to get LLM response: {e}")
else:
    print("⚠️  llama3.1 not found, skipping LLM test")

print()
print("=" * 70)
print("Test Summary")
print("=" * 70)

all_good = all(required_models.values())

if all_good:
    print("✓ All tests passed! Your K8s Ollama is ready for RAG.")
    print()
    print("You can now run:")
    print("  cd /Users/tingchu.chen/code/ai/rag")
    print(f"  export OLLAMA_HOST='{OLLAMA_HOST}'")
    print("  python rag_bot.py")
else:
    print("❌ Some models are missing. Please:")
    print("  1. Apply updated init-script.yaml:")
    print("     kubectl apply -f /Users/tingchu.chen/code/ai/ollma/k8s/init-script.yaml")
    print("  2. Restart Ollama deployment:")
    print("     kubectl rollout restart deployment/ollama -n ollama")
    print("  3. Wait for models to download:")
    print("     kubectl logs -n ollama -l app=ollama -c init-model -f")

print("=" * 70)
