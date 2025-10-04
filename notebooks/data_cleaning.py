import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/OnlineRetail.csv", encoding="latin1")

print("Initial shape:", df.shape)

# Drop missing CustomerID (many missing values there)
df = df.dropna(subset=["CustomerID"])

# Remove duplicates
df = df.drop_duplicates()

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Remove negative/zero quantities (cancellations, returns)
df = df[df["Quantity"] > 0]

# Remove negative/zero prices
df = df[df["UnitPrice"] > 0]

print("Cleaned shape:", df.shape)

# Save processed data
df.to_csv("data/processed/retail_cleaned.csv", index=False)
print("Processed data saved!")
