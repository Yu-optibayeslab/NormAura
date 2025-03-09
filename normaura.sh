#!/bin/bash

# Get the directory where the .sh file is located
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Construct the full path to NormAura.py
NORM_AURA_PATH="$SCRIPT_DIR/NormAura.py"

# Run the Streamlit app using the full path
streamlit run "$NORM_AURA_PATH"

