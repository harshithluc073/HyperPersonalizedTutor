from pydantic import BaseModel, Field
from typing import List, Optional

class DiagramDescription(BaseModel):
    label: str = Field(..., description="The title or label of the diagram identified.")
    description: str = Field(..., description="Detailed textual description of the visual elements and relationships in the diagram.")

class DigitizedNote(BaseModel):
    topic: str = Field(..., description="The main topic derived from the handwritten header.")
    date: Optional[str] = Field(None, description="Date found in the notes, if any.")
    raw_text: str = Field(..., description="The direct transcription of the handwritten text in Markdown format.")
    key_concepts: List[str] = Field(..., description="List of core concepts identified in the notes.")
    diagrams: List[DiagramDescription] = Field(default_factory=list, description="Structured descriptions of any diagrams or charts found.")