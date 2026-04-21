import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Simulador de Crédito", page_icon="🏦")

st.title("🏦 Simulador de Crédito - Banco Regional Andino")
st.write("Obtén una pre-aprobación en minutos")

nombre = st.text_input("Nombre")
edad = st.number_input("Edad", min_value=18, max_value=100)
ingresos = st.number_input("Ingresos mensuales", min_value=0.0)
deudas = st.number_input("Deudas actuales", min_value=0.0)

if st.button("Evaluar crédito"):
    if not nombre:
        st.warning("Por favor ingresa tu nombre")
        st.stop()

    if ingresos > 2000 and deudas < 0.3 * ingresos:
        resultado = "Aprobado"
    else:
        resultado = "Rechazado"

    if resultado == "Aprobado":
        st.success("✅ Crédito pre-aprobado")
    else:
        st.error("❌ Requiere evaluación adicional")

    data = {
        "nombre": nombre,
        "edad": edad,
        "ingresos": ingresos,
        "deudas": deudas,
        "resultado": resultado
    }

    try:
        supabase.table("solicitudes_credito").insert(data).execute()
        st.success("📌 Solicitud guardada")
    except Exception:
        st.error("Error al guardar en la base de datos")

st.subheader("📋 Historial de solicitudes")

@st.cache_data
def obtener_datos():
    response = supabase.table("solicitudes_credito").select("*").execute()
    return response.data

try:
    datos = obtener_datos()
    st.dataframe(datos)
except Exception:
    st.warning("No se pudieron cargar los datos")