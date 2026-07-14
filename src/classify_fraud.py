import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
 
fact = pd.read_csv("warehouse/fact_transactions.csv")
dim_type = pd.read_csv("warehouse/dim_txn_type.csv")
f = fact.merge(dim_type, on="txn_type_sk")
f = f[f["type"].isin(["TRANSFER", "CASH_OUT"])].copy()   # fraud lives only here
 
features = ["amount","oldbalanceOrg","newbalanceOrig",
            "oldbalanceDest","newbalanceDest","errorBalanceOrig"]
X, y = f[features], f["is_fraud"]

