# GetAccountResource

Query an account's bandwidth (Net) + energy (Energy) + TronPower resource usage.

- Service: `Wallet` only

```protobuf
rpc GetAccountResource (Account) returns (AccountResourceMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getaccountresource](../../http/account/getaccountresource.md).
