# GetContractInfo

Get a contract's full runtime information (runtime code, state, and energy info included).

- Service: `Wallet` only

```protobuf
rpc GetContractInfo (BytesMessage) returns (SmartContractDataWrapper) {}
```

See the corresponding HTTP endpoint at [/wallet/getcontractinfo](../../http/smart-contract/getcontractinfo.md).
