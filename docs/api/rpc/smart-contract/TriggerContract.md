# TriggerContract

Build an unsigned smart-contract transaction and return its construction status. When the contract's on-chain ABI marks the function as `view` or `pure`, or sets the legacy `constant` flag to `true`, this method executes a constant call and returns its simulation result. Use [TriggerConstantContract](TriggerConstantContract.md) to simulate an ordinary state-changing call.

- Service: `Wallet` only

```protobuf
rpc TriggerContract (TriggerSmartContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/triggersmartcontract](../../http/smart-contract/triggersmartcontract.md).
