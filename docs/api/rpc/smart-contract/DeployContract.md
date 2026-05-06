# DeployContract

Deploy a smart contract. Returns an unsigned deployment transaction.

- Service: `Wallet` only

```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/deploycontract](../../http/smart-contract/deploycontract.md).
