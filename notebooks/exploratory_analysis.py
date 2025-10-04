import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/processed/retail_cleaned.csv")

# Add revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# ====== 1. Monthly Revenue Trend ======
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = df.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot(marker="o")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.xlabel("Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("reports/monthly_revenue_trend.png")
plt.close()

# ====== 2. Top 10 Products ======
top_products = df.groupby("Description")["Revenue"].sum().sort_values(ascending=False).head(10)
top_products.plot(kind="bar", figsize=(10,5))
plt.title("Top 10 Products by Revenue")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("reports/top_products.png")
plt.close()

# ====== 3. Top 10 Customers ======
top_customers = df.groupby("CustomerID")["Revenue"].sum().sort_values(ascending=False).head(10)
top_customers.plot(kind="bar", figsize=(10,5))
plt.title("Top 10 Customers by Revenue")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("reports/top_customers.png")
plt.close()

print("EDA complete! Charts saved in reports/")
