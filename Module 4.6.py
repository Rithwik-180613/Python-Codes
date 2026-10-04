import os
import requests
HF_API_KEY ="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"
DEFAULT_MODEL = "google/pegasus-xsum"

def summarize_text(text, model, headers):
    url = f"https://router.huggingface.co/hf-inference/models/{model}"
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 200,
            "min_length": 80,
            "do_sample": False
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        summary = data[0]['summary_text']
        return summary
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    text = input("Enter the text to summarize: ")
    model = input(f"Enter the model name (default: {DEFAULT_MODEL}): ") or DEFAULT_MODEL
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    summary = summarize_text(text, model, headers)
    print(f"Summary: {summary}")
