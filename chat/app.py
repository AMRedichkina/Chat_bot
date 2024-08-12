import time
import streamlit as st
from agent import generate_response

# Set page config
st.set_page_config("Library bot", page_icon=":books:")

# Initialize session state for storing messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm the Library Chatbot!  How can I help you?"},
    ]

def write_message(role, content, save = True):
    """Helper function to save and display messages in the chat."""
    if save:
        st.session_state.messages.append({"role": role, "content": content})

    # Option: avatar + name
    if role == "assistant":
        avatar = ":material/support_agent: "
        
    else:
        avatar = ":material/person_edit: "

    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def handle_submit(message):
    """Handle submission of user input."""
    try:
        with st.spinner('Thinking...'):
            response = generate_response(message)
            write_message('assistant', response)
    except Exception as e:
        st.error(f"### Error\nAn unexpected error occurred:\n\n**{str(e)}**")

# Option 1
st.title("Library  ChatBot")

# Display previous messages
for message in st.session_state.messages:
    write_message(message['role'], message['content'], save=False)

#This conditional ensures handle_submit is called only when there's an input
if question := st.chat_input("Ask me to find your next book..."):
    write_message('user', question)
    handle_submit(question)

#Option 2: Side_panel
# with st.sidebar:
#     st.title("Library  ChatBot")
#     chat_container = st.container(height=600)
#     with chat_container:
#         for message in st.session_state.messages:
#             write_message(message['role'], message['content'], save=False)
#     if question := st.chat_input("Ask me to find your next book..."):
#         with chat_container:
#             write_message('user', question)
#             handle_submit(question)

# Option 3: Expander
#Use an expander to mimic a modal window
# with st.expander("Open Library  ChatBot", expanded=True):
#     st.title("Library  ChatBot")
#     chat_container = st.container(height=600)
#     with chat_container:
#         for message in st.session_state.messages:
#             write_message(message['role'], message['content'], save=False)
#     if question := st.chat_input("Ask me to find your next book..."):
#         with chat_container:
#             write_message('user', question)
#             handle_submit(question)