# GetDelegatedResource

> **Legacy query**: returns delegation records stored under Stake 1.0 only; does not see V2 data. The source has no version gate, so it can still be called after V2 activation to read historical V1 positions. New work should use [`GetDelegatedResourceV2`](../stake-v2/GetDelegatedResourceV2.md).

Look up all resource-delegation records between `from` → `to` (Stake 1.0).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetDelegatedResource (DelegatedResourceMessage) returns (DelegatedResourceList) {}
```

See the corresponding HTTP endpoint at [/wallet/getdelegatedresource](../../http/stake-v1/getdelegatedresource.md).
