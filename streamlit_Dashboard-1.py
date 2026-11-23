import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import plotly.express as px

username = 'root'
password = '12345'
host = 'localhost'
database = 'credit_analysis'
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

# 1. Page setup
st.set_page_config(page_title="Simple Dashboard", layout="wide")
st.title("📊 Credit risk analysis dashboard")
st.write("A clean starting point with sidebar filters, KPI metrics, a chart, and a data table.")


# 2. Executive Management Styling
st.markdown(
    """
    <style>
        .stApp {
            primaryColor = "#0F766E"
            backgroundColor = "#F4F7F6"
            secondaryBackgroundColor = "#FFFFFF"
            textColor = "#111827"
            font = "sans serif"
        }
        .exec-header {
            background: linear-gradient(90deg, #0F172A 0%, #1E3A8A 100%);
            color: #FFFFFF;
            padding: 1.25rem 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.25rem;
        }
        .exec-header h1 {
            color: #FFFFFF;
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0 0 0.25rem 0;
        }
        .exec-header p {
            color: #CBD5E1;
            margin: 0;
            font-size: 0.95rem;
        }
        div[data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 0.95rem 1.15rem;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
        }
        div[data-testid="stMetricLabel"] {
            color: #475569;
            font-weight: 600;
        }
        div[data-testid="stMetricValue"] {
            color: #0F172A;
            font-weight: 700;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="exec-header">
        <h1>Credit Risk Analysis</h1>
        <p>Portfolio exposure and credit distribution by contract status</p>
    </div>
    """,
    unsafe_allow_html=True,
)

#3. data loading
df = pd.read_csv(r"D:\pandas\.venv\project files\cleaned_loan_data.csv")

# 4. Contract Status Filter
status_col = "NAME_CONTRACT_STATUS"
credit_col = "AMT_CREDIT"

if status_col in df.columns:
    all_statuses = sorted(df[status_col].dropna().unique().tolist())
    selected_statuses = st.multiselect(
        "Contract Status",
        options=all_statuses,
        default=all_statuses,
    )
    if selected_statuses:
        filtered_df = df[df[status_col].isin(selected_statuses)].copy()
    else:
        filtered_df = df.iloc[0:0].copy()
else:
    filtered_df = df.copy()

# 5. KPI Summary Row
col1, col2, col3 = st.columns(3)
col1.metric("Total Applications", f"{len(filtered_df):,}")

if credit_col in filtered_df.columns and len(filtered_df) > 0:
    total_credit = filtered_df[credit_col].sum()
    avg_credit = filtered_df[credit_col].mean()
    col2.metric("Total Credit", f"{total_credit:,.0f}")
    col3.metric("Average Credit", f"{avg_credit:,.0f}")
else:
    col2.metric("Total Credit", "0")
    col3.metric("Average Credit", "0")

# 6. Total Credit by Contract Status Chart
if status_col in filtered_df.columns and credit_col in filtered_df.columns and len(filtered_df) > 0:
    status_summary = (
        filtered_df.groupby(status_col, as_index=False)[credit_col]
        .sum()
        .sort_values(by=credit_col, ascending=False)
    )

    fig_status = px.bar(
        status_summary,
        x=status_col,
        y=credit_col,
        title="Total Credit by Contract Status",
        labels={
            status_col: "Contract Status",
            credit_col: "Total Credit Amount (AMT_CREDIT)",
        },
        text_auto=".3s",
    )

    fig_status.update_traces(
        marker_color="#1D4ED8",
        hovertemplate="<b>%{x}</b><br>Total Credit: %{y:,.0f}<extra></extra>",
    )

    fig_status.update_layout(
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(color="#F8FAFC"),
        title=dict(font=dict(size=18, color="#F8FAFC")),
        xaxis=dict(showgrid=False, linecolor="#334155"),
        yaxis=dict(showgrid=True, gridcolor="#334155", linecolor="#334155"),
    )

    st.plotly_chart(fig_status, use_container_width=True)

# 7. Optional Collapsible Data Preview for Management Review
with st.expander("View Cleaned Loan Data Sample"):
    st.dataframe(filtered_df.head(50), use_container_width=True)

st.subheader("Queries", divider="rainbow")
option = st.selectbox(
    "select a query",
    (
        "Retrieve all records from the loan_data table.",
        "Display all loan applications with their contract type and contract status.",
        "Retrieve all applications where the contract status is 'Approved'.",
        "Display all applications where the contract status is 'Refused'.",
        "Retrieve all applications belonging to the 'Repeater' client type.",
        "Calculate the total number of loan applications.",
        "Calculate the total credit amount across all applications.",
        "Calculate the average loan application amount.",
        "Count the number of applications for each contract status.",
        "Calculate the average annuity amount for each contract type.",
        "Retrieve loan applications where the credit amount is greater than 500,000.",
        "Find applications where the down payment amount is greater than 50,000.",
        "Count the number of applications for each client type.",
        "Calculate the average credit amount for each loan contract status.",
        "Find the top 5 product combinations with the highest number of applications.",
        "Calculate the total credit amount for approved and refused applications separately.",
        "Find the top 3 contract types with the highest average credit amount.",
        "Calculate the total application amount for each payment type.",
        "Identify the top 5 seller industries based on total credit amount.",
        "Calculate the approval percentage for each contract type.",
    )
)
if option == "Retrieve all records from the loan_data table.":
    query1 = "SELECT * FROM loan_data;"
    df = pd.read_sql(query1, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Display all loan applications with their contract type and contract status.":
    query2 = "SELECT NAME_CONTRACT_TYPE, NAME_CONTRACT_STATUS FROM loan_data;"
    df = pd.read_sql(query2, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Retrieve all applications where the contract status is 'Approved'.":
    query3 = "SELECT * FROM loan_data WHERE NAME_CONTRACT_STATUS = 'Approved';"
    df = pd.read_sql(query3, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Display all applications where the contract status is 'Refused'.":
    query4 = "SELECT * FROM loan_data WHERE NAME_CONTRACT_STATUS = 'Refused';"
    df = pd.read_sql(query4, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Retrieve all applications belonging to the 'Repeater' client type.":
    query5 = "SELECT * FROM loan_data WHERE NAME_CLIENT_TYPE = 'Repeater';"
    df = pd.read_sql(query5, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the total number of loan applications.":
    query6 = "SELECT COUNT(*) AS total_applications FROM loan_data;"
    df = pd.read_sql(query6, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the total credit amount across all applications.":
    query7 = "SELECT SUM(AMT_CREDIT) AS total_credit_amount FROM loan_data;"
    df = pd.read_sql(query7, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the average loan application amount.":
    query8 = "SELECT AVG(AMT_APPLICATION) AS average_application_amount FROM loan_data;"
    df = pd.read_sql(query8, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Count the number of applications for each contract status.":
    query9 = "SELECT NAME_CONTRACT_STATUS, COUNT(*) AS application_count FROM loan_data GROUP BY NAME_CONTRACT_STATUS;"
    df = pd.read_sql(query9, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the average annuity amount for each contract type.":
    query10 = "SELECT NAME_CONTRACT_TYPE, AVG(AMT_ANNUITY) AS average_annuity_amount FROM loan_data GROUP BY NAME_CONTRACT_TYPE;"
    df = pd.read_sql(query10, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Retrieve loan applications where the credit amount is greater than 500,000.":
    query11 = "SELECT * FROM loan_data WHERE AMT_CREDIT > 500000;"
    df = pd.read_sql(query11, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Find applications where the down payment amount is greater than 50,000.":
    query12 = "SELECT * FROM loan_data WHERE AMT_DOWN_PAYMENT > 50000;"
    df = pd.read_sql(query12, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Count the number of applications for each client type.":
    query13 = "SELECT NAME_CLIENT_TYPE, COUNT(*) AS application_count FROM loan_data GROUP BY NAME_CLIENT_TYPE;"
    df = pd.read_sql(query13, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the average credit amount for each loan contract status.":
    query14 = "SELECT NAME_CONTRACT_STATUS, AVG(AMT_CREDIT) AS average_credit_amount FROM loan_data GROUP BY NAME_CONTRACT_STATUS;"
    df = pd.read_sql(query14, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Find the top 5 product combinations with the highest number of applications.":
    query15 = "SELECT PRODUCT_COMBINATION, COUNT(*) AS application_count FROM loan_data GROUP BY PRODUCT_COMBINATION ORDER BY application_count DESC LIMIT 5;"
    df = pd.read_sql(query15, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the total credit amount for approved and refused applications separately.":
    query16 = "SELECT NAME_CONTRACT_STATUS, SUM(AMT_CREDIT) AS total_credit_amount FROM loan_data WHERE NAME_CONTRACT_STATUS IN ('Approved', 'Refused') GROUP BY NAME_CONTRACT_STATUS;"
    df = pd.read_sql(query16, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Find the top 3 contract types with the highest average credit amount.":
    query17 = "SELECT NAME_CONTRACT_TYPE, AVG(AMT_CREDIT) AS avg_credit_amount FROM loan_data GROUP BY NAME_CONTRACT_TYPE ORDER BY avg_credit_amount DESC LIMIT 3;"
    df = pd.read_sql(query17, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the total application amount for each payment type.":
    query18 = "SELECT NAME_PAYMENT_TYPE, SUM(AMT_APPLICATION) AS total_application_amount FROM loan_data GROUP BY NAME_PAYMENT_TYPE;"
    df = pd.read_sql(query18, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Identify the top 5 seller industries based on total credit amount.":
    query19 = "SELECT NAME_SELLER_INDUSTRY, SUM(AMT_CREDIT) AS total_credit_amount FROM loan_data GROUP BY NAME_SELLER_INDUSTRY ORDER BY total_credit_amount DESC LIMIT 5;"
    df = pd.read_sql(query19, con=engine)
    st.dataframe(df, use_container_width=True)
if option == "Calculate the approval percentage for each contract type.":
    query20 = """SELECT NAME_CONTRACT_TYPE, COUNT(*) AS total_applications, SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) AS approved_count, ROUND(
        SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 0) AS approval_percentage FROM loan_data GROUP BY NAME_CONTRACT_TYPE;"""
    df = pd.read_sql(query20, con=engine)
    st.dataframe(df, use_container_width=True)