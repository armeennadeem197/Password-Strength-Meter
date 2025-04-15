# 🔒 Advanced Multi-Feature Streamlit App

This is a powerful multi-functional Streamlit web application that combines the following features:

- 🔐 **Password Strength Checker**  
- 🔑 **Secure Password Generator**  
- 💭 **Passphrase Generator**  
- 😊 **Mood Tracker with Data Visualization**

---

## 🚀 Features

### 1. Password Strength Checker
- Analyzes passwords for length, complexity, and common vulnerabilities
- Gives visual strength feedback and improvement suggestions
- Calculates entropy and shows time-to-crack estimate
- Displays password hash using SHA-256

### 2. Password Generator
- Customizable length and character types (uppercase, lowercase, digits, special characters)
- Ensures strong and random password generation
- Also provides feedback and strength evaluation

### 3. Passphrase Generator
- Creates secure passphrases using words from a local `wordlist.txt` file

### 4. Mood Tracker
- Lets users log their daily mood and notes
- Stores mood history during the session
- Visualizes mood trends using interactive charts (Plotly)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
https://github.com/armeennadeem197/Password-Strength-Meter.git
cd app.py

```
2. Install Dependencies
Make sure you have Python installed, then run:
```
pip install -r requirements.txt

```
4. Run the App

   streamlit run app.py

🧰 Requirements
Python 3.7+

Streamlit

pandas

plotly

Install manually if needed:
pip install streamlit pandas plotly
