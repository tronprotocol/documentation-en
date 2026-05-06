# GetBlockBalanceTrace

Return the balance-change trace (block balance trace) for all transactions in a given block.

- Service: `Wallet` only

```protobuf
rpc GetBlockBalanceTrace (BlockBalanceTrace.BlockIdentifier) returns (BlockBalanceTrace) {}
```

See the corresponding HTTP endpoint at [/wallet/getblockbalance](../../http/block-and-tx-query/getblockbalance.md).
