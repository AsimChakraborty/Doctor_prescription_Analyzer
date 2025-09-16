<!-- Kaggle Dataset: https://www.kaggle.com/datasets/mehaksingal/illegible-medical-prescription-images-dataset -->



# Prescription Analyzer

## Overview

The Prescription Analyzer is a Streamlit application designed to extract structured information from prescription images using the power of Large Language Models (LLMs). It processes uploaded images, identifies key details such as patient information, doctor information, medications, and additional notes, and presents them in an organized and user-friendly format. The application also leverages clinical advice generation for each medication.

## Features

*   **Image Upload:** Accepts prescription images in PNG, JPG, and JPEG formats.
*   **Information Extraction:** Automatically extracts patient details, doctor details, prescription date, medication lists (name, dosage, frequency, duration), and additional notes from the image.
*   **Structured Output:** Presents extracted information in clear tables for easy readability.
*   **Medication Advice:** Generates and displays potential side effects, precautions, drug interactions, and general health advice for each prescribed medication.
*   **Summary Generation:** Provides a concise summary of the overall prescription, including its purpose and important instructions.
*   **User-Friendly Interface:** Built with Streamlit for an intuitive and interactive experience.

## Technologies Used

*   **Python:** The core programming language.
*   **Streamlit:** For building the interactive web application.
*   **Langchain:** Framework for creating LLM-powered chains.
*   **Google Gemini API:** The LLM used for information extraction and advice generation.
*   **Pydantic:** For data validation and schema definition.
*   **Pandas:** For creating and displaying data tables.


## Prerequisites

Before running the application, ensure you have the following:

1.  **Python 3.7+:**  (Ideally 3.8 or higher)
2.  **API Key:** A Google Gemini API key. You can obtain one by signing up for the Google AI Studio: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
3.  **Required Python Packages:** Install the necessary packages using `pip`:

    ```bash
    pip install streamlit langchain langchain-google-genai pydantic pandas python-dotenv
    ```

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone [your_repository_url]
    cd Doctor_prescription_agent
    ```

2.  **Create `keys.py`:**

    Create a file named `keys.py` in the root directory (`prescription_analyzer/`) and store your Google Gemini API key in it:

    ```python
    # keys.py
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"  # Replace with your actual API key
    ```

    **Important:**  Do not commit the `keys.py` file to your repository to avoid exposing your API key.  Add it to your `.gitignore` file.

3.  **Environment Variables:**

    The application uses the `GEMINI_API_KEY` environment variable. The `config.py` file reads the API key from the `keys.py` file, sets it as an environment variable, and configures Langchain's debug mode.

## Running the Application

1.  **Navigate to the Project Directory:**

    ```bash
    cd Doctor_prescription_agent
    ```

2.  **Run the Streamlit App:**

    ```bash
    streamlit run app.py
    ```

    This will start the Streamlit application in your web browser.

## Usage

1.  **Upload an Image:** Click the "Browse files" button and select a prescription image from your local file system.
2.  **View Extracted Information:** The application will process the image and display the extracted information in a table format.  This includes patient details, doctor details, prescription date, and additional notes.
3.  **View Medication Details:**  A separate table will display a list of medications along with their dosage, frequency, duration, and clinical advice (side effects, precautions, interactions, and general advice).
4.  **Disclaimer:**  Please note the disclaimer at the bottom of the page, emphasizing that the information is for educational purposes only and not a substitute for professional medical advice.

