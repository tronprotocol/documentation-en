# getTransactionSignWeight

**Supported API**: `wallet`

TRON API method that checks the multi-signature status of a transaction. It returns the total weight of signatures provided, the threshold required, and a list of authorized addresses, helping verify if a transaction has enough approvals to be broadcast.

```protobuf
rpc GetTransactionSignWeight (Transaction) returns (TransactionSignWeight) {}
```
