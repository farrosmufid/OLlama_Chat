import streamlit as st
import ollama
import tempfile
import time

# App title
st.title("Ghost AI 🗿🗿🗿")

# Initialise message
init_msg = """Hey there! **Ghost AI** 🗿🗿🗿 here, your **handy recruitment assistant**.
Got any **questions** about your **application progress**?\n\nNo worries! **Just ask!**\n\n
Feel free to mention your **name**, the **position** you applied for, 
and the **company**—or we can just have a **casual chat**.\n\nWhether you need 
**updates**, **info**, or **someone** to **keep you company** during the wait, 
I’m here to help!"""

# First time load messages is empty
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to stream the assistant first
def stream_first(stream):
    for chunk in stream:
        yield chunk + " "
        time.sleep(0.09)

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
            model='ghost-ai',
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
            st.image('ghost_img.png', caption='Ghost AI 🗿🗿🗿')
            st.write_stream(stream_first(message["content"].split(" ")))


