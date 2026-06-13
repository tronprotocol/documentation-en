# GetAssetIssueById

Look up a TRC-10 token by token id (recommended; token id is globally unique).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetAssetIssueById (BytesMessage) returns (AssetIssueContract) {}
```

See the corresponding HTTP endpoint at [/wallet/getassetissuebyid](../../http/asset/getassetissuebyid.md).
