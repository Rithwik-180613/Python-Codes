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

def run_activity():

    prompt = input("Enter your prompt: ")
    zero_shot = f"Please provide a detailed response to the following prompt:\n{prompt}\n\n"
    print("Using Zero Shot Learning approach...")
    print(generate_with_groq(zero_shot))

    one_shot = f"Example_1 :  Your name: Surya Meaning = Sun, {prompt} meaning ="
    print("Using One Shot Learning approach...")    
    print(generate_with_groq(one_shot))

    few_shot = f"Example_1 :  Your name: Surya Meaning = Sun, Example_2 : Your name: Badal Meaning = Cloud, {prompt} meaning ="
    print("Using Few Shot Learning approach...")
    print(generate_with_groq(few_shot))

if __name__ == "__main__":
    run_activity()

