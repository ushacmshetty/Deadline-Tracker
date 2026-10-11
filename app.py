
import streamlit as st
from datetime import datetime, timedelta
import html
from database import delete_deadline
from email_service import send_deadline_digest

from prompts import DEADLINE_EXTRACTION_PROMPT
from gemini_service import extract_deadlines
from database import (
    add_deadline,
    get_deadlines,
    update_deadline_status,
)


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Deadline Tracker",
    page_icon="📅",
    layout="wide",
)


# --------------------------------------------------
# 2. CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
    color: #1e293b;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #1e3a5f !important;
}

.stApp p, .stApp label {
    color: #334155;
}




/* Remove the dark Streamlit header */
[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}

/* Hide the header's toolbar area */
[data-testid="stToolbar"] {
    visibility: hidden !important;
    height: 0 !important;
}

/* Keep the main content properly positioned */
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
}



/* Elegant sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #ffffff 0%,
        #f0f6ff 100%
    ) !important;
    border-right: 1px solid #dbe7f5;
}

/* Sidebar text */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #173b67 !important;
}

/* Sidebar navigation labels */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #294766 !important;
    font-weight: 600;
    padding: 8px 10px;
    border-radius: 10px;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #dbe7f5 !important;
}

/* Sidebar captions */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #718096 !important;
    font-size: 12px;
}


[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-weight: 600;
}

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #dbe4f0;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(30, 58, 95, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #526079 !important;
}

[data-testid="stMetricValue"] {
    color: #1d3557 !important;
    font-weight: 700;
}

.stButton > button {
    background-color: #2563eb;
    color: #ffffff !important;
    border: none;
    border-radius: 9px;
    padding: 0.55rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border: 1px dashed #93a8c7;
    border-radius: 14px;
    padding: 16px;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: #e2e8f0;
}


/* Clean academic document uploader */
[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1px solid #dbe7f5 !important;
    border-radius: 14px !important;
    padding: 14px !important;
}

/* Improve uploader text visibility */
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small {
    color: #173b67 !important;
}


[data-testid="stFileUploader"] button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 18px !important;
}

/* Ensure the button's text and icon are white */
[data-testid="stFileUploader"] button p,
[data-testid="stFileUploader"] button span,
[data-testid="stFileUploader"] button svg {
    color: #ffffff !important;
    fill: #ffffff !important;

}


[data-testid="stFileUploader"] section {
    background: #f4f8ff !important;
    border: 1px dashed #c5d7f2 !important;
    border-radius: 12px !important;
    padding: 12px !important;
}

[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 1px solid #dbe7f5 !important;
    border-radius: 14px !important;
    padding: 14px !important;
    box-shadow: 0 4px 14px rgba(23, 59, 103, 0.05);
}


/* Make the upload area light and readable */
[data-testid="stFileUploader"] section {
    background: #f8fbff !important;
    border-radius: 10px !important;
}



/* Show file type and size instructions */
[data-testid="stFileUploaderDropzoneInstructions"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #526581 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] * {
    color: #526581 !important;
    visibility: visible !important;
    opacity: 1 !important;
    font-size: 13px !important;
}



</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 3. SIDEBAR NAVIGATION
# --------------------------------------------------

with st.sidebar:
    
    st.markdown(
    """
    <div style="
        padding: 12px 4px 18px 4px;
        border-bottom: 1px solid #dbe7f5;
        margin-bottom: 18px;
    ">
        <div style="font-size: 28px; margin-bottom: 8px;">
            📅
        </div>
        <div style="
            font-size: 21px;
            font-weight: 750;
            color: #173b67;
            letter-spacing: -0.5px;
        ">
            Deadline Tracker
        </div>
        <div style="
            color: #718096;
            font-size: 12px;
            margin-top: 5px;
        ">
            Plan smarter. Finish on time.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "☁️ Upload Document",
            "📋 Saved Deadlines",
        ],
        label_visibility="collapsed",
        key="navigation_page",
    )

    st.divider()
    st.caption("✨ Powered by Gemini AI")
    st.caption("Turn your notes into organized deadlines.")


# --------------------------------------------------
# 4. SHARED DATA AND HELPER FUNCTION
# --------------------------------------------------

today = datetime.today().date()
today_date = today.strftime("%A, %d %B %Y")

all_deadlines = get_deadlines()


def get_task_status(deadline):
    """Return the current status of a saved deadline."""

    date_text = str(deadline[2] or "").strip()
    completed = bool(deadline[4])

    if completed:
        return "Completed"

    if not date_text:
        return "Date missing"

    try:
        due_date = datetime.strptime(
            date_text, "%Y-%m-%d"
        ).date()
    except ValueError:
        return "Check date"

    if due_date < today:
        return "Overdue"

    return "Pending"


# Calculate dashboard totals.
total_tasks = len(all_deadlines)

completed_tasks = sum(
    1 for task in all_deadlines
    if get_task_status(task) == "Completed"
)

overdue_tasks = sum(
    1 for task in all_deadlines
    if get_task_status(task) == "Overdue"
)

pending_tasks = sum(
    1 for task in all_deadlines
    if get_task_status(task) == "Pending"
)


# --------------------------------------------------
# 5. DASHBOARD PAGE
# --------------------------------------------------

if page == "🏠 Dashboard":

    st.title("☀️ Good Morning!")
    st.write(
        "Stay organized, meet your deadlines, achieve your goals."
    )
    st.caption(f"📅 Today is {today_date}")
    st.divider()

    st.subheader("📊 Your Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📋 Total Tasks", total_tasks)
    col2.metric("✅ Completed", completed_tasks)
    col3.metric("⏳ Pending", pending_tasks)
    col4.metric("⚠️ Overdue", overdue_tasks)

    
st.divider()

st.subheader("📧 Email Deadline Digest")

st.write(
    "Send a summary of pending deadlines due today "
    "or within the next 3 days to your email."
)

if st.button("📨 Send Email Digest", key="send_email_digest"):
    with st.spinner("Sending email..."):
        success, message = send_deadline_digest()

    if success:
        st.success(message)
    else:
        st.error(message)



    

    st.divider()
    st.subheader("📅 Upcoming Deadlines (Next 7 Days)")

    next_week = today + timedelta(days=7)
    upcoming = []

    for deadline in all_deadlines:
        if get_task_status(deadline) != "Pending":
            continue

        try:
            due_date = datetime.strptime(
                deadline[2], "%Y-%m-%d"
            ).date()
        except (ValueError, TypeError):
            continue

        if today <= due_date <= next_week:
            upcoming.append(deadline)

    upcoming.sort(key=lambda task: task[2])

    if upcoming:
        for deadline in upcoming:
            task_name = html.escape(str(deadline[1] or "Untitled task"))
            date_text = html.escape(str(deadline[2] or "No date"))
            subject = html.escape(str(deadline[3] or "Not specified"))

            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #dbe4f0;
                    border-left:5px solid #2563eb;
                    border-radius:12px;
                    padding:16px;
                    margin-bottom:10px;">
                    <h3 style="margin:0 0 8px 0;">📌 {task_name}</h3>
                    <p>📅 Due date: {date_text}</p>
                    <p>📚 Subject: {subject}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No upcoming deadlines in the next 7 days. 🎉")

    st.caption("Open Saved Deadlines to view and manage every task.")


# --------------------------------------------------
# 6. UPLOAD DOCUMENT PAGE
# --------------------------------------------------

elif page == "☁️ Upload Document":

    st.title("☁️ Upload Your Academic Document")
    st.write(
        "Upload a syllabus, timetable, or assignment image. "
        "Gemini AI will help extract the deadlines."
    )
    st.divider()

    uploaded_file = st.file_uploader(
        "Choose an academic document",
        type=["png", "jpg", "jpeg", "webp"],
        key="academic_document",
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption="Uploaded academic document",
            use_container_width=True,
        )

        if st.button("🤖 Extract Deadlines", type="primary"):

            try:
                with st.spinner("AI is analyzing your document..."):

                    extracted = extract_deadlines(
                        uploaded_file.getvalue(),
                        uploaded_file.type,
                        DEADLINE_EXTRACTION_PROMPT,
                    )

                    if not isinstance(extracted, list):
                        raise ValueError(
                            "AI did not return a valid list of deadlines."
                        )

                    valid_deadlines = []
                    invalid_deadlines = []

                    for item in extracted:
                        if not isinstance(item, dict):
                            continue

                        task_name = str(
                            item.get("task", "")
                        ).strip()

                        date_text = str(
                            item.get("date", "")
                        ).strip()

                        subject = str(
                            item.get("subject", "")
                        ).strip()

                        if not task_name:
                            continue

                        try:
                            datetime.strptime(
                                date_text, "%Y-%m-%d"
                            )

                            add_deadline(
                                task_name,
                                date_text,
                                subject,
                            )

                            valid_deadlines.append({
                                "task": task_name,
                                "date": date_text,
                                "subject": subject,
                            })

                        except ValueError:
                            invalid_deadlines.append({
                                "task": task_name,
                                "date": date_text,
                                "subject": subject,
                            })

                    st.session_state["extracted_deadlines"] = (
                        valid_deadlines
                    )
                    st.session_state["invalid_deadlines"] = (
                        invalid_deadlines
                    )

            except Exception as error:
                st.error(f"Could not extract deadlines: {error}")

    # Show the extraction results on the Upload page.
    valid_results = st.session_state.get(
        "extracted_deadlines", []
    )
    invalid_results = st.session_state.get(
        "invalid_deadlines", []
    )

    if valid_results:
        st.divider()
        st.subheader("📋 Extracted Deadlines")
        st.success(
            f"Found {len(valid_results)} valid deadline(s)."
        )

        for item in valid_results:
            st.markdown(f"**📌 {item['task']}**")
            st.write(f"📅 Date: {item['date']}")
            st.write(
                f"📚 Subject: {item['subject'] or 'Not specified'}"
            )
            st.divider()

    if invalid_results:
        st.subheader("⚠️ Deadlines Needing Confirmation")

        for item in invalid_results:
            st.warning(
                f"{item['task']} — Date: "
                f"{item['date'] or 'Unclear'}"
            )
            st.write(
                f"Subject: {item['subject'] or 'Not specified'}"
            )


# --------------------------------------------------
# 7. SAVED DEADLINES PAGE
# --------------------------------------------------

elif page == "📋 Saved Deadlines":

    st.title("📋 All Saved Deadlines")
    st.write("View and manage all your academic tasks.")
    st.divider()

    # Reload saved tasks from the database.
    saved_deadlines = get_deadlines()

    if not saved_deadlines:
        st.info(
            "No deadlines saved yet. Upload a document to get started."
        )

    else:
        # Search and status filter.
        
        search_col, filter_col, sort_col = st.columns([2, 1, 1])
  
        with search_col:
            search_query = st.text_input(
                "🔍 Search tasks",
                placeholder="Search by task name or subject...",
                key="task_search",
            ).strip().lower()

        with filter_col:
            filter_status = st.selectbox(
                "Filter by status",
                [
                    "All Tasks",
                    "Pending",
                    "Completed",
                    "Overdue",
                    "Date missing",
                    "Check date",
                ],
                key="task_status_filter",
            )
        
        with sort_col:
           sort_order = st.selectbox(
              "Sort by deadline",
              [
                 "Nearest first",
                 "Latest first",
        ],
        key="deadline_sort_order",
    )





        # Filter tasks without deleting anything from the database.
        filtered_deadlines = []

        for deadline in saved_deadlines:
            task_name = str(deadline[1] or "").lower()
            subject_name = str(deadline[3] or "").lower()

            matches_search = (
                not search_query
                or search_query in task_name
                or search_query in subject_name
            )

            task_status = get_task_status(deadline)

            matches_status = (
                filter_status == "All Tasks"
                or filter_status == task_status
            )

            if matches_search and matches_status:
                filtered_deadlines.append(deadline)

        
        if sort_order == "Nearest first":
                filtered_deadlines.sort(
                   key=lambda task: (
                       not bool(task[2]),
                       task[2] or "9999-12-31"
                   )
                )
        else:
                filtered_deadlines.sort(
                    key=lambda task: (
                        not bool(task[2]),
                        task[2] or ""
                    ),
                    reverse=True
    )


        st.caption(
            f"Showing {len(filtered_deadlines)} of "
            f"{len(saved_deadlines)} saved task(s)."
        )

        if not filtered_deadlines:
            st.warning(
                "No tasks match your search or selected status. "
                "Try clearing the search or choosing All Tasks."
            )

        for deadline in filtered_deadlines:
            deadline_id = deadline[0]
            task_name = str(deadline[1] or "Untitled task")
            date_text = str(deadline[2] or "Not available")
            subject = str(deadline[3] or "Not specified")
            completed = bool(deadline[4])

            status = get_task_status(deadline)

            status_styles = {
                "Completed": ("#dcfce7", "#166534", "#16a34a"),
                "Pending": ("#fef3c7", "#92400e", "#d97706"),
                "Overdue": ("#fee2e2", "#991b1b", "#dc2626"),
                "Date missing": ("#e2e8f0", "#334155", "#64748b"),
                "Check date": ("#e2e8f0", "#334155", "#64748b"),
            }

            bg_color, text_color, border_color = (
                status_styles[status]
            )

            safe_task = html.escape(task_name)
            safe_date = html.escape(date_text)
            safe_subject = html.escape(subject)

            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    border:1px solid #dbe4f0;
                    border-left:6px solid {border_color};
                    border-radius:14px;
                    padding:20px;
                    margin-top:12px;
                    box-shadow:0 4px 12px rgba(30,58,95,0.06);">
                    <h3 style="margin:0 0 12px 0;">
                        📌 {safe_task}
                    </h3>
                    <p>📅 <b>Deadline:</b> {safe_date}</p>
                    <p>📚 <b>Subject:</b> {safe_subject}</p>
                    <span style="
                        display:inline-block;
                        background:{bg_color};
                        color:{text_color};
                        border-radius:20px;
                        padding:6px 12px;
                        font-weight:600;">
                        {status}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )


            
        
            confirm_key = f"confirm_delete_{deadline_id}"

            if st.button(
                "🗑️ Delete Task",
                key=f"delete_{deadline_id}",
            ):
                st.session_state[confirm_key] = True

            if st.session_state.get(confirm_key, False):
                st.warning(
                    f"Are you sure you want to delete '{task_name}'?"
                )

                confirm_col, cancel_col = st.columns(2)

                with confirm_col:
                    if st.button(
                        "Yes, Delete",
                        key=f"yes_delete_{deadline_id}",
                    ):
                        deleted = delete_deadline(deadline_id)

                        if deleted:
                            st.session_state.pop(confirm_key, None)
                            st.success("Task deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Task could not be deleted.")

                with cancel_col:
                    if st.button(
                        "Cancel",
                        key=f"cancel_delete_{deadline_id}",
                    ):
                        st.session_state.pop(confirm_key, None)
                        st.rerun()



# --------------------------------------------------
# 8. FOOTER
# --------------------------------------------------

st.divider()
st.caption(
    "📅 Deadline Tracker | Powered by Python, "
    "Streamlit, Gemini AI, and SQLite"
)
