# data.py
import google.generativeai as genai
import json
import streamlit as st

# This function will use Gemini to generate food items dynamically
def generate_food_items(meal_type, dietary_preferences=None, allergies=None):
    """
    Generate food items for a specific meal type using Gemini API
    
    Parameters:
    meal_type (str): 'breakfast', 'lunch', or 'dinner'
    dietary_preferences (list): List of dietary preferences (vegan, vegetarian, etc.)
    allergies (list): List of food allergies to avoid
    
    Returns:
    dict: Nested dictionary of food categories and items with calorie values
    """
    
    # Get API key from Streamlit secrets
    try:
        api_key = st.secrets["gemini_apikey"]
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Error configuring Gemini API: {e}")
        # Return default food items if API fails
        return get_default_food_items(meal_type)
    
    # Construct prompt for Gemini
    preferences_str = ", ".join(dietary_preferences) if dietary_preferences else "none"
    allergies_str = ", ".join(allergies) if allergies else "none"
    
    prompt = f"""
    Generate a detailed, realistic food database for {meal_type} meal planning.
    
    Dietary preferences to consider: {preferences_str}
    Allergies to avoid: {allergies_str}
    
    Create a JSON structure with the following format:
    {{
        "category_name": {{
            "food_item": calorie_value,
            "food_item2": calorie_value,
            ...
        }},
        ...
    }}
    
    For {meal_type}, include these categories:
    """
    
    # Add specific categories based on meal type
    if meal_type == "breakfast":
        prompt += """
        - protein (eggs, yogurt, etc.)
        - whole_grains (bread, oatmeal, etc.)
        - fruits
        - vegetables
        - healthy_fats (nuts, seeds, etc.)
        - dairy or dairy alternatives
        - other (condiments, beverages, etc.)
        """
    elif meal_type == "lunch":
        prompt += """
        - protein (chicken, fish, tofu, etc.)
        - whole_grains (rice, quinoa, etc.)
        - vegetables
        - legumes
        - healthy_fats
        - dairy_or_dairy_alternatives
        - additional_toppings_condiments
        """
    else:  # dinner
        prompt += """
        - proteins
        - grains_and_starches
        - vegetables
        - legumes
        - healthy_fats
        - dairy_or_dairy_alternatives
        - sauces_and_condiments
        - herbs_and_spices
        """
    
    prompt += """
    For each food item, provide a realistic calorie value as an integer.
    Return ONLY the JSON structure with no additional text or explanation.
    """
    
    try:
        # Call Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text'):
            # Parse the response text as JSON
            try:
                # Extract just the JSON part (in case there's any extra text)
                json_text = response.text
                # Find the start and end of JSON
                start_idx = json_text.find('{')
                end_idx = json_text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_text = json_text[start_idx:end_idx]
                
                food_items = json.loads(json_text)
                return food_items
            except json.JSONDecodeError as e:
                st.error(f"Error parsing Gemini response: {e}")
                return get_default_food_items(meal_type)
        else:
            return get_default_food_items(meal_type)
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return get_default_food_items(meal_type)

# Default food items to use as fallback
def get_default_food_items(meal_type):
    """Return default food items if Gemini API fails"""
    if meal_type == "breakfast":
        return {
            "protein": {
                "eggs": 78,
                "greek_yogurt": 130,
                "cottage_cheese": 206,
                "turkey_slices": 104,
                "smoked_salmon": 117
            },
            "whole_grains": {
                "whole_wheat_bread": 79,
                "oatmeal": 150,
                "quinoa": 222,
                "whole_grain_cereal": 120,
                "granola": 494
            },
            "fruits": {
                "berries": 50,
                "bananas": 96,
                "apples": 52,
                "oranges": 62,
                "grapefruit": 52,
                "melon_slices": 30
            },
            "vegetables": {
                "spinach": 7,
                "tomatoes": 18,
                "avocado": 160,
                "bell_peppers": 25,
                "mushrooms": 15
            },
            "healthy_fats": {
                "nut_butter": 94,
                "nuts": 163,
                "chia_seeds": 58,
                "flaxseeds": 55,
                "avocado_slices": 50
            },
            "dairy": {
                "milk": 103,
                "cheese": 113,
                "yogurt": 150,
                "dairy-free_alternatives": 80
            },
            "other": {
                "honey": 64,
                "maple_syrup": 52,
                "coffee": 2,
                "jam": 49,
                "peanut_butter": 188,
                "cocoa_powder": 12
            }
        }
    elif meal_type == "lunch":
        return {
            "protein": {
                "grilled_chicken_breast": 165,
                "salmon_fillet": 206,
                "tofu": 144,
                "lean_beef": 176,
                "shrimp": 99
            },
            "whole_grains": {
                "brown_rice": 216,
                "quinoa": 222,
                "whole_wheat_pasta": 180,
                "barley": 270,
                "couscous": 176
            },
            "vegetables": {
                "leafy_greens": 10,
                "broccoli": 55,
                "cauliflower": 25,
                "carrots": 41,
                "bell_peppers": 31,
                "cucumbers": 16,
                "tomatoes": 18,
                "zucchini": 17
            },
            "legumes": {
                "chickpeas": 269,
                "lentils": 230,
                "black_beans": 227,
                "kidney_beans": 225,
                "edamame": 121
            },
            "healthy_fats": {
                "avocado": 234,
                "nuts": 160,
                "seeds": 160,
                "olive_oil": 119,
                "coconut_oil": 121
            },
            "dairy_or_dairy_alternatives": {
                "greek_yogurt": 130,
                "cottage_cheese": 206,
                "cheese": 113,
                "dairy-free_alternatives": 80
            },
            "additional_toppings_condiments": {
                "sliced_avocado": 50,
                "hummus": 27,
                "salsa": 20,
                "salad_dressings": 73,
                "herbs_and_spices": 0
            }
        }
    else:  # dinner
        return {
            "proteins": {
                "chicken_breast": 165,
                "salmon": 206,
                "beef_steak": 250,
                "tofu": 144,
                "shrimp": 84,
                "lentils": 116
            },
            "grains_and_starches": {
                "brown_rice": 216,
                "quinoa": 222,
                "sweet_potatoes": 180,
                "whole_wheat_pasta": 174,
                "couscous": 176,
                "barley": 193
            },
            "vegetables": {
                "broccoli": 55,
                "cauliflower": 25,
                "green_beans": 31,
                "asparagus": 27,
                "brussels_sprouts": 38,
                "carrots": 41,
                "zucchini": 17
            },
            "legumes": {
                "black_beans": 227,
                "chickpeas": 269,
                "kidney_beans": 333,
                "lentils": 353
            },
            "healthy_fats": {
                "avocado": 160,
                "olive_oil": 119,
                "nuts": 160,
                "seeds": 150
            },
            "dairy_or_dairy_alternatives": {
                "greek_yogurt": 59,
                "cheese": 113,
                "almond_milk": 40
            },
            "sauces_and_condiments": {
                "tomato_sauce": 32,
                "soy_sauce": 8,
                "balsamic_vinegar": 14,
                "mustard": 10,
                "salsa": 15,
                "guacamole": 50,
                "hummus": 27
            },
            "herbs_and_spices": {
                "basil": 22,
                "oregano": 5,
                "rosemary": 2,
                "thyme": 3,
                "cumin": 22,
                "paprika": 20,
                "garlic_powder": 9,
                "onion_powder": 7
            }
        }

# For caching purposes - to avoid regenerating the same data multiple times
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_food_items(meal_type, dietary_preferences=None, allergies=None):
    """Cached wrapper for generate_food_items"""
    return generate_food_items(meal_type, dietary_preferences, allergies)