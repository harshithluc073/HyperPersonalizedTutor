import json
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import FastLanguageModel # Best-in-class optimization library
import torch

# Configuration
max_seq_length = 2048
dtype = None # Auto detection
load_in_4bit = True # Use 4bit quantization to reduce memory usage

def train_grader_model(data_path: str, output_dir: str = "models/fine_tuned_grader"):
    """
    Fine-tunes a Small Language Model (Phi-3 or Llama-3) on grading data.
    """
    
    # 1. Load the Base Model (SLM)
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = "unsloth/Phi-3-mini-4k-instruct", 
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )

    # 2. Add LoRA Adapters (The Fine-Tuning Magic)
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16, # Rank
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0, 
        bias = "none", 
        use_gradient_checkpointing = "unsloth", 
        random_state = 3407,
        use_rslora = False, 
        loftq_config = None, 
    )

    # 3. Prepare Data
    # Convert our JSON format to the chat format the model expects
    with open(data_path, 'r') as f:
        raw_data = json.load(f)

    def format_prompts(examples):
        # This converts our structured feedback into a conversation format
        texts = []
        for doc in examples['examples']: # Assuming JSON structure from Step 3
            input_text = f"Question: {doc['question']}\nStudent Answer: {doc['student_answer']}\nCorrect Answer: {doc['correct_answer']}"
            output_text = f"Grade: {doc['grade_score']}/10\nFeedback: {doc['feedback']}"
            
            # Phi-3 / Llama-3 specific prompt format
            prompt = f"<|user|>\n{input_text}<|end|>\n<|assistant|>\n{output_text}<|end|>"
            texts.append(prompt)
        return {"text": texts}

    # Convert list of dicts to HuggingFace Dataset
    dataset = Dataset.from_list(raw_data)
    dataset = dataset.map(format_prompts, batched=True)

    # 4. Initialize Trainer
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 2,
        args = TrainingArguments(
            per_device_train_batch_size = 2,
            gradient_accumulation_steps = 4,
            warmup_steps = 5,
            max_steps = 60, # Increase for real training
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 1,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "linear",
            seed = 3407,
            output_dir = output_dir,
        ),
    )

    # 5. Train
    print("Starting training...")
    trainer.train()

    # 6. Save Model (merged) for GGUF/Ollama serving
    model.save_pretrained_merged(output_dir, tokenizer, save_method = "merged_16bit",)
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    # Example usage
    # Ensure you have generated data in data/training_data.json first
    pass