import pandas as pd
from operator import attrgetter

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
cohort_data.rename(columns={"CustomerID": "CustomerCount"}, inplace=True)

# Calculate cohort size (customers in month 0)
cohort_sizes = cohort_data[cohort_data["CohortIndex"] == 0][["CohortMonth", "CustomerCount"]]
cohort_sizes.rename(columns={"CustomerCount": "CohortSize"}, inplace=True)

# Merge to get cohort size
cohort_data = cohort_data.merge(cohort_sizes, on="CohortMonth", how="left")

# Calculate retention rate
cohort_data["RetentionRate"] = (cohort_data["CustomerCount"] / cohort_data["CohortSize"] * 100).round(2)

# Convert CohortMonth to string for Power BI compatibility
cohort_data["CohortMonth"] = cohort_data["CohortMonth"].astype(str)

# Save in LONG format (Power BI friendly!)
cohort_data.to_csv("data/processed/cohort_analysis.csv", index=False)

print("✅ Cohort analysis complete! Saved at data/processed/cohort_analysis.csv")
print(f"📊 Total cohorts: {cohort_data['CohortMonth'].nunique()}")
print(f"📈 Max cohort index: {cohort_data['CohortIndex'].max()} months")
print("\nSample data:")
print(cohort_data.head(10))