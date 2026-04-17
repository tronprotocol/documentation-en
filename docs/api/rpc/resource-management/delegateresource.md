# delegateResource

**Supported API**: `wallet`

TRON API method that delegates resources to another account. This method allows you to delegate bandwidth or energy resources obtained from staking TRX to another address, enabling that address to use your resources for transactions.

```protobuf
rpc DelegateResource (DelegateResourceContract) returns (TransactionExtention) {}
```
