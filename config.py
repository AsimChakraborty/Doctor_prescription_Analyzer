# prescription_analyzer/config.py
import os
from langchain import globals
from keys import GEMINI_API_KEY # Assuming keys.py is in the root or accessible

# --- Environment Setup ---
def setup_environment():
    os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
    globals.set_debug(False) # Set Langchain debug globally

# --- Model Configuration ---
GEMINI_MODEL_NAME = "gemini-1.5-flash"
TEMPERATURE = 0.3 # Model temperature