import os
import gradio as gr
from huggingface_hub import hf_hub_download

os.system("pip install llama-cpp-python==0.3.13")

REPO_ID = "VivekHaridas01/sat-tutor-gemma3n-gguf"
FILENAME = "model.gguf"

MODEL_PATH = os.environ.get("MODEL_PATH") or hf_hub_download(
    repo_id="VivekHaridas01/sat-tutor-gemma3n-gguf",
    filename="model.gguf",
    local_dir="models",
)


# Optional: sanity log
try:
    print(f"[boot] Using {MODEL_PATH} size={os.path.getsize(MODEL_PATH)/1e9:.2f} GB")
except Exception as e:
    print("[boot] stat failed:", e)

# CPU threads
os.environ.setdefault("OMP_NUM_THREADS", "2")

# Lazy import so the Space/host can boot the UI even if model is still being uploaded.
def load_llm(model_path: str):
    from llama_cpp import Llama
    # Keep settings conservative for CPU Spaces. Adjust as needed.
    return Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=int(os.environ.get("N_THREADS", "4")),
        n_gpu_layers=int(os.environ.get("N_GPU_LAYERS", "0")),  # 0 for pure CPU
        rope_scaling={"type": "dynamic", "factor": 1.0},
        verbose=True
    )

# Global singleton (loaded on first call)
_llm = None

def ensure_model_ready():
    global _llm
    if _llm is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Couldn't find GGUF model at {MODEL_PATH}. "
                "Upload your model file as 'model.gguf' or set MODEL_PATH env var."
            )
        _llm = load_llm(MODEL_PATH)
    return _llm

SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT", "You are a helpful assistant.")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "512"))
TEMPERATURE = float(os.environ.get("TEMPERATURE", "0.2"))
TOP_P = float(os.environ.get("TOP_P", "0.95"))

def chat_fn(history, user_message):
    llm = ensure_model_ready()

    # Format the full prompt using OpenAI-style roles
    full_prompt = (
        f"System: {SYSTEM_PROMPT}\n" +
        "\n".join([
            f"User: {msg['content']}" if msg["role"] == "user" else f"Assistant: {msg['content']}"
            for msg in history
        ]) +
        f"\nUser: {user_message}\nAssistant:"
    )

    out = llm(
        prompt=full_prompt,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        stop=["\nUser:"],
        echo=False,
    )

    text = out["choices"][0]["text"].strip()

    # Append the messages using OpenAI-style roles
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": text})

    return history, ""


with gr.Blocks(title="Gemma 3N (GGUF) – Public Demo") as demo:
    gr.Markdown(
        """
        # Gemma 3N (GGUF) – Public Demo
        This demo runs **llama.cpp** via **llama-cpp-python** on CPU by default.
        Processing may take time since this is a Q8 model running on CPU.
        """
    )

    with gr.Row():
        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=450, type="messages")
            user_box = gr.Textbox(label="Your message")
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear")

        with gr.Column(scale=1):
            gr.Markdown("### Settings")
            sys_prompt = gr.Textbox(
                value=SYSTEM_PROMPT, label="System Prompt", lines=4
            )
            max_tokens = gr.Slider(64, 2048, value=MAX_TOKENS, step=32, label="Max tokens")
            temperature = gr.Slider(0.0, 1.5, value=TEMPERATURE, step=0.05, label="Temperature")
            top_p = gr.Slider(0.1, 1.0, value=TOP_P, step=0.05, label="Top P")

    def on_change_settings(sp, mt, temp, tp):
        global SYSTEM_PROMPT, MAX_TOKENS, TEMPERATURE, TOP_P
        SYSTEM_PROMPT, MAX_TOKENS, TEMPERATURE, TOP_P = sp, int(mt), float(temp), float(tp)

    # Wire up actions
    send_btn.click(
        chat_fn,
        inputs=[chatbot, user_box],
        outputs=[chatbot, user_box],
    )
    clear_btn.click(lambda: [], None, chatbot)

    # Apply settings live
    sys_prompt.change(on_change_settings, [sys_prompt, max_tokens, temperature, top_p], None)
    max_tokens.change(on_change_settings, [sys_prompt, max_tokens, temperature, top_p], None)
    temperature.change(on_change_settings, [sys_prompt, max_tokens, temperature, top_p], None)
    top_p.change(on_change_settings, [sys_prompt, max_tokens, temperature, top_p], None)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", "7860")))