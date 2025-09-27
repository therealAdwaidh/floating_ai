from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

# Load API key
# Always load .env located alongside this file, regardless of CWD
_here = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_here / ".env")

# Prefer NVIDIA_API_KEY, fall back to OPENAI_API_KEY for convenience
api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "No API key found. Set NVIDIA_API_KEY (or OPENAI_API_KEY) in a .env next to ai_client.py."
    )

# Initialize NVIDIA client
client = OpenAI(
    api_key=api_key,
    base_url="https://integrate.api.nvidia.com/v1",  # NVIDIA endpoint
)

# Available models
# Allow override via NVIDIA_MODEL env var. Must be a fully qualified model id.
env_model = os.getenv("NVIDIA_MODEL")
if env_model and env_model.strip():
    AVAILABLE_MODELS = [env_model.strip()]
else:
    # Fallback default that commonly exists in NVIDIA Integrate
    AVAILABLE_MODELS = [
        "nvidia/nemotron-3-8b-instruct",
    ]

RULES = """
You must strictly follow these rules for every response:

1. **Format**: Always respond in valid, well-structured Markdown.
2. **Clarity**: Use plain, simple language — avoid jargon unless defining it.
3. **Structure**: Organize with headers (#, ##), subheaders, bullet points, and numbered lists where helpful.
4. **Highlighting**: Use **bold** or *italic* for emphasis on important terms.
5. **Conciseness**: Keep answers to the point — no filler or repetition.
6. **Grammar & Tone**: Use correct grammar, spelling, punctuation, and maintain a consistent, professional, and friendly tone.
7. **Readability**: Use short paragraphs and line breaks for better flow.
8. **Examples**: Provide relevant examples, definitions, or tables when useful.
9. **Voice**: Use active voice instead of passive voice.
10. **Context**: Base your response on the provided chat history, your in-build persistent memory and personality settings.
11. **Focus**: Only answer the user's query — no extra commentary or unrelated information.
"""

def get_personality():
    try:
        with open("features/personality.txt", "r") as f:
            return f.read()
    except:
        return ""

def get_memory(maxchars=10000):
    try:
        with open("features/memory.txt", "r", encoding="utf-8") as f:
            memory = f.read()
        return memory[-maxchars:]
    except:
        return ""

def ai_response(user_query, model_index=0):
    """
    Generate AI response using NVIDIA Nemotron.
    model_index: index in AVAILABLE_MODELS (default 0)
    """
    personality = get_personality()
    memory = get_memory()

    prompt = f"""
{RULES}

Your Personality:
{personality}

Your Memory:
{memory}

User Query:
{user_query}
"""

    # Ensure valid model index
    if model_index < 0 or model_index >= len(AVAILABLE_MODELS):
        model_index = 0

    try:
        chat_completion = client.chat.completions.create(
            model=AVAILABLE_MODELS[model_index],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as error:
        # Surface underlying server message if present
        message = str(error)
        try:
            # OpenAI SDK HTTP errors often carry .response or .status_code
            response = getattr(error, "response", None)
            if response is not None:
                # response.json() may fail if text, so prefer text
                status = getattr(response, 'status_code', 'error')
                body_text = getattr(response, 'text', message)
                message = f"HTTP {status}: {body_text}"
        except Exception:
            pass
        # Add guidance for common 404 from wrong model id
        if "401" in message:
            message = (
                f"{message}\nHint: Authentication failed. Ensure your NVIDIA_API_KEY is valid, "
                "has access to the selected model, and your .env is in the Floating-AI folder."
            )
        if "404" in message:
            model_hint = (
                "Set NVIDIA_MODEL in your .env to a valid model id, e.g. "
                "NVIDIA_MODEL=meta/llama-3.1-8b-instruct or NVIDIA_MODEL=nvidia/nemotron-3-8b-instruct"
            )
            message = f"{message}\nHint: {model_hint}"
        raise RuntimeError(message)
