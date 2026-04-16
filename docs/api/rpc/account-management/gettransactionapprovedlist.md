# getTransactionApprovedList

**Supported API**: `wallet`

TRON API method that returns the addresses that signed (approved) a specific signed transaction. Submit the fully signed transaction object and the endpoint derives the approver addresses from the signatures.

```protobuf
rpc GetTransactionApprovedList (Transaction) returns (TransactionApprovedList) {}
```
