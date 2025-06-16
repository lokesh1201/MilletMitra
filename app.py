import streamlit as st
from trans import EnhancedFoodDataProcessor

# Initialize processor
processor = EnhancedFoodDataProcessor()

# Page Config
st.set_page_config(
    page_title="🌾 Food & Nutrition Explorer",
    page_icon="🥗",
    layout="wide"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .stRadio > label {
        font-weight: bold;
        font-size: 18px;
    }
    .stTextInput input {
        border-radius: 5px;
        padding: 8px;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Title and Header
st.title("🌿 Food & Nutrition Explorer")
st.markdown("Explore foods across languages, compare nutrition, get meal suggestions, and more!")

# Sidebar Navigation
with st.sidebar:
    st.image("https://via.placeholder.com/150x150?text=Logo", use_container_width=True)
    menu = st.radio("📌 Choose an action:", [
        "🔍 Search Food Item",
        "⚖️ Compare Nutrition",
        "🍽️ Meal Suggestions",
        "📂 Browse by Category"
    ])

# --- Search Section --- 
if menu == "🔍 Search Food Item":
    st.header("🔍 Search for a Food Item")
    st.markdown("Enter any name in English, Telugu, Hindi, Tamil, Kannada, or phonetic spelling.")

    query = st.text_input("Enter food name (e.g., 'Ragi', 'Raagulu', 'రాగులు'):")
    
    if st.button("🔎 Search"):
        if not query.strip():
            st.warning("Please enter a valid food name.")
        else:
            results = processor.get_food_info(query)
            if isinstance(results, dict) and "error" in results:
                st.error(results["error"])
            else:
                for info in results:
                    st.markdown(f"""
                        ### {info['english']} ({info['telugu']})
                        - **Hindi:** {info['hindi']}
                        - **Tamil:** {info['tamil']}
                        - **Kannada:** {info['kannada']}
                        - **Category:** {info['category']} | **Type:** {info['type']}
                        - **Health Benefits:** {', '.join(info['health_benefits'])}
                        - **Nutrition per 100g:** 
                    """)
                    st.json(info['nutrition_per_100g'])
                    st.markdown("---")

# --- Compare Nutrition Section ---
elif menu == "⚖️ Compare Nutrition":
    st.header("⚖️ Compare Nutritional Values")
    st.markdown("Enter up to 5 food names separated by commas (e.g., 'Ragi, Wheat, Oats').")

    food_list = st.text_input("Enter food names to compare:")
    
    if st.button("📊 Compare"):
        if not food_list.strip():
            st.warning("Please enter at least one food name.")
        else:
            names = [x.strip() for x in food_list.split(",") if x.strip()]
            comparison = processor.create_nutrition_comparison(names)
            if comparison:
                st.write("### 📊 Nutrition Comparison Table")
                st.table({
                    "Food": [c["name"] for c in comparison],
                    **{k: [c["nutrition"].get(k, "N/A") for c in comparison]
                       for k in set().union(*(c["nutrition"].keys() for c in comparison))}
                })
            else:
                st.error("No valid food items found for comparison.")

# --- Meal Suggestions Section ---
elif menu == "🍽️ Meal Suggestions":
    st.header("🍽️ Get Personalized Meal Suggestions")
    st.markdown("Select your dietary preference below.")

    pref = st.selectbox("Choose dietary preference:", ["Balanced", "Diabetic", "Weight Loss"])
    
    if st.button("🍴 Get Suggestions"):
        suggestions = processor.generate_meal_suggestions(pref.lower())
        st.markdown("### Here are your meal suggestions:")
        for meal, items in suggestions.items():
            with st.expander(meal.capitalize()):
                for item in items:
                    st.markdown(f"- **{item['english']} ({item['telugu']})**: {', '.join(item['benefits'])}")

# --- Browse by Category Section ---
elif menu == "📂 Browse by Category":
    st.header("📂 Browse Foods by Category")
    categories = ["Millet", "Pulse", "Grain", "Spice", "Seeds"]
    selected = st.selectbox("Select a category:", categories)
    
    if st.button("🧾 Show Foods"):
        foods = processor.get_category_foods(selected)
        if foods:
            st.markdown(f"### Foods under category **{selected}**:")
            for food in foods:
                st.markdown(f"- **{food['english']} ({food['telugu']})**: {', '.join(food['benefits'])}")
        else:
            st.warning("No foods found in this category.")

# Footer
st.markdown("---")
st.markdown('<div class="footer">© 2025 Food & Nutrition Explorer | Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)