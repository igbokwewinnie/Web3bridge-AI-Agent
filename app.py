import streamlit as st
import os
from dotenv import load_dotenv
import asyncio
from app import ingest, search_agent, logs

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# --- App setup ---
st.set_page_config(page_title="Web3Bridge AI Assistant", page_icon="⚡", layout="centered")
st.title("⚡ Web3Bridge Cohort XIII AI Assistant")
st.caption("Ask me anything about the Web3Bridge Cohort XIII repository")

REPO_OWNER = "Bloceducare"
REPO_NAME = "Web3bridge-Web3-Cohort-XIII"


# --- Initialization (cached) ---
@st.cache_resource
def init_agent():
    """Initialize the agent and index (cached for performance)."""
    st.write("🔄 Building index and initializing agent...")
    index = ingest.index_data(REPO_OWNER, REPO_NAME, chunk=True)
    agent = search_agent.init_agent(REPO_OWNER, REPO_NAME)
    return agent


agent = init_agent()  # ✅ no args needed here anymore


# --- Chat history setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- Streaming helper ---
def stream_response(prompt: str):
    """Stream model responses word by word using asyncio."""
    async def agen():
        async with agent.run_stream(user_prompt=prompt) as result:
            last_len = 0
            full_text = ""
            async for chunk in result.stream_output(debounce_by=0.01):
                new_text = chunk[last_len:]
                last_len = len(chunk)
                full_text = chunk
                if new_text:
                    yield new_text
            logs.log_interaction_to_file(agent, result.new_messages())
            st.session_state._last_response = full_text

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    agen_obj = agen()

    try:
        while True:
            piece = loop.run_until_complete(agen_obj.__anext__())
            yield piece
    except StopAsyncIteration:
        return


# --- User Input Section ---
if prompt := st.chat_input("Ask your Web3Bridge question..."):
    # Show user question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant reply
    with st.chat_message("assistant"):
        response_text = st.write_stream(stream_response(prompt))

    # Save assistant's reply to session
    final_text = getattr(st.session_state, "_last_response", response_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})
