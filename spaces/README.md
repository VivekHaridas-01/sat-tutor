---
title: SAT Tutor (Gemma 3N)
emoji: 📚
colorFrom: indigo
colorTo: gray
sdk: gradio
app_file: app.py
pinned: false
---

# Gemma 3N (GGUF) – Public Demo

A minimal **Gradio** app that serves a local **GGUF** model via **llama-cpp-python** (llama.cpp).  
Perfect for hosting on **Hugging Face Spaces** or **Streamlit Cloud** for hackathon demos.

## Quick Start (Locally)

```bash
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
# Put your GGUF file next to app.py as: model.gguf
python app.py
# Open http://localhost:7860
```

## Hugging Face Spaces (No login for viewers)
1. Create a new **Space** (Python runtime is fine).
2. Upload these files: `app.py`, `requirements.txt`, `README.md`.
3. Add your model file as `model.gguf` (Large files should be committed via **Git LFS**).
4. Once the Space builds, it will expose a public URL you can share with judges.

> Tip: A 4B model in a 4-bit quantization usually runs ok on a CPU Space (latency a few seconds per reply).  
> If you need faster responses, switch the Space to a GPU runtime.

## Alternative: Download model at startup
Instead of shipping the big GGUF, host it on the Hugging Face Hub and download at app start:
```python
# add to app.py before load_llm()
from huggingface_hub import hf_hub_download
MODEL_PATH = os.environ.get("MODEL_PATH") or hf_hub_download(
    repo_id="YOUR_USERNAME/YOUR_REPO_WITH_GGUF",
    filename="model.gguf",
    local_dir=".",
)
```
Make sure the repo is **public** so the Space can fetch it without auth.

## Environment Variables
- `MODEL_PATH`: Path to GGUF file (defaults to `model.gguf`).
- `N_THREADS`: CPU threads for llama.cpp (default: 8).
- `N_GPU_LAYERS`: Keep `0` for pure CPU.
- `SYSTEM_PROMPT`, `MAX_TOKENS`, `TEMPERATURE`, `TOP_P`.

## Notes
- Ensure your finetune complies with the base model's license.
- Spaces "CPU Basic" usually has ~16GB RAM; a 4B 4-bit model fits comfortably.
- If you see "FileNotFoundError: model.gguf", upload your model or set `MODEL_PATH`.
