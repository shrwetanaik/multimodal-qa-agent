import requests
import json

def query_ollama(prompt: str, image_base64: str = None, model: str = "llava") -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
    }

    if image_base64:
        payload["images"] = [image_base64]

    try:
        response = requests.post(url, json=payload, stream=True)
        output = ""

        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    output += data.get("response", "")
                except json.JSONDecodeError:
                    continue

        return output.strip()
    except requests.exceptions.RequestException as e:
        return f"❌ Ollama request failed: {e}"
def query_ollama_text_only(prompt: str, model: str = "llama3") -> str:
    """
    Uses Ollama for prompt-only generation (e.g., to convert test steps to code).
    """
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt}

    try:
        response = requests.post(url, json=payload, stream=True)
        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    output += data.get("response", "")
                except json.JSONDecodeError:
                    continue
        return output.strip()
    except requests.exceptions.RequestException as e:
        return f"❌ Ollama request failed: {e}"
