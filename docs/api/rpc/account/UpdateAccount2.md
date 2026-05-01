# UpdateAccount2

Update the account nickname (`account_name`). The field is not unique.

- Service: `Wallet` only

```protobuf
rpc UpdateAccount2 (AccountUpdateContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/updateaccount](../../http/account/updateaccount.md).
