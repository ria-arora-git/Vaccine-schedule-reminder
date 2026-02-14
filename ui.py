import streamlit as st
import requests
from datetime import date

API_BASE = "http://127.0.0.1:8000"

children = requests.get(f"{API_BASE}/children/").json()

if children:
    child_options = {c["name"]: c["id"] for c in children}

    selected_child_name = st.selectbox(
        "Select Child",
        list(child_options.keys())
    )

    selected_child_id = child_options[selected_child_name]
else:
    st.warning("No children registered yet.")
    selected_child_id = None


st.title("🍼 Vaccine Reminder App")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Add Child", "Add Vaccine Manually", "Upload Vaccine Sheet", "View Pending"]
)

if menu == "Add Child":
    st.header("Add Child")

    name = st.text_input("Child Name", key="child_name")
    email = st.text_input("Parent Email", key="parent_email")
    birth_date = st.date_input("Birth Date", key="birth_date")



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
            st.success("Child created successfully")
            st.write(response.json())



elif menu == "Add Vaccine Manually":
    st.header("Add Vaccine Schedule")

    if children:
        child_options = {c["name"]: c["id"] for c in children}
        selected_child_name = st.selectbox(
            "Select Child",
            list(child_options.keys()),
            key="manual_child"
        )
        child_id = child_options[selected_child_name]
    else:
        st.warning("No children available.")
        child_id = None

    vaccine_name = st.text_input("Vaccine Name")
    due_date = st.date_input("Due Date")

    if st.button("Add Vaccine") and child_id:
        response = requests.post(
            f"{API_BASE}/schedule/",
            json={
                "child_id": child_id,
                "vaccine_name": vaccine_name,
                "scheduled_date": str(due_date)
            }
        )
        st.success(response.json())


elif menu == "Upload Vaccine Sheet":
    st.header("Upload Vaccine Sheet")

    # Fetch children from backend
    children_response = requests.get(f"{API_BASE}/children/")
    children = children_response.json()

    if children:
        child_options = {c["name"]: c["id"] for c in children}

        selected_child_name = st.selectbox(
            "Select Child",
            list(child_options.keys())
        )

        selected_child_id = child_options[selected_child_name]
    else:
        st.warning("No children registered yet.")
        selected_child_id = None

    file = st.file_uploader("Upload PDF or Image")

    if st.button("Upload and Parse") and file and selected_child_id:
        response = requests.post(
            f"{API_BASE}/upload-sheet/?child_id={selected_child_id}",
            files={"file": (file.name, file, file.type)}
        )

        st.write("Status Code:", response.status_code)
        st.write("Raw Response:", response.text)



elif menu == "View Pending":
    st.header("Pending Vaccines")

    response = requests.get(f"{API_BASE}/pending/")
    data = response.json()

    if data:
        for item in data:
            st.write(
                f"{item['child_name']} - {item['vaccine_name']} due on {item['scheduled_date']}"
            )

            if st.button(f"Mark Done {item['id']}"):
                requests.put(f"{API_BASE}/mark-done/{item['id']}")
                st.success("Marked as done")
    else:
        st.success("No pending vaccines.")


