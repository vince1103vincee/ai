#!/bin/bash

echo "========================================================================"
echo "RAG System Setup"
echo "========================================================================"
echo ""

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Option 1: Install with --user flag (system-wide for your user)"
    echo "  pip install --user ollama numpy"
    echo ""
    echo "Option 2: Create a virtual environment (recommended)"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install ollama numpy"
    echo ""
    read -p "Choose option (1 or 2): " choice

    if [ "$choice" = "1" ]; then
        echo ""
        echo "Installing packages with --user flag..."
        pip install --user ollama numpy
    elif [ "$choice" = "2" ]; then
        echo ""
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "Activating virtual environment..."
        source venv/bin/activate
        echo "Installing packages..."
        pip install ollama numpy
        echo ""
        echo "✓ Setup complete!"
        echo ""
        echo "To use the RAG system in the future:"
        echo "  1. Activate the virtual environment: source venv/bin/activate"
        echo "  2. Run the bot: python rag_bot.py"
        echo "  3. When done: deactivate"
    else
        echo "Invalid choice. Please run again and choose 1 or 2."
        exit 1
    fi
else
    echo "Virtual environment detected: $VIRTUAL_ENV"
    echo "Installing packages..."
    pip install ollama numpy
fi

echo ""
echo "========================================================================"
echo "Verifying installation..."
echo "========================================================================"
python3 -c "import ollama; import numpy; print('✓ ollama:', ollama.__version__ if hasattr(ollama, '__version__') else 'installed'); print('✓ numpy:', numpy.__version__)"

echo ""
echo "========================================================================"
echo "Setup complete! You can now use the RAG system."
echo "========================================================================"
