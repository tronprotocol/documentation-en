# getPaginatedNowWitnessList

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves the real-time vote counts of all Super Representatives (SRs) in the current epoch, sorted in descending order, and returns a paginated list within the specified range.

```protobuf
rpc GetPaginatedNowWitnessList (PaginatedMessage) returns (WitnessList) {}
```
