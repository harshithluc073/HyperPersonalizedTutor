# The Hyper-Personalized Tutor (Multi-Modal) 🎓

An advanced educational platform designed to ingest messy handwritten notes using **Vision-Language Models (VLMs)** and generate adaptive study materials using **Fine-Tuned Small Language Models (SLMs)**.

## 🚀 Key Features

*   **VLM Ingestion Pipeline**: Converts raw images of handwritten notes and diagrams into structured JSON/Markdown using `GPT-4o` (Prototype) or `Llama-3.2-Vision` (Production).
*   **Semantic Extraction**: Goes beyond OCR; understands the relationship between diagram labels and descriptions.
*   **Fine-Tuned Grading Logic**: Uses **QLoRA** to fine-tune a lightweight model (Phi-3-Mini) to grade student answers with specific pedagogical feedback, optimizing for cost/latency vs. generic API calls.
*   **Production Architecture**: Built with FastAPI (Backend), Streamlit (Frontend), and Dockerized for deployment.

## 🏗️ Architecture

1.  **Ingestion Layer**: `src/ingestion` - Handles image processing and VLM inference.
2.  **Grading Engine**: `src/grading` - Contains the synthetic data generator and QLoRA training scripts.
3.  **API**: `src/api` - FastAPI endpoints serving the models.
4.  **UI**: `src/ui` - Streamlit dashboard for student interaction.

## 🛠️ Tech Stack

*   **Models**: GPT-4o, Phi-3-Mini, Llama-3.2-Vision
*   **Training**: Unsloth, Hugging Face PEFT, PyTorch
*   **Backend**: FastAPI, Pydantic
*   **Frontend**: Streamlit
*   **DevOps**: Docker, Docker Compose

## ⚡ Quick Start

### Local Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env` with your API keys.
4. Run Backend: `uvicorn src.api.main:app --reload`
5. Run Frontend: `streamlit run src/ui/app.py`

### Docker Setup
```bash
docker-compose up --build
```
## 📜 License
MIT