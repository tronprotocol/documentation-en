# GetEnergyPrices

Get the historical energy unit price (a new entry is appended every time a proposal changes it).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetEnergyPrices (EmptyMessage) returns (PricesResponseMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getenergyprices](../../http/node-and-tools/getenergyprices.md).
