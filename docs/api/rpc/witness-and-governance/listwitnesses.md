# listWitnesses

**Supported API**: `wallet` `walletsolidity`

TRON API method that retrieves a complete list of all witnesses (validators) on the TRON network. Witnesses are responsible for block production and network governance in TRON’s Delegated Proof of Stake (DPoS) consensus mechanism.

```protobuf
rpc ListWitnesses (EmptyMessage) returns (WitnessList) {}
```
