# UnfreezeAsset2

Unfreeze tokens locked by the issuer in `frozen_supply` (issuer-only; succeeds only after maturity).

- Service: `Wallet` only

```protobuf
rpc UnfreezeAsset2 (UnfreezeAssetContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/unfreezeasset](../../http/asset/unfreezeasset.md).
