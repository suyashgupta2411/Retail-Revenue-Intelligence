import pandas as pd
import datetime as dt

# Load cleaned dataset
df = pd.read_csv("data/processed/retail_cleaned.csv")
df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Reference date (max date in dataset + 1 day)
reference_date = df["InvoiceDate"].max() + dt.timedelta(days=1)

# RFM Calculation
rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (reference_date - x.max()).days,  # Recency
    "InvoiceNo": "count",   # Frequency
    "Revenue": "sum"        # Monetary
})

rfm.rename(columns={
    "InvoiceDate": "Recency",
    "InvoiceNo": "Frequency",
    "Revenue": "Monetary"
}, inplace=True)

# Assign RFM Scores (1 = low, 4 = high)
rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
rfm["M_Score"] = pd.qcut(rfm["Monetary"], 4, labels=[1,2,3,4])

# Combine RFM Score
rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)

# Save to CSV for Power BI
rfm.to_csv("data/processed/rfm_results.csv")

print("RFM segmentation complete! Saved at data/processed/rfm_results.csv")
