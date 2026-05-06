# UnfreezeBalanceV2

Initiate an unfreeze (Stake 2.0). Enters a 14-day waiting period, after which the matured amount can be withdrawn via `WithdrawExpireUnfreeze`.

- Service: `Wallet` only

```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/unfreezebalancev2](../../http/stake-v2/unfreezebalancev2.md).
