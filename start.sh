#!/bin/bash

# Quick start script for Toddle Ops
set -e

echo "🚀 Starting Toddle Ops..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - GOOGLE_API_KEY (required)"
    echo "   - SUPABASE_USER (required)"
    echo "   - SUPABASE_PASSWORD (required)"
    echo ""
    read -p "Press Enter after you've updated .env file..."
fi

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "🐳 Docker detected!"
    echo ""
    echo "Choose deployment method:"
    echo "1) Docker Compose (recommended)"
    echo "2) Local with Streamlit"
    echo "3) CLI mode"
    read -p "Enter choice [1-3]: " choice
    
    case $choice in
        1)
            echo ""
            echo "🐳 Starting with Docker Compose..."
            docker-compose up -d
            echo ""
            echo "✅ Started! Access the UI at:"
            echo "   http://localhost:8501"
            echo ""
            echo "📊 View logs with: docker-compose logs -f"
            echo "🛑 Stop with: docker-compose down"
            ;;
        2)
            echo ""
            echo "🎨 Starting Streamlit locally..."
            if command -v uv &> /dev/null; then
                uv run streamlit run src/toddle_ops/ui.py
            else
                echo "❌ uv not found. Install with: pip install uv"
                exit 1
            fi
            ;;
        3)
            echo ""
            echo "💻 Starting CLI mode..."
            cd src/toddle_ops/agents
            if command -v adk &> /dev/null; then
                adk run orchestrator
            else
                echo "❌ adk not found. Install dependencies with: uv sync"
                exit 1
            fi
            ;;
        *)
            echo "Invalid choice"
            exit 1
            ;;
    esac
else
    echo "🎨 Docker not found. Starting Streamlit locally..."
    if command -v uv &> /dev/null; then
        uv run streamlit run src/toddle_ops/ui.py
    else
        echo "❌ uv not found. Please install:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi
