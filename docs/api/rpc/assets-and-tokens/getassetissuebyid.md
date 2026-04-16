# getAssetIssueById

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves detailed information about a TRC10 token using its unique asset ID. TRC10 tokens are native TRON assets that can be issued directly on the blockchain without requiring smart contracts.

```protobuf
rpc GetAssetIssueById (BytesMessage) returns (AssetIssueContract) {}
```
