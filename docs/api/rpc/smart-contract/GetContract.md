# GetContract

Get a contract's metadata by address. Returns the `SmartContract` body (including the `bytecode` from deployment), but **not the `runtimecode` or `contract_state`**. For runtime information, use `GetContractInfo`.

- Service: `Wallet` only

```protobuf
rpc GetContract (BytesMessage) returns (SmartContract) {}
```

See the corresponding HTTP endpoint at [/wallet/getcontract](../../http/smart-contract/getcontract.md).
