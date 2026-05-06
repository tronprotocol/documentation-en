# GetTransactionInfoByBlockNum

Return an array of `TransactionInfo` (execution results) for all transactions in a given block.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetTransactionInfoByBlockNum (NumberMessage) returns (TransactionInfoList) {}
```

See the corresponding HTTP endpoint at [/wallet/gettransactioninfobyblocknum](../../http/block-and-tx-query/gettransactioninfobyblocknum.md).
