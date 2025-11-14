#!/bin/bash

echo "========================================================================"
echo "RAG System Demo"
echo "========================================================================"
echo ""
echo "This demo will:"
echo "  1. Create sample documents"
echo "  2. Show you how to run the RAG bot"
echo "  3. Provide example commands"
echo ""
echo "Press Enter to continue..."
read

# Create sample docs
echo ""
echo "Step 1: Creating sample documents in ./demo_docs..."
python3 << 'PYTHON'
from document_processor import DocumentProcessor
processor = DocumentProcessor()
processor.create_sample_documents('./demo_docs')
PYTHON

echo ""
echo "✓ Created sample documents!"
echo ""
echo "Step 2: To start the interactive RAG bot, run:"
echo "  python rag_bot.py"
echo ""
echo "Step 3: Inside the bot, run these commands:"
echo "  /index ./demo_docs"
echo "  What is Python?"
echo "  What are the types of machine learning?"
echo "  /context on"
echo "  How does RAG work?"
echo "  /stats"
echo "  /save demo_index.pkl"
echo "  /quit"
echo ""
echo "Next time, you can load the saved index:"
echo "  /load demo_index.pkl"
echo ""
echo "========================================================================"
echo "Ready to start! Run: python rag_bot.py"
echo "========================================================================"
