from openai import OpenAI

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1"

PROVIDER = "groq"
GROQ_MODELS ="openai/gpt-oss-20b"


def generate_with_groq(
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.8,
):

    client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_URL)
    response = client.chat.completions.create(
        model= GROQ_MODELS,
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def reinforcement_learning():
    prompt = input("Enter your prompt: ")
    initial_response = generate_with_groq(prompt)
    print(f"Initial response: {initial_response}")

    feedback = input("Provide feedback on the response (e.g., 'good', 'bad', 'needs more detail'): ")
    improved_prompt = f"""
Original user question:
{prompt}
Previous AI response:
{initial_response}
User feedback:
{feedback if feedback else "Improve clarity and accuracy."}
Rewrite the response based on the feedback.
Provide a clear, accurate, and improved answer.
Do not simply repeat the previous answer.
"""

    improved_response = generate_with_groq(improved_prompt)
    print(f"Improved response: {improved_response}")    


if __name__ == "__main__":
    reinforcement_learning()

