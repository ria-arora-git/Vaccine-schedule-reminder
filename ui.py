import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Vaccine Reminder", layout="wide")

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(180deg, #e6f2ff 0%, #cce6ff 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
    padding-top: 40px;
}

/* Sidebar text */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p {
    color: #003366;
}

/* Sidebar buttons */
section[data-testid="stSidebar"] button {
    background-color: #003366;
    color: white;
    border-radius: 8px;
    border: none;
    margin-bottom: 12px;
    font-weight: 600;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #002244;
}

/* Input boxes */
input, textarea, .stDateInput input {
    background-color: white !important;
    color: #003366 !important;
    border-radius: 8px !important;
    border: 2px solid #003366 !important;
}

/* Remove red focus border */
input:focus, textarea:focus {
    border: 2px solid #003366 !important;
    box-shadow: none !important;
}

/* Main Buttons */
div.stButton > button {
    background-color: white;
    color: #003366;
    border-radius: 8px;
    border: 2px solid #003366;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #003366;
    color: white;
    border: 2px solid white;
}

/* Headings */
h1, h2, h3 {
    color: #003366;
    font-weight: 700;
}

/* Card style */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
}
            
/* Override all alert boxes */
div[data-testid="stAlert"] {
    background-color: #cc0000 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 15px !important;
    font-weight: 600;
}

/* Remove ugly icons spacing */
div[data-testid="stAlert"] svg {
    display: none;
}

/* Make text inside alert white */
div[data-testid="stAlert"] p {
    color: white !important;
}


</style>
""", unsafe_allow_html=True)

st.title("Vaccine Reminder App")

st.sidebar.title("Menu")

if "menu" not in st.session_state:
    st.session_state.menu = "Add Child"

if st.sidebar.button("Add Child"):
    st.session_state.menu = "Add Child"

if st.sidebar.button("Add Vaccine Manually"):
    st.session_state.menu = "Add Vaccine Manually"

if st.sidebar.button("Upload Vaccine Sheet"):
    st.session_state.menu = "Upload Vaccine Sheet"

if st.sidebar.button("View Pending"):
    st.session_state.menu = "View Pending"

menu = st.session_state.menu


def fetch_children():
    try:
        response = requests.get(f"{API_BASE}/children/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []


# ADD CHILD
if menu == "Add Child":
    st.header("Add Child")

    name = st.text_input("Child Name")
    email = st.text_input("Parent Email")
    birth_date = st.date_input("Birth Date")

    if st.button("Create Child"):
        if not name.strip() or not email.strip():
            st.error("Name and Email are required")
        else:
            response = requests.post(
                f"{API_BASE}/child/",
                json={
                    "name": name.strip(),
                    "parent_email": email.strip(),
                    "birth_date": str(birth_date)
                }
            )

            if response.status_code == 200:
                st.success("Child created successfully")
                st.json(response.json())
            else:
                st.error("Something went wrong")


# ADD VACCINE
elif menu == "Add Vaccine Manually":
    st.header("Add Vaccine Schedule")

    children = fetch_children()

    if not children:
        st.warning("No children registered yet.")
    else:
        child_options = {c["name"]: c["id"] for c in children}
        selected_child = st.selectbox("Select Child", list(child_options.keys()))
        child_id = child_options[selected_child]

        vaccine_name = st.text_input("Vaccine Name")
        due_date = st.date_input("Due Date")

        if st.button("Add Vaccine"):
            response = requests.post(
                f"{API_BASE}/schedule/",
                json={
                    "child_id": child_id,
                    "vaccine_name": vaccine_name,
                    "scheduled_date": str(due_date)
                }
            )

            if response.status_code == 200:
                st.success("Vaccine scheduled")
                st.json(response.json())
            else:
                st.error("Failed to schedule vaccine")


# UPLOAD SHEET
elif menu == "Upload Vaccine Sheet":
    st.header("Upload Vaccine Sheet")

    children = fetch_children()

    if not children:
        st.warning("No children registered yet.")
    else:
        child_options = {c["name"]: c["id"] for c in children}
        selected_child = st.selectbox("Select Child", list(child_options.keys()))
        selected_child_id = child_options[selected_child]

        file = st.file_uploader("Upload PDF or Image")

        if st.button("Upload and Parse") and file:
            response = requests.post(
                f"{API_BASE}/upload-sheet/?child_id={selected_child_id}",
                files={"file": (file.name, file, file.type)}
            )

            if response.status_code == 200:
                st.success("Sheet processed successfully")
                st.json(response.json())
            else:
                st.error("Upload failed")
                st.text(response.text)


# VIEW PENDING
elif menu == "View Pending":
    st.header("Pending Vaccines")

    response = requests.get(f"{API_BASE}/pending/")

    if response.status_code != 200:
        st.error("Failed to fetch pending vaccines")
    else:
        data = response.json()

        if not data:
            st.success("No pending vaccines 🎉")
        else:
            for item in data:
                st.markdown(f"""
                <div class="card">
                    <b style="color:#003366">{item['child_name']}</b><br>
                    {item['vaccine_name']}<br>
                    Due: {item['scheduled_date']}
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Mark Done {item['id']}"):
                    done_resp = requests.put(
                        f"{API_BASE}/mark-done/{item['id']}"
                    )

                    if done_resp.status_code == 200:
                        st.success("Marked as done")
                        st.rerun()
                    else:
                        st.error("Failed to update")
