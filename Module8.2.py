import streamlit as st
from openai import OpenAI
from huggingface_hub import InferenceClient
import config
import io

GROQ_API_KEY = "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"
HF_API_KEY = "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"

GROQ_MODELS = ["openai/gpt-oss-20b"]
GROQ_URL = "https://api.groq.com/openai/v1"

HF_MODELS = ["meta-llama/Llama-3.1-8B-Instruct"]

def generate_groq_response(prompt, temperature=0.3, max_completions_tokens=512):
    key = getattr(config, "GROQ_API_KEY", None)

    if not key:
        return "Error: GROQ_API_KEY missing in config.py"

    client = OpenAI(api_key=key, base_url=GROQ_URL)
    last_error = None

    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
               max_completion_tokens=max_completions_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            last_error = e

    return f"Groq failed: {last_error}"


def generate_hf_response(prompt, temperature=0.3, max_tokens=512):
    key = getattr(config, "HF_API_KEY", None)

    if not key:
        return "Error: HF_API_KEY missing in config.py"

    last_error = None

    for model in HF_MODELS:
        try:
            client = InferenceClient(
                model=model,
                token=key
            )

            response = client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            last_error = e

    return f"Hugging Face failed: {last_error}"


# Choose which provider your app should use.
def generate_response(prompt, temperature=0.3, max_tokens=512):
    return generate_groq_response(
        prompt, temperature, max_tokens
    )


def export_bytes(history):
    text = "".join(
        f"Q{i}: {item['question']}\n"
        f"A{i}: {item['answer']}\n\n"
        for i, item in enumerate(history, 1)
    )
    return io.BytesIO(text.encode("utf-8"))


def setup_ui():
    st.set_page_config(
        page_title="AI Teaching Assistant",
        layout="centered"
    )
    st.title("🤖 AI Teaching Assistant")
    st.write(
        "Ask me anything about various subjects, "
        "and I'll provide an insightful answer."
    )

    st.session_state.setdefault("history", [])

    col_clear, col_export = st.columns([1, 2])

    with col_clear:
        if st.button("🧹 Clear Conversation"):
            st.session_state.history = []
            st.rerun()

    with col_export:
        if st.session_state.history:
            st.download_button(
                label="📤 Export Chat History",
                data=export_bytes(st.session_state.history),
                file_name="AI_Teaching_Assistant_Conversation.txt",
                mime="text/plain",
            )

    user_input = st.text_input("Enter your question here:")

    if st.button("Ask"):
        question = user_input.strip()

        if question:
            with st.spinner("Generating AI response..."):
                answer = generate_response(question)

            st.session_state.history.insert(
                0,
                {"question": question, "answer": answer}
            )
            st.rerun()
        else:
            st.warning("Please enter a question first.")

    st.markdown("### Conversation History")

    for i, item in enumerate(st.session_state.history, 1):
        st.markdown(f"**Q{i}: {item['question']}**")
        st.write(item["answer"])
        st.divider()


def main():
    setup_ui()


if __name__ == "__main__":
    main()