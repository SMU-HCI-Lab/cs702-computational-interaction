#!/bin/bash

# Exit on error
set -e

echo "Starting dependency installation..."

# Install uv package installer
echo "Installing uv..."
pip install uv || { echo "Failed to install uv"; exit 1; }

# Install Python dependencies from requirements.txt
echo "Installing Python packages from requirements.txt..."
pip install -r requirements.txt || { echo "Failed to install Python packages"; exit 1; }

# Install IPOPT solver
echo "Installing IPOPT solver..."
conda install -y -c conda-forge ipopt || { echo "Failed to install IPOPT"; exit 1; }

echo "All dependencies installed successfully!"