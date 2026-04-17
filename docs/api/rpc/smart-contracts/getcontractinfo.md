# getContractInfo

**Supported API**: `wallet`

TRON API method that retrieves detailed information about a smart contract, including its ABI, bytecode, source code, and metadata. This method is essential for understanding and interacting with deployed contracts on the TRON network.

```protobuf
rpc GetContractInfo (BytesMessage) returns (SmartContractDataWrapper) {}
```
