import streamlit as st
from notion_client import Client
import os

NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
DATABASE_ID = st.secrets["DATABASE_ID"]
PROP_CARGA = "Carga"
INCREMENTO = 2.5

notion = Client(auth=NOTION_TOKEN)

def aumentar_carga(nome_exercicio):
    query = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "property": "Exercício",
                "title": {
                    "equals": nome_exercicio
                }
            }
        }
    )

    if not query["results"]:
        st.error(f"Exercício '{nome_exercicio}' não encontrado.")
        return

    page = query["results"][0]
    page_id = page["id"]
    props = page["properties"]
    carga_atual = props[PROP_CARGA]["number"] or 0
    nova_carga = carga_atual + INCREMENTO

    notion.pages.update(
        page_id=page_id,
        properties={
            PROP_CARGA: {"number": nova_carga}
        }
    )

    st.success(f"Carga do exercício '{nome_exercicio}' aumentada de {carga_atual} para {nova_carga}.")

st.title("🏋️‍♂️ Workout Monarch – Atualizador de Carga")

exercicio = st.selectbox("Escolha o exercício:", [
    "Supino Reto", "Remada Curvada", "Agachamento", "Terra", "Desenvolvimento Militar"
])

if st.button("Aumentar carga em +2.5"):
    aumentar_carga(exercicio)
