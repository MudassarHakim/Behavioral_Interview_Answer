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
You are a behavioral interview coach specializing in helping candidates prepare for interviews using the STAR (Situation, Task, Action, Result) method. When I provide you with a question and a candidate's answer, your task is to format the response according to the STAR method.

Please structure your response as follows:

- **Situation**: Describe the context or background of the scenario related to the question.
- **Task**: Explain the specific challenge or responsibility the candidate faced.
- **Action**: Detail the actions the candidate took to address the task.
- **Result**: Summarize the outcomes of those actions, including any successes, learnings, or impacts.

Input:
Question: {question}  
Candidate's Answer: {answer}  

Respond using the format above to help clarify the candidate's response and highlight their skills effectively.
"""
                response = model.generate_content(prompt)
                st.markdown("### ⭐ STAR-Formatted Answer")
                st.write(response.text)

        # --- Evaluate Answer ---
        if eval_clicked and answer:
            with st.spinner("Scoring your answer..."):
                eval_prompt = f"""
You are a senior hiring manager tasked with evaluating a behavioral interview response. Please evaluate the following candidate answer based on the scoring criteria outlined below.

Answer:
{answer}

### Evaluation Criteria
Please assign a score from 1 to 5 for each of the following areas, along with a brief comment justifying your score:

1. **Situation Clarity**  
   - Score (1-5):  
   - Comments:

2. **Task Clarity**  
   - Score (1-5):  
   - Comments:

3. **Actions Taken** (leadership, initiative)  
   - Score (1-5):  
   - Comments:

4. **Results** (impact, metrics)  
   - Score (1-5):  
   - Comments:

5. **Alignment with Engineering Manager Role**  
   - Score (1-5):  
   - Comments:

6. **Communication Clarity**  
   - Score (1-5):  
   - Comments:

### Final Assessment
- **Overall Score**: X / 30

Please ensure that your feedback is concise and constructive, focusing on specific strengths and areas for improvement in the candidate's response.
"""
                eval_response = model.generate_content(eval_prompt)
                st.markdown("### 🧾 Evaluation Scorecard")
                st.write(eval_response.text)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.warning("Please enter your Gemini API key to begin.")
