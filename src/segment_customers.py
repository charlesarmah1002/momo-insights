import pandas as pd, numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
 
fact = pd.read_csv("warehouse/fact_transactions.csv")
cust = (fact.groupby("customer_sk")
            .agg(txn_count=("amount", "size"),
                 total_amount=("amount", "sum"),
                 avg_amount=("amount", "mean"),
                 fraud_count=("is_fraud", "sum"))
            .reset_index())

feat = ["txn_count", "total_amount", "avg_amount"]
X = StandardScaler().fit_transform(cust[feat])

inertia = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inertia.append(km.inertia_)
plt.plot(range(1, 11), inertia, "o-", color="#0891B2")
plt.xlabel("k"); plt.ylabel("inertia"); plt.title("Elbow method")
plt.tight_layout(); plt.savefig("reports/figures/elbow.png", dpi=150); plt.clf()

k = 4  # read this off the elbow chart
km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
cust["segment"] = km.labels_
 
profile = cust.groupby("segment")[feat].mean().round(2)
profile["customers"] = cust["segment"].value_counts().sort_index()
print(profile)
cust.to_csv("warehouse/customer_segments.csv", index=False)
