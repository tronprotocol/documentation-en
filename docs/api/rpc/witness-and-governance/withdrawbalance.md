# withdrawBalance

**Supported API**: `wallet`

TRON API method that allows Super Representatives (witnesses) to withdraw their accumulated block production rewards. Witnesses earn TRX rewards for producing blocks and maintaining the network, and this method enables them to claim these earnings.

```protobuf
rpc WithdrawBalance (WithdrawBalanceContract) returns (Transaction) {}
```
