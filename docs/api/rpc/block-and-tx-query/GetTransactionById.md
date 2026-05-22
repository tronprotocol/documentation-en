# GetTransactionById

Look up a transaction by its txID (**execution result not included** — returns only the pre-execution transaction body).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetTransactionById (BytesMessage) returns (Transaction) {}
```

See the corresponding HTTP endpoint at [/wallet/gettransactionbyid](../../http/block-and-tx-query/gettransactionbyid.md).
