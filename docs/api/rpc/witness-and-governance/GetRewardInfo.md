# GetRewardInfo

Query an account's claimable (unwithdrawn) voting reward.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetRewardInfo (BytesMessage) returns (NumberMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getReward](../../http/witness-and-governance/getReward.md).
