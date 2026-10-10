from openai import OpenAI
from huggingface_hub import InferenceClient

GROQ_API_KEY = "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"
HF_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "openai/gpt-oss-20b"

def generate_with_groq(
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.8,
):

    client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_URL)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def generate_respose(
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.8
):
    print("Trying Groq...")
    groq_error = None

    try:
        return generate_with_groq(prompt, max_tokens, temperature)
    except Exception as e:
        groq_error = e
        print(f"Groq failed with error: {e}")       

def main():
    vauge = input("Enter a vague prompt: ")
    response = generate_respose(vauge)
    print(f"Response: {response}")  

if __name__ == "__main__":
    main()