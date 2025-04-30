import streamlit as st
import pandas as pd

# --- Funciones de cálculo ---
def calc_bmr(weight, height, age, sex):
    if sex == 'Male':
        return 10*weight + 6.25*height - 5*age + 5
    else:
        return 10*weight + 6.25*height - 5*age - 161

def calc_tdee(bmr, activity_factor):
    return bmr * activity_factor

def calc_macros(tdee, weight):
    protein_g = 1.9 * weight
    fat_g = (0.25 * tdee) / 9
    carbs_g = (tdee - (protein_g*4 + fat_g*9)) / 4
    return protein_g, fat_g, carbs_g

# --- Sidebar: Datos del usuario ---
st.sidebar.title("Datos del usuario")
weight = st.sidebar.number_input("Peso (kg)", 30, 200, 70)
height = st.sidebar.number_input("Altura (cm)", 100, 220, 170)
age = st.sidebar.number_input("Edad", 10, 100, 30)
sex = st.sidebar.selectbox("Sexo", ["Male", "Female"])
activity = st.sidebar.selectbox("Actividad", [
    ("Sedentario (1.2)", 1.2),
    ("Ligero (1.375)", 1.375),
    ("Moderado (1.55)", 1.55),
    ("Activo (1.725)", 1.725),
    ("Muy activo (1.9)", 1.9)
])

# --- Calcular metas ---
bmr = calc_bmr(weight, height, age, sex)
tdee = calc_tdee(bmr, activity[1])
prot_goal, fat_goal, carb_goal = calc_macros(tdee, weight)

# --- Mostrar metas ---
st.title("MyFitness MVP Dashboard")
st.subheader("Metas diarias calculadas")
st.write(f"**TDEE estimado:** {tdee:.0f} Cal/día")
st.write(f"**Proteína:** {prot_goal:.1f} g, **Grasa:** {fat_goal:.1f} g, **Carbohidratos:** {carb_goal:.1f} g")

# --- Registro de alimentos ---
st.subheader("Añadir alimento")
with st.form("food_form"):
    name = st.text_input("Nombre del alimento")
    cal = st.number_input("Calorías", 0, 2000, 0)
    prot = st.number_input("Proteína (g)", 0.0, 200.0, 0.0)
    fat = st.number_input("Grasa (g)", 0.0, 200.0, 0.0)
    carb = st.number_input("Carbohidratos (g)", 0.0, 300.0, 0.0)
    submitted = st.form_submit_button("Añadir")

if "log" not in st.session_state:
    st.session_state["log"] = pd.DataFrame(columns=["Alimento", "Calorías", "Proteína", "Grasa", "Carbs"])

if submitted and name:
    new_row = {"Alimento": name, "Calorías": cal, "Proteína": prot, "Grasa": fat, "Carbs": carb}
    st.session_state["log"] = pd.concat([st.session_state["log"], pd.DataFrame([new_row])], ignore_index=True)

# --- Mostrar progreso ---
st.subheader("Progreso del día")
totals = st.session_state["log"][["Calorías", "Proteína", "Grasa", "Carbs"]].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Calorías", f"{totals['Calorías']:.0f} / {tdee:.0f}")
col2.metric("Proteína (g)", f"{totals['Proteína']:.1f} / {prot_goal:.1f}")
col3.metric("Grasa (g)", f"{totals['Grasa']:.1f} / {fat_goal:.1f}")
col4.metric("Carbs (g)", f"{totals['Carbs']:.1f} / {carb_goal:.1f}")

st.progress(min(totals['Calorías']/tdee, 1.0))
st.dataframe(st.session_state["log"])
