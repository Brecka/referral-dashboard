import streamlit as st
import pandas as pd

st.title("Referral Dashboard")

df = pd.read_excel(
    r"C:\Users\Sarbreck.Brown\Downloads\Dashboard.xlsx",
    sheet_name="Referral_Clean"
)

levels = ["All"] + sorted(df["Level of Care"].dropna().unique().tolist())
selected_level = st.selectbox("Select Level of Care", levels)

if selected_level == "All":
    filtered_df = df
else:
    filtered_df =df[df["Level of Care"] == selected_level]
st.write("Total Referrals:", len(filtered_df))

st.subheader("Referrals by Day of Week")

days = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

counts = filtered_df["Day Name"].value_counts().reindex(days, fill_value=0)

st.line_chart(counts)