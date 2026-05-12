import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Insights App", layout="wide")

st.title("📊 Data Insights Web App")

# Upload CSV
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # ---------------- FILTER SECTION ----------------
    st.subheader("🎯 Filter Data")

    col1, col2 = st.columns(2)

    with col1:
        selected_column = st.selectbox("Select column to filter", df.columns)

    with col2:
        unique_values = df[selected_column].dropna().unique()
        selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]

    st.write("Filtered Data", filtered_df)

    # ---------------- COLUMN SELECT ----------------
    st.subheader("📂 Select Columns")

    selected_columns = st.multiselect("Choose columns to display", df.columns)

    if selected_columns:
        st.write(df[selected_columns])
    else:
        st.write("Showing full dataset")
        st.write(df)

    # ---------------- SUMMARY ----------------
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # ---------------- CHARTS ----------------
    st.subheader("📊 Visualizations")

    numeric_columns = df.select_dtypes(include=['number']).columns

    if len(numeric_columns) > 0:
        chart_column = st.selectbox("Select numeric column for chart", numeric_columns)

        st.write("Bar Chart")
        st.bar_chart(df[chart_column])

        st.write("Line Chart")
        st.line_chart(df[chart_column])
    else:
        st.write("No numeric columns available for charts")

else:
    st.info("👆 Upload a CSV file to get started")