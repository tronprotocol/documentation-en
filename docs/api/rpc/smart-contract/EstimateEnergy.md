# EstimateEnergy

Estimate the energy required to call a contract. Requires `vm.estimateEnergy=true` on the node.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc EstimateEnergy (TriggerSmartContract) returns (EstimateEnergyMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/estimateenergy](../../http/smart-contract/estimateenergy.md).
