
import streamlit as st
from google import genai
from google.genai import types
import bcrypt

st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# Password login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 My AI Chatbot Login")

    with st.form("login_form"):
        password = st.text_input(
            "Enter Password", type="password"
        )
        login = st.form_submit_button("Login")

    if login:
        if bcrypt.checkpw(
            password.encode("utf-8"),
            st.secrets["PASSWORD_HASH"].encode("utf-8")
        ):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()

# Custom dark design
st.markdown("""
<style>
.stApp {
    background-color: #171717;
    color: #f5f5f5;
}

[data-testid="stSidebar"] {
    background-color: #202020;
}

[data-testid="stHeader"] {
    background-color: #171717;
}

.stChatMessage {
    border-radius: 15px;
}

[data-testid="stChatInput"] {
    border-radius: 20px;
}

h1 {
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🤖 My AI")
    st.caption("Powered by Google Gemini")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.write("Model: Gemini")
    st.success("Online AI")


# Main interface
st.title("My AI Assistant")

if not st.session_state.messages:
    st.markdown("### How can I help you today?")
    st.caption("Ask questions, learn coding, or explore ideas.")

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

       
    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                client = genai.Client(
                    api_key=st.secrets["GEMINI_API_KEY"]
                )

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=[
                        types.Content(
                            role="model" if msg["role"] == "assistant" else "user",
                            parts=[
                                types.Part.from_text(text=msg["content"])
                            ]
                        )
                        for msg in st.session_state.messages
                    ]
                )

                answer = response.text or "No response generated."

            st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Error: {e}")
