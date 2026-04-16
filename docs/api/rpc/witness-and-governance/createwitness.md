# createWitness

**Supported API**: `wallet`

TRON API method that creates a transaction to register an account as a witness (validator) on the TRON network. Witnesses participate in block production and network governance through the Delegated Proof of Stake (DPoS) consensus mechanism.

```protobuf
rpc CreateWitness (WitnessCreateContract) returns (Transaction) {}
```
