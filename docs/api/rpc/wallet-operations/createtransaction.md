# createTransaction

**Supported API**: `wallet`

TRON API method that creates an unsigned TRX transfer transaction. This method generates a transaction object that transfers TRX from one address to another, which can then be signed and broadcast to the network.

```protobuf
rpc CreateTransaction (TransferContract) returns (Transaction) {}
```
