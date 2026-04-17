# getBrokerageInfo

**Supported API**: `wallet` `walletsolidity`

TRON API method that returns a witness’s brokerage percentage (0–100). Witnesses set this rate to determine how much of their block rewards they keep before sharing the remainder with voters.

```protobuf
rpc GetBrokerageInfo (BytesMessage) returns (NumberMessage) {}
```
