# GetTransactionFromPending

Fetch a transaction from the pending pool by txID.

- Service: `Wallet` only

```protobuf
rpc GetTransactionFromPending (BytesMessage) returns (Transaction) {}
```

See the corresponding HTTP endpoint at [/wallet/gettransactionfrompending](../../http/block-and-tx-query/gettransactionfrompending.md).
