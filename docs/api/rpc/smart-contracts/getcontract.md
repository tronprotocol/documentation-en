# getContract

**Supported API**: `wallet`

TRON API method that retrieves detailed information about a smart contract deployed on the TRON network. This method provides comprehensive contract data including bytecode, ABI, deployment information, and resource configuration.

```protobuf
rpc GetContract (BytesMessage) returns (SmartContract) {}
```
