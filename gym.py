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
st.subheader("Daily Targets")
st.write(f"**Estimated TDEE:** {tdee:.0f} kcal/day")
st.write(f"**Protein:** {prot_goal:.1f} g, **Fat:** {fat_goal:.1f} g, **Carbs:** {carb_goal:.1f} g")
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



# --- Lista de alimentos predefinidos ---
predefined_foods = {
    "Chicken Breast (grilled)": {"Calories": 165, "Protein": 31, "Fat": 3.6, "Carbs": 0},
    "White Rice (cooked)": {"Calories": 130, "Protein": 2.7, "Fat": 0.3, "Carbs": 28},
    "Broccoli (boiled)": {"Calories": 35, "Protein": 2.4, "Fat": 0.4, "Carbs": 7.2},
    "Salmon (grilled)": {"Calories": 206, "Protein": 22, "Fat": 13, "Carbs": 0},
    "Oats (raw)": {"Calories": 389, "Protein": 16.9, "Fat": 6.9, "Carbs": 66.3}
}
# --- Agregar alimento predefinido ---
st.subheader("Add Predefined Food")

selected_food = st.selectbox("Select a food", ["-- Choose one --"] + list(predefined_foods.keys()))
amount_predef = st.number_input("Amount consumed (g)", 1, 1000, 100, key="amount_predef")

if st.button("Add Predefined Food"):
    if selected_food != "-- Choose one --":
        data = predefined_foods[selected_food]
        factor = amount_predef / 100
        new_row = {
            "Food": selected_food,
            "Calories": data["Calories"] * factor,
            "Protein": data["Protein"] * factor,
            "Fat": data["Fat"] * factor,
            "Carbs": data["Carbs"] * factor
        }
        st.session_state["log"] = pd.concat(
            [st.session_state["log"], pd.DataFrame([new_row])], ignore_index=True
        )
        st.success(f"{selected_food} added.")

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


