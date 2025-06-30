import sqlite3
import pandas as pd
import os

# Connect to SQLite database
conn = sqlite3.connect("database/unicorns.db")

# Create analysis results directory
os.makedirs("analysis_results", exist_ok=True)

# 1) Unicorn count per country
query1 = """
SELECT country, COUNT(*) AS unicorn_count
FROM unicorns
GROUP BY country
ORDER BY unicorn_count DESC
"""
df_country = pd.read_sql_query(query1, conn)
df_country.to_csv("analysis_results/unicorns_per_country.csv", index=False)
print("Saved unicorns per country")

# 2) Total valuation per country
query2 = """
SELECT country, SUM(valuation_billion) AS total_valuation
FROM unicorns
WHERE valuation_billion IS NOT NULL
GROUP BY country
ORDER BY total_valuation DESC
"""
df_total_valuation = pd.read_sql_query(query2, conn)
df_total_valuation.to_csv("analysis_results/total_valuation_per_country.csv", index=False)
print("Saved total valuation per country")

# 3) Average valuation per country
query3 = """
SELECT country, AVG(valuation_billion) AS avg_valuation
FROM unicorns
WHERE valuation_billion IS NOT NULL
GROUP BY country
ORDER BY avg_valuation DESC
"""
df_avg_valuation = pd.read_sql_query(query3, conn)
df_avg_valuation.to_csv("analysis_results/avg_valuation_per_country.csv", index=False)
print("Saved average valuation per country")

# 4) Countries with unicorns
query4 = """
SELECT DISTINCT country
FROM unicorns
ORDER BY country
"""
df_countries = pd.read_sql_query(query4, conn)
df_countries.to_csv("analysis_results/countries_with_unicorns.csv", index=False)
print("Saved countries with unicorns")

# 5) Top 20 unicorns by valuation
query5 = """
SELECT company_name, valuation_billion, country
FROM unicorns
WHERE valuation_billion IS NOT NULL
ORDER BY valuation_billion DESC
LIMIT 20
"""
df_top_unicorns = pd.read_sql_query(query5, conn)
df_top_unicorns.to_csv("analysis_results/top_20_unicorns.csv", index=False)
print("Saved top 20 unicorns")

# 6) KPIs: total unicorns, global valuation, global average
total_unicorns = df_country['unicorn_count'].sum()
total_valuation_global = df_total_valuation['total_valuation'].sum()
average_valuation_global = total_valuation_global / total_unicorns if total_unicorns else 0

kpis = pd.DataFrame({
    "KPI": [
        "Total number of unicorns",
        "Total global unicorn valuation ($B)",
        "Average unicorn valuation globally ($B)"
    ],
    "Value": [
        total_unicorns,
        round(total_valuation_global, 2),
        round(average_valuation_global, 2)
    ]
})
kpis.to_csv("analysis_results/kpis.csv", index=False)
print("Saved core KPIs")

# 7) Gini coefficient as a measure of valuation concentration
valuations = pd.read_sql_query("SELECT valuation_billion FROM unicorns WHERE valuation_billion IS NOT NULL", conn)['valuation_billion'].sort_values().values
if len(valuations) > 0:
    n = len(valuations)
    cumulative = (2 * (valuations * (range(1, n + 1))).sum()) / (n * valuations.sum())
    gini = cumulative - (n + 1) / n
else:
    gini = None

pd.DataFrame({"Metric": ["Gini coefficient of unicorn valuations"], "Value": [round(gini, 3) if gini is not None else None]}).to_csv(
    "analysis_results/gini_coefficient.csv", index=False)
print("Saved Gini coefficient")

# 8) Valuation percentiles
percentiles = [25, 50, 75]
percentile_values = [round(pd.Series(valuations).quantile(p / 100), 2) if len(valuations) else None for p in percentiles]
df_percentiles = pd.DataFrame({"Percentile": ["25%", "50%", "75%"], "Valuation ($B)": percentile_values})
df_percentiles.to_csv("analysis_results/valuation_percentiles.csv", index=False)
print("Saved valuation percentiles")

# 9) Top investors by unicorn count (if data exists)
query_investors = """
SELECT lead_investors, COUNT(*) AS unicorn_count
FROM unicorns
WHERE lead_investors IS NOT NULL AND lead_investors != ''
GROUP BY lead_investors
ORDER BY unicorn_count DESC
LIMIT 20
"""
df_top_investors = pd.read_sql_query(query_investors, conn)
df_top_investors.to_csv("analysis_results/top_investors.csv", index=False)
print("Saved top investors")

# 10) Regional analysis: unicorn count and total valuation by region
query_region = """
SELECT region, COUNT(*) AS unicorn_count, SUM(valuation_billion) AS total_valuation
FROM unicorns
WHERE region IS NOT NULL AND valuation_billion IS NOT NULL
GROUP BY region
ORDER BY unicorn_count DESC
"""
df_region = pd.read_sql_query(query_region, conn)
df_region.to_csv("analysis_results/unicorns_by_region.csv", index=False)
print("Saved regional analysis")

# 11) KPI ratios: top 3 countries' share of unicorns and valuations
top3_unicorns = df_country.head(3)['unicorn_count'].sum()
top3_unicorn_ratio = (top3_unicorns / total_unicorns * 100) if total_unicorns else 0

top3_valuation = df_total_valuation.head(3)['total_valuation'].sum()
top3_valuation_ratio = (top3_valuation / total_valuation_global * 100) if total_valuation_global else 0

df_kpi_ratios = pd.DataFrame({
    "Metric": [
        "Top 3 countries' share of unicorns (%)",
        "Top 3 countries' share of total unicorn valuation (%)"
    ],
    "Value": [
        round(top3_unicorn_ratio, 2),
        round(top3_valuation_ratio, 2)
    ]
})
df_kpi_ratios.to_csv("analysis_results/kpi_ratios.csv", index=False)
print("Saved KPI ratios for top 3 countries")

# Close connection
conn.close()
