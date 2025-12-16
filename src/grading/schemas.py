from pydantic import BaseModel, Field

class GradingExample(BaseModel):
    concept: str = Field(..., description="The specific academic concept being tested.")
    question: str = Field(..., description="A quiz question derived from the concept.")
    correct_answer: str = Field(..., description="The precise, correct answer.")
    student_answer: str = Field(..., description="A simulated student answer (can be correct, partially correct, or wrong).")
    grade_score: int = Field(..., description="Score from 0 to 10.")
    feedback: str = Field(..., description="Constructive, encouraging feedback explaining the grade.")