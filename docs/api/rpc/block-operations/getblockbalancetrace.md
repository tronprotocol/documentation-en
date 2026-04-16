# getBlockBalanceTrace

**Supported API**: `wallet`

TRON API method that returns the balance deltas within a specific block. It shows, per transaction, how account balances changed in that block.

```protobuf
rpc GetBlockBalanceTrace (BlockIdentifier) returns (BlockBalanceTrace) {}
```
