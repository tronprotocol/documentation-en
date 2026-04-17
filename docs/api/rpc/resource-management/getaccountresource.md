# getAccountResource

**Supported API**: `wallet`

TRON API method that queries the resource information of an account, including bandwidth, energy, and TRON Power (voting power). This endpoint provides comprehensive resource metrics for managing transaction costs and network participation.

```protobuf
rpc GetAccountResource (Account) returns (AccountResourceMessage) {}
```
