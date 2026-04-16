# estimateEnergy

**Supported API**: `wallet` `walletsolidity`

TRON API method that estimates the energy consumption for executing a smart contract function call. This method helps predict the energy costs before actually executing a transaction, enabling better cost planning and user experience optimization.

```protobuf
rpc EstimateEnergy (TriggerSmartContract) returns (EstimateEnergyMessage) {}
```
