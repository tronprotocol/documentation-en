# GetTransactionApprovedList

Return the list of addresses that have already signed a multi-sig transaction (signers only, no weight calculation).

- Service: `Wallet` only

```protobuf
rpc GetTransactionApprovedList (Transaction) returns (TransactionApprovedList) {}
```

See the corresponding HTTP endpoint at [/wallet/getapprovedlist](../../http/tx-build-and-broadcast/getapprovedlist.md).
