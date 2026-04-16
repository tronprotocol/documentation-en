# updateEnergyLimit

**Supported API**: `wallet`

TRON API method that updates the origin energy limit for a smart contract. This setting determines the maximum amount of energy the contract creator provides for contract execution, affecting how much energy users need to provide when calling the contract.

```protobuf
rpc UpdateEnergyLimit (UpdateEnergyLimitContract) returns (TransactionExtention) {}
```
