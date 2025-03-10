import streamlit as st
import pandas as pd
import csv
import os
import datetime
import re
import random
import string
import plotly.express as px
import plotly.graph_objects as go
import hashlib
from datetime import timedelta
import base64
import io

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
        .password-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .mood-container {
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
    </style>
    """, unsafe_allow_html=True)

# Password Strength Checker with advanced features
def check_password_strength(password):
    score = 0
    feedback = []
    
    # Basic checks
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase the length to at least 8 characters.")
    
    if re.search(r"\\d", password):
        score += 1
    else:
        feedback.append("Add at least one number.")
    
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")
    
    if re.search(r"[@$!%*?&]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (@$!%*?&).")
    
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")
    
    # Advanced checks
    if len(password) >= 12:
        score += 1
    
    # Check for sequential characters
    if re.search(r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789)", password.lower()):
        score -= 1
        feedback.append("Avoid sequential characters (like 'abc' or '123').")
    
    # Check for repeated characters
    if re.search(r"(.)\\1{2,}", password):
        score -= 1
        feedback.append("Avoid repeated characters (like 'aaa').")
    
    # Check for common passwords
    common_passwords = ["password", "123456", "qwerty", "admin", "welcome", "password123"]
    if password.lower() in common_passwords:
        score = 0
        feedback.append("This is a commonly used password and very insecure.")
    
    # Ensure score is within bounds
    score = max(0, min(score, 6))
    
    return score, feedback

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
        password.append(random.choice(string.ascii_lowercase))
    if include_uppercase:
        password.append(random.choice(string.ascii_uppercase))
    if include_numbers:
        password.append(random.choice(string.digits))
    if include_special:
        password.append(random.choice(string.punctuation))
    
    # Fill the rest of the password
    remaining_length = length - len(password)
    password.extend(random.choice(characters) for _ in range(remaining_length))
    
    # Shuffle the password
    random.shuffle(password)
    return ''.join(password)

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
            if score >= 5:
                st.markdown(f"""
                <div style="
                    width: 100%;
                    height: 20px;
                    background: linear-gradient(to right, #ff0000 0%, #ffff00 50%, #00ff00 100%);
                    border-radius: 5px;
                    position: relative;
                ">
                    <div style="
                        position: absolute;
                        left: {progress_percentage * 100}%;
                        top: -10px;
                        transform: translateX(-50%);
                        font-size: 20px;
                    ">▼</div>
                </div>
                """, unsafe_allow_html=True)
                st.success("✅ Strong password!")
            elif score >= 3:
                st.markdown(f"""
                <div style="
                    width: 100%;
                    height: 20px;
                    background: linear-gradient(to right, #ff0000 0%, #ffff00 50%, #00ff00 100%);
                    border-radius: 5px;
                    position: relative;
                ">
                    <div style="
                        position: absolute;
                        left: {progress_percentage * 100}%;
                        top: -10px;
                        transform: translateX(-50%);
                        font-size: 20px;
                    ">▼</div>
                </div>
                """, unsafe_allow_html=True)
                st.warning("⚠️ Medium strength password.")
            else:
                st.markdown(f"""
                <div style="
                    width: 100%;
                    height: 20px;
                    background: linear-gradient(to right, #ff0000 0%, #ffff00 50%, #00ff00 100%);
                    border-radius: 5px;
                    position: relative;
                ">
                    <div style="
                        position: absolute;
                        left: {progress_percentage * 100}%;
                        top: -10px;
                        transform: translateX(-50%);
                        font-size: 20px;
                    ">▼</div>
                </div>
                """, unsafe_allow_html=True)
                st.error("❌ Weak password!")
            
            # Password entropy calculation
            char_set_size = 0
            if re.search(r"[a-z]", password): char_set_size += 26
            if re.search(r"[A-Z]", password): char_set_size += 26
            if re.search(r"\\d", password): char_set_size += 10
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

# Enhanced Mood Tracker
def mood_tracker():
    MOOD_FILE = "mood_log.csv"
    
    def load_mood_data():
        if not os.path.exists(MOOD_FILE):
            # Create file with headers if it doesn't exist
            with open(MOOD_FILE, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "Mood", "Intensity", "Factors", "Notes"])
            return pd.DataFrame(columns=["Date", "Time", "Mood", "Intensity", "Factors", "Notes"])
        
        # Read the CSV file
        df = pd.read_csv(MOOD_FILE, encoding="utf-8")
        
        # Check if the DataFrame is not empty and has the Date column
        if not df.empty and "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
        
        return df

    def save_mood_data(date, time, mood, intensity, factors, notes):
        with open(MOOD_FILE, "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, time, mood, intensity, factors, notes])
    
    def get_download_link(df, filename, text):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 {text}</a>'
        return href

    st.markdown("<div class='header-style'>🌟 Advanced Mood Tracker 🌟</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Log Mood", "View Analytics"])
    
    with tab1:
        st.markdown("<div class='mood-container'>", unsafe_allow_html=True)
        st.markdown("<div class='subheader-style'>How are you feeling today?</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", datetime.date.today())
            time_now = datetime.datetime.now().strftime("%H:%M")
            time_input = st.time_input("Time", datetime.datetime.strptime(time_now, "%H:%M").time())
            
            mood_options = {
                "Happy 😊": "😊",
                "Excited 🤩": "🤩",
                "Calm 😌": "😌",
                "Neutral 😐": "😐",
                "Tired 😴": "😴",
                "Anxious 😰": "😰",
                "Sad 😢": "😢",
                "Angry 😠": "😠",
                "Stressed 😫": "😫"
            }
            
            mood = st.selectbox("Select your mood", list(mood_options.keys()))
            intensity = st.slider("Intensity", 1, 10, 5, help="How strongly do you feel this emotion?")
            
        with col2:
            factors = st.multiselect(
                "What factors contributed to this mood?",
                ["Work", "Relationships", "Health", "Weather", "Sleep", "Exercise", 
                 "Food", "Social Media", "News", "Finances", "Family", "Other"]
            )
            factors_str = ", ".join(factors) if factors else "None specified"
            
            notes = st.text_area("Notes (optional)", height=150, 
                                help="Add any additional thoughts or context about your mood")
            
        if st.button("Log Mood", key="log_mood_button"):
            save_mood_data(date, time_input.strftime("%H:%M"), mood, intensity, factors_str, notes)
            st.success(f"✅ Mood logged Successfully for {date} at {time_input.strftime('%H:%M')}!")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        data = load_mood_data()
        
        if data.empty or len(data) <= 1:
            st.info("Not enough mood data to display analytics. Please log your mood first.")
        else:
            st.markdown("<div class='mood-container'>", unsafe_allow_html=True)
            
            # Data preparation - FIXED: Added checks to prevent KeyError
            if "Date" in data.columns:
                # Date is already converted to datetime in load_mood_data function
                if "Time" in data.columns:
                    data["DateTime"] = pd.to_datetime(data["Date"].astype(str) + " " + data["Time"])
                
                if "Mood" in data.columns:
                    data["Mood_Only"] = data["Mood"].apply(lambda x: x.split()[0])
                
                # Date range filter
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start Date", data["Date"].min())
                with col2:
                    end_date = st.date_input("End Date", data["Date"].max())
                
                filtered_data = data[(data["Date"] >= pd.Timestamp(start_date)) & 
                                    (data["Date"] <= pd.Timestamp(end_date))]
                
                if filtered_data.empty:
                    st.warning("No data available for the selected date range.")
                else:
                    # Download option
                    st.markdown(get_download_link(filtered_data, "mood_data.csv", 
                                                "Download Mood Data"), unsafe_allow_html=True)
                    
                    # Mood distribution
                    if "Mood" in filtered_data.columns:
                        st.markdown("<div class='subheader-style'>📊 Mood Distribution</div>", unsafe_allow_html=True)
                        mood_counts = filtered_data["Mood"].value_counts().reset_index()
                        mood_counts.columns = ["Mood", "Count"]
                        
                        fig = px.pie(mood_counts, values="Count", names="Mood", 
                                    title="Mood Distribution", hole=0.4)
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Mood over time
                    if "Mood" in filtered_data.columns and "DateTime" in filtered_data.columns:
                        st.markdown("<div class='subheader-style'>📈 Mood Trends Over Time</div>", unsafe_allow_html=True)
                        
                        # Create a mapping of moods to numeric values for the line chart
                        mood_mapping = {
                            "Happy 😊": 5,
                            "Excited 🤩": 5,
                            "Calm 😌": 4,
                            "Neutral 😐": 3,
                            "Tired 😴": 2,
                            "Anxious 😰": 2,
                            "Sad 😢": 1,
                            "Angry 😠": 1,
                            "Stressed 😫": 1
                        }
                        
                        filtered_data["Mood_Value"] = filtered_data["Mood"].map(mood_mapping)
                        
                        # Line chart for mood over time
                        fig = px.line(filtered_data, x="DateTime", y="Mood_Value", 
                                    title="Mood Trend Over Time",
                                    labels={"Mood_Value": "Mood (Higher is Better)", "DateTime": "Date & Time"})
                        
                        # Add markers for each data point
                        fig.update_traces(mode="lines+markers", marker=dict(size=10))
                        
                        # Add a hover template to show the actual mood
                        fig.update_traces(
                            hovertemplate="<b>Date:</b> %{x|%Y-%m-%d %H:%M}<br>" +
                                        "<b>Mood:</b> %{text}<br>" +
                                        "<b>Intensity:</b> %{customdata}",
                            text=filtered_data["Mood"],
                            customdata=filtered_data["Intensity"]
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Intensity analysis
                    if "Intensity" in filtered_data.columns and "Mood" in filtered_data.columns:
                        st.markdown("<div class='subheader-style'>🔥 Mood Intensity Analysis</div>", unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Average intensity by mood
                            avg_intensity = filtered_data.groupby("Mood")["Intensity"].mean().reset_index()
                            avg_intensity = avg_intensity.sort_values("Intensity", ascending=False)
                            
                            fig = px.bar(avg_intensity, x="Mood", y="Intensity", 
                                        title="Average Intensity by Mood",
                                        color="Intensity", color_continuous_scale="Viridis")
                            st.plotly_chart(fig, use_container_width=True)
                        
                        with col2:
                            # Intensity distribution
                            fig = px.histogram(filtered_data, x="Intensity", 
                                            title="Intensity Distribution",
                                            color_discrete_sequence=["#6495ED"])
                            fig.update_layout(bargap=0.1)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    # Factors analysis
                    if "Factors" in filtered_data.columns:
                        st.markdown("<div class='subheader-style'>🔍 Mood Factors Analysis</div>", unsafe_allow_html=True)
                        
                        # Extract all unique factors
                        all_factors = []
                        for factors_list in filtered_data["Factors"].dropna():
                            if factors_list != "None specified":
                                all_factors.extend([f.strip() for f in factors_list.split(",")])
                        
                        factor_counts = pd.Series(all_factors).value_counts().reset_index()
                        if not factor_counts.empty:
                            factor_counts.columns = ["Factor", "Count"]
                            
                            fig = px.bar(factor_counts, x="Factor", y="Count", 
                                        title="Common Mood Factors",
                                        color="Count", color_continuous_scale="Viridis")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No mood factors have been recorded yet.")
                    
                    # Mood patterns
                    if "Time" in filtered_data.columns and "Mood_Value" in filtered_data.columns:
                        st.markdown("<div class='subheader-style'>🧩 Mood Patterns & Insights</div>", unsafe_allow_html=True)
                        
                        # Time of day analysis
                        filtered_data["Hour"] = pd.to_datetime(filtered_data["Time"]).dt.hour
                        
                        # Define time periods
                        def get_time_period(hour):
                            if 5 <= hour < 12:
                                return "Morning"
                            elif 12 <= hour < 17:
                                return "Afternoon"
                            elif 17 <= hour < 21:
                                return "Evening"
                            else:
                                return "Night"
                        
                        filtered_data["Time_Period"] = filtered_data["Hour"].apply(get_time_period)
                        
                        time_period_mood = filtered_data.groupby("Time_Period")["Mood_Value"].mean().reset_index()
                        time_period_order = ["Morning", "Afternoon", "Evening", "Night"]
                        time_period_mood["Time_Period"] = pd.Categorical(
                            time_period_mood["Time_Period"], 
                            categories=time_period_order, 
                            ordered=True
                        )
                        time_period_mood = time_period_mood.sort_values("Time_Period")
                        
                        fig = px.bar(time_period_mood, x="Time_Period", y="Mood_Value",
                                    title="Average Mood by Time of Day",
                                    color="Mood_Value", color_continuous_scale="Viridis")
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Generate insights
                        st.markdown("<div class='highlight'>", unsafe_allow_html=True)
                        
                        # Most common mood
                        if "Mood" in filtered_data.columns:
                            most_common_mood = filtered_data["Mood"].mode()[0]
                            st.write(f"📊 Your most common mood was **{most_common_mood}**")
                        
                        # Best time of day
                        if not time_period_mood.empty:
                            best_time = time_period_mood.loc[time_period_mood["Mood_Value"].idxmax()]["Time_Period"]
                            st.write(f"🌞 Your mood tends to be best during the **{best_time}**")
                        
                        # Mood improvement or decline
                        if len(filtered_data) >= 3 and "Mood_Value" in filtered_data.columns:
                            first_half = filtered_data.iloc[:len(filtered_data)//2]["Mood_Value"].mean()
                            second_half = filtered_data.iloc[len(filtered_data)//2:]["Mood_Value"].mean()
                            
                            if second_half > first_half:
                                st.write(f"📈 Your mood has been **improving** over this period")
                            elif second_half < first_half:
                                st.write(f"📉 Your mood has been **declining** over this period")
                            else:
                                st.write(f"📊 Your mood has been **stable** over this period")
                        
                        # Most impactful factor if available
                        if all_factors:
                            most_common_factor = pd.Series(all_factors).value_counts().index[0]
                            st.write(f"🔍 The factor most frequently affecting your mood was **{most_common_factor}**")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("The mood data format is incorrect. Please log a new mood entry to fix this issue.")
            
            st.markdown("</div>", unsafe_allow_html=True)

# Main app
def main():
    local_css()
    
    # Sidebar
    st.sidebar.title("Navigation")
    
    # Add app logo/header to sidebar
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
    
    # Theme selector
    theme = st.sidebar.selectbox(
        "Choose Theme",
        ["Light", "Dark"],
        index=0
    )
    
    # Apply dark mode if selected
    if theme == "Dark":
        st.markdown("""
        <style>
            .stApp {
                background-color: #121212;
                color: #FFFFFF;
            }
            .password-container, .mood-container {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .highlight {
                background-color: #2D2D2D;
                border-left: 3px solid #4CAF50;
            }
        </style>
        """, unsafe_allow_html=True)
    
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