# Hyper-Personalized Tutor (Multi-Modal)

The Hyper-Personalized Tutor is an advanced educational platform designed to bridge the gap between analog study materials and digital adaptive learning. Unlike generic study tools that rely on pre-existing content, this system ingests raw handwritten notes, diagrams, and whiteboards to generate a bespoke curriculum.

The core engineering distinction of this project is its move away from generic "wrapper" architectures. Instead of relying solely on expensive, general-purpose LLM APIs, it employs a hybrid architecture: high-parameter Vision-Language Models (VLMs) for semantic extraction and localized, fine-tuned Small Language Models (SLMs) for high-frequency grading tasks.

## System Architecture

The application is composed of three distinct processing stages:

1.  **Ingestion Pipeline (VLM):**
    *   Input: Raw images (JPEG/PNG) of handwritten notes.
    *   Process: Utilizes state-of-the-art Vision-Language Models (e.g., GPT-4o, Llama-3.2-Vision) to perform semantic extraction.
    *   Output: Structured JSON containing raw text, identified key concepts, and semantic descriptions of visual diagrams.

2.  **Assessment Engine (Fine-Tuned SLM):**
    *   Input: Generated questions and student answers.
    *   Process: A dedicated Small Language Model (e.g., Phi-3-Mini, Llama-3-8B) fine-tuned using Quantized Low-Rank Adaptation (QLoRA).
    *   Optimization: This model is specifically trained on grading rubrics, allowing it to provide pedagogical feedback with lower latency and compute costs than general-purpose models.

3.  **Application Layer:**
    *   **Backend:** FastAPI service orchestrating the models and data flow.
    *   **Frontend:** A professional dashboard built with Streamlit for user interaction.
    *   **Deployment:** Dockerized container orchestration.

## Technical Stack

*   **Language:** Python 3.10+
*   **Vision-Language Models:** GPT-4o / Llama-3.2-Vision
*   **Inference & Fine-Tuning:** Unsloth, Hugging Face PEFT, PyTorch, QLoRA
*   **Backend API:** FastAPI, Uvicorn, Pydantic
*   **Frontend Interface:** Streamlit (Custom CSS)
*   **Containerization:** Docker, Docker Compose

## Repository Structure

```text
.
├── src/
│   ├── api/            # FastAPI backend endpoints and logic
│   ├── ingestion/      # VLM integration and image processing services
│   ├── grading/        # SLM fine-tuning scripts (QLoRA) and synthetic data generation
│   └── ui/             # Streamlit frontend application
├── models/             # Directory for storing local model weights and adapters
├── tests/              # Unit and integration tests
├── Dockerfile          # Container build instructions
├── docker-compose.yml  # Service orchestration
└── requirements.txt    # Python dependency management
```

## Installation and Setup

### Prerequisites

*   Python 3.10 or higher
*   Git
*   Docker Desktop (optional, for containerized deployment)
*   OpenAI API Key (for VLM ingestion prototype)

### Method 1: Local Development

1.  **Clone the repository**
    ```bash
    git clone https://github.com/harshithluc073/HyperPersonalizedTutor.git
    cd HyperPersonalizedTutor
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

5.  **Run the Application**
    *   Terminal 1 (Backend):
        ```bash
        uvicorn src.api.main:app --reload
        ```
    *   Terminal 2 (Frontend):
        ```bash
        streamlit run src/ui/app.py
    ```

### Method 2: Docker Deployment

This method builds both the backend and frontend into isolated containers.

1.  **Build and Run**
    ```bash
    docker-compose up --build
    ```

2.  **Access**
    *   Frontend: http://localhost:8501
    *   Backend API Docs: http://localhost:8000/docs

## Fine-Tuning Workflow

To replicate the grading model fine-tuning:

1.  **Generate Data:** Run `src/grading/generator.py` to create a synthetic dataset of Q&A pairs.
2.  **Train Model:** Run `src/grading/train.py`. This script utilizes Unsloth for optimized QLoRA training. A GPU is required for this step.
3.  **Inference:** The trained adapters are saved to `models/fine_tuned_grader` and loaded by the inference engine.

## License

This project is licensed under the MIT License.