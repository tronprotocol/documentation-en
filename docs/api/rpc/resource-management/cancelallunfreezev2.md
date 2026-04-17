# cancelAllUnfreezeV2

**Supported API**: `wallet`

TRON API method that cancels all unfreezing operations for an account under the Stake 2.0 mechanism. This allows users to cancel pending unfreeze requests and return resources to the frozen state.

```protobuf
rpc CancelAllUnfreezeV2 (CancelAllUnfreezeV2Contract) returns (TransactionExtention) {}
```
