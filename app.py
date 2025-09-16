# prescription_analyzer/app.py
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import shutil

# Import from your new modules
from config import setup_environment, GEMINI_MODEL_NAME, TEMPERATURE
from models.schemas import PrescriptionInformations
from utils.helpers import local_css, remove_temp_folder
from utils.llm_chains import get_prescription_informations
from langchain_core.output_parsers import JsonOutputParser

# Setup environment variables (e.g., API key)
setup_environment()

st.set_page_config(layout="wide")

# Load CSS file
local_css("styles/styles.css")

def main():
    st.title(' 🧾 Prescription Summary & Health Advice')
    st.write("Upload a prescription image to extract structured details and get per-medication advice.")

    # Initialize parser for the main function, although it's also initialized in get_prescription_informations
    # This global or re-initialization can be simplified if parser is only used within get_prescription_informations.
    # For now, keeping it here as it was in the original, but noting it could be more streamlined.
    # In a fully modular setup, the parser might be created within llm_chains.py and passed.
    global parser
    parser = JsonOutputParser(pydantic_object=PrescriptionInformations)

    uploaded_file = st.file_uploader("Upload a Prescription image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = uploaded_file.name.split('.')[0].replace(' ', '_')
        output_folder = os.path.join(".", f"Check_{filename_base}_{timestamp}")
        os.makedirs(output_folder, exist_ok=True)

        check_path = os.path.join(output_folder, uploaded_file.name)
        with open(check_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.expander("Prescription Image", expanded=False):
            st.image(uploaded_file, caption='Uploaded Prescription Image.', use_column_width=True)

        with st.spinner('Processing Prescription...'):
            final_result = get_prescription_informations([check_path], GEMINI_MODEL_NAME, TEMPERATURE)

            # Process and display results
            if 'additional_notes' in final_result:
                additional_notes = final_result['additional_notes']
                # Format additional notes as bullet points
                if isinstance(additional_notes, list):
                    # Handle cases where additional_notes might be a list of strings
                    formatted_notes = "<br> ".join([f"<li>{note}</li>" for note in additional_notes])
                    final_result['additional_notes'] = f"<ul>{formatted_notes}</ul>"
                else:
                    # Handle cases where it's a single string with newlines
                    # Split by newline and wrap each part in <li>
                    note_lines = additional_notes.split('\n')
                    formatted_notes = "<br> ".join([f"<li>{line.strip()}</li>" for line in note_lines if line.strip()])
                    if formatted_notes: # Only wrap in ul if there are notes
                         final_result['additional_notes'] = f"<ul>{formatted_notes}</ul>"
                    else:
                         final_result['additional_notes'] = "Not available" # Or empty string


            # Convert final_result to a list of tuples for DataFrame creation
            # Filter out 'medications' for the first DataFrame
            data = [(key, final_result[key]) for key in final_result if key != 'medications']
            df = pd.DataFrame(data, columns=["Field", "Value"])

            st.subheader("Prescription Details")
            # Display the DataFrame with custom styling
            st.write(df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)

            # Display medications in a separate table with custom styling
            if 'medications' in final_result and final_result['medications']:
                # Flatten the medication advice into the main medication DataFrame for display
                medications_with_advice_data = []
                for med in final_result['medications']:
                    med_data = {
                        "Name": med.get("name", "N/A"),
                        "Dosage": med.get("dosage", "N/A"),
                        "Frequency": med.get("frequency", "N/A"),
                        "Duration": med.get("duration", "N/A"),
                        "Common Side Effects": med.get("advice", {}).get("common_side_effects", "N/A"),
                        "Precautions": med.get("advice", {}).get("precautions", "N/A"),
                        "Drug Interactions": med.get("advice", {}).get("drug_interactions", "N/A"),
                        "General Advice": med.get("advice", {}).get("general_advice", "N/A"),
                    }
                    medications_with_advice_data.append(med_data)

                if medications_with_advice_data:
                    medications_df = pd.DataFrame(medications_with_advice_data)
                    st.subheader("Medications with Clinical Advice")
                    st.write(medications_df.to_html(classes='custom-table', index=False, escape=False), unsafe_allow_html=True)
                else:
                    st.write("No medication details or advice found.")
            else:
                st.write("No medications found in the prescription.")


        # Delete temp folder
        remove_temp_folder(output_folder)

    # Footer disclaimer
    st.markdown("""
                
    <hr style='margin-top:40px;margin-bottom:10px;border:1px solid #e94646;'>
    <div style='font-size:0.95rem; color:#e94646; font-weight:bold;'>
    ❗ DISCLAIMER:<br>
    <span style='font-weight:normal; color:#0B7E85;'>
    This information is for educational purposes only and not a substitute for professional medical advice, diagnosis, or treatment.<br>
    Always consult your physician or pharmacist.
    </span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()