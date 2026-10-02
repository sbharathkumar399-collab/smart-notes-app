import json
import os
from datetime import datetime
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Smart Notes App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

NOTES_FILE = "notes.json"

def load_notes():
    """Load saved notes from local JSON storage."""
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_notes(notes):
    """Save notes to local JSON storage."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

# Initialize Session State
if "notes" not in st.session_state:
    st.session_state.notes = load_notes()

# App Header
st.title("📝 Smart Notes Manager")
st.caption("A clean dashboard to capture, filter, and organize your ideas.")

# Sidebar - Create Note
st.sidebar.header("➕ Create New Note")
note_title = st.sidebar.text_input("Note Title", placeholder="e.g., Project Roadmap")
note_category = st.sidebar.selectbox(
    "Category",
    ["Work", "Personal", "Study", "Ideas", "Other"]
)
note_content = st.sidebar.text_area("Content", placeholder="Write your details here...", height=150)

if st.sidebar.button("💾 Save Note", use_container_width=True):
    if note_title.strip() and note_content.strip():
        new_note = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "title": note_title.strip(),
            "category": note_category,
            "content": note_content.strip(),
            "date": datetime.now().strftime("%b %d, %Y - %I:%M %p")
        }
        st.session_state.notes.insert(0, new_note)
        save_notes(st.session_state.notes)
        st.sidebar.success("Note saved successfully!")
        st.rerun()
    else:
        st.sidebar.error("Please fill in both title and content.")

# Search and Filter
col_search, col_filter = st.columns([3, 1])

with col_search:
    search_query = st.text_input("🔍 Search Notes", placeholder="Search by title or text...")

with col_filter:
    all_categories = ["All"] + list(set(n.get("category", "Other") for n in st.session_state.notes))
    selected_category = st.selectbox("Category Filter", all_categories)

# Filtering Logic
filtered_notes = st.session_state.notes

if selected_category != "All":
    filtered_notes = [n for n in filtered_notes if n.get("category") == selected_category]

if search_query.strip():
    q = search_query.lower()
    filtered_notes = [
        n for n in filtered_notes
        if q in n["title"].lower() or q in n["content"].lower()
    ]

st.divider()

# Note List Display
total_count = len(st.session_state.notes)
showing_count = len(filtered_notes)
st.markdown(f"**Showing {showing_count} of {total_count} notes**")

if not filtered_notes:
    st.info("No matching notes found. Use the sidebar to create one!")
else:
    for idx, note in enumerate(filtered_notes):
        header_text = f"📌 {note['title']}  |  🏷️ {note.get('category', 'General')}  |  🕒 {note['date']}"
        with st.expander(header_text):
            st.write(note["content"])
            st.divider()
            if st.button("🗑️ Delete Note", key=f"del_{note['id']}_{idx}"):
                st.session_state.notes = [n for n in st.session_state.notes if n["id"] != note["id"]]
                save_notes(st.session_state.notes)
                st.success("Note deleted!")
                st.rerun()



