# getAssetIssueListByName

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves a list of TRC10 tokens that match a specified name pattern. This method allows searching for tokens by their names and is useful for discovering assets with similar or related names.

```protobuf
rpc GetAssetIssueListByName (BytesMessage) returns (AssetIssueList) {}
```
