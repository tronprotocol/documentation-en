# unfreezeBalance

**Supported API**: `wallet`

TRON API method that unstakes TRX previously frozen for bandwidth or energy resources (deprecated method). This method releases TRX tokens that were previously frozen, making them available for transfer after the lock period expires. This is the legacy unstaking mechanism; for the current staking model, use unfreezebalancev2. legacy unstake works only for legacy freezesOn mainnet, new legacy freezes are disabled. You can only use wallet/unfreezebalance if your account still has legacy‑frozen balance. For v2 staking, use wallet/unfreezebalancev2.

```protobuf
rpc UnfreezeBalance (UnfreezeBalanceContract) returns (Transaction) {}
```
