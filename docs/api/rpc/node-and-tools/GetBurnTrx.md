# GetBurnTrx

Return the cumulative amount of TRX burned (including fees, contract burns, etc.).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetBurnTrx (EmptyMessage) returns (NumberMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getburntrx](../../http/node-and-tools/getburntrx.md).
