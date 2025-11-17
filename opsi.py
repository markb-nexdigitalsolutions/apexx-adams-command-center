import streamlit as st
import pandas as pd
from utils import load_opsi_data, send_opsi_task


def opsi_page():
    st.header("OPSI - Operations & Policy System")

    df = load_opsi_data()

    status_col = "Status " if "Status " in df.columns else "Status"
    priority_col = "Priority " if "Priority " in df.columns else "Priority"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        pending = len(df[df[status_col] == "New"]) if not df.empty else 0
        st.metric("Pending", pending)

    with col2:
        in_progress = len(df[df[status_col] == "In Progress"]) if not df.empty else 0
        st.metric("In Progress", in_progress)

    with col3:
        high = len(df[df[priority_col] == "High"]) if not df.empty else 0
        st.metric("High Priority", high)

    with col4:
        st.metric("Total Tasks", len(df))

    st.markdown("---")


    # ----------------------------------------------------
    # CREATE TASK
    # ----------------------------------------------------
    with st.expander("➕ Create New Task"):
        with st.form("task_form"):

            title = st.text_input("Task Title*")

            task_type = st.selectbox(
                "Task Type*",
                ["Select option", "RFP Submission", "Contract Renewal", "Audit", "Compliance Report"]
            )

            assigned_to = st.text_input("Assigned To*", placeholder="Enter person name")

            deadline = st.date_input("Deadline Date*")

            priority = st.selectbox(
                "Priority*",
                ["Select option", "High", "Medium", "Low"]
            )

            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Create Task")

            if submitted:
                errors = []

                if not title.strip():
                    errors.append("Task title is required.")
                if task_type == "Select option":
                    errors.append("Task type is required.")
                if priority == "Select option":
                    errors.append("Priority is required.")
                if not assigned_to.strip():
                    errors.append("Assigned To is required.")

                if errors:
                    for e in errors:
                        st.error(e)
                else:
                    task_data = {
                        "title": title,
                        "taskType": task_type,
                        "assignedTo": assigned_to,
                        "deadline": str(deadline),
                        "priority": priority,
                        "notes": notes,
                    }
                    result = send_opsi_task(task_data)

                    if result:
                        st.success("Task created successfully.")
                        st.cache_data.clear()
                        st.rerun()


    # ----------------------------------------------------
    # ACTIVE TASKS
    # ----------------------------------------------------
    st.subheader("Active Tasks")

    if not df.empty:
        st.dataframe(df, hide_index=True, use_container_width=True)
    else:
        st.info("No tasks found.")

