# CreateTransaction2

Build an unsigned TRX transfer transaction (`TransferContract`).

- Service: `Wallet` only

```protobuf
rpc CreateTransaction2 (TransferContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/createtransaction](../../http/tx-build-and-broadcast/createtransaction.md).
