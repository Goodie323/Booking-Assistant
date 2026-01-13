import streamlit as st
from scripts.booking_chat_pipelines import chat

# Page setup with custom theme
st.set_page_config(
    page_title="AI Booking Assistant", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 1rem;
    }
    
    /* Header styling */
    .header {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 2rem;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    /* User message styling */
    [data-testid="stChatMessage"]:has(.user-message) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 3rem;
    }
    
    /* Bot message styling */
    [data-testid="stChatMessage"]:has(.assistant-message) {
        background: rgba(255, 255, 255, 0.98);
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-right: 3rem;
        color: #333333 !important;
    }
    
    /* Ensure text in bot messages is visible */
    .assistant-message {
        color: #333333 !important;
        font-weight: 500;
    }
    
    /* User message text */
    .user-message {
        color: white !important;
        font-weight: 500;
    }
    
    /* Chat input container styling */
    .stChatInputContainer {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        padding: 10px;
    }
    
    /* Chat input text area - FIXED VISIBILITY */
    .stChatInput textarea {
    color: red !important;
    background-color: transparent !important;
    font-weight: 500;
    font-size: 16px;
    }
    
    /* Chat input placeholder */
    .stChatInput textarea::placeholder {
        color: #666666 !important;
        opacity: 0.8;
    }
    
    /* Focus state for input */
    .stChatInput textarea:focus {
        color: red !important;
        background-color: transparent !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Quick action buttons */
    .quick-action-btn {
        background: rgba(255, 255, 255, 0.9) !important;
        color: #333333 !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
    }
    
    .quick-action-btn:hover {
        background: rgba(102, 126, 234, 0.1) !important;
        border: 1px solid #667eea !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    
    /* Ensure all text in the app is properly colored */
    .stApp {
        color: #333333;
    }
    
    /* Fix for any Streamlit text elements */
    .stMarkdown, .stText, .stAlert, .stSuccess {
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main container with gradient background
st.markdown('<div class="main">', unsafe_allow_html=True)

# Header section
st.markdown("""
<div class="header">
    <div style="text-align: center;">
        <h1 style="color: #333; margin-bottom: 0.5rem; font-size: 2.5rem;">🤖 AI Booking Assistant</h1>
        <p style="color: #666; font-size: 1.1rem; margin-bottom: 1rem;">
            Your personal travel planning companion
        </p>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 2px; border-radius: 20px; display: inline-block;">
            <div style="background: white; padding: 0.5rem 2rem; border-radius: 18px;">
                <p style="color: #333; margin: 0; font-weight: 600;">
                    🏨 Hotels • 🚆 Trains • 🍽️ Restaurants • 📅 Bookings
                </p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat container with custom styling
chat_container = st.container()

with chat_container:
    # Display chat history
    for turn in st.session_state.history:
        # Split into role and message
        role, message = turn.split(":", 1)
        message = message.strip()  # remove leading space

        if role == "User":
            with st.chat_message("user"):
                st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
        else:
            with st.chat_message("assistant"):
                st.markdown(f'<div class="assistant-message">{message}</div>', unsafe_allow_html=True)

# Quick action buttons
st.markdown("---")
st.markdown("### 💡 Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏨 Find Hotels", key="hotels"):
        if "User: Find hotels in my area" not in [turn for turn in st.session_state.history]:
            st.session_state.history.append("User: Find hotels in my area")
            st.rerun()

with col2:
    if st.button("🚆 Train Tickets", key="trains"):
        if "User: Show me train options" not in [turn for turn in st.session_state.history]:
            st.session_state.history.append("User: Show me train options")
            st.rerun()

with col3:
    if st.button("🍽️ Restaurants", key="restaurants"):
        if "User: Recommend restaurants" not in [turn for turn in st.session_state.history]:
            st.session_state.history.append("User: Recommend restaurants")
            st.rerun()

with col4:
    if st.button("🔄 Clear Chat", key="clear"):
        st.session_state.history = []
        st.rerun()

# Input box at bottom with enhanced styling
st.markdown("<br>", unsafe_allow_html=True)
user_input = st.chat_input("💬 Ask about hotels, trains, restaurants, or bookings...")

if user_input:
    # Add user message
    st.session_state.history.append(f"User: {user_input}")

    # Get bot reply
    with st.spinner("🤔 Thinking..."):
        bot_reply = chat(user_input, st.session_state.history)
        st.session_state.history.append(f"Bot: {bot_reply}")

    # Rerun to refresh chat
    st.rerun()

# Close main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; color: white; margin-top: 2rem; font-size: 0.9rem;">
    <p>✨ Powered by SmartBott • Your trusted booking companion ✨</p>
</div>
""", unsafe_allow_html=True)