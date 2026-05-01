# GetBrokerageInfo

Query an SR's reward-share ratio (brokerage) for the current cycle.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetBrokerageInfo (BytesMessage) returns (NumberMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getBrokerage](../../http/witness-and-governance/getBrokerage.md).
