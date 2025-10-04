import pandas as pd
from operator import attrgetter  # <-- FIX

# Load cleaned data
df = pd.read_csv("data/processed/retail_cleaned.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Extract InvoiceMonth
df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M")

# Cohort group = customer's first purchase month
df["CohortMonth"] = df.groupby("CustomerID")["InvoiceMonth"].transform("min")

# Calculate Cohort Index (distance in months)
df["CohortIndex"] = (df["InvoiceMonth"] - df["CohortMonth"]).apply(attrgetter("n"))

# Count unique customers per cohort
cohort_data = df.groupby(["CohortMonth", "CohortIndex"])["CustomerID"].nunique().reset_index()

# Pivot table for retention
cohort_pivot = cohort_data.pivot(index="CohortMonth", columns="CohortIndex", values="CustomerID")

# Save results
cohort_pivot.to_csv("data/processed/cohort_analysis.csv")

print("Cohort analysis complete! Saved at data/processed/cohort_analysis.csv")
