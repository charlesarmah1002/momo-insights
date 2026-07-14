import pandas as pd
from pathlib import Path
 
RAW = "data/raw/paysim-dataset.csv"
OUT = Path("warehouse"); OUT.mkdir(exist_ok=True)
 
df = pd.read_csv(RAW)
df = df.rename(columns={"nameOrig": "customer_id",
                        "nameDest": "merchant_id",
                        "isFraud": "is_fraud",
                        "isFlaggedFraud": "is_flagged_fraud"})

df["hour"] = df["step"] % 24
df["day"] = (df["step"] // 24) + 1  # day 1..31
# 98% of frauds drain the origin account — make that visible as a feature
df["errorBalanceOrig"] = (df["newbalanceOrig"] + df["amount"]
                          -df["oldbalanceOrg"]).round(2)
dim_customer = (df[["customer_id"]].drop_duplicates()
                 .reset_index(drop=True))
dim_customer["customer_sk"] = dim_customer.index + 1
 
dim_merchant = (df[["merchant_id"]].drop_duplicates()
                 .reset_index(drop=True))
dim_merchant["merchant_sk"] = dim_merchant.index + 1
 
dim_txn_type = (df[["type"]].drop_duplicates().reset_index(drop=True))
dim_txn_type["txn_type_sk"] = dim_txn_type.index + 1
 
dim_date = (df[["step", "day", "hour"]].drop_duplicates()
             .sort_values("step").reset_index(drop=True))
dim_date["date_sk"] = dim_date.index + 1

fact = (df.merge(dim_customer, on="customer_id")
          .merge(dim_merchant, on="merchant_id")
          .merge(dim_txn_type, on="type")
          .merge(dim_date, on=["step", "day", "hour"]))
fact["transaction_sk"] = fact.index + 1
 
keep = ["transaction_sk", "customer_sk", "merchant_sk", "date_sk", "txn_type_sk",
        "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest",
        "newbalanceDest", "errorBalanceOrig", "is_fraud", "is_flagged_fraud"]
fact[keep].to_csv(OUT / "fact_transactions.csv", index=False)
dim_customer.to_csv(OUT / "dim_customer.csv", index=False)
dim_merchant.to_csv(OUT / "dim_merchant.csv", index=False)
dim_date.to_csv(OUT / "dim_date.csv", index=False)
dim_txn_type.to_csv(OUT / "dim_txn_type.csv", index=False)
print("Warehouse written:", fact.shape[0], "facts")
