#!/bin/bash

# Define color codes
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages with color
log_message() {
    local level="$1"
    local message="$2"
    local color="$3"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "${color}[${timestamp}] ${level}: ${message}${NC}"
}

# Check if Poetry is installed
log_message "INFO" "Checking if Poetry is installed..." "${BLUE}"
if ! command -v poetry &> /dev/null; then
    log_message "ERROR" "Poetry is not installed. Please install Poetry first." "${RED}"
    exit 1
fi
log_message "SUCCESS" "Poetry is installed." "${GREEN}"

# Run poetry build
log_message "INFO" "Building the package..." "${BLUE}"
if poetry build; then
    log_message "SUCCESS" "Poetry build completed successfully." "${GREEN}"
else
    log_message "ERROR" "Poetry build failed." "${RED}"
    exit 1
fi

# Run poetry install
log_message "INFO" "Running poetry install..." "${BLUE}"
if poetry install; then
    log_message "SUCCESS" "Poetry install completed successfully." "${GREEN}"
else
    log_message "ERROR" "Poetry install failed." "${RED}"
    exit 1
fi

# Make the crawler script executable if it isn't already
log_message "INFO" "Making crawler script executable..." "${BLUE}"
if chmod +x ./scripts/crawler.sh; then
    log_message "SUCCESS" "Crawler script made executable successfully." "${GREEN}"
else
    log_message "ERROR" "Failed to make crawler script executable." "${RED}"
    exit 1
fi

# Create a symlink to the crawler script in ~/.local/bin/
log_message "INFO" "Creating symlink for crawler script..." "${BLUE}"
mkdir -p ~/.local/bin/
if poetry env info --path | xargs -I {} ln -sf {}/bin/crawler ~/.local/bin/solana-crawler; then
    log_message "SUCCESS" "Symlink created successfully." "${GREEN}"
else
    log_message "ERROR" "Failed to create symlink." "${RED}"
    exit 1
fi

# Update shell configuration
log_message "INFO" "Updating shell configuration..." "${BLUE}"
if [ -n "$BASH_VERSION" ]; then
    log_message "INFO" "Sourcing ~/.bashrc..." "${BLUE}"
    source ~/.bashrc 2>/dev/null || log_message "WARNING" "~/.bashrc not found or could not be sourced." "${YELLOW}"
elif [ -n "$ZSH_VERSION" ]; then
    log_message "INFO" "Sourcing ~/.zshrc..." "${BLUE}"
    source ~/.zshrc 2>/dev/null || log_message "WARNING" "~/.zshrc not found or could not be sourced." "${YELLOW}"
fi

# Log completion of installation
log_message "SUCCESS" "Installation completed successfully!" "${GREEN}"
