#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up Playwright Flask App${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install Playwright browsers
echo -e "${YELLOW}Installing Playwright browsers...${NC}"
playwright install

# Install additional system dependencies for Playwright
echo -e "${YELLOW}Installing system dependencies for Playwright...${NC}"
playwright install-deps

echo -e "${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To run the application:${NC}"
echo -e "  source venv/bin/activate"
echo -e "  python app.py"
echo -e ""
echo -e "${YELLOW}To test the client:${NC}"
echo -e "  source venv/bin/activate"
echo -e "  python client_example.py"
