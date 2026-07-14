1. Business Understanding — TeleCash wants to flag fraud and segment customers.
2. Data Understanding   — 6.36M PaySim rows; fraud only in TRANSFER & CASH_OUT.
3. Data Preparation     — star schema + errorBalanceOrig + log(amount) (done).
4. Modeling             — Decision Tree & KNN for fraud (Wk6);
                          K-Means for segments (Wk7).
5. Evaluation           — precision/recall/F1 for fraud; silhouette & profiles
                          for segments. Why accuracy is the wrong fraud metric.
6. Deployment           — a one-page Power BI executive dashboard (Wk8).