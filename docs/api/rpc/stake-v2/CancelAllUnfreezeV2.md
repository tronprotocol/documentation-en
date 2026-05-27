# CancelAllUnfreezeV2

Cancel all of an account's pending unfreeze entries: the immature portion is re-frozen, while the matured portion is automatically withdrawn to the balance.

- Service: `Wallet` only

```protobuf
rpc CancelAllUnfreezeV2 (CancelAllUnfreezeV2Contract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/cancelallunfreezev2](../../http/stake-v2/cancelallunfreezev2.md).
