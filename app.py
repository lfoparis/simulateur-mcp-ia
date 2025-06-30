import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="MCP Simulateur", page_icon="🤖")

st.title("💬 Simulateur MCP avec IA intégrée")
st.markdown("Pose une question, l'IA te répondra via un message MCP simulé.")

api_key = st.text_input("🔑 Ta clé OpenAI :", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
    question = st.text_input("🧑 Message du client :")

    if st.button("Envoyer"):
        with st.spinner("⏳ Attente de la réponse de l'IA..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant francophone utile."},
                        {"role": "user", "content": question}
                    ]
                )
                content = response.choices[0].message.content

                st.success("🟣 Réponse du serveur IA :")
                st.markdown(f"> {content}")

            except Exception as e:
                st.error(f"Erreur lors de l’appel à l’IA : {e}")