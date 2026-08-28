import streamlit as st
import pandas as pd
import database
import classifier

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Campus Issue Triage System",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for styling cards, badges, and metrics
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .badge-high {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-medium {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-low {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .card-box {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Ensure DB has sample data if running for the first time
database.seed_sample_data()

# Header Section
st.markdown("<div class='main-header'>🎓 AI Campus Issue Triage System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Automated issue classification, priority routing, and department dispatch system</div>", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["1. Submit Issue", "2. Admin Dashboard", "3. Search & Filter"])

st.sidebar.divider()
st.sidebar.info("""
**Tech Stack:**
- **Python** (Core Logic)
- **Streamlit** (UI Web Framework)
- **SQLite** (Database Engine)
- **Rule-Based AI Classifier** (Triage Logic)
""")

# ==========================================
# PAGE 1: SUBMIT ISSUE
# ==========================================
if page == "1. Submit Issue":
    st.subheader("📝 Submit a New Campus Issue")
    st.write("Enter your issue details below. The AI classifier will automatically categorize and prioritize your report.")

    col1, col2 = st.columns([1, 1])

    with col1:
        student_name = st.text_input("Student Name", placeholder="e.g. Rashmi Ranjan Sharma")
        location = st.text_input("Campus Location / Room", placeholder="e.g. Block C - Room 302, Library, Lab 2")
        issue_text = st.text_area("Issue Description", placeholder="e.g. The Wi-Fi in Block C has stopped working for everyone since morning.", height=120)

        # Real-time preview of classification logic
        triage_result = None
        if issue_text.strip():
            triage_result = classifier.classify_issue(issue_text, location)

        submit_btn = st.button("🚀 Submit Issue Report", type="primary", use_container_width=True)

        if submit_btn:
            if not student_name or not location or not issue_text:
                st.error("⚠️ Please fill in all fields (Name, Location, and Issue Description).")
            else:
                result = triage_result if triage_result else classifier.classify_issue(issue_text, location)
                
                # Save into SQLite database
                new_id = database.add_issue(
                    student_name=student_name,
                    location=location,
                    issue_text=issue_text,
                    category=result["category"],
                    priority=result["priority"],
                    department=result["department"],
                    suggested_action=result["suggested_action"]
                )
                
                st.success(f"✅ Issue successfully submitted! Ticket ID: **#{new_id}**")
                st.balloons()

    with col2:
        st.markdown("### 🤖 Live AI Classification Preview")
        if triage_result:
            p_color = {
                "HIGH": "🔴 HIGH",
                "MEDIUM": "🟡 MEDIUM",
                "LOW": "🟢 LOW"
            }.get(triage_result["priority"], "🟢 LOW")

            st.markdown(f"""
            <div class='card-box'>
                <h4>Automatic Triage Results:</h4>
                <p><b>Category:</b> {triage_result['category']}</p>
                <p><b>Priority:</b> {p_color}</p>
                <p><b>Assigned Department:</b> {triage_result['department']}</p>
                <p><b>Suggested Action:</b><br>{triage_result['suggested_action']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("👈 Type an issue description on the left to see the AI classification in real-time!")


# ==========================================
# PAGE 2: ADMIN DASHBOARD
# ==========================================
elif page == "2. Admin Dashboard":
    st.subheader("📊 Campus Admin Triage Dashboard")
    
    # Fetch metrics from SQLite
    stats = database.get_issue_stats()

    # Metric Cards
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Total Issues", stats["total"])
    m2.metric("🔴 High Priority", stats["high"])
    m3.metric("🟡 Medium Priority", stats["medium"])
    m4.metric("🟢 Low Priority", stats["low"])
    m5.metric("📬 Open Tickets", stats["open"])

    st.divider()

    st.markdown("### 📋 All Campus Tickets")
    all_issues = database.get_all_issues()

    if not all_issues:
        st.info("No issues reported yet.")
    else:
        for issue in all_issues:
            priority_badge = {
                "HIGH": "<span class='badge-high'>🔴 HIGH</span>",
                "MEDIUM": "<span class='badge-medium'>🟡 MEDIUM</span>",
                "LOW": "<span class='badge-low'>🟢 LOW</span>"
            }.get(issue["priority"], "LOW")

            with st.expander(f"Ticket #{issue['id']} - {issue['category']} | {issue['student_name']} ({issue['location']}) - Status: {issue['status']}"):
                col_a, col_b = st.columns([2, 1])

                with col_a:
                    st.markdown(f"**Description:** {issue['issue_text']}")
                    st.markdown(f"**Category:** {issue['category']} | **Priority:** {priority_badge}", unsafe_allow_html=True)
                    st.markdown(f"**Assigned Department:** `{issue['department']}`")
                    st.markdown(f"**Suggested Action:** {issue['suggested_action']}")
                    st.caption(f"Reported at: {issue['created_at']}")

                with col_b:
                    st.markdown("**Update Status:**")
                    status_options = ["OPEN", "IN PROGRESS", "RESOLVED"]
                    current_idx = status_options.index(issue['status']) if issue['status'] in status_options else 0
                    
                    new_status = st.selectbox(
                        "Change Status",
                        options=status_options,
                        index=current_idx,
                        key=f"status_select_{issue['id']}"
                    )
                    
                    if new_status != issue['status']:
                        if st.button("Update Status", key=f"btn_update_{issue['id']}"):
                            database.update_issue_status(issue['id'], new_status)
                            st.success(f"Status updated to {new_status}!")
                            st.rerun()


# ==========================================
# PAGE 3: SEARCH & FILTER
# ==========================================
elif page == "3. Search & Filter":
    st.subheader("🔍 Search & Filter Issues")
    
    all_issues = database.get_all_issues()
    if not all_issues:
        st.info("No issues in database.")
    else:
        # Search and Filter Bar
        f_col1, f_col2, f_col3, f_col4 = st.columns([1, 1, 1, 1.5])

        with f_col1:
            category_filter = st.selectbox("Category", ["All", "Network", "Equipment", "Infrastructure", "General"])
        with f_col2:
            priority_filter = st.selectbox("Priority", ["All", "HIGH", "MEDIUM", "LOW"])
        with f_col3:
            status_filter = st.selectbox("Status", ["All", "OPEN", "IN PROGRESS", "RESOLVED"])
        with f_col4:
            search_query = st.text_input("Search Keyword", placeholder="e.g. Wi-Fi, projector, Rashmi")

        # Apply filters
        filtered_issues = all_issues

        if category_filter != "All":
            filtered_issues = [i for i in filtered_issues if i["category"] == category_filter]

        if priority_filter != "All":
            filtered_issues = [i for i in filtered_issues if i["priority"] == priority_filter]

        if status_filter != "All":
            filtered_issues = [i for i in filtered_issues if i["status"] == status_filter]

        if search_query.strip():
            sq = search_query.lower()
            filtered_issues = [
                i for i in filtered_issues 
                if sq in i["issue_text"].lower() or sq in i["student_name"].lower() or sq in i["location"].lower()
            ]

        st.markdown(f"**Showing {len(filtered_issues)} results:**")

        # Convert to Pandas DataFrame for table display
        if filtered_issues:
            df = pd.DataFrame(filtered_issues)
            # Reorder display columns
            df_display = df[["id", "student_name", "location", "issue_text", "category", "priority", "department", "suggested_action", "status", "created_at"]]
            df_display.columns = ["ID", "Student", "Location", "Issue Description", "Category", "Priority", "Department", "Suggested Action", "Status", "Date"]
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.warning("No issues found matching the selected filters.")
