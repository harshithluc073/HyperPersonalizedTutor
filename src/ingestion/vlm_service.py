import base64
import os
from PIL import Image
from io import BytesIO
from .schemas import DigitizedNote
# We will use OpenAI for the VLM prototype (swappable for Llama-3-Vision later)
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class NoteDigitizer:
    def __init__(self):
        # In production, we can swap this for a local Llama-3-Vision client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
        self.model = "gpt-4o" # High performance VLM

    def encode_image(self, image_path: str) -> str:
        """Convert image to base64 string for API ingestion."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def digitize(self, image_path: str) -> DigitizedNote:
        """
        Takes a path to a handwritten note image and returns a structured DigitizedNote object.
        """
        base64_image = self.encode_image(image_path)

        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an advanced academic assistant. Your task is to transcribe handwritten notes into structured Markdown. Pay special attention to diagrams—describe them semantically so a blind student could understand them. Extract key concepts."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Transcribe this handwritten note."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ],
                }
            ],
            response_format=DigitizedNote,
        )

        return response.choices[0].message.parsed