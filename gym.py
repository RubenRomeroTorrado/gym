import streamlit as st
import pandas as pd

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
st.title("MyFitness MVP Dashboard")
st.subheader("Daily Targets")
st.write(f"**Estimated TDEE:** {tdee:.0f} kcal/day")
st.write(f"**Protein:** {prot_goal:.1f} g, **Fat:** {fat_goal:.1f} g, **Carbs:** {carb_goal:.1f} g")

# --- Registro de alimentos ---
st.subheader("Log Food")
with st.form("food_form"):
    name = st.text_input("Food name")
    cal = st.number_input("Calories", 0, 2000, 0)
    prot = st.number_input("Protein (g)", 0.0, 200.0, 0.0)
    fat = st.number_input("Fat (g)", 0.0, 200.0, 0.0)
    carb = st.number_input("Carbs (g)", 0.0, 300.0, 0.0)
    submitted = st.form_submit_button("Add Food")

if "log" not in st.session_state:
    st.session_state["log"] = pd.DataFrame(columns=["Food", "Calories", "Protein", "Fat", "Carbs"])

if submitted and name:
    new_row = {"Food": name, "Calories": cal, "Protein": prot, "Fat": fat, "Carbs": carb}
    st.session_state["log"] = pd.concat([st.session_state["log"], pd.DataFrame([new_row])], ignore_index=True)

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
col1.metric("Calories", f"{totals['Calories']:.0f} / {tdee:.0f}")
col2.metric("Protein (g)", f"{totals['Protein']:.1f} / {prot_goal:.1f}")
col3.metric("Fat (g)", f"{totals['Fat']:.1f} / {fat_goal:.1f}")
col4.metric("Carbs (g)", f"{totals['Carbs']:.1f} / {carb_goal:.1f}")

st.progress(min(totals['Calories'] / tdee, 1.0))
st.dataframe(st.session_state["log"])
