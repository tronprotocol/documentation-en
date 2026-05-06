# GetAvailableUnfreezeCount

Query how many additional unfreeze requests the account can still initiate (Stake 2.0 caps an account at 32 simultaneous unfreezes in flight).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetAvailableUnfreezeCount (GetAvailableUnfreezeCountRequestMessage) returns (GetAvailableUnfreezeCountResponseMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getavailableunfreezecount](../../http/stake-v2/getavailableunfreezecount.md).
