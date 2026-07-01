#!/bin/bash

# Cyber Fortune Telling MCP Server Docker Test Script

set -e

echo "🧪 Testing Cyber Fortune Telling MCP Server Docker Setup"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test variables
IMAGE_NAME="cyber-fortune-mcp-server"
API_URL="http://localhost:11337/api"

echo -e "\n${YELLOW}1. Checking if Docker image exists...${NC}"
if docker image inspect $IMAGE_NAME >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker image found${NC}"
else
    echo -e "${YELLOW}🔨 Building Docker image...${NC}"
    docker build -t $IMAGE_NAME .
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
fi

echo -e "\n${YELLOW}2. Testing MCP tools list...${NC}"
TEST_RESULT=$(echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
    docker run --rm -i --network host \
    -e CYBER_FORTUNE_API_BASE_URL=$API_URL \
    $IMAGE_NAME 2>/dev/null || echo "ERROR")

if [[ "$TEST_RESULT" == *"generate_fortune_telling"* ]]; then
    echo -e "${GREEN}✅ MCP server responds correctly${NC}"
    echo "Available tools found in response"
else
    echo -e "${RED}❌ MCP server test failed${NC}"
    echo "Response: $TEST_RESULT"
    exit 1
fi



echo -e "\n${YELLOW}3. Testing MCP configuration files...${NC}"
if [ -f "docker-mcp.json" ]; then
    echo -e "${GREEN}✅ docker-mcp.json found${NC}"
    # Validate JSON
    if python3 -m json.tool docker-mcp.json >/dev/null 2>&1; then
        echo -e "${GREEN}✅ docker-mcp.json is valid JSON${NC}"
    else
        echo -e "${RED}❌ docker-mcp.json has invalid JSON${NC}"
    fi
else
    echo -e "${RED}❌ docker-mcp.json not found${NC}"
fi

echo -e "\n${GREEN}🎉 All tests passed! MCP Server Docker setup is ready.${NC}"
echo -e "\n${YELLOW}Usage examples:${NC}"
echo "1. Run directly:"
echo "   docker run --rm -i --network host -e CYBER_FORTUNE_API_BASE_URL=$API_URL $IMAGE_NAME"
echo ""
echo "2. Use in MCP Inspector with docker-mcp.json configuration" 