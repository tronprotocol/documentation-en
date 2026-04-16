# withdrawExpireUnfreeze

**Supported API**: `wallet`

TRON API method that withdraws TRX tokens that have completed the unstaking waiting period. This method allows you to claim TRX that was previously unstaked using unfreezebalancev2 and has passed the mandatory 14-day waiting period, making the tokens available for transfer.

```protobuf
rpc WithdrawExpireUnfreeze (WithdrawExpireUnfreezeContract) returns (TransactionExtention) {}
```
