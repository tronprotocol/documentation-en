# CreateWitness2

Apply to become a Super Representative candidate. The fee is the current chain parameter `getAccountUpgradeCost`, expressed in sun; its default is 9,999,000,000 sun (9999 TRX). Governance proposals can change this fee.

- Service: `Wallet` only

```protobuf
rpc CreateWitness2 (WitnessCreateContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/createwitness](../../http/witness-and-governance/createwitness.md).
