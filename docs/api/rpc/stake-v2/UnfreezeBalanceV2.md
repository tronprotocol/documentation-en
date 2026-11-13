# UnfreezeBalanceV2

Initiate an unfreeze (Stake 2.0). The waiting period is set by the chain parameter `UNFREEZE_DELAY_DAYS` (currently 14 days on Mainnet). After maturity, the amount can be withdrawn via `WithdrawExpireUnfreeze`.

- Service: `Wallet` only

```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/unfreezebalancev2](../../http/stake-v2/unfreezebalancev2.md).
