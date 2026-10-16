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

def bias_mitigation():
   print("\nBias Mitigation Module")
   prompt = input("Enter a prompt to explore Bias: ")
   if not prompt.strip():
       print("No prompt provided. Exiting.")
       return

   initial_response = generate_with_groq(prompt, temperature=0.3, max_tokens=1024)
   print(f"\nInitial response:\n{initial_response}")

   modified_prompt = input("Modify the prompt to make it more neutral: ").strip()
   if modified_prompt:
       modified_response = generate_with_groq(
              modified_prompt, temperature=0.3, max_tokens=1024
       )
       print(f"\nModified response:\n{modified_response}")
   else:
       print("No modified prompt provided. Exiting.")

if __name__ == "__main__":
    bias_mitigation()

       

   