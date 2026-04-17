# getTransactionListFromPending

**Supported API**: `wallet`

TRON API method that retrieves a list of all pending transactions currently in the mempool. This allows applications to monitor unconfirmed transactions awaiting inclusion in a block.

```protobuf
rpc GetTransactionListFromPending (EmptyMessage) returns (TransactionIdList) {}
```
