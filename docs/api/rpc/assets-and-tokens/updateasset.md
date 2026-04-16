# updateAsset

**Supported API**: `wallet`

TRON API method that creates an unsigned transaction for updating the information of an existing TRC10 token. This allows token issuers to modify certain properties of their tokens after creation.

```protobuf
rpc UpdateAsset (UpdateAssetContract) returns (Transaction) {}
```
