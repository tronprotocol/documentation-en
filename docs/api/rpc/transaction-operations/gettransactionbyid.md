# getTransactionById

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves transaction details by transaction ID. This method returns comprehensive information about a specific transaction, including its execution results, resource consumption, and contract details.

```protobuf
rpc GetTransactionById (BytesMessage) returns (Transaction) {}
```
