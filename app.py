import streamlit as st
import google.generativeai as genai

# --- Page Setup ---
st.set_page_config(page_title="STAR Answer Formatter & Evaluator - Mudassar Hakim", layout="centered")

st.title("🌟 STAR Interview Answer Formatter")
st.markdown("""
Use this app to **structure your behavioral answers** using the STAR framework and get them **scored using a real interview rubric**.

> **🔐 Note**: Your Gemini API key is only used **temporarily in this session** and is **not stored or sent anywhere else**.

👉 [How to get your Gemini API Key](https://aistudio.google.com/app/apikey)  
""")

# --- Gemini API Key ---
api_key = st.text_input("Enter your Gemini API Key", type="password", help="Your key is only used during this session.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
# model = genai.GenerativeModel("gemini-1.5-pro")

        st.success("✅ Gemini API connected successfully!")

        # --- Inputs ---
        question = st.text_input("🎯 Behavioral Question")
        answer = st.text_area("✍️ Paste your raw behavioral answer")

        # --- Buttons ---
        col1, col2 = st.columns(2)
        with col1:
            format_clicked = st.button("🛠 Format with STAR")
        with col2:
            eval_clicked = st.button("📊 Evaluate Answer")

        # --- Format with STAR ---
        if format_clicked and question and answer:
            with st.spinner("Formatting with STAR..."):
                prompt = f"""
You are a behavioral interview coach. Format the following response using the STAR method.

Question: {question}

Candidate's Answer:
{answer}

Respond in this structure:
- **Situation**:
- **Task**:
- **Action**:
- **Result**:
"""
                response = model.generate_content(prompt)
                st.markdown("### ⭐ STAR-Formatted Answer")
                st.write(response.text)

        # --- Evaluate Answer ---
        if eval_clicked and answer:
            with st.spinner("Scoring your answer..."):
                eval_prompt = f"""
You are a senior hiring manager. Score the following behavioral answer using the criteria below.

Answer:
{answer}

Evaluation Criteria (score from 1 to 5 for each):
1. Situation clarity
2. Task clarity
3. Actions taken (leadership, initiative)
4. Results (impact, metrics)
5. Alignment with Engineering Manager role
6. Communication clarity

Respond like this:
- Situation: score (1-5) + comment
- Task: score + comment
- Action: score + comment
- Result: score + comment
- Alignment: score + comment
- Clarity: score + comment
- Overall Score: X/30
"""
                eval_response = model.generate_content(eval_prompt)
                st.markdown("### 🧾 Evaluation Scorecard")
                st.write(eval_response.text)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.warning("Please enter your Gemini API key to begin.")
