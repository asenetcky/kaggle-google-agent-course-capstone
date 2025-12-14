"""Streamlit UI for Toddle Ops - AI-powered toddler project generator."""

import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.genai import types

from toddle_ops.app import app
from toddle_ops.services.memory import memory_service
from toddle_ops.services.sessions import session_service

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Toddle Ops - AI Project Generator",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .project-box {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize session state
def init_session_state():
    """Initialize Streamlit session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = "streamlit_user"
    if "runner" not in st.session_state:
        st.session_state.runner = Runner(
            app=app, session_service=session_service, memory_service=memory_service
        )
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


async def create_session(user_id: str):
    """Create a new ADK session."""
    session = await session_service.create_session(
        app_name=app.name, user_id=user_id
    )
    return session


def run_async_task(coro):
    """Run async task in a separate thread with its own event loop."""
    def run_in_thread():
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
    
    # Run in a thread to avoid Streamlit's event loop conflicts
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_in_thread)
        return future.result()


async def generate_project(prompt: str, user_id: str, session_id: str | None, runner):
    """Generate a project using the agent."""
    # Ensure session exists
    if session_id is None:
        session = await create_session(user_id)
        session_id = session.id

    # Create message content
    content = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])

    # Run the agent
    response_text = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            response_text = event.content.parts[0].text

    return response_text, session_id


def main():
    """Main Streamlit application."""
    init_session_state()

    # Header
    st.markdown(
        """
        <div class="main-header">
            <h1>👶 Toddle Ops</h1>
            <p>AI-Powered Project Generation for Exhausted Caregivers</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar
    with st.sidebar:
        st.image(
            "https://raw.githubusercontent.com/asenetcky/toddle-ops/main/images/toddle-ops.png",
            width="stretch",
        )
        st.markdown("---")

        st.markdown("### 🎯 About")
        st.write(
            "Generate safe, engaging activities for toddlers (ages 1-3) using AI. "
            "All projects are validated for safety and edited for clarity."
        )

        st.markdown("---")
        st.markdown("### 🔧 Features")
        st.markdown(
            """
        - 🤖 Multi-agent AI system
        - 🛡️ Safety validation
        - ✏️ Editorial polish
        - 📝 Structured format
        """
        )

        st.markdown("---")
        if st.button("🔄 New Session"):
            st.session_state.messages = []
            st.session_state.session_id = None
            st.rerun()

        st.markdown("---")
        st.markdown("### 💡 Quick Prompts")
        if st.button("🎨 Creative Project"):
            st.session_state.pending_prompt = "Create a creative art project for my toddler"
            st.rerun()

        if st.button("🌈 Sensory Activity"):
            st.session_state.pending_prompt = "Give me a sensory activity for a 2-year-old"
            st.rerun()

        if st.button("🏃 Active Play"):
            st.session_state.pending_prompt = "Suggest an active indoor activity for a toddler"
            st.rerun()

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 💬 Chat with Toddle Ops")

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Process pending prompt from quick buttons
        if st.session_state.pending_prompt:
            prompt = st.session_state.pending_prompt
            st.session_state.pending_prompt = None
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Generating project..."):
                    response, new_session_id = run_async_task(
                        generate_project(
                            prompt,
                            st.session_state.user_id,
                            st.session_state.session_id,
                            st.session_state.runner
                        )
                    )
                    if new_session_id:
                        st.session_state.session_id = new_session_id
                    st.markdown(response)

            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        # Chat input
        if prompt := st.chat_input(
            "Ask for a project (e.g., 'I need a project for my 2-year-old')"
        ):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("🤖 Generating project..."):
                    response, new_session_id = run_async_task(
                        generate_project(
                            prompt,
                            st.session_state.user_id,
                            st.session_state.session_id,
                            st.session_state.runner
                        )
                    )
                    if new_session_id:
                        st.session_state.session_id = new_session_id
                    st.markdown(response)

            # Add assistant message
            st.session_state.messages.append({"role": "assistant", "content": response})

    with col2:
        st.markdown("### 📊 Session Info")
        st.info(
            f"""
        **Session ID:** `{st.session_state.session_id or 'Not created'}`  
        **User ID:** `{st.session_state.user_id}`  
        **Messages:** {len(st.session_state.messages)}  
        **Time:** {datetime.now().strftime('%H:%M:%S')}
        """
        )

        st.markdown("---")
        st.markdown("### 🎓 Example Prompts")
        st.markdown(
            """
        - "Create a new project"
        - "I need something with paint"
        - "Give me a water play activity"
        - "Something that takes 20 minutes"
        - "Project using household items"
        """
        )

        st.markdown("---")
        st.markdown("### ⚠️ Safety Note")
        st.warning(
            "Always supervise toddlers during activities. "
            "Projects are validated by AI but parental judgment is essential."
        )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 1rem;">
            Made with ❤️ and ☕ by <a href="https://github.com/asenetcky/toddle-ops" target="_blank">asenetcky</a>
            | Powered by Google ADK & Gemini
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("❌ GOOGLE_API_KEY not found! Please set it in your .env file.")
        st.stop()

    if not os.getenv("SUPABASE_USER") or not os.getenv("SUPABASE_PASSWORD"):
        st.warning(
            "⚠️ Supabase credentials not found. Session persistence will be limited."
        )

    main()
