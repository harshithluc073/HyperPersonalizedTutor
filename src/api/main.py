from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from src.ingestion.vlm_service import NoteDigitizer
from src.ingestion.schemas import DigitizedNote

app = FastAPI(title="Hyper-Personalized Tutor API")

# Initialize Services
# In a real production environment, we might load the SLM model here globally
digitizer = NoteDigitizer()

class GradingRequest(BaseModel):
    question: str
    student_answer: str
    correct_answer: str

class GradingResponse(BaseModel):
    grade: int
    feedback: str

@app.get("/")
def health_check():
    return {"status": "active", "system": "Hyper-Personalized Tutor"}

@app.post("/ingest", response_model=DigitizedNote)
async def ingest_notes(file: UploadFile = File(...)):
    """
    Uploads a raw image of handwritten notes and returns structured data.
    """
    try:
        # Save temp file
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process with VLM
        result = digitizer.digitize(temp_filename)
        
        # Cleanup
        os.remove(temp_filename)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/grade", response_model=GradingResponse)
async def grade_answer(request: GradingRequest):
    """
    Evaluates a student answer. 
    (Currently a placeholder: In production, this calls the fine-tuned SLM inference engine).
    """
    # TODO: Connect this to src/grading/inference.py when model is trained.
    # For now, we return a mock response to prove API connectivity.
    return {
        "grade": 8,
        "feedback": "This is a placeholder response. Once the SLM (Phi-3) is fine-tuned and loaded, it will generate specific feedback based on the engineering logic defined in Step 4."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)