#!/bin/bash
echo "--- Technocore Agent Toolkit Setup ---"
echo "1. Updating system..."
sudo apt update && sudo apt install -y git python3 python3-pip nodejs npm

echo "2. Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install requests mnemonic

echo "3. Ready! Use 'python3 technocore_agent.py init' to start."
echo "--- Build with love by anaraydinli ---"

