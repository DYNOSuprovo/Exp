import os
import streamlit as st
import google.generativeai as genai
import nltk
from nltk.tokenize import word_tokenize

# ---------------- Ensure NLTK Data is Available ----------------
nltk.download("punkt")

# ---------------- Load API Key from Streamlit Secrets ----------------
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("⚠️ API key is missing! Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ---------------- Pre-trained Q&A ----------------
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
income = st.slider("Monthly Income (₹)", 500, 50000, 25000)
expenses = {
    "rent": st.slider("Rent/Mortgage (₹)", 0, 20000, 10000),
    "food": st.slider("Food Expenses (₹)", 0, 15000, 5000),
    "transport": st.slider("Transport (₹)", 0, 5000, 2000),
    "entertainment": st.slider("Entertainment (₹)", 0, 5000, 1000),
    "savings": st.slider("Savings (₹)", 0, 20000, 5000),
}

# User inputs
user_question = st.text_input("Ask a budgeting question:")
user_expense_input = st.text_area("Describe any other expenses (optional)")

# Function to get pre-trained answer
def get_pretrained_answer(query):
    tokens = word_tokenize(query.lower())
    for q in pre_trained_qa:
        q_tokens = word_tokenize(q)
        if all(token in q_tokens for token in tokens):
            return pre_trained_qa[q]
    return None

# Function to get AI-generated advice
def get_gemini_advice(expenses, income, user_input=""):
    """Sends expense details to Gemini API for personalized financial advice."""
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

# Process user question
if user_question:
    answer = get_pretrained_answer(user_question)
    st.subheader("💡 Answer:")
    st.write(answer if answer else get_gemini_advice(expenses, income, user_question))

# AI Budget Advice Button
if st.button("Get AI Budget Advice"):
    advice = get_gemini_advice(expenses, income, user_expense_input)
    st.subheader("💡 AI Advice:")
    st.write(advice)
