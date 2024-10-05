import streamlit as st
import ollama
import tempfile
import time

# App title
st.title("Linguo Bot")
st.image('linguo_img.webp', width = 200, caption='Linguo Bot: Still under development')

init_msg = """
Hi, I'm Linguo Bot, a grammar-checking robot inspired by The Simpsons. 
I'm an expert in checking grammar. 
Send me a sentence you'd like me to fix!"
"""

# Function to stream the assistant first
def stream_first(stream):
    for chunk in stream:
        yield chunk + " "
        time.sleep(0.09)

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
            model='linguo-ai',
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

# Assistant asks first
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": init_msg})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write_stream(stream_first(message["content"].split(" ")))
