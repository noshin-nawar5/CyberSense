#!/bin/bash

# CyberSense Local Development Script
# This script helps you run the project locally

set -e

echo "🛡️  CyberSense - Local Development"
echo "=================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking requirements..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Function to setup backend
setup_backend() {
    echo ""
    echo "🔧 Setting up backend..."
    cd backend
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt
    
    # Download NLTK data
    echo "Downloading NLTK data..."
    python3 -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)"
    
    echo -e "${GREEN}✓${NC} Backend setup complete"
    cd ..
}

# Function to run backend
run_backend() {
    echo ""
    echo "🚀 Starting backend server..."
    cd backend
    source venv/bin/activate
    
    # Check if models exist
    if [ ! -f "models/best_model.joblib" ]; then
        echo -e "${YELLOW}⚠ Models not found - running in DEMO MODE${NC}"
        echo "   To use ML models, train them using notebooks/Main.ipynb"
    fi
    
    echo ""
    echo -e "${GREEN}Backend running at: http://localhost:5000${NC}"
    echo "Press Ctrl+C to stop"
    echo ""
    
    python3 app/main.py
}

# Function to run frontend
run_frontend() {
    echo ""
    echo "🌐 Starting frontend server..."
    cd frontend
    
    echo ""
    echo -e "${GREEN}Frontend running at: http://localhost:3000${NC}"
    echo "Press Ctrl+C to stop"
    echo ""
    
    python3 -m http.server 3000 --directory public
}

# Function to run tests
run_tests() {
    echo ""
    echo "🧪 Running tests..."
    cd backend
    source venv/bin/activate
    
    echo "Installing test dependencies..."
    pip install -q pytest pytest-cov
    
    echo ""
    echo "Running pytest..."
    python3 -m pytest tests/ -v
    
    cd ..
}

# Main menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo ""
    echo "1) Setup backend (first time only)"
    echo "2) Run backend server"
    echo "3) Run frontend server"
    echo "4) Run both (backend + frontend)"
    echo "5) Run tests"
    echo "6) Exit"
    echo ""
    read -p "Enter choice [1-6]: " choice
    
    case $choice in
        1)
            setup_backend
            show_menu
            ;;
        2)
            run_backend
            ;;
        3)
            run_frontend
            ;;
        4)
            echo ""
            echo "Starting both servers..."
            echo "Backend will run in background"
            echo ""
            
            # Start backend in background
            cd backend
            source venv/bin/activate
            python3 app/main.py &
            BACKEND_PID=$!
            cd ..
            
            sleep 2
            
            # Start frontend in foreground
            echo ""
            echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
            run_frontend
            
            # Kill backend when frontend stops
            kill $BACKEND_PID 2>/dev/null
            ;;
        5)
            run_tests
            show_menu
            ;;
        6)
            echo ""
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            show_menu
            ;;
    esac
}

# Check if first run
if [ ! -d "backend/venv" ]; then
    echo ""
    echo -e "${YELLOW}⚠ First time setup required${NC}"
    echo ""
    read -p "Run setup now? (y/n): " setup_choice
    
    if [ "$setup_choice" = "y" ] || [ "$setup_choice" = "Y" ]; then
        setup_backend
    else
        echo ""
        echo "Please run option 1 (Setup backend) first"
    fi
fi

# Show menu
show_menu
