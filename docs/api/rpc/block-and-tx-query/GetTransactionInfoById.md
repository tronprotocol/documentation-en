# GetTransactionInfoById

Look up a transaction's **execution result** by txID (includes receipt, logs, internal calls, resource consumption).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetTransactionInfoById (BytesMessage) returns (TransactionInfo) {}
```

See the corresponding HTTP endpoint at [/wallet/gettransactioninfobyid](../../http/block-and-tx-query/gettransactioninfobyid.md).
