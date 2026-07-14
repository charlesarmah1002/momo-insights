#Momo Insights Data Warehouse and Mining Project

##Executive brief
This data analysis project is to find out 

1. Which transactions are fraudulent, and can we flag them automatically?
2. How do our customers group by behaviour, so marketing can target them?
3. What is happening across the business that an executive should see at a glance?

##Data sources & Features
**Source:** Raw transaction data for June 2026

##Star Schema Structure
fact_transactions (grain: one transaction)
    transactions_sk     PK
    customer_sk         ->  dim_customer
    merchant_sk         ->  dim_merchant
    date_sk             ->  dim_date
    txn_type_sk         ->  dim_txn_type
    amount, oldbalanceOrg, newbalanceOrig,
    oldbalanceDest, newbalanceDest,
    errorBalanceOrig (derived), is_fraud, is_flagged_fraud

dim_customer    (customer_sk, customer_id)
dim_merchant    (merchant_sk, merchant_id)
dim_date        (date_sk, step, day, hour)
dim_txn_type    (txn_type_sk, type)