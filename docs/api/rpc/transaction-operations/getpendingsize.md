# getPendingSize

**Supported API**: `wallet`

TRON API method that returns the current size of the pending transaction pool (mempool). This provides insight into network congestion and the number of unconfirmed transactions awaiting processing.

```protobuf
rpc GetPendingSize (EmptyMessage) returns (NumberMessage) {}
```
