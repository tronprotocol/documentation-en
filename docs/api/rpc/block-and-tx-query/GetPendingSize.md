# GetPendingSize

Return the number of transactions currently in the node's pending pool.

- Service: `Wallet` only

```protobuf
rpc GetPendingSize (EmptyMessage) returns (NumberMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getpendingsize](../../http/block-and-tx-query/getpendingsize.md).
