# updateBrokerage

**Supported API**: `wallet`

TRON API method that creates a transaction to update the brokerage rate for witness rewards. Only witnesses can call this method to adjust how they share block production rewards with their voters.

```protobuf
rpc UpdateBrokerage (UpdateBrokerageContract) returns (TransactionExtention) {}
```
