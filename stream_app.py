from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Credit Risk Dashboard",
    page_icon="📊",
    layout="wide",
)

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
# 3. Data Loading
DATA_PATH = Path(r"D:\pandas\.venv\project files\cleaned_loan_data.parquet").parent / "cleaned_loan_data.parquet"


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path)


if not DATA_PATH.exists():
    st.warning("Run your cleaning notebook first to generate cleaned_loan_data.parquet.")
    st.stop()

df = load_data(DATA_PATH)

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
