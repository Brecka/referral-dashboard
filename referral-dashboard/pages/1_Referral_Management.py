import streamlit as st

st.title("Referral Management")

st.write("Enter, search, and manage referral records.")

st.subheader("New Referral")

with st.form("referral_form"):
    client_name = st.text_input("Client Name")

    level = st.selectbox(
        "Level of Care",
        ["ASAM 3.1", "ASAM 3.5", "ASAM 3.7", "ASAM 4.0"]
    )

    status = st.selectbox(
        "Status",
        ["Pending", "Approved", "Denied"]
    )

    submitted = st.form_submit_button("Save Referral")

if submitted:
    st.success(f"Referral entered for {client_name}")
