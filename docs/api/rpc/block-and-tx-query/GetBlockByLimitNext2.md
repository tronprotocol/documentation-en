# GetBlockByLimitNext2

Get the list of blocks in the range `[startNum, endNum)` (endNum excluded).

- Service: `Wallet` only

```protobuf
rpc GetBlockByLimitNext2 (BlockLimit) returns (BlockListExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/getblockbylimitnext](../../http/block-and-tx-query/getblockbylimitnext.md).
