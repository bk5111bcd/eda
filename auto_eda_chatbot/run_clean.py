#!/usr/bin/env python3
"""
Clean Streamlit launcher without Hugging Face warnings
"""
import os
import sys
import warnings
from contextlib import suppress

# Suppress all warnings from the start
warnings.filterwarnings('ignore')
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Suppress any library warnings
import logging
logging.getLogger('huggingface_hub').setLevel(logging.ERROR)
logging.getLogger('transformers').setLevel(logging.ERROR)

if __name__ == '__main__':
    import subprocess
    
    # Run streamlit with minimal logging
    result = subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        'auto_eda_chatbot/app.py',
        '--logger.level=error',
        '--client.showErrorDetails=false'
    ], 
    cwd=os.path.dirname(os.path.abspath(__file__)) or '/home/balaji/Downloads/pro'
    )
    sys.exit(result.returncode)
