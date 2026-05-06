# GetTransactionListFromPending

Return the txID list of every transaction in the pending pool.

- Service: `Wallet` only

```protobuf
rpc GetTransactionListFromPending (EmptyMessage) returns (TransactionIdList) {}
```

See the corresponding HTTP endpoint at [/wallet/gettransactionlistfrompending](../../http/block-and-tx-query/gettransactionlistfrompending.md).
