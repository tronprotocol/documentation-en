# GetDelegatedResourceAccountIndex

> **Legacy query**: returns the delegation counterparty index stored under Stake 1.0 only; does not see V2 data. The source has no version gate, so it can still be called after V2 activation to read historical V1 positions. New work should use [`GetDelegatedResourceAccountIndexV2`](../stake-v2/GetDelegatedResourceAccountIndexV2.md).

Look up the counterparty addresses where the account acts as delegator or receiver in delegations (Stake 1.0).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetDelegatedResourceAccountIndex (BytesMessage) returns (DelegatedResourceAccountIndex) {}
```

See the corresponding HTTP endpoint at [/wallet/getdelegatedresourceaccountindex](../../http/stake-v1/getdelegatedresourceaccountindex.md).
