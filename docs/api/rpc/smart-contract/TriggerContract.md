# TriggerContract

Trigger a smart contract (state-changing call). Returns an unsigned transaction along with the pre-execution result.

- Service: `Wallet` only

```protobuf
rpc TriggerContract (TriggerSmartContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/triggersmartcontract](../../http/smart-contract/triggersmartcontract.md).
