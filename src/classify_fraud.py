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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, stratify=y, random_state=42)

dt = DecisionTreeClassifier(max_depth=5, class_weight="balanced",
                            random_state=42)
dt.fit(X_train, y_train)
print("DECISION TREE")
print(confusion_matrix(y_test, dt.predict(X_test)))
print(classification_report(y_test, dt.predict(X_test), digits=4))

scaler = StandardScaler().fit(X_train)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(scaler.transform(X_train), y_train)
pred = knn.predict(scaler.transform(X_test))
print("KNN")
print(confusion_matrix(y_test, pred))
