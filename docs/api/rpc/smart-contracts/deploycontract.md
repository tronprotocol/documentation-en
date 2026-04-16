# deployContract

**Supported API**: `wallet`

TRON API method that creates a transaction to deploy a new smart contract to the TRON network. This method prepares the deployment transaction with all necessary parameters, which must then be signed and broadcast to complete the contract deployment.

```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```
