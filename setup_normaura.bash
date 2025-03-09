#!/bin/bash

# Get the current directory
CURRENT_DIR=$(pwd)

# Print the current directory
echo "Current directory: $CURRENT_DIR"

# Check if requirements.txt exists
if [ -f "$CURRENT_DIR/requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r "$CURRENT_DIR/requirements.txt"
else
    echo "requirements.txt not found in the current directory."
    exit 1
fi

# Check if normaura.sh exists
if [ -f "$CURRENT_DIR/normaura.sh" ]; then
    find . -name "normaura.sh" -exec chmod +x {} \;
    echo "Setting up alias for normaura.sh..."
    # Create an alias for normaura.sh
    alias normaura="$CURRENT_DIR/normaura.sh"
    echo "Alias 'normaura' created. You can now use 'normaura' to start the app."
else
    echo "normaura.sh not found in the current directory."
    exit 1
fi

# Add the alias to ~/.bashrc for persistence
echo "Adding alias to ~/.bashrc for future sessions..."
echo "alias normaura='$CURRENT_DIR/normaura.sh'" >> ~/.bashrc

# Reload ~/.bashrc to apply the alias immediately
source ~/.bashrc

echo "Setup complete! You can now use the 'normaura' command to start the app."
