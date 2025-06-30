import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="Unicorn Companies Dashboard", layout="wide")
st.title("Unicorn Companies Dashboard")


# Helper: reset table index to start from 1
def reset_index_for_display(df):
    df_reset = df.copy()
    df_reset.index = df_reset.index + 1
    return df_reset


tabs = st.tabs(["Predict Company Valuation", "Analysis"])

# -----------------------
# Tab 1: Prediction
# -----------------------
with tabs[0]:
    st.header("Predict Unicorn Valuation")

    # Load unique country-region pairs from database
    conn = sqlite3.connect("database/unicorns.db")
    df_options = pd.read_sql_query("""
        SELECT DISTINCT country, region 
        FROM unicorns 
        WHERE country IS NOT NULL AND region IS NOT NULL
    """, conn)
    conn.close()

    countries = sorted(df_options["country"].unique())
    selected_country = st.selectbox("Select Country", countries)

    # Filter regions linked only to the selected country
    filtered_regions = df_options[df_options["country"] == selected_country]["region"].dropna().unique()
    regions = sorted(filtered_regions)
    selected_region = st.selectbox("Select Region", regions)

    # Prepare input for prediction
    X_input = pd.DataFrame({"country": [selected_country], "region": [selected_region]})
    X_input_encoded = pd.get_dummies(X_input)

    # Load training columns to align input
    df_predicted = pd.read_csv("prediction_results/predicted_company_valuations.csv")
    X_train_encoded = pd.get_dummies(df_predicted[["country", "region"]])

    X_input_aligned = X_input_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

    # Retrain model on full data for simplicity
    y = df_predicted["valuation_billion"]
    model = RandomForestRegressor()
    model.fit(X_train_encoded, y)

    # Predict valuation
    predicted_val = model.predict(X_input_aligned)[0]

    st.success(f"Predicted Unicorn Valuation: ${predicted_val:.2f} billion USD")

# -----------------------
# Tab 2: Analysis
# -----------------------
with tabs[1]:
    st.header("Unicorn Analysis Results")

    # Unicorns per Country
    st.subheader("Unicorns per Country")
    df_unicorns_per_country = pd.read_csv("analysis_results/unicorns_per_country.csv")
    st.dataframe(reset_index_for_display(df_unicorns_per_country))
    fig1 = px.bar(df_unicorns_per_country.head(20), x="country", y="unicorn_count",
                  title="Top 20 Countries by Unicorn Count",
                  labels={"unicorn_count": "Number of Unicorns", "country": "Country"})
    st.plotly_chart(fig1, use_container_width=True)

    # Total Valuation per Country
    st.subheader("Total Valuation per Country")
    df_total_valuation = pd.read_csv("analysis_results/total_valuation_per_country.csv")
    st.dataframe(reset_index_for_display(df_total_valuation))
    fig2 = px.bar(df_total_valuation.head(20), x="country", y="total_valuation",
                  title="Top 20 Countries by Total Unicorn Valuation",
                  labels={"total_valuation": "Total Valuation ($B)", "country": "Country"})
    st.plotly_chart(fig2, use_container_width=True)

    # Average Valuation per Country
    st.subheader("Average Valuation per Country")
    df_avg_valuation = pd.read_csv("analysis_results/avg_valuation_per_country.csv")
    st.dataframe(reset_index_for_display(df_avg_valuation))
    fig3 = px.bar(df_avg_valuation.head(20), x="country", y="avg_valuation",
                  title="Top 20 Countries by Average Unicorn Valuation",
                  labels={"avg_valuation": "Average Valuation ($B)", "country": "Country"})
    st.plotly_chart(fig3, use_container_width=True)

    # KPIs
    st.subheader("KPIs")
    df_kpis = pd.read_csv("analysis_results/kpis.csv")
    st.dataframe(reset_index_for_display(df_kpis))
