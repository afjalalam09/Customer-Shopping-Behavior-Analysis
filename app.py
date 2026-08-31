import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("🛍️ Customer Shopping Behavior Analytics")
st.write("End-to-End Analytics Dashboard built with Python, SQL, and Streamlit")

# 2. Data Loading (Path set to your Data folder)
@st.cache_data
def load_data():
    # Tumhare Data folder me rakhi hui cleaned CSV file
    df = pd.read_csv("Data/cleaned_customer_data.csv")
    return df

try:
    df = load_data()

    # 3. Sidebar Filters
    st.sidebar.header("Filter Data")

    category_list = df["category"].unique() if "category" in df.columns else []
    selected_category = st.sidebar.multiselect("Category", options=category_list, default=category_list)

    subscription_list = df["subscription_status"].unique() if "subscription_status" in df.columns else []
    selected_sub = st.sidebar.multiselect("Subscription Status", options=subscription_list, default=subscription_list)

    # Filtered Data
    filtered_df = df[
        (df["category"].isin(selected_category)) & 
        (df["subscription_status"].isin(selected_sub))
    ]

    # 4. KPI Metrics
    st.subheader("Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    total_revenue = filtered_df["purchase_amount"].sum() if "purchase_amount" in filtered_df.columns else 0
    total_customers = len(filtered_df)
    avg_spend = filtered_df["purchase_amount"].mean() if "purchase_amount" in filtered_df.columns else 0
    avg_rating = filtered_df["review_rating"].mean() if "review_rating" in filtered_df.columns else 0

    kpi1.metric("Total Revenue", f"${total_revenue:,.2f}")
    kpi2.metric("Total Customers", f"{total_customers}")
    kpi3.metric("Avg Spend", f"${avg_spend:,.2f}")
    kpi4.metric("Avg Rating", f"{avg_rating:.2f} / 5.0")

    st.markdown("---")

    # 5. Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue by Category")
        if "category" in filtered_df.columns and "purchase_amount" in filtered_df.columns:
            cat_df = filtered_df.groupby("category")["purchase_amount"].sum().reset_index()
            fig_cat = px.bar(cat_df, x="purchase_amount", y="category", orientation="h", color="category")
            st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        st.subheader("Age Group Revenue Split")
        if "age_group" in filtered_df.columns and "purchase_amount" in filtered_df.columns:
            age_df = filtered_df.groupby("age_group")["purchase_amount"].sum().reset_index()
            fig_age = px.pie(age_df, values="purchase_amount", names="age_group", hole=0.4)
            st.plotly_chart(fig_age, use_container_width=True)

except Exception as e:
    st.error(f"Please check your file path. Error: {e}")