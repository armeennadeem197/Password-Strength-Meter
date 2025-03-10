import streamlit as st
import pandas as pd
import re
import random
import string
import secrets
import hashlib
import base64
from datetime import datetime
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Advanced Multi-Feature App",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
def local_css():
    st.markdown("""
    <style>
        .main {
            padding: 1rem 1rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 2.5em;
            font-weight: bold;
        }
        .password-container, .mood-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .header-style {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .subheader-style {
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        .highlight {
            background-color: #f6f6f6;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #4CAF50;
        }
        .tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted black;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 120px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -60px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
    </style>
    """, unsafe_allow_html=True)

# Password Strength Checker
def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase the length to at least 8 characters.")
    
    # Character diversity
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"[@$!%*?&]", password): score += 1
    
    # Common patterns and dictionary checks
    common_passwords = ["password", "123456", "qwerty", "admin", "welcome", "password123"]
    if password.lower() in common_passwords:
        score = 0
        feedback.append("This is a commonly used password and very insecure.")
    
    # Sequential and repeated characters
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)", password.lower()):
        score -= 1
        feedback.append("Avoid sequential characters (like 'abc' or '123').")
    
    if re.search(r"(.)\1{2,}", password):
        score -= 1
        feedback.append("Avoid repeated characters (like 'aaa').")
    
    # Ensure score is within bounds
    score = max(0, min(score, 6))
    
    return score, feedback

# Password Generator
def generate_password(length=12, include_uppercase=True, include_lowercase=True, 
                     include_numbers=True, include_special=True):
    characters = ""
    
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation
    
    if not characters:
        characters = string.ascii_lowercase
    
    # Ensure at least one character from each selected type
    password = []
    if include_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if include_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if include_numbers:
        password.append(secrets.choice(string.digits))
    if include_special:
        password.append(secrets.choice(string.punctuation))
    
    # Fill the rest of the password
    remaining_length = length - len(password)
    password.extend(secrets.choice(characters) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

# Passphrase Generator
def generate_passphrase(num_words=4):
    with open("wordlist.txt", "r") as f:
        words = f.read().splitlines()
    return ' '.join(secrets.choice(words) for _ in range(num_words))

# Password Strength Meter UI
def password_strength_meter():
    st.markdown("<div class='header-style'>🔒 Advanced Password Strength Meter</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='password-container'>", unsafe_allow_html=True)
        password = st.text_input("Enter your password:", type="password")
        
        if password:
            score, feedback = check_password_strength(password)
            progress_percentage = min(score / 6, 1.0)
            
            # Visual strength indicator
            st.progress(progress_percentage)
            if score >= 5:
                st.success("✅ Strong password!")
            elif score >= 3:
                st.warning("⚠️ Medium strength password.")
            else:
                st.error("❌ Weak password!")
            
            # Password entropy calculation
            char_set_size = 0
            if re.search(r"[a-z]", password): char_set_size += 26
            if re.search(r"[A-Z]", password): char_set_size += 26
            if re.search(r"\d", password): char_set_size += 10
            if re.search(r"[@$!%*?&]", password): char_set_size += 32
            
            if char_set_size > 0:
                entropy = len(password) * (len(password) / 100) * (char_set_size / 10)
                st.write(f"**Estimated password entropy:** {entropy:.2f}")
                
                # Time to crack estimation
                if entropy < 40:
                    st.write("⚡ This password could be cracked instantly.")
                elif entropy < 60:
                    st.write("⏱️ This password might take a few hours to crack.")
                elif entropy < 80:
                    st.write("🕰️ This password might take a few days to crack.")
                else:
                    st.write("🔐 This password would take years to crack with current technology.")
            
            if feedback:
                st.markdown("<div class='subheader-style'>Suggestions to improve your password:</div>", unsafe_allow_html=True)
                for tip in feedback:
                    st.write(f"- {tip}")
                    
            # Password hash display
            st.markdown("<div class='subheader-style'>Password Hash:</div>", unsafe_allow_html=True)
            st.code(hashlib.sha256(password.encode()).hexdigest())
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='password-container'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader-style'>Password Generator</div>", unsafe_allow_html=True)
        
        length = st.slider("Password Length", min_value=8, max_value=32, value=16)
        include_uppercase = st.checkbox("Include Uppercase Letters", value=True)
        include_lowercase = st.checkbox("Include Lowercase Letters", value=True)
        include_numbers = st.checkbox("Include Numbers", value=True)
        include_special = st.checkbox("Include Special Characters", value=True)
        
        if st.button("Generate Password"):
            generated_password = generate_password(
                length, 
                include_uppercase, 
                include_lowercase, 
                include_numbers, 
                include_special
            )
            st.text_input("Generated Password:", value=generated_password)
            
            # Show strength of generated password
            gen_score, gen_feedback = check_password_strength(generated_password)
            progress_percentage = min(gen_score / 6, 1.0)
            
            if gen_score >= 5:
                st.success(f"Generated password strength: Strong ({gen_score}/6)")
            elif gen_score >= 3:
                st.warning(f"Generated password strength: Medium ({gen_score}/6)")
            else:
                st.error(f"Generated password strength: Weak ({gen_score}/6)")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Password tips
        st.markdown("<div class='password-container'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader-style'>Password Security Tips</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='highlight'>
        - Use a different password for each account
        - Consider using a password manager
        - Enable two-factor authentication when available
        - Change passwords regularly
        - Never share your passwords
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Mood Tracker
def mood_tracker():
    st.markdown("<div class='header-style'>😊 Mood Tracker</div>", unsafe_allow_html=True)
    
    # Load or initialize mood data
    if 'mood_data' not in st.session_state:
        st.session_state.mood_data = pd.DataFrame(columns=["Date", "Mood", "Notes"])
    
    # Input form
    with st.form("mood_form"):
        mood = st.selectbox("How are you feeling today?", ["😊 Happy", "😐 Neutral", "😢 Sad", "😡 Angry", "😴 Tired"])
        notes = st.text_area("Any notes about your mood?")
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            new_entry = pd.DataFrame({
                "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                "Mood": [mood],
                "Notes": [notes]
            })
            st.session_state.mood_data = pd.concat([st.session_state.mood_data, new_entry], ignore_index=True)
            st.success("Mood entry saved!")
    
    # Display mood history
    if not st.session_state.mood_data.empty:
        st.markdown("<div class='subheader-style'>Mood History</div>", unsafe_allow_html=True)
        st.dataframe(st.session_state.mood_data)
        
        # Visualizations
        mood_counts = st.session_state.mood_data["Mood"].value_counts().reset_index()
        mood_counts.columns = ["Mood", "Count"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(px.pie(mood_counts, values="Count", names="Mood", title="Mood Distribution"))
        with col2:
            st.plotly_chart(px.line(st.session_state.mood_data, x="Date", y="Mood", title="Mood Over Time"))
        
        # Export data
        st.markdown("<div class='subheader-style'>Export Data</div>", unsafe_allow_html=True)
        csv = st.session_state.mood_data.to_csv(index=False)
        st.download_button(
            label="Download Mood Data as CSV",
            data=csv,
            file_name="mood_data.csv",
            mime="text/csv"
        )

# Main app
def main():
    local_css()
    
    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #4CAF50;">🛠️ Multi-Tool App</h1>
        <p>Advanced features for everyday use</p>
    </div>
    """, unsafe_allow_html=True)
    
    # App selection
    option = st.sidebar.radio(
        "Choose a feature",
        ["Password Strength Meter", "Mood Tracker"]
    )
    
    # App info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="font-size: 0.8em;">
        <p>📅 Last updated: March 2025</p>
        <p>💻 Made with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content
    if option == "Password Strength Meter":
        password_strength_meter()
    elif option == "Mood Tracker":
        mood_tracker()

if __name__ == "__main__":
    main()