import streamlit as st
from datetime import datetime
from cora import cora_page, get_cora_status, get_cora_leads
from mark import mark_page, get_mark_status
from opsi import opsi_page, get_opsi_status, load_opsi_tasks

# ========================================
# PAGE CONFIGURATION
# ========================================
st.set_page_config(
    page_title="ApexxAdams Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CUSTOM STYLING
# ========================================
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
    .metric-card {
        background: #f9fafb;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR NAVIGATION
# ========================================
with st.sidebar:
    st.markdown("### ⚡ ApexxAdams")
    st.markdown("**Multi-Agent Command Center**")
    st.markdown("---")
    
    st.markdown("### 🧭 Navigation")
    selected_page = st.radio(
        "Select View:",
        ["Dashboard Overview", "CORA (Lead Generation)", "MARK (Marketing AI)", "OPSI (Operations)"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    # Get agent statuses dynamically
    cora_status = get_cora_status()
    mark_status = get_mark_status()
    opsi_status = get_opsi_status()
    
    # Map status to CSS class
    status_class_map = {
        "Active": "status-active",
        "Idle": "status-idle",
        "Offline": "status-offline"
    }
    
    st.markdown(f'<span class="{status_class_map.get(cora_status, "status-offline")}">● CORA: {cora_status}</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="{status_class_map.get(mark_status, "status-offline")}">● MARK: {mark_status}</span>', unsafe_allow_html=True)
    st.markdown(f'<span class="{status_class_map.get(opsi_status, "status-offline")}">● OPSI: {opsi_status}</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption(f"v1.0 • Last updated: {datetime.now().strftime('%H:%M:%S')}")

# ========================================
# MAIN CONTENT AREA
# ========================================

# Header
st.markdown('<p class="main-header">⚡ ApexxAdams Multi-Agent Command Center</p>', unsafe_allow_html=True)
st.markdown("**Your AI-Powered Business Operations Platform**")
st.markdown("---")

# ========================================
# PAGE ROUTING
# ========================================

if selected_page == "Dashboard Overview":
    # ========================================
    # DASHBOARD OVERVIEW PAGE
    # ========================================
    
    # Agent Status Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_badge = f'<span class="{status_class_map.get(cora_status, "status-offline")}">{cora_status.upper()}</span>'
        st.markdown(f"""
        <div class="agent-card">
            <h3>🎯 CORA</h3>
            <p>Community Outreach & Research Assistant</p>
            <div style="margin-top: 1rem;">
                {status_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        status_badge = f'<span class="{status_class_map.get(mark_status, "status-offline")}">{mark_status.upper()}</span>'
        st.markdown(f"""
        <div class="agent-card">
            <h3>📧 MARK</h3>
            <p>Marketing & Research Knowledge</p>
            <div style="margin-top: 1rem;">
                {status_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        status_badge = f'<span class="{status_class_map.get(opsi_status, "status-offline")}">{opsi_status.upper()}</span>'
        st.markdown(f"""
        <div class="agent-card">
            <h3>📋 OPSI</h3>
            <p>Operations & Policy System</p>
            <div style="margin-top: 1rem;">
                {status_badge}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Get data from agents
    cora_leads = get_cora_leads()
    opsi_tasks = load_opsi_tasks()
    
    with col1:
        st.metric("Total Leads", len(cora_leads))
    
    with col2:
        qualified = sum(1 for lead in cora_leads if lead.get('Status') == 'Qualified')
        st.metric("Qualified Leads", qualified)
    
    with col3:
        contacted = sum(1 for lead in cora_leads if lead.get('Status') == 'Contacted')
        st.metric("Contacted", contacted)
    
    with col4:
        pending_tasks = len([t for t in opsi_tasks.to_dict('records') if t.get('Status') == 'New' or t.get('Status ') == 'New']) if not opsi_tasks.empty else 0
        st.metric("Pending Tasks", pending_tasks)
    
    st.markdown("---")
    
    # Recent Activity
    st.subheader("📊 Recent Activity")
    
    if cora_leads:
        import pandas as pd
        recent_df = pd.DataFrame(cora_leads).head(5)
        st.dataframe(recent_df, use_container_width=True, hide_index=True)
    else:
        st.info("No recent activity. Run CORA to generate leads.")
    
    # Quick Actions
    st.markdown("---")
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 View CORA Leads", use_container_width=True):
            st.session_state.page = "CORA (Lead Generation)"
            st.rerun()
    
    with col2:
        if st.button("📧 Check MARK Status", use_container_width=True):
            st.session_state.page = "MARK (Marketing AI)"
            st.rerun()
    
    with col3:
        if st.button("📋 Manage OPSI Tasks", use_container_width=True):
            st.session_state.page = "OPSI (Operations)"
            st.rerun()

elif selected_page == "CORA (Lead Generation)":
    # Route to CORA page
    cora_page()

elif selected_page == "MARK (Marketing AI)":
    # Route to MARK page
    mark_page()

elif selected_page == "OPSI (Operations)":
    # Route to OPSI page
    opsi_page()

# ========================================
# FOOTER
# ========================================
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>ApexxAdams Multi-Agent Command Center</strong></p>
        <p>CORA | MARK | OPSI | Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    """,
    unsafe_allow_html=True
)
