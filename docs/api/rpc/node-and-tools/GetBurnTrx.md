# GetBurnTrx

Return the cumulative TRX burned, excluding amounts transferred to the blackhole account.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetBurnTrx (EmptyMessage) returns (NumberMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getburntrx](../../http/node-and-tools/getburntrx.md).
