# GetCanWithdrawUnfreezeAmount

Query the unfreeze amount the account can withdraw at a given timestamp (Stake 2.0).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetCanWithdrawUnfreezeAmount (CanWithdrawUnfreezeAmountRequestMessage) returns (CanWithdrawUnfreezeAmountResponseMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getcanwithdrawunfreezeamount](../../http/stake-v2/getcanwithdrawunfreezeamount.md).
