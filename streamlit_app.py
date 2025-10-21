import streamlit as st
from openai import OpenAI

st.title("💬 Chatbot mit Assistant API")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Bitte API-Key eingeben.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Session-State für Thread-ID (Konversation)
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Eingabe vom User
    if prompt := st.chat_input("Was möchtest du fragen?"):
        # Nachricht zum Thread hinzufügen
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt,
        )

        # Run starten (den Assistant verwenden)
        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread_id,
            assistant_id="asst_EA9GFmy9Q4jcR8dKnMh798K1",
        )

        # Antwort abrufen
        if run.status == "completed":
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            # Letzte Assistentenantwort anzeigen
            for m in reversed(messages.data):
                if m.role == "assistant":
                    st.chat_message("assistant").markdown(m.content[0].text.value)
                    break
        else:
            st.error(f"Fehler oder abgebrochener Run: {run.status}")
