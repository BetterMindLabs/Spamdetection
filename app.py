import streamlit as st
import re
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("🛡️ URL / SMS / Email Spam Checker")

st.markdown("""
Check if a message, email, or URL might be spam or phishing.  
Get detailed AI-powered advice on what to do next.
""")

# Input type
input_type = st.selectbox("Choose input type", ["URL", "SMS Text", "Email Content"])

# User input
user_text = st.text_area("Enter content to analyze")

def basic_heuristic_check(text):
    spam_keywords = ["free", "urgent", "click here", "win", "limited time", "act now", "verify account"]
    suspicious = False
    score = 0

    # Check for keywords
    for kw in spam_keywords:
        if kw.lower() in text.lower():
            score += 1

    # Check for many exclamation marks
    if text.count("!") > 3:
        score += 1

    # Check for all caps words
    if any(word.isupper() and len(word) > 4 for word in text.split()):
        score += 1

    # Check for suspicious shortened URLs
    if re.search(r"(bit\.ly|tinyurl|t\.co|goo\.gl)", text):
        score += 2

    suspicious = score >= 2
    return suspicious, score

if st.button("Analyze"):
    if not user_text.strip():
        st.error("Please enter some text or a URL first.")
    else:
        # Basic heuristic
        suspicious, score = basic_heuristic_check(user_text)

        st.subheader("⚡ Heuristic Result")
        st.write(f"Suspicion Score: {score}")
        st.write("Likely Suspicious: ✅ Yes" if suspicious else "❌ No")

        # Gemini analysis
        prompt = f"""
        Here is a user-submitted content to check for spam, phishing, or scam:

        Content: {user_text}

        Heuristic suspicion score: {score}
        Basic suspicion: {"Yes" if suspicious else "No"}

        Provide:
        - A short explanation of why this may or may not be spam or phishing.
        - Clear recommendations for the user (e.g., don't click, report, or safe to ignore).
        - Keep it simple and friendly.
        """

        with st.spinner("Consulting Gemini AI..."):
            response = model.generate_content(prompt)
            advice = response.text

        st.subheader("🤖 Gemini AI Recommendations")
        st.markdown(advice)

st.caption("🔍 Built with Python, Streamlit & Gemini API")
