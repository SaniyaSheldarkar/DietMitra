# recipe.py
import google.generativeai as genai
import streamlit as st
import json

def generate_recipe(food_items, meal_type, name, dietary_preferences=None, allergies=None):
    """
    Generate a detailed recipe based on selected food items using Gemini API
    
    Parameters:
    food_items (list): List of food items to include in the recipe
    meal_type (str): 'breakfast', 'lunch', or 'dinner'
    name (str): User's name for personalization
    dietary_preferences (list): List of dietary preferences (vegan, vegetarian, etc.)
    allergies (list): List of food allergies to avoid
    
    Returns:
    dict: Recipe with title, ingredients, instructions, nutrition info and tips
    """
    
    # Get API key from Streamlit secrets
    try:
        api_key = st.secrets["gemini_apikey"]
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        return {"error": "Failed to configure API"}
    
    # Construct prompt for Gemini
    preferences_str = ", ".join(dietary_preferences) if dietary_preferences else "none"
    allergies_str = ", ".join(allergies) if allergies else "none"
    food_items_str = ", ".join(food_items)
    
    prompt = f"""
    Create a detailed, personalized Indian cuisine recipe for {name} using the following ingredients for their {meal_type}:
    {food_items_str}
    
    Consider these dietary preferences: {preferences_str}
    Avoid these allergens: {allergies_str}
    
    Generate a comprehensive recipe with these sections:
    1. Recipe Title: Create a creative, appetizing name for this Indian {meal_type} dish
    2. Introduction: A brief, personalized welcome message to {name} explaining the dish's benefits
    3. Preparation Time: Realistic prep time, cooking time, and total time in minutes
    4. Servings: How many people this recipe serves
    5. Ingredients: Detailed list with exact measurements for all ingredients (including those from the list above and add necessary Indian spices/extras)
    6. Instructions: Step-by-step cooking directions in numbered format, be specific about Indian cooking techniques
    7. Nutrition Information: Include calories, protein, carbs, fat, fiber per serving
    8. Chef's Tips: 2-3 practical tips to enhance the recipe or make preparation easier with authentic Indian flavors
    9. Variations: 1-2 simple variations to modify the recipe for different tastes while maintaining Indian character
    
    Format your response in markdown with clear section headers.
    Make the recipe realistic and executable by a home cook.
    Keep the total cooking time under 40 minutes for breakfast, under 60 minutes for lunch/dinner.
    Ensure all main ingredients from the provided list are used in the recipe.
    Use traditional Indian spices and cooking methods where appropriate.
    Use a warm, encouraging tone throughout.
    """
    
    try:
        # Call Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text'):
            return {"recipe": response.text}
        else:
            return {"error": "Failed to generate recipe"}
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return {"error": f"Failed to generate recipe: {str(e)}"}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_recipe(food_items, meal_type, name, dietary_preferences=None, allergies=None):
    """Cached wrapper for generate_recipe"""
    return generate_recipe(food_items, meal_type, name, dietary_preferences, allergies)