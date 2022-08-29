# GreatVoyage-4.1.3(Thales)
GreatVoyage-4.1.3(Thales)  is released with the following new features and modifications:
# Core Protocol
## 1.Sorting the transactions in pending pool,  SR will prioritize the transactions with high packing fee
In GreatVoyage-4.1.2 and earlier versions, SR packaging transactions are carried out in accordance with the time sequence of the arrival of the transaction.This will easily be attacked by low transaction fees.

After this optimization, block producers sort the transactions to be packaged according to the cost, and then prioritize the transaction with high cost to prevent low-cost transaction attacks.

# API
## 1.Add new API to support transaction query in pending pool.
It is currently impossible to query the intermediate state information of a certain transaction from after it is issued to before it is on the chain.After a transaction is sent, if it is not on the chain, we cannot know whether it is waiting for packaging or has been discarded.

In this upgrade, the Fullnode node provides 3 API to obtain detailed information about the pending pool:
- /wallet/gettransactionfrompending: Obtain the transaction information from pending pool through the - transaction ID
- /wallet/gettransactionlistfrompending: Get all transactions from the pending pool
- /wallet/getpendingsize: Get the number of transactions in pending pool


The optimization of transaction packaging logic of GreatVoyage-4.1.3(Thales)  will effectively reduce low-cost attacks and greatly improve the security of the TRON public chain.


---