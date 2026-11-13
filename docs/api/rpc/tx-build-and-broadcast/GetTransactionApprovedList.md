# GetTransactionApprovedList

Return the transaction's signing addresses after validating all signatures against the account's current permissions. If validation fails, return an error without an approved-address list.

- Service: `Wallet` only

```protobuf
rpc GetTransactionApprovedList (Transaction) returns (TransactionApprovedList) {}
```

See the corresponding HTTP endpoint at [/wallet/getapprovedlist](../../http/tx-build-and-broadcast/getapprovedlist.md).
