import streamlit as st

from app.bootstrap import bootstrap
from app.ui.styles import load_css


# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Software Engineering Assistant",
    page_icon="🤖",
    layout="wide"
)

load_css()


# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:

    with st.spinner("Bootstrapping AI Assistant..."):

        st.session_state.agent = bootstrap()

agent = st.session_state.agent


# Current repository URL stored in session

if "current_repository" not in st.session_state:
    st.session_state.current_repository = None


# ----------------------------------------------------
# Sidebar
# ----------------------------------------------------

with st.sidebar:

    st.markdown("# ⚙️ Repository")

    repository_url = st.text_input(
        "GitHub Repository URL",
        value=st.session_state.current_repository or "",
        placeholder="https://github.com/user/repo"
    )

    # --------------------------------------------
    # Open repository only if URL changed
    # --------------------------------------------

    if (
        repository_url
        and repository_url != st.session_state.current_repository
    ):

        with st.spinner("Opening repository..."):

            try:

                agent.repository_manager.open_repository(
                    repository_url
                )

                st.session_state.current_repository = repository_url

                st.success("Repository loaded successfully.")

            except Exception as e:

                st.error(str(e))

    st.markdown("---")

    st.markdown("## Features")

    st.markdown(
        """
✅ Repository Q&A

✅ GitHub MCP

✅ Filesystem MCP

✅ Semantic Search

✅ Multi-Repository Support

✅ Gemini 2.5
"""
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.markdown(
    """
<div class="hero">

<h1>🤖 AI Software Engineering Assistant</h1>

<p>
Ask repository questions,
execute GitHub tools,
understand codebases,
or ask general programming questions.
</p>

</div>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------
# Chat History
# ----------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ----------------------------------------------------
# User Input
# ----------------------------------------------------

prompt = st.chat_input(
    "Ask anything about software engineering..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = agent.run(
                query=prompt,
                repository_url=st.session_state.current_repository
            )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )