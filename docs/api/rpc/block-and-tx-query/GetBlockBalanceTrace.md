# GetBlockBalanceTrace

Return the block balance trace, containing only transactions with recorded TRX balance changes. Match entries by `transaction_identifier`; the list need not contain every transaction in the block.

- Service: `Wallet` only

```protobuf
rpc GetBlockBalanceTrace (BlockBalanceTrace.BlockIdentifier) returns (BlockBalanceTrace) {}
```

See the corresponding HTTP endpoint at [/wallet/getblockbalance](../../http/block-and-tx-query/getblockbalance.md).
