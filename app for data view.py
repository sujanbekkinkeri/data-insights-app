import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Data Insights App", layout="wide")

st.title("📊 Data Insights Dashboard")

# -------------------------
# File Upload
# -------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        # Safe CSV reading (handles encoding issues)
        try:
            df = pd.read_csv(uploaded_file)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding="latin1")

        # Drop completely empty rows/cols
        df.dropna(how="all", inplace=True)
        df.dropna(axis=1, how="all", inplace=True)

        st.success("File uploaded successfully!")

        # -------------------------
        # Data Preview
        # -------------------------
        st.subheader("📄 Data Preview")
        st.dataframe(df.head())

        st.subheader("📌 Dataset Info")
        st.write("Shape:", df.shape)
        st.write("Columns:", list(df.columns))

        # -------------------------
        # Filters
        # -------------------------
        st.subheader("🔍 Filters")

        if len(df.columns) > 0:

            column = st.selectbox("Choose column to filter", df.columns)

            # NUMERIC FILTER
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

            # CATEGORICAL FILTER
            else:
                unique_vals = df[column].dropna().unique()

                selected = st.multiselect(
                    "Select values",
                    unique_vals,
                    default=list(unique_vals)
                )

                if selected:
                    df = df[df[column].isin(selected)]

        # -------------------------
        # Check empty dataset after filtering
        # -------------------------
        if df.empty:
            st.warning("No data available after filtering.")
            st.stop()

        st.subheader("📊 Filtered Data")
        st.dataframe(df)

        # -------------------------
        # Visualization
        # -------------------------
        st.subheader("📈 Data Visualization")

        chart_type = st.selectbox("Select chart type", ["Bar", "Line", "Scatter"])

        col1 = st.selectbox("X-axis", df.columns)
        col2 = st.selectbox("Y-axis", df.columns)

        fig = None

        try:
            if chart_type == "Bar":
                fig = px.bar(df, x=col1, y=col2)
            elif chart_type == "Line":
                fig = px.line(df, x=col1, y=col2)
            elif chart_type == "Scatter":
                fig = px.scatter(df, x=col1, y=col2)

            st.plotly_chart(fig, use_container_width=True)

        except Exception as chart_error:
            st.error(f"Chart error: {chart_error}")

    except Exception as e:
        st.error(f"Error reading file: {e}")

else:
    st.info("📂 Upload a CSV file to get started.")
