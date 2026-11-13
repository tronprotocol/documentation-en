# GetPaginatedNowWitnessList

List all SR candidates with pagination, sorted by their current vote totals. These totals include vote changes in the current cycle, unlike the stored vote counts returned by [ListWitnesses](ListWitnesses.md). The results are not restricted to the 27 active SRs or to candidates with `isJobs=true`.

- Service: both `Wallet` and `WalletSolidity`

```protobuf
rpc GetPaginatedNowWitnessList (PaginatedMessage) returns (WitnessList) {}
```

See the corresponding HTTP endpoint at [/wallet/getpaginatednowwitnesslist](../../http/witness-and-governance/getpaginatednowwitnesslist.md).
