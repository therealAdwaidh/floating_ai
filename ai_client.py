import requests
import json
import os
from dotenv import load_dotenv
from pathlib import Path


# Load API key
_here = Path(__file__).resolve().parent
load_dotenv(dotenv_path=_here / ".env")

# Get OpenRouter API key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("No API key found. Set OPENROUTER_API_KEY in a .env next to ai_client.py.")

# Available models
AVAILABLE_MODELS = [
    "nvidia/nemotron-nano-9b-v2:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "microsoft/phi-3-mini-128k-instruct:free"
]

def ai_response(query, model_index=0):
    """
    Send a query to the AI and return the response.
    
    Args:
        query (str): The user's question/message
        model_index (int): Index of the model to use from AVAILABLE_MODELS
    
    Returns:
        str: The AI's response
    """
    try:
        # Select model
        model = AVAILABLE_MODELS[model_index] if model_index < len(AVAILABLE_MODELS) else AVAILABLE_MODELS[0]
        
        # Make API request
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/your-repo",  # Optional
                "X-Title": "Floating AI",  # Optional
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ],
            })
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        return f"Error making API request: {str(e)}"
    except KeyError as e:
        return f"Error parsing API response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"