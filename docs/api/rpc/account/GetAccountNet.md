# GetAccountNet

Query an account's bandwidth (Net) resource usage. **Deprecated**; use [`GetAccountResource`](GetAccountResource.md) instead.

- Service: `Wallet` only

```protobuf
rpc GetAccountNet (Account) returns (AccountNetMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getaccountnet](../../http/account/getaccountnet.md).
