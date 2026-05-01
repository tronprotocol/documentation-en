# GetAssetIssueByName

Look up a single TRC10 token by name. **Note**: since the `ALLOW_SAME_TOKEN_NAME` proposal, name is no longer unique, and this method returns an error when duplicates exist; prefer `GetAssetIssueById` or `GetAssetIssueListByName`.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetAssetIssueByName (BytesMessage) returns (AssetIssueContract) {}
```

See the corresponding HTTP endpoint at [/wallet/getassetissuebyname](../../http/asset/getassetissuebyname.md).
