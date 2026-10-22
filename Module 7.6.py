from openai import OpenAI

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1"
GROQ_MODELS = ["openai/gpt-oss-20b"]

def generate_with_groq(
    prompt: str,
    max_tokens: int = 512,
    temperature: float = 0.8,
):
    
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Set it in your code."
        )

    client = OpenAI(
        api_key= GROQ_API_KEY,
        base_url= GROQ_URL,
    )

    response = client.chat.completions.create(
        model=GROQ_MODELS,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content or ""

def get_details():
    topic = input("Enter a topic to get details: ").strip()
    type = input("Enter the type of details you want (e.g., argumentative, explanation): ").strip()
    length = input("Enter the desired length of the response (e.g., 300 Words, 500 Words, 1000 Words): ").strip()
    target = input("Enter the target audience (e.g., students, professionals, general public): ").strip()

    intro_prompt = f"""
Write an introduction for an essay.
Topic: {topic}
Essay Type: {type}
Target Audience: {target}
Total Essay Length: {length}
words. Use clear and simple English.
"""
    response = generate_with_groq(intro_prompt, temperature=0.3, max_tokens=1024)
    print(f"\nInitial Introduction:\n{response}")
    if not response:
        print("No response generated. Exiting.")
        return

if __name__ == "__main__":
    get_details()
