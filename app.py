import streamlit as st
from openai import OpenAI
from supabase import create_client, Client
import uuid
from datetime import datetime
import pandas as pd

# 🔧 Interface
st.set_page_config(page_title="MCP avec Supabase", page_icon="🤖")
st.title("💬 Simulateur MCP avec IA et Supabase")

# 🧩 Zone de configuration (barre latérale)
st.sidebar.header("🔐 Connexion Supabase & OpenAI")

SUPABASE_URL = st.sidebar.text_input("🌐 URL Supabase", placeholder="https://xyz.supabase.co")
SUPABASE_KEY = st.sidebar.text_input("🔑 Clé API Supabase", type="password")

OPENAI_KEY = st.sidebar.text_input("🔑 Clé OpenAI", type="password")

# 🧠 Initialisation Supabase
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    if OPENAI_KEY:
        client = OpenAI(api_key=OPENAI_KEY)

        question = st.text_input("🧑 Message du client MCP :")

        if st.button("Envoyer") and question.strip():
            try:
                # 📡 Appel OpenAI
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant francophone utile."},
                        {"role": "user", "content": question}
                    ]
                )
                answer = response.choices[0].message.content

                # 💾 Insertion Supabase
                result = supabase.table("messages").insert({
                    "id": str(uuid.uuid4()),
                    "timestamp": datetime.utcnow().isoformat(),
                    "sender": "client_web",
                    "question": question,
                    "response": answer,
                    "model": "gpt-3.5-turbo"
                }).execute()

                st.success("🟣 Réponse du serveur IA :")
                st.markdown(f"> {answer}")

            except Exception as e:
                st.error(f"Erreur IA : {str(e)}")

        # 📜 Historique
        with st.expander("📄 Historique enregistré dans Supabase", expanded=True):
            try:
                rows = supabase.table("messages").select("*").order("timestamp", desc=True).limit(100).execute()
                data = rows.data

                if data:
                    df = pd.DataFrame(data)
                    df = df[["timestamp", "sender", "question", "response"]]
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Aucun message enregistré.")
            except Exception as e:
                st.error(f"Erreur lors de la récupération : {str(e)}")

    else:
        st.info("🧠 Saisis ta clé OpenAI dans la barre latérale.")
else:
    st.info("🔧 Saisis les informations de connexion Supabase dans la barre latérale.")
