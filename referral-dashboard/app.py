import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("Referral Dashboard")

df = pd.read_excel(
    "referral-dashboard/Dashboard.xlsx",
    sheet_name="Referral_Clean"

)

levels = ["All"] + sorted(df["Level of Care"].dropna().unique().tolist())
selected_level = st.sidebar.selectbox("Select Level of Care", levels)

if selected_level == "All":
    filtered_df = df
else:
    filtered_df =df[df["Level of Care"] == selected_level]
st.write("Total Referrals:", len(filtered_df))


days = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

counts = filtered_df["Day Name"].value_counts().reindex(days, fill_value=0)
col1, col2 = st.columns(2)


with col1:
    st.subheader("Referrals by Day of Week")
st.line_chart(counts, x_label="Day of Week")

with col2:
    st.subheader("Referrals by Level of Care")
    level_counts = filtered_df["Level of Care"].value_counts()
    st.bar_chart(level_counts)
    
