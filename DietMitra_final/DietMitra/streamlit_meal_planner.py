import streamlit as st
import pandas as pd
import google.generativeai as genai
import random
import time
from data import get_food_items
from recipe import get_recipe
from prompts import pre_prompt_b, pre_prompt_l, pre_prompt_d, pre_breakfast, pre_lunch, pre_dinner, end_text, \
    example_response_l, example_response_d, negative_prompt
import base64

# Import required libraries for pip installation at runtimefz
import subprocess
import sys

# Install required packages if needed
if 'packages_installed' not in st.session_state:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        st.session_state['packages_installed'] = True
    except Exception as e:
        st.error(f"Failed to install required packages: {e}")



GEMINI_API_KEY = st.secrets["gemini_apikey"]
ANTHROPIC_API_KEY = st.secrets["anthropic_apikey"]

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

UNITS_CM_TO_IN = 0.393701
UNITS_KG_TO_LB = 2.20462
UNITS_LB_TO_KG = 0.453592
UNITS_IN_TO_CM = 2.54

# Function to set background image and styling
def add_bg_and_styling():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=2940&auto=format&fit=crop");
             background-attachment: fixed;
             background-size: cover;
             background-position: center;
         }}
         
         /* Increase overall font size */
         body, p, li, label, .stTextInput, .stSelectbox, .stNumberInput {{
             font-size: 18px !important;
         }}
         
         h1 {{
             font-size: 42px !important;
         }}
         
         h2 {{
             font-size: 32px !important;
         }}
         
         h3 {{
             font-size: 26px !important;
         }}
         
         .stSubheader {{
             font-size: 24px !important;
         }}
         
         /* Card Styling */
         .card {{
             background-color: rgba(255, 255, 255, 0.95);
             border-radius: 15px;
             padding: 25px;
             margin-bottom: 25px;
             box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
             color: #333333;
         }}
         
         /* Section Cards */
         .section-card {{
             background-color: rgba(255, 255, 255, 0.95);
             border-radius: 15px;
             padding: 20px;
             margin-bottom: 20px;
             box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
             border-left: 5px solid #3498db;
         }}
         
         /* Header styling */
         .main-header {{
             color: #FFFFFF;
             text-shadow: 2px 2px 4px #000000;
             text-align: center;
             padding: 25px;
             margin-bottom: 25px;
             background-color: rgba(0, 0, 0, 0.6);
             border-radius: 15px;
         }}
         
         /* Tab styling */
         .tab-content {{
             background-color: rgba(255, 255, 255, 0.95);
             border-radius: 15px;
             padding: 20px;
             margin-top: 15px;
             color: #333333;
         }}
         
         .stTabs [data-baseweb="tab-list"] {{
             gap: 15px;
         }}
         
         .stTabs [data-baseweb="tab"] {{
             rgb(0 0 0 / 95%) !important
             border-radius: 8px 8px 0 0;
             padding: 8px 20px;
             border: none;
             font-size: 18px !important;
         }}
         
         .stTabs [aria-selected="true"] {{
             background-color: rgba(255, 255, 255, 0.95) !important;
             font-weight: bold;
         }}
         
         /* Input fields styling for better visibility */
         .stTextInput>div>div>input, .stNumberInput>div>div>input {{
             background-color: #ffffff !important;
             color: #000000 !important;
             font-size: 18px !important;
             border: 2px solid #3498db !important;
             padding: 5px 10px !important;
         }}
         
         /* Select and multiselect styling */
         .stSelectbox>div>div>div, .stMultiSelect>div>div>div {{
             background-color: #ffffff !important;
            color: #000000 !important;
             font-size: 18px !important;
             border: 2px solid #3498db !important;
         }}
         
         /* Labels for better visibility */
         .stTextInput label, .stNumberInput label, .stSelectbox label, .stMultiSelect label {{
             color: #FFFFFF !important;
             font-weight: bold !important;
             font-size: 20px !important;
             text-shadow: 1px 1px 2px #000000;
             margin-bottom: 8px !important;
         }}
         
         /* Section header */
         .section-header {{
             background-color: #7f4545;
             color: white;
             padding: 15px;
             border-radius: 10px;
             margin-bottom: 20px;
             font-size: 22px !important;
             font-weight: bold;
             text-align: center;
         }}
         
         /* Info boxes */
         .info-box {{
             background-color: rgba(52, 152, 219, 0.2);
             border-left: 5px solid #3498db;
             padding: 15px;
             border-radius: 5px;
             margin: 15px 0;
             font-size: 20px !important;
         }}
         
         /* Success boxes */
         .success-box {{
             background-color: rgba(46, 204, 113, 0.2);
             border-left: 5px solid #2ecc71;
             padding: 15px;
             border-radius: 5px;
             margin: 15px 0;
             font-size: 20px !important;
         }}
         
         /* Button styling */
         .stButton>button {{
             background-color: #27ae60;
             color: white;
             font-weight: bold;
             font-size: 20px !important;
             padding: 12px 20px;
             border-radius: 10px;
             border: none;
             box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
             transition: all 0.3s;
         }}
         
         .stButton>button:hover {{
             background-color: #2ecc71;
             box-shadow: 0 6px 10px rgba(0, 0, 0, 0.3);
             transform: translateY(-2px);
         }}
         
         /* Dataframe styling */
         .dataframe {{
             background-color: #ffffff !important;
             color: #333333 !important;
             font-size: 18px !important;
         }}
         
         /* Radio buttons and checkboxes */
         .stRadio label, .stCheckbox label {{
             color: #FFFFFF !important;
             font-size: 18px !important;
             text-shadow: 1px 1px 2px #000000;
         }}
         
         /* Expander */
         .streamlit-expanderHeader {{
             background-color: rgba(52, 152, 219, 0.2) !important;
             color: #FFFFFF !important;
             font-size: 20px !important;
             font-weight: bold !important;
             border-radius: 10px !important;
             padding: 10px !important;
             text-shadow: 1px 1px 2px #000000;
         }}
         
         .streamlit-expanderContent {{
             background-color: rgba(255, 255, 255, 0.9) !important;
             border-radius: 0 0 10px 10px !important;
             padding: 15px !important;
             color: #333333 !important;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Set page configuration
st.set_page_config(page_title="AI - Meal Planner", page_icon="🍴", layout="wide")

# Add background image and styling
add_bg_and_styling()

# Main header with custom styling
st.markdown('<div class="main-header"><h1>🍽️ AI Meal Planner</h1></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="card"><p>This is an AI-powered meal planner that creates personalized meal plans with detailed recipes based on your information, dietary preferences, and calorie needs.</p><p><em>Powered by Google Gemini</em></p></div>',
    unsafe_allow_html=True
)

# Create two columns for user input and plan display
col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    # Personal Information Card
   
    st.markdown('<div class="section-header">Personal Information</div>', unsafe_allow_html=True)
    
    name = st.text_input("Enter your name", placeholder="e.g., John")
    age = st.number_input("Enter your age", min_value=1, max_value=120, step=1, value=30)
    gender = st.radio("Gender:", ["Male", "Female"], horizontal=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Height & Weight Card
   # st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Height & Weight</div>', unsafe_allow_html=True)
    
    unit_preference = st.radio("Preferred units:", ["Metric (kg, cm)", "Imperial (lb, ft + in)"])

    if unit_preference == "Metric (kg, cm)":
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0)
        with col2:
            height = st.number_input("Height (cm)", min_value=1.0, value=170.0)
    else:
        col1, col2 = st.columns(2)
        with col1:
            weight_lb = st.number_input("Weight (lb)", min_value=1.0, value=154.0)
        
        # Use columns to align feet and inches inputs next to each other
        with col2:
            height_ft = st.number_input("Height (ft)", min_value=0, value=5)
            height_in = st.number_input("Height (in)", min_value=0.0, max_value=11.0, value=9.0)

        # Convert imperial to metric
        weight = weight_lb * UNITS_LB_TO_KG
        height = (height_ft * 12 + height_in) * UNITS_IN_TO_CM
    st.markdown('</div>', unsafe_allow_html=True)

    # Dietary Preferences Card
   # st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Dietary Preferences & Allergies</div>', unsafe_allow_html=True)
    
    dietary_preferences = st.multiselect(
        "Select your dietary preferences:",
        ["Vegetarian", "Vegan", "Pescatarian", "Keto", "Paleo", "Gluten-free", "Dairy-free", "Low-carb", "Mediterranean"]
    )

    allergies = st.multiselect(
        "Select your food allergies:",
        ["Peanuts", "Tree nuts", "Milk", "Eggs", "Fish", "Shellfish", "Wheat", "Soy", "Sesame"]
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Activity Level Card
    #st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Activity Level</div>', unsafe_allow_html=True)
    
    activity_level = st.select_slider(
        "Select your activity level:",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
        value="Moderately Active"
    )
    
    # Calculate BMR with activity factor
    def calculate_bmr(weight, height, age, gender, activity):
        # Base BMR calculation
        if gender == "Male":
            bmr = 9.99 * weight + 6.25 * height - 4.92 * age + 5
        else:
            bmr = 9.99 * weight + 6.25 * height - 4.92 * age - 161
        
        # Apply activity factor
        activity_factors = {
            "Sedentary": 1.2,
            "Lightly Active": 1.375,
            "Moderately Active": 1.55,
            "Very Active": 1.725,
            "Extremely Active": 1.9
        }
        
        return bmr * activity_factors[activity]

    bmr = calculate_bmr(weight, height, age, gender, activity_level)
    round_bmr = round(bmr, 2)
    
    st.markdown(f'<div class="info-box">Daily Calorie Needs: <strong>{round_bmr}</strong> calories</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Weight Management Card
    #st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Weight Management (Optional)</div>', unsafe_allow_html=True)
    
    weight_goal = st.radio("Weight goal:", ["Maintain", "Lose", "Gain"], horizontal=True)
    
    if weight_goal == "Lose":
        calorie_deficit = st.slider("Calorie deficit per day:", 200, 800, 500)
        round_bmr -= calorie_deficit
        st.markdown(f'<div class="success-box">Adjusted calories: <strong>{round(round_bmr, 2)}</strong></div>', unsafe_allow_html=True)
    elif weight_goal == "Gain":
        calorie_surplus = st.slider("Calorie surplus per day:", 200, 800, 500)
        round_bmr += calorie_surplus
        st.markdown(f'<div class="success-box">Adjusted calories: <strong>{round(round_bmr, 2)}</strong></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Plan Button Card
   # st.markdown('<div class="section-card">', unsafe_allow_html=True)
    if st.button("Generate Meal Plan", type="primary", use_container_width=True):
        st.session_state['generate_meal_plan'] = True
    st.markdown('</div>', unsafe_allow_html=True)

def knapsack(target_calories, food_groups):
    items = []
    for group, foods in food_groups.items():
        for item, calories in foods.items():
            items.append((calories, item))

    n = len(items)
    dp = [[0 for _ in range(target_calories + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(target_calories + 1):
            value, _ = items[i - 1]

            if value > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - value] + value)

    selected_items = []
    j = target_calories
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i - 1][j]:
            _, item = items[i - 1]
            selected_items.append(item)
            j -= items[i - 1][0]

    return selected_items, dp[n][target_calories]

# Update the session state model
if "model" not in st.session_state:
    st.session_state["model"] = "gemini-1.5-flash"

with col_output:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    if 'generate_meal_plan' in st.session_state and st.session_state['generate_meal_plan']:
        if not name or age <= 0 or (unit_preference == "Metric (kg, cm)" and (not weight or not height)) or (unit_preference == "Imperial (lb, ft + in)" and (not weight_lb or (height_ft == 0 and height_in == 0))):
            st.error("Please fill in all required information before generating a meal plan.")
        else:
            st.markdown(f'<div class="section-header"><h2>{name}\'s Personalized Meal Plan</h2></div>', unsafe_allow_html=True)
            
            with st.spinner("Generating your personalized meal plan..."):
                # Calculate calorie distribution for each meal
                calories_breakfast = round((round_bmr * 0.3), 2)  # 30% for breakfast
                calories_lunch = round((round_bmr * 0.4), 2)      # 40% for lunch
                calories_dinner = round((round_bmr * 0.3), 2)     # 30% for dinner
                
                # Generate dynamic food items based on user preferences and allergies
                food_items_breakfast = get_food_items("breakfast", dietary_preferences, allergies)
                food_items_lunch = get_food_items("lunch", dietary_preferences, allergies)
                food_items_dinner = get_food_items("dinner", dietary_preferences, allergies)
                
                # Generate meal items using knapsack algorithm
                meal_items_morning, cal_m = knapsack(int(calories_breakfast), food_items_breakfast)
                meal_items_lunch, cal_l = knapsack(int(calories_lunch), food_items_lunch)
                meal_items_dinner, cal_d = knapsack(int(calories_dinner), food_items_dinner)
            
            # Create tabs for each meal with custom styling
            st.markdown('<div class="tab-container">', unsafe_allow_html=True)
            breakfast_tab, lunch_tab, dinner_tab = st.tabs(["🍳 Breakfast", "🥗 Lunch", "🍲 Dinner"])
            
            with breakfast_tab:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.subheader("Breakfast Plan")
                col_b1, col_b2 = st.columns([1, 2])
                
                with col_b1:
                    st.markdown(f'<div class="info-box">Target Calories: <strong>{calories_breakfast}</strong></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="success-box">Total Calories: <strong>{cal_m}</strong></div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame({"Breakfast Items": meal_items_morning}), use_container_width=True)
                
                with col_b2:
                    with st.spinner("Generating breakfast recipe..."):
                        breakfast_recipe = get_recipe(meal_items_morning, "breakfast", name, dietary_preferences, allergies)
                        if "error" in breakfast_recipe:
                            st.error(breakfast_recipe["error"])
                        else:
                            st.markdown(breakfast_recipe["recipe"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with lunch_tab:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.subheader("Lunch Plan")
                col_l1, col_l2 = st.columns([1, 2])
                
                with col_l1:
                    st.markdown(f'<div class="info-box">Target Calories: <strong>{calories_lunch}</strong></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="success-box">Total Calories: <strong>{cal_l}</strong></div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame({"Lunch Items": meal_items_lunch}), use_container_width=True)
                
                with col_l2:
                    with st.spinner("Generating lunch recipe..."):
                        lunch_recipe = get_recipe(meal_items_lunch, "lunch", name, dietary_preferences, allergies)
                        if "error" in lunch_recipe:
                            st.error(lunch_recipe["error"])
                        else:
                            st.markdown(lunch_recipe["recipe"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            with dinner_tab:
                st.markdown('<div class="tab-content">', unsafe_allow_html=True)
                st.subheader("Dinner Plan")
                col_d1, col_d2 = st.columns([1, 2])
                
                with col_d1:
                    st.markdown(f'<div class="info-box">Target Calories: <strong>{calories_dinner}</strong></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="success-box">Total Calories: <strong>{cal_d}</strong></div>', unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame({"Dinner Items": meal_items_dinner}), use_container_width=True)
                
                with col_d2:
                    with st.spinner("Generating dinner recipe..."):
                        dinner_recipe = get_recipe(meal_items_dinner, "dinner", name, dietary_preferences, allergies)
                        if "error" in dinner_recipe:
                            st.error(dinner_recipe["error"])
                        else:
                            st.markdown(dinner_recipe["recipe"])
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add a download button for the meal plan
           # st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="success-box" style="text-align: center; font-size: 22px !important;">Thank you for using our AI Meal Planner! Save your plan below.</div>', unsafe_allow_html=True)
            
            # Create a markdown export of all recipes
            def create_meal_plan_markdown():
                plan_md = f"# {name}'s Personalized Meal Plan\n\n"
                plan_md += f"Daily Calorie Needs: {round_bmr} calories\n\n"
                
                plan_md += "## 🍳 Breakfast\n"
                plan_md += f"Target Calories: {calories_breakfast}\n\n"
                if "recipe" in breakfast_recipe:
                    plan_md += breakfast_recipe["recipe"] + "\n\n"
                
                plan_md += "## 🥗 Lunch\n"
                plan_md += f"Target Calories: {calories_lunch}\n\n"
                if "recipe" in lunch_recipe:
                    plan_md += lunch_recipe["recipe"] + "\n\n"
                
                plan_md += "## 🍲 Dinner\n"
                plan_md += f"Target Calories: {calories_dinner}\n\n"
                if "recipe" in dinner_recipe:
                    plan_md += dinner_recipe["recipe"] + "\n\n"
                
                return plan_md
            
            meal_plan_md = create_meal_plan_markdown()
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Download Meal Plan",
                    data=meal_plan_md,
                    file_name=f"{name}_meal_plan.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 50px 0;">
                <h2>Welcome to your personalized meal planner</h2>
                <p style="font-size: 22px; color: white; text-shadow: 1px 1px 2px #000000;">Fill in your details on the left and click 'Generate Meal Plan' to get started</p>
                <div style="font-size: 80px; padding: 30px;">🍽️</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    footer:after {
                    content:'Built by Shravan and Team'; 
                    visibility: visible;
    	            display: block;
    	            position: relative;
    	            padding: 15px;
    	            top: 2px;
                    color: white;
                    text-align: center;
                    background-color: rgba(0, 0, 0, 0.6);
                    border-radius: 10px;
                    margin-top: 25px;
                    font-size: 18px;
    	            }
                    </style>
                    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
