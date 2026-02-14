import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Vaccine Reminder")

st.title("🍼 Vaccine Reminder App")

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
                st.write(
                    f"👶 {item['child_name']} | 💉 {item['vaccine_name']} | 📅 Due: {item['scheduled_date']}"
                )

                if st.button(f"Mark Done {item['id']}"):
                    done_resp = requests.put(
                        f"{API_BASE}/mark-done/{item['id']}"
                    )

                    if done_resp.status_code == 200:
                        st.success("Marked as done")
                        st.rerun()
                    else:
                        st.error("Failed to update")
