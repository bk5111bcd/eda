#!/bin/bash
# Fix environment and run the app

export PYTHONDONTWRITEBYTECODE=1
export PYTHONWARNINGS="ignore::DeprecationWarning,ignore::PendingDeprecationWarning"

cd /home/balaji/Downloads/pro
source venv/bin/activate

# Suppress Hugging Face warnings
python -c "
import os
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
" 

streamlit run auto_eda_chatbot/app.py --logger.level=error
