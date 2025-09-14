# prescription_analyzer/models/schemas.py
from typing import List
from datetime import datetime
from langchain_core.pydantic_v1 import BaseModel, Field

class MedicationAdvice(BaseModel):
    common_side_effects: str = Field(description="Common side effects of the medication")
    precautions: str = Field(description="Important precautions for this medication")
    drug_interactions: str = Field(description="Potential drug interactions")
    general_advice: str = Field(description="General health advice for the patient")

class MedicationItem(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str
    advice: MedicationAdvice = Field(default_factory=MedicationAdvice)

class PrescriptionInformations(BaseModel):
    """Information about an image."""
    patient_name: str = Field(description="Patient's name")
    patient_age: str = Field(description="Patient's age") # Changed to str to handle "45y", "60" directly
    patient_gender: str = Field(description="Patient's gender")
    doctor_name: str = Field(description="Doctor's name")
    doctor_license: str = Field(description="Doctor's license number")
    prescription_date: datetime = Field(description="Date of the prescription")
    medications: List[MedicationItem] = []
    additional_notes: str = Field(description="Additional notes or instructions")
    summary: str = Field(description="Concise summary of the prescription")