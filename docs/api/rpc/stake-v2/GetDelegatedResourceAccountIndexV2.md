# GetDelegatedResourceAccountIndexV2

Look up the counterparty addresses where the account acts as delegator or receiver in delegations (Stake 2.0).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetDelegatedResourceAccountIndexV2 (BytesMessage) returns (DelegatedResourceAccountIndex) {}
```

See the corresponding HTTP endpoint at [/wallet/getdelegatedresourceaccountindexv2](../../http/stake-v2/getdelegatedresourceaccountindexv2.md).
