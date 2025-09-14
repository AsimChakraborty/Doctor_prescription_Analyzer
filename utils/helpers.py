# prescription_analyzer/utils/helpers.py
import os
import shutil
import streamlit as st

def local_css(file_name):
    """Loads a CSS file and applies it to the Streamlit app."""
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_name}")

def remove_temp_folder(path):
    """Removes a file or a directory (and its contents)."""
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  
    elif os.path.isdir(path):
        shutil.rmtree(path)  