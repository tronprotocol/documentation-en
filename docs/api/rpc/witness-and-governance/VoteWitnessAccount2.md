# VoteWitnessAccount2

Vote for Super Representatives (SRs). Each call replaces all of the account's existing votes.

- Service: `Wallet` only

```protobuf
rpc VoteWitnessAccount2 (VoteWitnessContract) returns (TransactionExtention) {}
```

See the corresponding HTTP endpoint at [/wallet/votewitnessaccount](../../http/witness-and-governance/votewitnessaccount.md).
