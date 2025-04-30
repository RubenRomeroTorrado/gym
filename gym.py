import streamlit as st
import pandas as pd

# --- Inicializar registro si no existe ---
if "log" not in st.session_state:
    st.session_state["log"] = pd.DataFrame(columns=["Food", "Calories", "Protein", "Fat", "Carbs"])

# --- Funciones de cálculo ---
def calc_bmr(weight, height, age, sex):
    if sex == 'Male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calc_tdee(bmr, activity_factor):
    return bmr * activity_factor

def calc_macros(tdee, weight):
    protein_g = 1.9 * weight
    fat_g = (0.25 * tdee) / 9
    carbs_g = (tdee - (protein_g * 4 + fat_g * 9)) / 4
    return protein_g, fat_g, carbs_g

# --- Sidebar: Datos del usuario ---
st.sidebar.title("User Info")
weight = st.sidebar.number_input("Weight (kg)", 30, 200, 70)
height = st.sidebar.number_input("Height (cm)", 100, 220, 170)
age = st.sidebar.number_input("Age", 10, 100, 30)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
activity = st.sidebar.selectbox("Activity Level", [
    ("Sedentary (1.2)", 1.2),
    ("Light (1.375)", 1.375),
    ("Moderate (1.55)", 1.55),
    ("Active (1.725)", 1.725),
    ("Very Active (1.9)", 1.9)
])

# --- Calcular metas ---
bmr = calc_bmr(weight, height, age, sex)
tdee = calc_tdee(bmr, activity[1])
prot_goal, fat_goal, carb_goal = calc_macros(tdee, weight)

# --- Mostrar metas ---
st.title("RubensTracker Dashboard")





# --- Lista de alimentos predefinidos ---
predefined_foods = {
    "Chicken Breast (grilled)": {"Calories": 165, "Protein": 31, "Fat": 3.6, "Carbs": 0},
    "White Rice (cooked)": {"Calories": 130, "Protein": 2.7, "Fat": 0.3, "Carbs": 28},
    "Broccoli (boiled)": {"Calories": 35, "Protein": 2.4, "Fat": 0.4, "Carbs": 7.2},
    "Salmon (grilled)": {"Calories": 206, "Protein": 22, "Fat": 13, "Carbs": 0},
    "Oats (raw)": {"Calories": 389, "Protein": 16.9, "Fat": 6.9, "Carbs": 66.3},
    "Whole Egg": {"Calories": 143, "Protein": 12.6, "Fat": 9.5, "Carbs": 1.1},
    "Whole Wheat Bread": {"Calories": 247, "Protein": 13, "Fat": 4.2, "Carbs": 41},
    "Apple": {"Calories": 52, "Protein": 0.3, "Fat": 0.2, "Carbs": 14},
    "Banana": {"Calories": 89, "Protein": 1.1, "Fat": 0.3, "Carbs": 23},
    "Whole Milk": {"Calories": 61, "Protein": 3.2, "Fat": 3.3, "Carbs": 4.8},
    "Plain Yogurt": {"Calories": 59, "Protein": 10, "Fat": 0.4, "Carbs": 3.6},
    "Cheddar Cheese": {"Calories": 402, "Protein": 25, "Fat": 33, "Carbs": 1.3},
    "Cooked Pasta": {"Calories": 131, "Protein": 5, "Fat": 1.1, "Carbs": 25},
    "Boiled Potato": {"Calories": 87, "Protein": 1.9, "Fat": 0.1, "Carbs": 20},
    "Olive Oil": {"Calories": 884, "Protein": 0, "Fat": 100, "Carbs": 0},
    "Butter": {"Calories": 717, "Protein": 0.9, "Fat": 81, "Carbs": 0.1},
    "Almonds": {"Calories": 579, "Protein": 21, "Fat": 50, "Carbs": 22},
    "Walnuts": {"Calories": 654, "Protein": 15, "Fat": 65, "Carbs": 14},
    "Canned Tuna (in water)": {"Calories": 116, "Protein": 26, "Fat": 1, "Carbs": 0},
    "Cooked Turkey Breast": {"Calories": 135, "Protein": 30, "Fat": 1, "Carbs": 0},
    "Cooked Lentils": {"Calories": 116, "Protein": 9, "Fat": 0.4, "Carbs": 20},
    "Cooked Chickpeas": {"Calories": 164, "Protein": 8.9, "Fat": 2.6, "Carbs": 27},
    "Firm Tofu": {"Calories": 144, "Protein": 15, "Fat": 8, "Carbs": 3},
    "Boiled Spinach": {"Calories": 23, "Protein": 2.9, "Fat": 0.4, "Carbs": 3.6},
    "Raw Carrot": {"Calories": 41, "Protein": 0.9, "Fat": 0.2, "Carbs": 10},
    "Raw Tomato": {"Calories": 18, "Protein": 0.9, "Fat": 0.2, "Carbs": 3.9},
    "Raw Cucumber": {"Calories": 16, "Protein": 0.7, "Fat": 0.1, "Carbs": 3.6},
    "Red Bell Pepper": {"Calories": 31, "Protein": 1, "Fat": 0.3, "Carbs": 6},
    "Raw Onion": {"Calories": 40, "Protein": 1.1, "Fat": 0.1, "Carbs": 9.3},
    "Garlic (raw)": {"Calories": 149, "Protein": 6.4, "Fat": 0.5, "Carbs": 33},
    "Raw Mushrooms": {"Calories": 22, "Protein": 3.1, "Fat": 0.3, "Carbs": 3.3},
    "Zucchini": {"Calories": 17, "Protein": 1.2, "Fat": 0.3, "Carbs": 3.1},
    "Eggplant": {"Calories": 25, "Protein": 1, "Fat": 0.2, "Carbs": 6},
    "Romaine Lettuce": {"Calories": 17, "Protein": 1.2, "Fat": 0.3, "Carbs": 3.3},
    "Corn (boiled)": {"Calories": 96, "Protein": 3.4, "Fat": 1.5, "Carbs": 21},
    "Green Peas (cooked)": {"Calories": 84, "Protein": 5.4, "Fat": 0.4, "Carbs": 15},
    "Beetroot (boiled)": {"Calories": 44, "Protein": 1.7, "Fat": 0.2, "Carbs": 10},
    "Pumpkin (boiled)": {"Calories": 20, "Protein": 1, "Fat": 0.1, "Carbs": 5},
    "Black Beans (cooked)": {"Calories": 132, "Protein": 8.9, "Fat": 0.5, "Carbs": 24},
    "Greek Yogurt (plain)": {"Calories": 59, "Protein": 10, "Fat": 0.4, "Carbs": 3.6},
    "Low-fat Cottage Cheese": {"Calories": 98, "Protein": 11, "Fat": 4.3, "Carbs": 3.4},
    "Unsweetened Almond Milk": {"Calories": 15, "Protein": 0.6, "Fat": 1.2, "Carbs": 0.3},
    "Unsweetened Soy Milk": {"Calories": 33, "Protein": 3.3, "Fat": 1.6, "Carbs": 0.6}
    # Add more if needed
}


# --- Autocomplete-like UI (Using `st.text_input` with filtering) ---
st.subheader("Add Predefined Food")
search_term = st.text_input("Search food (start typing)")

# Filter the predefined foods based on the search term
filtered_foods = {food: data for food, data in predefined_foods.items() if search_term.lower() in food.lower()}

if filtered_foods:
    selected_food = st.selectbox("Select a food", list(filtered_foods.keys()))
    amount_predef = st.number_input("Amount consumed (g)", 1, 1000, 100)

    if st.button("Add Predefined Food"):
        if selected_food:
            data = filtered_foods[selected_food]
            factor = amount_predef / 100
            new_row = {
                "Food": selected_food,
                "Calories": data["Calories"] * factor,
                "Protein": data["Protein"] * factor,
                "Fat": data["Fat"] * factor,
                "Carbs": data["Carbs"] * factor
            }
            st.session_state["log"] = pd.concat([st.session_state["log"], pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"{selected_food} added.")
else:
    st.warning("No food found. Please type more characters or select a predefined one.")

# --- Registro de alimentos ---
st.subheader("Log Food (values per 100g)")
with st.form("food_form"):
    name = st.text_input("Food name")
    cal_100 = st.number_input("Calories per 100g", 0, 900, 0)
    prot_100 = st.number_input("Protein per 100g (g)", 0.0, 100.0, 0.0)
    fat_100 = st.number_input("Fat per 100g (g)", 0.0, 100.0, 0.0)
    carb_100 = st.number_input("Carbs per 100g (g)", 0.0, 100.0, 0.0)
    amount = st.number_input("Amount consumed (g)", 1, 1000, 100)
    submitted = st.form_submit_button("Add Food")

if "log" not in st.session_state:
    st.session_state["log"] = pd.DataFrame(columns=["Food", "Calories", "Protein", "Fat", "Carbs"])

if submitted and name and amount > 0:
    factor = amount / 100
    new_row = {
        "Food": name,
        "Calories": cal_100 * factor,
        "Protein": prot_100 * factor,
        "Fat": fat_100 * factor,
        "Carbs": carb_100 * factor
    }
    st.session_state["log"] = pd.concat(
        [st.session_state["log"], pd.DataFrame([new_row])], ignore_index=True
    )
# --- Eliminar alimento ---
st.subheader("Remove Food Entry")
if not st.session_state["log"].empty:
    food_options = [f"{i}: {row['Food']} ({int(row['Calories'])} cal)" for i, row in st.session_state["log"].iterrows()]
    selected = st.selectbox("Select an entry to remove", options=food_options)
    if st.button("Delete Selected Entry"):
        idx = int(selected.split(":")[0])
        st.session_state["log"].drop(index=idx, inplace=True)
        st.session_state["log"].reset_index(drop=True, inplace=True)
        st.success("Entry deleted!")

# --- Mostrar progreso ---
st.subheader("Daily Progress")
totals = st.session_state["log"][["Calories", "Protein", "Fat", "Carbs"]].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Calories", f"{round(totals['Calories'])} / {round(tdee)}")
col2.metric("Protein (g)", f"{round(totals['Protein'])} / {round(prot_goal)}")
col3.metric("Fat (g)", f"{round(totals['Fat'])} / {round(fat_goal)}")
col4.metric("Carbs (g)", f"{round(totals['Carbs'])} / {round(carb_goal)}")


st.progress(min(totals['Calories'] / tdee, 1.0))
st.dataframe(st.session_state["log"])
