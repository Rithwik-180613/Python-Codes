import re
import streamlit as st
from openai import OpenAI
from huggingface_hub import InferenceClient

PROVIDER = "groq"
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

def looks_incomplete(text):

    if not text or len(text.strip()) < 10:
        return True

    t = text.strip()

    if t.endswwith(("**", "*", "-", "--", ":", ",", "(", "[")):
        return True

    return False

def complete_answer(question, max_rounds=2):

    base_prompt = (
"You are a helpful AI Teaching Assistant. "
"Answer in simple English with clear explanations. "
"Use numbered points when appropriate. "
"Give examples wherever helpful. "
"Complete every sentence and point.\n\n"
f"Question: {question}"
)

    answer = generate_with_groq(
        base_prompt,
        temperature=0.3,
        max_tokens=1024
    )

    if answer.startswith("Error:"):
        return answer

    rounds = 0

    while rounds < max_rounds and looks_incomplete(answer):
        continuation_prompt = (
"Continue the following answer exactly "
"from where it stopped. "
"Do not repeat previous information. "
"Finish the incomplete explanation.\n\n"
f"Question: {question}\n\n"
f"Answer so far:\n{answer}\n\n"
"Continue:"
)

        more = generate_with_groq(
            continuation_prompt,
            temperature=0.3,
            max_tokens=1024
        )

        if not more or more.startswith("Error:"):
            break

        if more.strip() in answer:
            break

        answer = (
            answer.rstrip() + "\n" + more.lstrip()
        ).strip()

        rounds += 1

    return answer

def main():

    st.set_page_config(
        page_title="AI Teaching Assistant",
        page_icon="🎉",
        layout="centered"
    )

    st.title("🎉 AI Teaching Assistant")

    st.write(
        "Welcome! As questions about Python,"
        "Artificial Intelligence, Machine Learning,"
        "Computer Science, or any other subject."
    )

    st.markdown("---")

    user_input = st.text_input(
        "Enter your Question here:",
        placeholder="Example: What is Machine Learning?"
    )

    if st.button("Generate Answer"):

        if not user_input.strip():
            st.warning("Please enter a question.")

        else:
            st.markdown("### Your Question")
            st.write(user_input)

            with st.spinner("Generating answer..."):

                answer = complete_answer(user_input)

            if answer.startswith("Error:"):
                st.error(answer)
            else:
                st.markdown("### AI's Answer")
                st.markdown(answer)

    st.markdown("---")
    st.caption("Powered by Groq / Hugging Face")

if __name__ == "__main__":
    main()
