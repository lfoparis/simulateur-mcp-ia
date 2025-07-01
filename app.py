import streamlit as st
from openai import OpenAI
import time
import uuid

# 🧠 Configuration de la page
st.set_page_config(page_title="Simulateur MCP avec IA", page_icon="🤖")

st.title("💬 Simulateur de serveur MCP avec IA")
st.markdown("Envoie un message au serveur. Il te répondra comme dans un protocole MCP structuré.")

# 🔐 Clé API OpenAI
api_key = st.text_input("🔑 Rentre ta clé OpenAI", type="password")

# 💬 Initialisation de l'historique
if "history" not in st.session_state:
    st.session_state.history = []

# 🔧 Fonction MCP serveur
def mcp_server(message, client, model="gpt-3.5-turbo"):
    """Simule le serveur MCP qui reçoit un message, appelle OpenAI, et renvoie une réponse MCP"""
    if not isinstance(message, dict) or "content" not in message:
        return {
            "type": "error",
            "sender": "server_ai",
            "content": "Message MCP invalide."
        }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Tu es un assistant francophone utile."},
                {"role": "user", "content": message["content"]}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Erreur IA : {str(e)}"

    return {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "type": "answer",
        "sender": "server_ai",
        "content": answer
    }

# 🧠 Traitement si la clé API est fournie
if api_key:
    client = OpenAI(api_key=api_key)

    # Champ pour message utilisateur
    question = st.text_input("🧑 Message du client :")

    if st.button("Envoyer") and question.strip() != "":
        # Création d’un message MCP côté client
        client_message = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "type": "question",
            "sender": "client_web",
            "content": question
        }

        # Appel au serveur MCP simulé
        response = mcp_server(client_message, client)

        # Enregistrement dans l'historique
        st.session_state.history.append(("client", client_message))
        st.session_state.history.append(("server", response))

# 🖼️ Affichage de l'historique de messages façon chat
for sender, msg in st.session_state.history:
    if sender == "client":
        st.markdown(f"🧑 **Client** : {msg['content']}")
    elif sender == "server":
        st.markdown(f"🤖 **Serveur IA** : {msg['content']}")
