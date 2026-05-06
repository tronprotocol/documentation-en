# UnfreezeBalance2

> **Legacy retained**: unlike `FreezeBalance2`, this method **remains callable** after Stake 2.0 activation — `UnfreezeBalanceActuator` has no `supportUnfreezeDelay` gate, and legacy V1 positions still need it for unfreezing. New work should use [`UnfreezeBalanceV2`](../stake-v2/UnfreezeBalanceV2.md).

Unfreeze matured Stake 1.0 assets.

- Service: `Wallet` only

```protobuf
rpc UnfreezeBalance2 (UnfreezeBalanceContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/unfreezebalance](../../http/stake-v1/unfreezebalance.md).
