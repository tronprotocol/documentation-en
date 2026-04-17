# unfreezeBalanceV2

**Supported API**: `wallet`

TRON API method that unstakes TRX from the new staking mechanism. This method releases TRX tokens that were previously staked using freezebalancev2, initiating the unstaking process with a 14-day waiting period before tokens become available for withdrawal. This is the current recommended unstaking method.

```protobuf
rpc UnfreezeBalanceV2 (UnfreezeBalanceV2Contract) returns (TransactionExtention) {}
```
