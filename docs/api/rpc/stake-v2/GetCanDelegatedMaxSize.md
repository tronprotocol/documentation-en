# GetCanDelegatedMaxSize

Query the maximum resource amount the account can currently delegate (Stake 2.0).

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetCanDelegatedMaxSize (CanDelegatedMaxSizeRequestMessage) returns (CanDelegatedMaxSizeResponseMessage) {}
```

See the corresponding HTTP endpoint at [/wallet/getcandelegatedmaxsize](../../http/stake-v2/getcandelegatedmaxsize.md).
