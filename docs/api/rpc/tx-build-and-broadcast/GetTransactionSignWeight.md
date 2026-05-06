# GetTransactionSignWeight

Validate a partially-signed multi-sig transaction; returns the current accumulated weight and whether the threshold has been reached.

- Service: `Wallet` only

```protobuf
rpc GetTransactionSignWeight (Transaction) returns (TransactionSignWeight) {}
```

See the corresponding HTTP endpoint at [/wallet/getsignweight](../../http/tx-build-and-broadcast/getsignweight.md).
