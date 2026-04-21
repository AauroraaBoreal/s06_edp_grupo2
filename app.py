import streamlit as st
from supabase import create_client, Client

# 🔐 Credenciales (pon las tuyas)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("🏦 Simulador de Crédito - Banco Regional Andino")

st.write("Obtén una pre-aprobación en minutos")

# 📥 Formulario
nombre = st.text_input("Nombre")
edad = st.number_input("Edad", min_value=18, max_value=100)
ingresos = st.number_input("Ingresos mensuales")
deudas = st.number_input("Deudas actuales")

if st.button("Evaluar crédito"):

    # 🧠 Lógica simple
    if ingresos > 2000 and deudas < 0.3 * ingresos:
        resultado = "Aprobado"
    else:
        resultado = "Rechazado"

    # 📊 Mostrar resultado
    if resultado == "Aprobado":
        st.success("✅ Crédito pre-aprobado")
    else:
        st.error("❌ Requiere evaluación adicional")

    # 💾 Guardar en Supabase
    data = {
        "nombre": nombre,
        "edad": edad,
        "ingresos": ingresos,
        "deudas": deudas,
        "resultado": resultado
    }

    supabase.table("solicitudes_credito").insert(data).execute()

    st.write("📌 Solicitud guardada")

# 📊 Mostrar historial
st.subheader("📋 Historial de solicitudes")

response = supabase.table("solicitudes_credito").select("*").execute()

st.dataframe(response.data)
