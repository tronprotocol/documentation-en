# GetBlock

Look up a block by number or hash, optionally returning full transaction details. Unified replacement for `GetNowBlock` / `GetBlockByNum` / `GetBlockById`.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetBlock (BlockReq) returns (BlockExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/getblock](../../http/block-and-tx-query/getblock.md).
