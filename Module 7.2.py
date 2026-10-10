import time
from openai import OpenAI

GROQ_API_KEY = "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"
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


def temperature(
        prompt: str,
        max_tokens: int = 512,
):
    print("Trying Groq...")
    groq_error = None
    temp = [0.2, 0.5, 0.9]
    for t in temp:
        try:
            response = generate_with_groq(prompt, max_tokens, t)
            print(f"Temperature: {t}, Response: {response}")
        except Exception as e:
            groq_error = e
            print(f"Groq failed with error: {e}")

def various_responses(
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.3,):
    print("Trying Groq...")
    groq_error = None

    questions = [f"Explain more about this topic {prompt}", f"Explain this topic if I am a first calss student {prompt}"] 

    for question in questions:
        try:
            response = generate_with_groq(question, max_tokens, temperature)
            print(f"Question: {question}, Response: {response}")
        except Exception as e:
            groq_error = e
            print(f"Groq failed with error: {e}")

    

def main():
    prompt = input("Enter your prompt: ")
    # prompt = "Write a short story about a robot learning to love."
    max_tokens = 512

    print("\nTesting different temperatures:")
    temperature(prompt, max_tokens)
    various_responses(prompt, max_tokens, temperature=0.3)

if __name__ == "__main__":
    main()