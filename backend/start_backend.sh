#!/bin/bash

# AERTS Backend Startup Script

echo "🏥 Starting AERTS - Adaptive Emergency Response Training Simulator"
echo "STEMI Protocol Backend"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python $python_version detected"

# Navigate to backend directory
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

# Check for environment file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "📝 Created .env file from template. You may need to edit it with your API keys."
    else
        echo "ℹ️  No env.example found. Running without environment configuration."
    fi
fi

# Check for Google Cloud credentials (optional)
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ] && [ ! -f ".env" ]; then
    echo "ℹ️  No Google Cloud credentials found. AERTS will run with mock AI responses."
    echo "   To enable Gemini AI, set GOOGLE_APPLICATION_CREDENTIALS environment variable."
fi

echo ""
echo "🚀 Starting AERTS Backend Server..."
echo ""
echo "📊 API Documentation: http://localhost:8000/docs"
echo "🌐 API Base URL: http://localhost:8000"
echo "📚 OpenAPI Schema: http://localhost:8000/openapi.json"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
