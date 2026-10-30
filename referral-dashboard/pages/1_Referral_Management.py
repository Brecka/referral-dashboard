
import streamlit as st
import psycopg

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
        ["Pending", "Approved", "Denied", "Waitlisted"]
    )

    submitted = st.form_submit_button("Save Referral")

if submitted:
    if not client_name.strip():
        st.error("Please enter a client name.")
    else:
        try:
            with psycopg.connect(
                st.secrets["DATABASE_URL"],
                connect_timeout=10
            ) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO public.referrals
                            (client_name, level_of_care, status)
                        VALUES (%s, %s, %s)
                        """,
                        (client_name.strip(), level, status)
                    )

            st.success("Referral saved successfully!")

        except psycopg.Error:
            st.error(
                "Could not save the referral. "
                "Please check the database connection."
            )

st.subheader("Search Referrals")

search_name = st.text_input("Search by Client Name")

search_level = st.selectbox(
    "Filter by Level of Care",
    ["All", "ASAM 3.1", "ASAM 3.5", "ASAM 3.7", "ASAM 4.0"]
)

search_status = st.selectbox(
    "Filter by Status",
    ["All", "Pending", "Approved", "Denied","Waitlisted"]
)


try:
    with psycopg.connect(
        st.secrets["DATABASE_URL"],
        connect_timeout=10
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT referral_id, client_name,
                       level_of_care, status, date_created
                FROM public.referrals
                ORDER BY referral_id DESC
                """
            )
            records = cur.fetchall()
            columns = [column.name for column in cur.description]

    import pandas as pd

    df = pd.DataFrame(records, columns=columns)

    if search_name:
        df = df[
            df["client_name"].str.contains(
                search_name, case=False, na=False, regex=False
            )
        ]

    if search_level != "All":
        df = df[df["level_of_care"] == search_level]

    if search_status != "All":
        df = df[df["status"] == search_status]

    st.write("Matching Referrals:", len(df))

    st.dataframe(df, use_container_width=True, hide_index=True)

except psycopg.Error as e:
    st.error(f"Database error: {e}")


st.subheader("Update Referral Status")

referral_id = st.number_input(
    "Referral ID",
    min_value=1,
    step=1
)

new_status = st.selectbox(
    "New Status",
    ["Pending", "Approved", "Denied","Waitlisted"]
)

if st.button("Update Status"):
    try:
        with psycopg.connect(
            st.secrets["DATABASE_URL"],
            connect_timeout=10
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE public.referrals
                    SET status = %s
                    WHERE referral_id = %s
                    """,
                    (new_status, referral_id)
                )
                updated_rows = cur.rowcount

        if updated_rows:
            st.success("Referral status updated!")
            st.rerun()
        else:
            st.warning("No referral found with that ID.")

    except psycopg.Error as e:
        st.error(f"Database error: {e}")
