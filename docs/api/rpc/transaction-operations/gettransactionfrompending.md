# getTransactionFromPending

**Supported API**: `wallet`

TRON API method that retrieves a specific pending transaction from the mempool by its transaction ID. This allows applications to check the status and details of an unconfirmed transaction.

```protobuf
rpc GetTransactionFromPending (BytesMessage) returns (Transaction) {}
```
