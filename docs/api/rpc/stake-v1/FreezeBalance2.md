# FreezeBalance2

> **Disabled on chain**: after proposal #70 `UNFREEZE_DELAY_DAYS` was passed (mainnet has activated it), `FreezeBalanceActuator.validate()` throws `freeze v2 is open, old freeze is closed`, and any new request fails. Use [`FreezeBalanceV2`](../stake-v2/FreezeBalanceV2.md) instead.
>
> Note: the `2` suffix is a historical proto naming convention (the V1 method that returns `TransactionExtention`); it is not the same method as Stake 2.0's `FreezeBalanceV2`.

Freeze TRX to obtain bandwidth or energy, optionally delegating to another account. Minimum freeze period is 3 days.

- Service: `Wallet` only

```protobuf
rpc FreezeBalance2 (FreezeBalanceContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/freezebalance](../../http/stake-v1/freezebalance.md).
