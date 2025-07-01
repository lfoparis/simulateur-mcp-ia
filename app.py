import streamlit as st
from openai import OpenAI
import uuid
from db_utils import init_db, save_message, load_messages

st.set_page_config(page_title="Simulateur MCP avec IA", page_icon="🤖")
st.title("💬 Simulateur MCP avec IA (enregistrement SQLite)")

# 🔐 Clé OpenAI
api_key = st.text_input("🔑 Ta clé OpenAI :", type="password")

# 🧱 Initialiser la base si besoin
init_db()

# 🧠 Création du client OpenAI
if api_key:
    client = OpenAI(api_key=api_key)

    # 🧑 Message client
    question = st.text_input("🧑 Message du client :")

    if st.button("Envoyer") and question.strip():
        try:
            # 📡 Appel IA
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un assistant francophone utile."},
                    {"role": "user", "content": question}
                ]
            )
            answer = response.choices[0].message.content

            # 💾 Sauvegarde en base SQLite
            message_id = str(uuid.uuid4())
            save_message(message_id, "client_web", question, answer, "gpt-3.5-turbo")

            st.success("🟣 Réponse du serveur IA :")
            st.markdown(f"> {answer}")

        except Exception as e:
            st.error(f"Erreur IA : {str(e)}")

# 📜 Historique
with st.expander("📄 Historique enregistré (base SQLite)", expanded=True):
    rows = load_messages()
    if rows:
        for ts, sender, q, r in rows:
            st.markdown(f"**🕒 {ts} - {sender}**")
            st.markdown(f"- **Q :** {q}")
            st.markdown(f"- **R :** {r}")
            st.markdown("---")
    else:
        st.info("Aucun échange encore enregistré.")
