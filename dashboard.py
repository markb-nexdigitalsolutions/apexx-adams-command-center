import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests
import json

# Page setup
st.set_page_config(
    page_title="ApexxAdams Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .status-active {
        background: #10b981;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-idle {
        background: #f59e0b;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .status-offline {
        background: #6b7280;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 5px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Connect to Google Sheets
@st.cache_resource
def connect_to_sheets():
    try:
        credentials_dict = dict(st.secrets["google_credentials"])
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

# Load CORA data
@st.cache_data(ttl=300)
def load_cora_data():
    try:
        sheet_id = st.secrets["CORA_SHEET_ID"]
        client = connect_to_sheets()
        if client:
            sheet = client.open_by_key(sheet_id).sheet1
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

# Load OPSI data (placeholder for now)
@st.cache_data(ttl=300)
def load_opsi_data():
    # Placeholder - will connect to your OPSI Google Sheet later
    return pd.DataFrame({
        'task': ['Grant Application - City of Austin', 'RFP Review - Charlotte', 'Compliance Audit Q4'],
        'due_date': ['2025-11-05', '2025-11-12', '2025-11-30'],
        'priority': ['High', 'Medium', 'Low'],
        'status': ['In Progress', 'Not Started', 'Not Started']
    })

# Header
st.markdown('<p class="main-header">⚡ ApexxAdams Command Center</p>', unsafe_allow_html=True)
st.write("Multi-Agent System Dashboard - CORA | MARK | OPSI")

# Sidebar - Agent Selection
st.sidebar.title("🤖 Agent Control Panel")
st.sidebar.markdown("---")

# Agent Status
st.sidebar.subheader("Agent Status")
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    st.markdown('<span class="status-active">CORA ✓</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="status-idle">MARK</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="status-offline">OPSI</span>', unsafe_allow_html=True)

st.sidebar.markdown("---")

# Agent Selection
selected_agent = st.sidebar.selectbox(
    "Select Agent",
    ["📊 Dashboard Overview", "🎯 CORA (Lead Generation)", "📣 MARK (Marketing AI)", "🧩 OPSI (Operations)"]
)

st.sidebar.markdown("---")

# Quick Actions
st.sidebar.subheader("⚡ Quick Actions")
if st.sidebar.button("🎯 Run CORA Now"):
    st.sidebar.success("CORA workflow triggered!")
if st.sidebar.button("📣 Ask MARK"):
    st.sidebar.info("MARK chat opening...")
if st.sidebar.button("🧩 View OPSI Tasks"):
    st.sidebar.info("Loading tasks...")

# ============================================
# DASHBOARD OVERVIEW
# ============================================
if selected_agent == "📊 Dashboard Overview":
    
    # Load data
    cora_df = load_cora_data()
    opsi_df = load_opsi_data()
    
    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_leads = len(cora_df) if not cora_df.empty else 0
        st.metric("🎯 Total Leads (CORA)", total_leads, "+12 this week")
    
    with col2:
        st.metric("📣 Active Campaigns (MARK)", "Coming Soon", "")
    
    with col3:
        pending_tasks = len(opsi_df[opsi_df['status'] == 'Not Started']) if not opsi_df.empty else 0
        st.metric("🧩 Pending Tasks (OPSI)", pending_tasks, "")
    
    with col4:
        response_rate = "68%" if not cora_df.empty else "N/A"
        st.metric("📈 Overall Performance", response_rate, "+5%")
    
    st.markdown("---")
    
    # Agent Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="agent-card">
            <h3>🎯 CORA</h3>
            <p>Community Outreach & Research Assistant</p>
            <p><strong>Status:</strong> <span class="status-active">Active</span></p>
            <p><strong>Last Run:</strong> 2 hours ago</p>
            <p><strong>Today's Leads:</strong> 15</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="agent-card">
            <h3>📣 MARK</h3>
            <p>Marketing & Engagement Bot</p>
            <p><strong>Status:</strong> <span class="status-idle">Idle</span></p>
            <p><strong>Setup:</strong> In Progress</p>
            <p><strong>AI Model:</strong> GPT-4o</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="agent-card">
            <h3>🧩 OPSI</h3>
            <p>Operations & Policy System</p>
            <p><strong>Status:</strong> <span class="status-offline">Coming Soon</span></p>
            <p><strong>Setup:</strong> Pending</p>
            <p><strong>Tasks:</strong> 0</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 CORA Recent Leads")
        if not cora_df.empty:
            recent = cora_df.tail(5)[['name', 'organization', 'email']]
            st.dataframe(recent, use_container_width=True, hide_index=True)
        else:
            st.info("No leads yet. Run CORA to generate leads.")
    
    with col2:
        st.subheader("🧩 OPSI Upcoming Tasks")
        if not opsi_df.empty:
            st.dataframe(opsi_df[['task', 'due_date', 'priority']], use_container_width=True, hide_index=True)
        else:
            st.info("No tasks scheduled.")

# ============================================
# CORA PAGE
# ============================================
elif selected_agent == "🎯 CORA (Lead Generation)":
    
    st.header("🎯 CORA - Lead Generation Dashboard")
    
    df = load_cora_data()
    
    if not df.empty:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📊 Total Leads", len(df))
        
        with col2:
            today = datetime.now().strftime('%Y-%m-%d')
            today_leads = df[df['generated_date'] == today] if 'generated_date' in df.columns else pd.DataFrame()
            st.metric("📅 Today", len(today_leads))
        
        with col3:
            cities = df['organization'].str.contains('City', case=False, na=False).sum() if 'organization' in df.columns else 0
            st.metric("🏙️ Cities", cities)
        
        with col4:
            churches = df['organization'].str.contains('Church', case=False, na=False).sum() if 'organization' in df.columns else 0
            st.metric("⛪ Churches", churches)
        
        st.markdown("---")
        
        # Search
        search = st.text_input("🔍 Search leads", "")
        
        filtered_df = df.copy()
        if search:
            mask = (
                filtered_df['name'].str.contains(search, case=False, na=False) |
                filtered_df['email'].str.contains(search, case=False, na=False) |
                filtered_df['organization'].str.contains(search, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        
        st.subheader(f"📋 All Leads ({len(filtered_df)})")
        
        display_columns = ['name', 'title', 'organization', 'email', 'suggested_action', 'generated_date']
        available_columns = [col for col in display_columns if col in filtered_df.columns]
        
        st.dataframe(filtered_df[available_columns], use_container_width=True, hide_index=True)
        
        # Download
        csv = filtered_df.to_csv(index=False)
        st.download_button("📥 Export CSV", csv, f"cora_leads_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    else:
        st.warning("⚠️ No leads data available.")
        st.info("👉 Run the CORA workflow in n8n to generate leads.")

# ============================================
# MARK PAGE (NEW!)
# ============================================
elif selected_agent == "📣 MARK (Marketing AI)":
    
    st.header("📣 MARK - Marketing & Engagement AI")
    st.write("*Your AI Marketing Assistant - Powered by GPT-4o*")
    
    # MARK Info Card
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### About MARK
        MARK is your AI-powered marketing assistant that helps you:
        - 📧 **Launch email/SMS campaigns** to engage prospects
        - 📅 **Schedule meetings** and follow-ups automatically
        - 📊 **Track engagement metrics** in real-time
        - 🤖 **Respond like a human expert** - Think Jarvis from Iron Man
        
        **Status:** Setup in progress  
        **AI Model:** GPT-4o  
        **Integrations:** GoHighLevel, Gmail, Calendar
        """)
    
    with col2:
        st.info("🚧 **Coming Soon!**\n\nMARK is being configured. Check back soon!")
    
    st.markdown("---")
    
    # Chat with MARK (Placeholder)
    st.subheader("💬 Chat with MARK")
    
    user_input = st.text_input("Ask MARK anything about marketing...", placeholder="e.g., How's our email campaign performing?")
    
    if user_input:
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant", avatar="📣"):
            st.write(f"*Good day, sir. I'm MARK, your marketing intelligence system.*")
            st.write(f"I've analyzed your query: '{user_input}'")
            st.write("However, I'm still being calibrated. My full capabilities will be online shortly. In the meantime, I recommend checking the CORA dashboard for recent lead activity.")
    
    st.markdown("---")
    
    # Campaign Metrics (Placeholder)
    st.subheader("📊 Campaign Performance")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Campaigns", "Coming Soon")
    with col2:
        st.metric("Total Sent", "Coming Soon")
    with col3:
        st.metric("Engagement Rate", "Coming Soon")

# ============================================
# OPSI PAGE
# ============================================
elif selected_agent == "🧩 OPSI (Operations)":
    
    st.header("🧩 OPSI - Operations & Policy System Integrator")
    st.write("*Internal Workflow & Compliance Management*")
    
    opsi_df = load_opsi_data()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pending Tasks", len(opsi_df[opsi_df['status'] == 'Not Started']))
    with col2:
        st.metric("In Progress", len(opsi_df[opsi_df['status'] == 'In Progress']))
    with col3:
        high_priority = len(opsi_df[opsi_df['priority'] == 'High'])
        st.metric("High Priority", high_priority)
    with col4:
        st.metric("Compliance Score", "94%")
    
    st.markdown("---")
    
    # Tasks Table
    st.subheader("📌 Active Tasks")
    st.dataframe(opsi_df, use_container_width=True, hide_index=True)
    
    st.info("🚧 OPSI is coming soon! This will track grants, RFPs, compliance deadlines, and internal tasks.")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>ApexxAdams Multi-Agent Command Center</strong></p>
        <p>CORA • MARK • OPSI | Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    """,
    unsafe_allow_html=True
)
