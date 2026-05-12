import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Insights App", layout="wide")

st.title("📊 Data Insights Dashboard")

# -------------------------
# File Upload
# -------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Handle encoding issues safely
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="latin1")

        st.success("File uploaded successfully!")

        # -------------------------
        # Show Data
        # -------------------------
        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        st.subheader("📌 Basic Info")
        st.write("Shape:", df.shape)
        st.write("Columns:", list(df.columns))

        # -------------------------
        # Filters
        # -------------------------
        st.subheader("🔍 Filters")

        column = st.selectbox("Choose column to filter", df.columns)

        if pd.api.types.is_numeric_dtype(df[column]):
            min_val = float(df[column].min())
            max_val = float(df[column].max())

            value_range = st.slider(
                "Select range",
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )

            df = df[(df[column] >= value_range[0]) & (df[column] <= value_range[1])]

        else:
            unique_vals = df[column].dropna().unique()
            selected = st.multiselect("Select values", unique_vals, default=unique_vals)
            df = df[df[column].isin(selected)]

        st.subheader("📊 Filtered Data")
        st.dataframe(df)

        # -------------------------
        # Plotly Visualization
        # -------------------------
        st.subheader("📈 Data Visualization")

        chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Scatter"])

        col1 = st.selectbox("X-axis", df.columns)
        col2 = st.selectbox("Y-axis", df.columns)

        if chart_type == "Bar":
            fig = px.bar(df, x=col1, y=col2)
        elif chart_type == "Line":
            fig = px.line(df, x=col1, y=col2)
        else:
            fig = px.scatter(df, x=col1, y=col2)

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("Upload a CSV file to get started.")
