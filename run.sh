#!/bin/bash

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements if needed
echo "Checking for dependencies..."
pip install -r requirements.txt

# Set optimized environment variables
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=10
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_THEME_BASE="dark"
export STREAMLIT_THEME_PRIMARY_COLOR="#4B8BF5"
export STREAMLIT_RUNNER_FAST_RERUNS=true
export PYTHONOPTIMIZE=2  # Enable Python optimizations (level 2)

# Run the app with optimized parameters
echo "Starting Better Promptly in dark mode..."
streamlit run Chat.py --server.enableCORS=false --server.enableXsrfProtection=true --server.maxUploadSize=10 --browser.serverAddress="localhost" --browser.gatherUsageStats=false --client.showErrorDetails=false --client.toolbarMode=minimal --theme.base=dark 