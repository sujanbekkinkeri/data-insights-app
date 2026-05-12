import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Smart Data Insights App", layout="wide")

st.title("📊 Smart CSV Data Insights App")

# -------------------- FILE UPLOAD --------------------
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:

    # Safe CSV loading (fix UnicodeDecodeError)
    try:
        df = pd.read_csv(file, encoding="utf-8")
    except UnicodeDecodeError:
        file.seek(0)
        df = pd.read_csv(file, encoding="ISO-8859-1")
    except Exception:
        file.seek(0)
        df = pd.read_csv(file, encoding="latin1", errors="replace")

    st.success("File loaded successfully!")

    # -------------------- SIDEBAR FILTERS --------------------
    st.sidebar.header("🔎 Filters")

    columns = df.columns.tolist()

    selected_columns = st.sidebar.multiselect(
        "Select Columns",
        columns,
        default=columns
    )

    df = df[selected_columns]

    # Search feature
    search = st.sidebar.text_input("Search in data")

    if search:
        df = df[df.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False)).any(axis=1)]

    # -------------------- DATA PREVIEW --------------------
    st.subheader("📌 Data Preview")
    st.dataframe(df)

    st.write("Shape:", df.shape)

    # -------------------- MISSING VALUES --------------------
    st.subheader("📉 Missing Values")
    st.dataframe(df.isnull().sum())

    # -------------------- BASIC AI INSIGHTS --------------------
    st.subheader("🧠 AI Insights (Auto Analysis)")

    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        st.write("📊 Summary Statistics")
        st.dataframe(numeric_df.describe())

        st.write("📌 Key Observations")

        for col in numeric_df.columns:
            st.write(f"- {col}: Avg = {numeric_df[col].mean():.2f}, Max = {numeric_df[col].max()}, Min = {numeric_df[col].min()}")

        if numeric_df.shape[1] > 1:
            st.write("🔗 Correlation Matrix")
            st.dataframe(numeric_df.corr())
    else:
        st.info("No numeric columns found for statistical insights.")

    # -------------------- CHART SECTION --------------------
    st.subheader("📈 Data Visualizations")

    chart_type = st.selectbox("Choose Chart Type", ["Bar Chart", "Pie Chart", "Histogram"])

    if not df.empty:

        col = st.selectbox("Select Column for Chart", df.columns)

        if chart_type == "Bar Chart":
            st.plotly_chart(px.bar(df[col].value_counts().reset_index(),
                                   x="index", y=col,
                                   title="Bar Chart"))

        elif chart_type == "Pie Chart":
            st.plotly_chart(px.pie(df, names=col, title="Pie Chart"))

        elif chart_type == "Histogram":
            if pd.api.types.is_numeric_dtype(df[col]):
                st.plotly_chart(px.histogram(df, x=col, title="Histogram"))
            else:
                st.warning("Histogram works only for numeric columns.")

    # -------------------- DOWNLOAD CLEANED DATA --------------------
    st.subheader("⬇️ Download Processed Data")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "processed_data.csv",
        "text/csv"
    )

else:
    st.info("Upload a CSV file to start analysis 👆")
