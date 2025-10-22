import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from app import ingest, search_agent, logs

# --- Load environment variables ---
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# --- Streamlit setup ---
st.set_page_config(page_title="Web3Bridge AI Assistant", page_icon="⚡", layout="centered")
st.title("⚡ Web3Bridge Cohort XIII AI Assistant")
st.caption("Ask me anything about the Web3Bridge Cohort XIII repository!")

REPO_OWNER = "Bloceducare"
REPO_NAME = "Web3bridge-Web3-Cohort-XIII"


# --- Initialize agent (cached) ---
@st.cache_resource
def init_agent():
    """Initialize and cache the agent."""
    st.write("🔄 Building index and initializing agent...")
    ingest.index_data(REPO_OWNER, REPO_NAME, chunk=True)
    agent = search_agent.init_agent(REPO_OWNER, REPO_NAME)
    return agent

agent = init_agent()


# --- Manage chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- Streaming function (Groq-safe, async-friendly) ---
def stream_response(prompt: str):
    """Safely stream responses, compatible with Streamlit Cloud."""
    async def agen():
        async with agent.run_stream(user_prompt=prompt) as result:
            try:
                # Try the newer streaming API
                async for chunk in result.stream_output(debounce_by=0.01):
                    yield chunk
            except AttributeError:
                try:
                    # Fallback to older API (if available)
                    async for chunk in result.stream_text():
                        yield chunk
                except AttributeError:
                    # Final fallback: non-streamed
                    text = await result.get_output_text()
                    yield text

            # Log the interaction after streaming
            logs.log_interaction_to_file(agent, result.new_messages())

    # Run async generator safely in Streamlit (non-blocking)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    agen_obj = agen()

    try:
        while True:
            piece = loop.run_until_complete(agen_obj.__anext__())
            yield piece
    except StopAsyncIteration:
        pass


# --- Chat input section ---
if prompt := st.chat_input("Ask your Web3Bridge question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant’s response
    with st.chat_message("assistant"):
        try:
            response_text = st.write_stream(stream_response(prompt))
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
            st.stop()

    # Save the assistant's response
    final_text = getattr(st.session_state, "_last_response", response_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})
