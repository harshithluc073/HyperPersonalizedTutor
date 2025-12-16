import os
import json
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm
from .schemas import GradingExample

load_dotenv()

class SyntheticDataGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_batch(self, topic: str, batch_size: int = 5) -> List[GradingExample]:
        """
        Generates a batch of synthetic grading examples for a specific topic.
        """
        prompt = f"""
        Generate {batch_size} distinct Q&A scenarios for the topic: '{topic}'.
        
        For each scenario:
        1. Create a question based on handwritten notes logic.
        2. Provide the 100% correct answer.
        3. Simulate a student answer (mix of correct, vague, and wrong answers).
        4. Provide a grade (0-10) and detailed feedback as a tutor would.
        """

        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini", # Using mini to save costs during generation
            messages=[
                {"role": "system", "content": "You are a dataset generator for fine-tuning an educational AI."},
                {"role": "user", "content": prompt}
            ],
            response_format=grading_response_schema, # Defined dynamically below
        )
        
        return response.choices[0].message.parsed.examples

# Helper schema to handle the list response
from pydantic import BaseModel
class GradingBatch(BaseModel):
    examples: List[GradingExample]

grading_response_schema = GradingBatch

if __name__ == "__main__":
    # Test run
    gen = SyntheticDataGenerator()
    data = gen.generate_batch("Linear Algebra - Eigenvectors", 2)
    print(json.dumps([d.model_dump() for d in data], indent=2))