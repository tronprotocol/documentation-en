# unfreezeAsset

**Supported API**: `wallet`

TRON API method that creates an unsigned transaction for unfreezing TRC10 tokens that were previously frozen during token creation. This releases frozen tokens back to the token issuer’s available balance.

```protobuf
rpc UnfreezeAsset (UnfreezeAssetContract) returns (Transaction) {}
```
