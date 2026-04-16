# getTransactionInfoById

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves detailed transaction receipt and execution information by transaction ID. This method provides comprehensive data about a transaction’s execution status, resource usage, fees, and any smart contract events that occurred.

```protobuf
rpc GetTransactionInfoById (BytesMessage) returns (TransactionInfo) {}
```
