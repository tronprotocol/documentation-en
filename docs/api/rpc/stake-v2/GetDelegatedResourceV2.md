# GetDelegatedResourceV2

Look up resource-delegation records between `from` → `to` (Stake 2.0).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetDelegatedResourceV2 (DelegatedResourceMessage) returns (DelegatedResourceList) {}
```

See the corresponding HTTP endpoint at [/wallet/getdelegatedresourcev2](../../http/stake-v2/getdelegatedresourcev2.md).
