import streamlit as st
import google.generativeai as genai

# UI: Page config
st.set_page_config(page_title="STAR Answer Formatter for EM Interviews", layout="centered")

st.title("🌟 STAR Formatter & Evaluator")
st.subheader("Use Gemini to structure and evaluate your behavioral interview answer.")

# Step 1: Input Gemini API Key
api_key = st.text_input("🔐 Enter your Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

    # Step 2: Enter behavioral question and answer
    question = st.text_input("🎯 Enter the Behavioral Question")
    answer = st.text_area("✍️ Paste your raw behavioral answer")

    # Step 3: Actions
    if st.button("🛠 Format with STAR"):
        with st.spinner("Processing..."):
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"""
You are a behavioral interview coach. Format the following response using the STAR method.

Question: {question}

Candidate Answer:
{answer}

Provide the output in this structure:
- Situation:
- Task:
- Action:
- Result:
"""
            response = model.generate_content(prompt)
            st.markdown("### ⭐ STAR-Formatted Answer")
            st.write(response.text)

    if st.button("📊 Evaluate Answer"):
        with st.spinner("Scoring your answer..."):
            model = genai.GenerativeModel("gemini-pro")
            eval_prompt = f"""
You are a senior hiring manager. Score the following behavioral answer using the below parameters from 1 to 5 (5 being excellent).

Answer:
{answer}

Criteria:
1. Situation clarity
2. Task clarity
3. Actions taken (leadership, decision-making)
4. Results (impact, metrics)
5. Alignment to role (engineering manager)
6. Communication clarity

Respond in this format:
- Situation: score + comment
- Task: score + comment
- Action: score + comment
- Result: score + comment
- Alignment: score + comment
- Clarity: score + comment
- Overall Score: X/30
"""
            response = model.generate_content(eval_prompt)
            st.markdown("### 🧾 Evaluation Scorecard")
            st.write(response.text)
else:
    st.warning("Please enter your Gemini API key to continue.")

