#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 ML Feature Engineering API - Docker Deployment${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
        echo -e "${YELLOW}   Please install Docker from https://docs.docker.com/get-docker/${NC}"
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        echo -e "${RED}❌ Docker Compose is not installed or not in PATH${NC}"
        echo -e "${YELLOW}   Please install Docker Compose from https://docs.docker.com/compose/install/${NC}"
        exit 1
    fi
}

# Function to stop existing containers
stop_containers() {
    echo -e "${YELLOW}🛑 Stopping existing containers...${NC}"
    docker compose down --remove-orphans
}

# Function to build and start containers
start_containers() {
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    docker compose build --no-cache
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Docker image built successfully${NC}"
    else
        echo -e "${RED}❌ Docker build failed${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}🚀 Starting containers...${NC}"
    docker compose up -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Containers started successfully${NC}"
    else
        echo -e "${RED}❌ Failed to start containers${NC}"
        exit 1
    fi
}

# Function to check container health
check_health() {
    echo -e "${YELLOW}⏳ Waiting for services to be healthy...${NC}"
    
    # Wait for up to 60 seconds for health check
    timeout=60
    counter=0
    
    while [ $counter -lt $timeout ]; do
        health_status=$(docker compose ps -q | xargs docker inspect --format='{{.State.Health.Status}}' 2>/dev/null)
        
        if [ "$health_status" = "healthy" ]; then
            echo -e "${GREEN}✅ API Server is healthy${NC}"
            break
        fi
        
        echo -e "${YELLOW}   Waiting for health check... ($counter/$timeout)${NC}"
        sleep 2
        counter=$((counter + 2))
    done
    
    if [ $counter -ge $timeout ]; then
        echo -e "${RED}❌ Health check timeout${NC}"
        echo -e "${YELLOW}   Check container logs: docker compose logs${NC}"
    fi
}

# Function to show service information
show_services() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎉 ML Feature Engineering API is running in Docker!${NC}"
    echo ""
    echo -e "${BLUE}📊 API Server:${NC}"
    echo -e "   🔗 Main API: http://localhost:8002"
    echo -e "   🔗 Health Check: http://localhost:8002/health"
    echo -e "   🔗 FastAPI Docs: http://localhost:8002/docs"
    echo ""
    echo -e "${BLUE}📚 Documentation:${NC}"
    echo -e "   🔗 Beautiful Docs: http://localhost:5002/docs"
    echo -e "   🔗 Interactive Tester: http://localhost:5002/docs#testing"
    echo -e "   🔗 Code Examples: http://localhost:5002/docs#examples"
    echo ""
    echo -e "${BLUE}🐳 Docker Management:${NC}"
    echo -e "   🔗 View logs: docker compose logs -f"
    echo -e "   🔗 Stop services: docker compose down"
    echo -e "   🔗 Restart services: docker compose restart"
    echo -e "   🔗 View status: docker compose ps"
    echo ""
    echo -e "${YELLOW}💡 Tips:${NC}"
    echo -e "   • Use 'docker compose logs -f' to monitor real-time logs"
    echo -e "   • Use 'docker compose down' to stop all services"
    echo -e "   • Use 'docker compose up -d' to start services in background"
    echo -e "   • Container will auto-restart if it crashes"
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

# Function to handle cleanup
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down containers...${NC}"
    docker compose down
    echo -e "${GREEN}✅ Containers stopped${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM

# Main execution
main() {
    check_docker
    stop_containers
    start_containers
    check_health
    show_services
    
    echo -e "${YELLOW}Press Ctrl+C to stop all services...${NC}"
    echo -e "${YELLOW}Or run 'docker compose down' in another terminal${NC}"
    
    # Keep script running to show logs
    docker compose logs -f
}

# Check command line arguments
case "${1:-}" in
    "stop")
        echo -e "${YELLOW}🛑 Stopping Docker containers...${NC}"
        docker compose down
        echo -e "${GREEN}✅ Containers stopped${NC}"
        ;;
    "restart")
        echo -e "${YELLOW}🔄 Restarting Docker containers...${NC}"
        docker compose restart
        echo -e "${GREEN}✅ Containers restarted${NC}"
        ;;
    "logs")
        echo -e "${YELLOW}📋 Showing container logs...${NC}"
        docker compose logs -f
        ;;
    "status")
        echo -e "${YELLOW}📊 Container status:${NC}"
        docker compose ps
        ;;
    *)
        main
        ;;
esac 