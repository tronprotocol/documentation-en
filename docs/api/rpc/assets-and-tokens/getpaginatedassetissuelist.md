# getPaginatedAssetIssueList

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves a paginated list of all TRC10 tokens issued on the TRON network. This method provides efficient pagination support for browsing through large numbers of tokens without overwhelming the response.

```protobuf
rpc GetPaginatedAssetIssueList (PaginatedMessage) returns (AssetIssueList) {}
```
