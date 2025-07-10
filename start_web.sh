#!/bin/bash

# Start Flask app with web interface
echo "🚀 Starting Playwright Generic Tool..."

# Change to script directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Start Flask app
echo "Starting Flask app on http://localhost:5001"
echo "Web interface: http://localhost:5001/web"
echo "API docs: http://localhost:5001/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
