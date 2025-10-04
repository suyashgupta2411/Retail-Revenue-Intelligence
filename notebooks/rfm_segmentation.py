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
    "Revenue": "MonetaryValue"
}, inplace=True)

# Assign RFM Scores (1 = low, 4 = high)
rfm["Recency_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4,3,2,1])
rfm["Frequency_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
rfm["Monetary_Score"] = pd.qcut(rfm["MonetaryValue"], 4, labels=[1,2,3,4])

# Combine RFM Score
rfm["RFM_Score"] = rfm["Recency_Score"].astype(str) + rfm["Frequency_Score"].astype(str) + rfm["Monetary_Score"].astype(str)

# Add RFM Segments (Business-friendly names)
def assign_segment(row):
    r = int(row["Recency_Score"])
    f = int(row["Frequency_Score"])
    m = int(row["Monetary_Score"])
    
    # Champions: Best customers (high scores across all)
    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    
    # Loyal Customers: Buy frequently, recently
    elif r >= 3 and f >= 4:
        return "Loyal Customers"
    
    # Potential Loyalists: Recent customers, good frequency
    elif r >= 4 and f >= 2 and f <= 3:
        return "Potential Loyalists"
    
    # New Customers: Recent but low frequency
    elif r >= 4 and f <= 2:
        return "New Customers"
    
    # At Risk: Were good customers, haven't purchased recently
    elif r <= 2 and f >= 3:
        return "At Risk"
    
    # Can't Lose Them: High spenders, haven't returned
    elif r <= 2 and m >= 4:
        return "Can't Lose Them"
    
    # Hibernating: Low recency, frequency, but decent monetary
    elif r <= 2 and f <= 2 and m >= 3:
        return "Hibernating"
    
    # Lost: Haven't purchased in a long time
    elif r <= 2 and f <= 2:
        return "Lost"
    
    # Promising: Recent, moderate spending
    elif r >= 3 and m >= 3:
        return "Promising"
    
    # Need Attention: Below average but recoverable
    else:
        return "Need Attention"

rfm["RFM_Segment"] = rfm.apply(assign_segment, axis=1)

# Reset index to include CustomerID in CSV
rfm.reset_index(inplace=True)

# Save to CSV for Power BI
rfm.to_csv("data/processed/rfm_results.csv", index=False)

print("✅ RFM segmentation complete! Saved at data/processed/rfm_results.csv")
print("\n📊 Customer Segment Distribution:")
print(rfm["RFM_Segment"].value_counts())
print(f"\n💰 Total customers analyzed: {len(rfm)}")
print("\nSample data:")
print(rfm.head(10))