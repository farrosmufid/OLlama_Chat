import streamlit as st
import ollama
import tempfile

# App title
st.title("Tableau Public Bot")

# First time load messages is empty
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt for user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the assistant
    with st.chat_message("assistant"):
        # response = ollama.chat(
        #     model='llama3.1',
        #     messages=[
        #     {
        #         "role": "user", "content": prompt
        #      },
        # ])

        stream = ollama.chat(
            model='tableau-public-ai',
            messages=[{'role': 'user', 'content': prompt}],
            stream=True,
        )

        def stream_data():
            for chunk in stream:
                yield chunk['message']['content']

        response = st.write_stream(stream_data)

        #st.markdown(result)

    # Append response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})