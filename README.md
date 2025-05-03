# 🥗 DietMitra: Personalized Meal Planning App

**DietMitra** is an AI-driven web application that generates personalized meal plans based on a user's caloric needs and food preferences. It leverages powerful large language models and an intuitive UI to create engaging and health-focused meal suggestions.

---

## 🚀 Features

* 🔢 **Calorie Calculation**
  Automatically calculates daily calorie requirements based on user input like age, weight, height, and gender.

* 🥘 **Customized Meal Plans**
  Generates balanced meal plans for breakfast, lunch, and dinner using selected food categories and preferences.

* 🚫 **Food Restrictions**
  Users can specify allergies or dietary restrictions to avoid certain ingredients.

* 🤖 **AI-Powered Creativity**
  Uses **Meta-Llama-3-70B** to create unique and engaging meal names and descriptions.

* 🖥️ **Interactive Streamlit UI**
  Built with **Streamlit** for real-time interactivity and a clean interface.

* 📊 **Efficient Data Management**
  Handles food data and processing using **Pandas**.

---

## 🛠 Tech Stack

* **Python** – Core application logic
* **Streamlit** – Frontend user interface
* **Pandas** – Data manipulation and filtering
* **Meta-Llama-3-70B** – AI text generation
* **Gemini API (Google)** – AI integration (Gemini 1.5 Flash)
* **Streamlit Cloud** – Hosting platform

---

## 🔐 API Key Setup

To protect your API key, use Streamlit's secrets management:

1. Create a `.streamlit/secrets.toml` file in the root of your project.
2. Add your API key:

   ```toml
   openai_apikey = "YOUR_ACTUAL_API_KEY"
   gemini_apikey = "YOUR_ACTUAL_GEMINI_KEY"
   ```

---

## 🛠️ Setup Instructions

### 1. Create and activate virtual environment

```bash
# For Windows
python -m venv .venv
.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

---

## 🌐 Live Demo

🚀 [**Access the Streamlit App Here**](https://dietmitra-bysaniya.streamlit.app/)

