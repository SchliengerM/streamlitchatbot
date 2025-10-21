import streamlit as st
from openai import OpenAI

st.title("💬 Chatbot (Assistant API)")

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Bitte füge deinen OpenAI API Key ein.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    if "thread_id" not in st.session_state:
        # Einmalig einen neuen Thread erstellen
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # Zeige bisherige Nachrichten an
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Deine Eingabe:"):
        # Benutzer-Nachricht anzeigen und speichern
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Nachricht an Thread anhängen
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt,
        )

        # Einen Run mit deinem Assistant starten
        run = client.beta.threads.runs.create_and_poll(
            thread_id=st.session_state.thread_id,
            assistant_id="asst_EA9GFmy9Q4jcR8dKnMh798K1",
        )

        # Wenn der Run abgeschlossen ist, hole die Antwort
        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
            last_msg = messages.data[0].content[0].text.value  # neueste Nachricht
            with st.chat_message("assistant"):
                st.markdown(last_msg)
            st.session_state.messages.append({"role": "assistant", "content": last_msg})
        else:
            st.error(f"Run status: {run.status}")
