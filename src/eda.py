import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sns
 
fact = pd.read_csv("warehouse/fact_transactions.csv")
print(fact.isna().sum())  # missing values per column
fact[["amount", "errorBalanceOrig"]].describe().round(2)

q1, q3 = fact["amount"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
print("outlier share:", (fact["amount"] > upper).mean().round(3))
fact["amount_log"] = np.log1p(fact["amount"])  # log(1+x), safe at 0

import os; os.makedirs("reports/figures", exist_ok=True)
 
# 1) Fraud rate by transaction type (join the type dimension back)
dim_type = pd.read_csv("warehouse/dim_txn_type.csv")
f = fact.merge(dim_type, on="txn_type_sk")
ax = (f.groupby("type")["is_fraud"].mean()
        .sort_values().plot.barh(color="#0891B2"))
ax.set_title("Fraud rate by transaction type")
plt.tight_layout(); plt.savefig("reports/figures/fraud_by_type.png", dpi=150); plt.clf()
 
# 2) Distribution of (log) amount, fraud vs legit
sns.kdeplot(data=f, x="amount_log", hue="is_fraud", common_norm=False)
plt.title("Amount distribution: fraud vs legitimate")
plt.tight_layout(); plt.savefig("reports/figures/amount_dist.png", dpi=150); plt.clf()
