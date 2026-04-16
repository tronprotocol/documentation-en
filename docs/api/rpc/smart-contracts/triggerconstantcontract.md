# triggerConstantContract

**Supported API**: `wallet` `walletsolidity`

TRON API method that calls a constant (read-only) smart contract method without consuming energy or bandwidth. This method allows you to query contract state and call view functions without broadcasting a transaction to the blockchain.

```protobuf
rpc TriggerConstantContract (TriggerSmartContract) returns (TransactionExtention) {}
```
