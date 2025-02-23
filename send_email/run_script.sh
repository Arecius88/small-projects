#!/bin/bash
# Anger de olika sökvägarna
VENV_PATH="PAHT/TO/VENC"
PYTHON_PATH="$VENV_PATH/PATH/TO/PYTHON"
PROJECT_SCRIPT_PATH="PATH/TO/SCRIPT"

# Aktivera virtuella miljön 
source "$VENV_PATH/bin/activate"

# kör Python-skriptet
"$PYTHON_PATH" "$PROJECT_SCRIPT_PATH"

#deaktivera virtuella miljön
deactivate
