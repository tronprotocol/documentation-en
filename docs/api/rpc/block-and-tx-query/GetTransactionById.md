# GetTransactionById

Look up a transaction by its txID, including its basic execution status in `ret[].contractRet`. For detailed execution information such as the receipt, logs, and internal transactions, use [`GetTransactionInfoById`](GetTransactionInfoById.md).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetTransactionById (BytesMessage) returns (Transaction) {}
```

See the corresponding HTTP endpoint at [/wallet/gettransactionbyid](../../http/block-and-tx-query/gettransactionbyid.md).
