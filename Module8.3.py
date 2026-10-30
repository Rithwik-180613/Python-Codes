import html
import io
import streamlit as st
from openai import OpenAI

GROQ_API_KEY = ("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")
GROQ_URL = "https://api.groq.com/openai/v1"
GROQ_MODELS = [
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
]

def generate_groq_response(prompt, temperature=0.3, max_tokens=512):
   
    client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_URL)
    last_error = None

    for model in GROQ_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
               max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            last_error = e

    return f"Groq failed: {last_error}"


SYSTEM_PROMPT = """
You are a Math Mastermind.

For every math problem:
1. Show the solution step by step.
2. Explain the reasoning.
3. Give an alternate method if possible.
4. Verify the answer when possible.
5. Use proper mathematical notation.
6. Break complex problems into parts.

Format:
Problem → Steps → Final Answer → Concepts Used.

Be precise and educational.
"""


def math_generate(
    problem: str,
    level: str,
    temperature: float = 0.1,
    max_tokens: int = 1024,
) -> str:

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Math Problem ({level}): {problem}"
    )

    return generate_groq_response(
        prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )


def export_txt(history):
    txt = "\n\n".join(
        f"Q{i}: {item['q']}\nA{i}: {item['a']}"
        for i, item in enumerate(history, 1)
    )

    return io.BytesIO(txt.encode("utf-8"))


def setup_ui():
    st.set_page_config(
        page_title="Math Mastermind",
        page_icon="🧮",
        layout="centered",
    )

    st.title("🧮 Math Mastermind")
    st.write(
        "Solve math problems with detailed, "
        "step-by-step explanations."
    )

    with st.expander("📌 Examples"):
        st.markdown(
            '- Algebra: "Solve 2x² + 5x − 3 = 0"\n'
            '- Calculus: "Derivative of sin(x²) + ln(x)"\n'
            '- Geometry: "Area of triangle (0,0),(3,4),(6,0)"\n'
            '- Probability: "P(sum=7 with two dice)"'
        )

    st.session_state.setdefault("history", [])
    st.session_state.setdefault("k", 0)

    col1, col2 = st.columns([1, 2])

    if col1.button("🗑️ Clear"):
        st.session_state.history = []
        st.rerun()

    if st.session_state.history:
        col2.download_button(
            "📄 Export",
            data=export_txt(st.session_state.history),
            file_name="Math_Mastermind_Solutions.txt",
            mime="text/plain",
        )

    with st.form("math_form", clear_on_submit=True):
        question = st.text_area(
            "📝 Enter your math problem:",
            height=100,
            placeholder="Example: Solve x² + 5x + 6 = 0",
            key=f"q_{st.session_state.k}",
        )

        level = st.selectbox(
            "Level",
            ["Basic", "Intermediate", "Advanced"],
            index=1,
        )

        solve = st.form_submit_button(
            "🧠 Solve",
            use_container_width=True,
        )

        if solve:
            if not question.strip():
                st.warning("⚠️ Enter a problem first.")
            else:
                with st.spinner("Solving..."):
                    answer = math_generate(
                        question.strip(),
                        level,
                    )

                st.session_state.history.insert(
                    0,
                    {
                        "q": question.strip(),
                        "a": answer,
                        "lvl": level,
                    },
                )

                st.session_state.k += 1
                st.rerun()

    if not st.session_state.history:
        return

    st.markdown("### 🧾 Solution History (Latest First)")

    st.markdown(
        """
        <style>
        .box {
            max-height: 500px;
            overflow-y: auto;
            border: 2px solid #4CAF50;
            padding: 12px;
            background: #f7fbff;
            border-radius: 10px;
        }
        .q {
            font-weight: 700;
            color: #2E7D32;
            margin-top: 12px;
            overflow-wrap: anywhere;
        }
        .lvl {
            display: inline-block;
            background: #FF9800;
            color: #fff;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 8px;
        }
        .a {
            white-space: pre-wrap;
            overflow-wrap: anywhere;
            color: #1B5E20;
            background: #fff;
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #4CAF50;
            margin: 6px 0 14px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    content = ['<div class="box">']

    for i, item in enumerate(
        st.session_state.history, 1
    ):
        question = html.escape(str(item["q"]))
        answer = html.escape(str(item["a"]))
        level = html.escape(str(item["lvl"]))

        content.append(
            f'<div class="q">Q{i}: {question}'
            f'<span class="lvl">{level}</span></div>'
        )

        content.append(
            f'<div class="a">{answer}</div>'
        )

    content.append("</div>")

    st.markdown(
        "".join(content),
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    setup_ui()
