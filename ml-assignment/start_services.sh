#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 ML Feature Engineering API & Documentation Setup${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# Function to start the API server
start_api_server() {
    echo -e "${YELLOW}📡 Starting FastAPI Server...${NC}"
    
    # Check if Python is available
    if ! command_exists python3 && ! command_exists python; then
        echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
        return 1
    fi
    
    # Check if port 8000 is available
    if port_in_use 8000; then
        echo -e "${YELLOW}⚠️  Port 8002 is already in use. API server might already be running.${NC}"
        echo -e "${YELLOW}   Check http://localhost:8002/health${NC}"
    else
        # Start the API server in background
        if command_exists python3; then
            python3 main.py &
        else
            python main.py &
        fi
        
        API_PID=$!
        echo -e "${GREEN}✅ API Server started (PID: $API_PID)${NC}"
        echo -e "${GREEN}   Available at: http://localhost:8002${NC}"
    fi
}

# Function to start the documentation server
start_docs_server() {
    echo -e "${YELLOW}📚 Starting Documentation Server...${NC}"
    
    # Check if Node.js is available
    if ! command_exists node; then
        echo -e "${RED}❌ Node.js is not installed or not in PATH${NC}"
        echo -e "${YELLOW}   Please install Node.js from https://nodejs.org/${NC}"
        return 1
    fi
    
    # Check if npm is available
    if ! command_exists npm; then
        echo -e "${RED}❌ npm is not installed or not in PATH${NC}"
        return 1
    fi
    
    # Navigate to docs directory
    if [ ! -d "docs" ]; then
        echo -e "${RED}❌ docs directory not found${NC}"
        return 1
    fi
    
    cd docs
    
    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📦 Installing dependencies...${NC}"
        npm install
    fi
    
    # Check if port 5002 is available
    if port_in_use 5002; then
        echo -e "${YELLOW}⚠️  Port 5002 is already in use. Documentation server might already be running.${NC}"
        echo -e "${YELLOW}   Check http://localhost:5002/docs${NC}"
    else
        # Start the documentation server in background
        npm start &
        DOCS_PID=$!
        echo -e "${GREEN}✅ Documentation Server started (PID: $DOCS_PID)${NC}"
        echo -e "${GREEN}   Available at: http://localhost:5002/docs${NC}"
    fi
    
    cd ..
}

# Function to wait for services to start
wait_for_services() {
    echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
    sleep 3
    
    # Check API server health
    if curl -s http://localhost:8002/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ API Server is healthy${NC}"
    else
        echo -e "${YELLOW}⚠️  API Server health check failed${NC}"
    fi
    
    # Check documentation server
    if curl -s http://localhost:5002/api/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Documentation Server is healthy${NC}"
    else
        echo -e "${YELLOW}⚠️  Documentation Server health check failed${NC}"
    fi
}

# Function to display final information
show_final_info() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎉 Services are running!${NC}"
    echo ""
    echo -e "${BLUE}📊 API Server:${NC}"
    echo -e "   🔗 Main API: http://localhost:8002"
    echo -e "   🔗 Health Check: http://localhost:8002/health"
    echo ""
    echo -e "${BLUE}📚 Documentation:${NC}"
    echo -e "   🔗 Beautiful Docs: http://localhost:5002/docs"
    echo -e "   🔗 Interactive API Tester: http://localhost:5002/docs#testing"
    echo -e "   🔗 Code Examples: http://localhost:5002/docs#examples"
    echo ""
    echo -e "${YELLOW}💡 Tips:${NC}"
    echo -e "   • Use the interactive tester at http://localhost:5002/docs#testing"
    echo -e "   • Copy code examples from the documentation"
    echo -e "   • Monitor server status in real-time"
    echo -e "   • Press Ctrl+C to stop both services"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to handle cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Stopping services...${NC}"
    
    # Kill all background jobs
    jobs -p | xargs -r kill
    
    # Kill processes on specific ports
    if port_in_use 8000; then
        echo -e "${YELLOW}   Stopping API server (port 8000)...${NC}"
        lsof -ti:8000 | xargs -r kill
    fi
    
    if port_in_use 5002; then
        echo -e "${YELLOW}   Stopping documentation server (port 5002)...${NC}"
        lsof -ti:5002 | xargs -r kill
    fi
    
    echo -e "${GREEN}✅ Services stopped${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM EXIT

# Main execution
main() {
    # Start services
    start_api_server
    start_docs_server
    
    # Wait for services to start
    wait_for_services
    
    # Show final information
    show_final_info
    
    # Keep the script running
    echo -e "${YELLOW}Press Ctrl+C to stop all services...${NC}"
    while true; do
        sleep 1
    done
}

# Run main function
main 