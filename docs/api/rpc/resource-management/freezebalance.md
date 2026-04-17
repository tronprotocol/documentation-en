# freezeBalance

**Supported API**: `wallet`

TRON API method that stakes TRX for bandwidth or energy resources (deprecated method). This method freezes TRX tokens to obtain bandwidth or energy resources, which are required for transaction execution. legacy staking closed on mainnetThe legacy wallet/freezebalance endpoint is disabled on mainnet and returns:{"Error":"class org.tron.core.exception.ContractValidateException : freeze v2 is open, old freeze is closed"} Use the current staking method instead: wallet/freezebalancev2. The examples below are kept for historical context and may only work on specific networks where legacy staking is still enabled.

```protobuf
rpc FreezeBalance (FreezeBalanceContract) returns (Transaction) {}
```
