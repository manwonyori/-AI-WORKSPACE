"""
Streamlit Web UI for Computer Use Agent
"""

import streamlit as st
import asyncio
import json
import base64
from datetime import datetime
from pathlib import Path
import requests
from PIL import Image
import io

# Page config
st.set_page_config(
    page_title="Computer Use Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 0rem 1rem; }
    .stButton > button { width: 100%; }
    .screenshot-container { 
        border: 2px solid #ddd; 
        border-radius: 10px; 
        padding: 10px;
        margin: 10px 0;
    }
    .action-log {
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent_connected' not in st.session_state:
    st.session_state.agent_connected = False
if 'action_history' not in st.session_state:
    st.session_state.action_history = []
if 'current_screenshot' not in st.session_state:
    st.session_state.current_screenshot = None

# API endpoint
API_BASE_URL = "http://localhost:8000"

def check_api_connection():
    """Check if API is available"""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.status_code == 200
    except:
        return False

def execute_action(action_type, parameters):
    """Execute an action via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/execute",
            json={
                "type": action_type,
                "parameters": parameters
            }
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

def capture_screenshot():
    """Capture current screenshot"""
    try:
        response = requests.get(f"{API_BASE_URL}/screenshot")
        if response.status_code == 200:
            return response.json()["image"]
        return None
    except:
        return None

def execute_task(task_description):
    """Execute a complex task"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/task",
            json={"description": task_description}
        )
        return response.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# Header
st.title("🤖 Computer Use Agent")
st.markdown("**AI-Powered Computer Automation System**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Provider selection
    provider = st.selectbox(
        "AI Provider",
        ["Anthropic", "OpenAI", "AWS Bedrock", "Google Vertex"],
        index=0
    )
    
    # Model selection
    model = st.selectbox(
        "Model",
        ["claude-3-opus", "claude-3-sonnet", "gpt-4", "gpt-4-vision"],
        index=0
    )
    
    # Connection status
    st.header("📡 Status")
    if check_api_connection():
        st.success("✅ API Connected")
        st.session_state.agent_connected = True
    else:
        st.error("❌ API Disconnected")
        st.session_state.agent_connected = False
    
    # VNC Connection
    st.header("🖥️ Remote Desktop")
    if st.button("Open VNC Viewer"):
        st.info("VNC Server: localhost:5900")
        st.info(f"Password: computeruse")
    
    # Session Management
    st.header("💾 Session")
    if st.button("Save Session"):
        # Save current session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_path = f"session_{timestamp}.json"
        st.success(f"Session saved: {session_path}")
    
    if st.button("Load Session"):
        # Load session dialog
        st.info("Select a session file to load")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Screenshot display
    st.header("📸 Screen View")
    
    screenshot_container = st.container()
    with screenshot_container:
        if st.button("🔄 Refresh Screenshot"):
            screenshot = capture_screenshot()
            if screenshot:
                st.session_state.current_screenshot = screenshot
        
        if st.session_state.current_screenshot:
            # Display screenshot
            image_data = base64.b64decode(st.session_state.current_screenshot)
            image = Image.open(io.BytesIO(image_data))
            st.image(image, caption="Current Screen", use_column_width=True)
        else:
            st.info("Click 'Refresh Screenshot' to capture current screen")
    
    # Quick Actions
    st.header("⚡ Quick Actions")
    
    action_cols = st.columns(4)
    with action_cols[0]:
        if st.button("🖱️ Click"):
            with st.form("click_form"):
                x = st.number_input("X coordinate", min_value=0, value=500)
                y = st.number_input("Y coordinate", min_value=0, value=300)
                if st.form_submit_button("Execute Click"):
                    result = execute_action("click", {"x": x, "y": y})
                    st.session_state.action_history.append(result)
    
    with action_cols[1]:
        if st.button("⌨️ Type"):
            text = st.text_input("Text to type")
            if text and st.button("Send Text"):
                result = execute_action("type", {"text": text})
                st.session_state.action_history.append(result)
    
    with action_cols[2]:
        if st.button("📜 Scroll"):
            direction = st.selectbox("Direction", ["up", "down"])
            amount = st.slider("Amount", 1, 10, 3)
            if st.button("Execute Scroll"):
                result = execute_action("scroll", {
                    "direction": direction,
                    "amount": amount
                })
                st.session_state.action_history.append(result)
    
    with action_cols[3]:
        if st.button("🔍 Find"):
            query = st.text_input("Search for")
            if query and st.button("Search"):
                result = execute_action("find", {"query": query})
                st.session_state.action_history.append(result)

with col2:
    # Task Execution
    st.header("🎯 Task Execution")
    
    task_input = st.text_area(
        "Describe your task",
        placeholder="e.g., Open calculator and calculate 2+2",
        height=100
    )
    
    if st.button("🚀 Execute Task", type="primary"):
        if task_input:
            with st.spinner("Executing task..."):
                result = execute_task(task_input)
                if result.get("success"):
                    st.success("Task completed successfully!")
                else:
                    st.error(f"Task failed: {result.get('error')}")
                st.session_state.action_history.extend(
                    result.get("actions", [])
                )
    
    # Action History
    st.header("📜 Action History")
    
    if st.session_state.action_history:
        # Show last 10 actions
        for action in st.session_state.action_history[-10:]:
            action_type = action.get("type", "Unknown")
            success = action.get("success", False)
            
            status_icon = "✅" if success else "❌"
            st.markdown(
                f'<div class="action-log">'
                f'{status_icon} {action_type}: {action.get("parameters", {})}'
                f'</div>',
                unsafe_allow_html=True
            )
        
        if st.button("Clear History"):
            st.session_state.action_history = []
            st.rerun()
    else:
        st.info("No actions executed yet")
    
    # Statistics
    st.header("📊 Statistics")
    
    if st.session_state.action_history:
        total_actions = len(st.session_state.action_history)
        successful = sum(1 for a in st.session_state.action_history 
                        if a.get("success"))
        failed = total_actions - successful
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", total_actions)
        col2.metric("Success", successful)
        col3.metric("Failed", failed)

# Footer
st.markdown("---")
st.markdown(
    "**Computer Use Agent** | "
    "Powered by Claude & Anthropic | "
    "[Documentation](https://github.com/anthropics/computer-use) | "
    "[Report Issue](https://github.com/issues)"
)