# SAT Tutor Model - Local Setup Guide

This guide will help you run the fine-tuned SAT Tutor model locally using Ollama.

## Prerequisites

- **Ollama** installed on your system
- **Git** (for cloning the repository)
- **Bash** (for running the setup script)

### Installing Ollama

**macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [https://ollama.ai/download](https://ollama.ai/download)

## Quick Setup

1. **Create the model directory:**
```bash
mkdir -p ~/.ollama/models/your_path
```

2. **Copy the model files:**
```bash
cp model.gguf ~/.ollama/models/your_path/
cp Modelfile ~/.ollama/models/your_path/
```

3. **Create the model:**
```bash
cd ~/.ollama/models/your_path
ollama create your_path -f Modelfile
```

## 📁 File Structure

After setup, your Ollama models directory should look like:
```
~/.ollama/models/
└── your_path/
      ├── Modelfile
      └── model.gguf
```

## Usage Examples

### Interactive Chat
```bash
ollama run your_path
```

### Single Question
```bash
ollama run your_path "What is the area of a rectangle with length 8 and width 6?"
```
