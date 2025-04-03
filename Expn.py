import os
import streamlit as st
import google.generativeai as genai
import spacy

# ---------------- Ensure SpaCy Model is Installed ----------------
spacy_model = "en_core_web_sm"
if not spacy.util.is_package(spacy_model):
    os.system(f"python -m spacy download {spacy_model}")

# Load NLP Model
nlp = spacy.load(spacy_model)

# ---------------- Load API Key from Streamlit Secrets ----------------
api_key = st.secrets["GOOGLE_API_KEY"]

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API key is missing! Please add it in Streamlit Secrets.")

# ---------------- Pre-Trained Q&A ----------------
pre_trained_qa = {
    "how to save on groceries": "Try meal planning, bulk buying, and using discount coupons.",
    "how much should i save monthly": "A good rule is to save at least 20% of your income.",
    "how to reduce electricity bill": "Use energy-efficient appliances, unplug devices, and optimize usage.",
    "best way to track expenses": "Use budgeting apps or maintain an expense tracker.",
    "how to reduce transportation cost": "Use public transport, carpool, or opt for fuel-efficient vehicles."
}

# ---------------- Streamlit UI ----------------
st.title("💰 AI Expense Advisor (India Edition)")
st.write("Adjust your income and expenses to get budget advice.")

# Sliders for user input (INR instead of USD)
income = st.slider("Monthly Income (₹)", 500, 50000, 20000)
rent = st.slider("Rent/Mortgage (₹)", 0, 20000, 8000)
food = st.slider("Food Expenses (₹)", 0, 15000, 5000)
transport = st.slider("Transport (₹)", 0, 5000, 2000)
entertainment = st.slider("Entertainment (₹)", 0, 5000, 1000)
savings = st.slider("Savings (₹)", 0, 20000, 5000)

# User input for other expenses
user_expense_input = st.text_area("Describe any other expenses (optional)")
expenses = {
    "rent": rent,
    "food": food,
    "transport": transport,
    "entertainment": entertainment,
    "savings": savings
}

# User inputs a budgeting question
user_question = st.text_input("Ask a budgeting question:")

# ---------------- Function to Find Pre-Trained Answer ----------------
def get_pretrained_answer(user_query):
    """Checks if the user's question matches any pre-trained answers."""
    doc = nlp(user_query.lower())
    for q in pre_trained_qa:
        if all(token.text in q for token in doc):
            return pre_trained_qa[q]
    return None

# ---------------- Function to Get Advice from Gemini AI ----------------
def get_gemini_advice(expenses, income, user_input=""):
    """Sends expense details to Gemini API for analysis and personalized financial advice."""
    prompt = f"""
    My monthly income is ₹{income}. Here are my expenses: {expenses}.
    {user_input}
    Analyze my budget and suggest practical ways to save money without affecting my lifestyle.
    Provide specific, actionable tips.
    """
    try:
        response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error getting AI advice: {e}"

# ---------------- Handle User Question ----------------
if user_question:
    answer = get_pretrained_answer(user_question)
    if answer:
        st.subheader("💡 Pre-trained Answer:")
        st.write(answer)
    else:
        st.subheader("💡 AI Generated Answer:")
        st.write(get_gemini_advice(expenses, income, user_question))

# ---------------- Get AI Budget Advice Button ----------------
if st.button("Get AI Budget Advice"):
    advice = get_gemini_advice(expenses, income, user_expense_input)
    st.subheader("💡 AI Advice:")
    st.write(advice)
