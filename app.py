
import plotly.express as px
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

# 1. Page Configuration
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("📊 HR Analytics Interactive Web Dashboard")
st.markdown("PostgreSQL Live Database Connection")

# 2. Database Connection Setup
db_password = "admin123"  # <-- Apna PostgreSQL Password Yahan Enter Karein


@st.cache_data(ttl=60)
def load_data():
    engine = create_engine(
        f"postgresql://postgres:{db_password}@localhost:5432/hr_db"
    )
    query = "SELECT * FROM hr_data;"
    return pd.read_sql(query, engine)


try:
    df = load_data()

    # 3. Sidebar Filters
    st.sidebar.header("Filter Options")

    # Department Filter
    dept_options = ["All"] + list(df["department"].unique())
    selected_dept = st.sidebar.selectbox("Select Department", dept_options)

    # Employee Type Filter
    type_options = ["All"] + list(df["emp_type"].unique())
    selected_type = st.sidebar.selectbox("Select Employee Type", type_options)

    # Filtering Data
    filtered_df = df.copy()
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df["department"] == selected_dept]
    if selected_type != "All":
        filtered_df = filtered_df[filtered_df["emp_type"] == selected_type]

    # 4. KPI Cards Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Headcount", f"{len(filtered_df):,}")
    col2.metric("Average Salary", f"${filtered_df['salary'].mean():,.2f}")
    col3.metric(
        "Avg Leave Balance", f"{filtered_df['leave_balance'].mean():.1f} Days"
    )

    st.markdown("---")

    # 5. Visualizations
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Headcount by Department")
        dept_counts = (
            filtered_df["department"]
            .value_counts()
            .reset_index()
            .rename(columns={"count": "Headcount"})
        )
        fig_bar = px.bar(
            dept_counts,
            x="department",
            y="Headcount",
            text="Headcount",
            color="department",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_bar.update_traces(
            textposition="outside", texttemplate="%{text:,}"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.subheader("Gender Breakdown")
        fig_pie = px.pie(
            filtered_df,
            names="gender",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # 6. Detailed Data Table View
    st.subheader("Filtered Employee Records")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error connecting to PostgreSQL database: {e}")