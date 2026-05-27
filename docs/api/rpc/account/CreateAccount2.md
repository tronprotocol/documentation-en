# CreateAccount2

Build an unsigned transaction that creates a new account. Passive activation: the payer (`owner_address`) covers the activation fee, and the new address (`account_address`) is created.

- Service: `Wallet` only

```protobuf
rpc CreateAccount2 (AccountCreateContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/createaccount](../../http/account/createaccount.md).
