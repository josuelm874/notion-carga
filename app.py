import streamlit as st
from notion_client import Client

NOTION_TOKEN = st.secrets["NOTION_TOKEN"]
DATABASE_ID = st.secrets["DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

st.title("Workout Monarch")

if st.button("Level Up"):
    # Pegar todas as páginas da database
    response = notion.databases.query(database_id=DATABASE_ID)

    for page in response["results"]:
        page_id = page["id"]

        # Obter a carga atual
        props = page["properties"]
        carga_atual = props["Carga"]["number"]

        if carga_atual is not None:
            nova_carga = carga_atual + 2.5

            # Atualizar a página com a nova carga
            notion.pages.update(
                page_id=page_id,
                properties={
                    "Carga": {
                        "number": nova_carga
                    }
                }
            )

    st.success("")
