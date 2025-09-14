# prescription_analyzer/utils/llm_chains.py
import os
from typing import List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import chain
from langchain_core.output_parsers import JsonOutputParser

from models.schemas import PrescriptionInformations 
from utils.image_processing import load_images_chain 
from prompts.vision_prompt import VISION_PRESCRIPTION_EXTRACTION_PROMPT 

@chain
def image_model_invocation(inputs: dict) -> str | list[str] | dict:
    """
    Invoke model with images and prompt.
    The inputs dictionary is expected to contain 'images', 'prompt_text',
    'format_instructions', 'model_name', and 'temperature'.
    """
    # Extract model_name and temperature from the inputs dictionary
    model_name = inputs.get("model_name")
    temperature = inputs.get("temperature")

    # Initialize the model using the extracted parameters
    model = ChatGoogleGenerativeAI(api_key=os.environ["GEMINI_API_KEY"], model=model_name, temperature=temperature)
    image_urls = [{"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}} for img in inputs['images']]

    msg = model.invoke(
        [HumanMessage(
            content=[
                {"type": "text", "text": inputs['prompt_text']},
                {"type": "text", "text": inputs['format_instructions']},
                *image_urls
            ]
        )]
    )
    return msg.content

def get_prescription_informations(image_paths: List[str], model_name: str, temperature: float) -> dict:
    """
    Orchestrates the image loading, model invocation, and JSON parsing
    to extract prescription information.
    """
    parser = JsonOutputParser(pydantic_object=PrescriptionInformations)

    vision_prompt_text = VISION_PRESCRIPTION_EXTRACTION_PROMPT

    # Combine chains
    vision_chain = (
        load_images_chain
        | (lambda x: {
            "images": x["images"],
            "prompt_text": vision_prompt_text,
            "format_instructions": parser.get_format_instructions(),
            "model_name": model_name,    
            "temperature": temperature  
           })
        | image_model_invocation         
        | parser
    )

    return vision_chain.invoke({'image_paths': image_paths})