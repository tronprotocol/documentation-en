# TriggerConstantContract

Read-only contract call (off-chain), used to read `view`/`pure` functions or simulate a transaction.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc TriggerConstantContract (TriggerSmartContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/triggerconstantcontract](../../http/smart-contract/triggerconstantcontract.md).
