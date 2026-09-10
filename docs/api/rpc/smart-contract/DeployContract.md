# DeployContract

Deploy a smart contract. Returns an unsigned deployment transaction.

- Service: `Wallet` only

```protobuf
rpc DeployContract (CreateSmartContract) returns (TransactionExtention) {}
```

When constructing `CreateSmartContract`, ensure that `new_contract.name` is no more than 32 bytes. After the `VERSION_4_8_2_2` upgrade takes effect, the limit is measured using UTF-8 encoding, not by the number of characters. For example, most Chinese characters use three bytes each in UTF-8.

Leave `new_contract.code_hash` and `new_contract.trx_hash` empty. These fields are reserved for values set by the node; after the `VERSION_4_8_2_2` upgrade takes effect, deployment fails if either field is non-empty.

See the corresponding HTTP endpoint at [/wallet/deploycontract](../../http/smart-contract/deploycontract.md).
