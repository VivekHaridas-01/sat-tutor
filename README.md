# SAT Tutor - AI-Powered SAT Preparation Assistant

An intelligent SAT prep tutor built using **Gemma 3N** fine-tuned with **Unsloth AI**. This project creates a specialized AI assistant capable of solving and explaining SAT math and reasoning problems.

## Features

- **Subject-Specific Training**: Fine-tuned specifically for SAT math and reasoning problems
- **Multi-Format Support**: Handles various question types including algebra, geometry, and word problems
- **Step-by-Step Explanations**: Provides detailed solutions with clear explanations
- **Multiple Deployment Options**: Can be run locally using Ollama or on Hugging Face Spaces

## Project Structure

```
sat-tutor/
├── SAT_Tutor.ipynb           # Fine-tuning notebook using Unsloth AI
├── spaces/                   # Hugging Face Spaces deployment
│   ├── app.py                # Gradio web interface
│   ├── requirements.txt      # Python dependencies
│   ├── model.gguf            # Quantized model file
│   └── README.md             # Spaces deployment guide
├── local-ollama/             # Local Ollama deployment
│   ├── Modelfile             # Ollama model configuration
│   ├── model.gguf            # Quantized model file
│   └── README.md             # Local setup instructions
└── README.md                 # This file
```

## Quick Start

### Option 1: Hugging Face Spaces (Recommended for Demo)

The easiest way to try the SAT Tutor is through the hosted demo on Hugging Face Spaces:

1. Visit the [SAT Tutor Space](https://huggingface.co/spaces/VivekHaridas01/SAT-Tutor)
2. Start chatting with the SAT tutor. Ask SAT-style math and reasoning questions
3. Ask follow-up questions for more clarity

### Option 2: Local Ollama Setup

For running locally with Ollama:

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Clone this repository
gh repo clone VivekHaridas-01/sat-tutor
cd sat-tutor-main/local-ollama

# Set up the model
mkdir -p ~/.ollama/models/sat-tutor
cp model.gguf ~/.ollama/models/sat-tutor/
cp Modelfile ~/.ollama/models/sat-tutor/
cd ~/.ollama/models/sat-tutor
ollama create sat-tutor -f Modelfile

# Run the model
ollama run sat-tutor
```

### Option 3: Local Gradio Interface

For a web interface locally:

```bash
cd spaces
pip install -r requirements.txt
python app.py
# Open http://localhost:7860
```

## Model Details

- **Base Model**: Gemma 3N (4B parameters)
- **Fine-tuning**: LoRA adapters with Unsloth AI
- **Fine-tuning Data**: GSM8K, RACE, OpenBookQA, and TruthfulQA datasets
- **Quantization**: Q8_0 for optimal performance
- **Context Length**: 4096 tokens

## Fine-Tuning Process

The model was fine-tuned using the following approach:

1. **Data Preparation**: Combined multiple educational datasets in ShareGPT format
2. **LoRA Training**: Used parameter-efficient fine-tuning with Unsloth AI
3. **Conversation Format**: Trained on multi-turn conversations for better interaction
4. **Quantization**: Converted to GGUF format for efficient inference

### Key Training Parameters:
- **LoRA Rank**: 8
- **LoRA Alpha**: 8
- **Learning Rate**: Optimized for 4-bit training
- **Context Length**: 1024 tokens during training

## Technical Requirements

### For Local Deployment:
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: ~8GB for the quantized model
- **Python**: 3.8+ for Gradio interface
- **Ollama**: For local Ollama deployment

### For Hugging Face Spaces:
- **Runtime**: CPU Basic (16GB RAM)
- **Model Size**: ~4GB quantized model
- **Dependencies**: Gradio, llama-cpp-python

## Usage Examples

```
User: "What is the area of a rectangle with length 8 and width 6?"
Assistant: "To find the area of a rectangle, multiply the length by the width.
Area = length × width
Area = 8 × 6 = 48 square units"
```

## 🙏 Acknowledgments

- **Unsloth AI** for their excellent [Gemma 3N fine-tuning notebook](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Gemma3N_(4B)-Conversational.ipynb)
- **Google** for the Gemma 3N base model and Google Colab Pro access
- **Hugging Face** for the Spaces platform and model hosting
