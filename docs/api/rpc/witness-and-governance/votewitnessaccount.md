# voteWitnessAccount

**Supported API**: `wallet`

TRON API method that creates a transaction to vote for witnesses (validators) using frozen TRX balance. Voting is essential for TRON’s Delegated Proof of Stake (DPoS) governance system and helps determine which witnesses become Super Representatives.

```protobuf
rpc VoteWitnessAccount (VoteWitnessContract) returns (Transaction) {}
```
