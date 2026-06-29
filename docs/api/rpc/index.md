# java-tron gRPC API

A java-tron node exposes its API over gRPC. This directory lists short reference docs for 82 commonly used gRPC methods, organized by topic.

## Services and default ports

| Service | Default port | Description | Source |
|---|---|---|---|
| `protocol.Wallet` | `50051` | FullNode full-feature service (includes write transactions) | `framework/src/main/java/org/tron/core/services/RpcApiService.java` |
| `protocol.WalletSolidity` | `50061` | Returns solidified data only; read-only | `framework/src/main/java/org/tron/core/services/interfaceOnSolidity/RpcApiServiceOnSolidity.java` |

The ports can be overridden via `node.rpc.port` / `node.rpc.solidityPort` in the node configuration (see `framework/src/main/resources/config.conf`).

The proto definition lives in `protocol/src/main/protos/api/api.proto`.

## Calling

gRPC does not use URL paths to distinguish `wallet` from `walletsolidity` — they are two independent service stubs reached on different ports:

```text
# Wallet
grpc://<host>:50051   protocol.Wallet/<Method>

# WalletSolidity (read-only)
grpc://<host>:50061   protocol.WalletSolidity/<Method>
```

Each method doc contains:

- The method name (top-level heading, PascalCase, identical to the proto)
- A short description
- Service support (`Wallet` / `WalletSolidity` / both)
- The matching protobuf signature

## Account

| Method | Description |
|---|---|
| [GetAccount](account/GetAccount.md) | Look up an account by address |
| [GetAccountBalance](account/GetAccountBalance.md) | Query an account's balance at a specific block |
| [GetAccountNet](account/GetAccountNet.md) | Query an account's bandwidth resource |
| [GetAccountResource](account/GetAccountResource.md) | Query an account's bandwidth + energy + TronPower |
| [CreateAccount2](account/CreateAccount2.md) | Create an account on chain (consumes 1 TRX) |
| [UpdateAccount2](account/UpdateAccount2.md) | Update the account name |
| [AccountPermissionUpdate](account/AccountPermissionUpdate.md) | Configure multi-sig permissions |

## Block / transaction query

| Method | Description |
|---|---|
| [GetNowBlock2](block-and-tx-query/GetNowBlock2.md) | The latest block |
| [GetBlock](block-and-tx-query/GetBlock.md) | Generic block lookup (by num/hash) |
| [GetBlockByNum2](block-and-tx-query/GetBlockByNum2.md) | Look up a block by height |
| [GetBlockById](block-and-tx-query/GetBlockById.md) | Look up a block by hash |
| [GetBlockByLimitNext2](block-and-tx-query/GetBlockByLimitNext2.md) | Look up a range of blocks |
| [GetBlockByLatestNum2](block-and-tx-query/GetBlockByLatestNum2.md) | Get the most recent N blocks |
| [GetBlockBalanceTrace](block-and-tx-query/GetBlockBalanceTrace.md) | Query account balance changes within a block |
| [GetTransactionCountByBlockNum](block-and-tx-query/GetTransactionCountByBlockNum.md) | Number of transactions in a block |
| [GetTransactionById](block-and-tx-query/GetTransactionById.md) | Look up a transaction by txID |
| [GetTransactionInfoById](block-and-tx-query/GetTransactionInfoById.md) | Look up a transaction's receipt by txID |
| [GetTransactionInfoByBlockNum](block-and-tx-query/GetTransactionInfoByBlockNum.md) | Look up transaction receipts by block |
| [GetPendingSize](block-and-tx-query/GetPendingSize.md) | Pending pool size |
| [GetTransactionFromPending](block-and-tx-query/GetTransactionFromPending.md) | Look up a single pending transaction |
| [GetTransactionListFromPending](block-and-tx-query/GetTransactionListFromPending.md) | All pending transaction IDs |

## Transaction build / broadcast

| Method | Description |
|---|---|
| [CreateTransaction2](tx-build-and-broadcast/CreateTransaction2.md) | Build a TRX transfer transaction |
| [GetTransactionSignWeight](tx-build-and-broadcast/GetTransactionSignWeight.md) | Query the current accumulated multi-sig weight |
| [GetTransactionApprovedList](tx-build-and-broadcast/GetTransactionApprovedList.md) | List addresses that have signed a multi-sig transaction |
| [BroadcastTransaction](tx-build-and-broadcast/BroadcastTransaction.md) | Broadcast a signed transaction (JSON) |

## TRC-10 asset

| Method | Description |
|---|---|
| [CreateAssetIssue2](asset/CreateAssetIssue2.md) | Issue a TRC-10 token |
| [UpdateAsset2](asset/UpdateAsset2.md) | Update a TRC-10's description / URL / bandwidth limit |
| [TransferAsset2](asset/TransferAsset2.md) | Transfer TRC-10 |
| [ParticipateAssetIssue2](asset/ParticipateAssetIssue2.md) | Participate in a TRC-10 sale |
| [UnfreezeAsset2](asset/UnfreezeAsset2.md) | Unfreeze TRC-10 locked by the issuer |
| [GetAssetIssueById](asset/GetAssetIssueById.md) | Look up TRC-10 by id (recommended) |
| [GetAssetIssueByName](asset/GetAssetIssueByName.md) | Look up TRC-10 by name (errors on duplicate names) |
| [GetAssetIssueListByName](asset/GetAssetIssueListByName.md) | List TRC-10s sharing a given name |
| [GetAssetIssueByAccount](asset/GetAssetIssueByAccount.md) | TRC-10s issued by an account |
| [GetAssetIssueList](asset/GetAssetIssueList.md) | All TRC-10s on chain |
| [GetPaginatedAssetIssueList](asset/GetPaginatedAssetIssueList.md) | Paginated TRC-10 list |

## Smart contract

| Method | Description |
|---|---|
| [DeployContract](smart-contract/DeployContract.md) | Deploy a contract |
| [TriggerContract](smart-contract/TriggerContract.md) | Trigger a contract (write) |
| [TriggerConstantContract](smart-contract/TriggerConstantContract.md) | Read-only contract call |
| [EstimateEnergy](smart-contract/EstimateEnergy.md) | Estimate the energy cost of a call |
| [GetContract](smart-contract/GetContract.md) | Query contract metadata |
| [GetContractInfo](smart-contract/GetContractInfo.md) | Query a contract's full runtime info |
| [ClearContractABI](smart-contract/ClearContractABI.md) | Clear a contract's ABI |
| [UpdateSetting](smart-contract/UpdateSetting.md) | Update the user-energy percentage |
| [UpdateEnergyLimit](smart-contract/UpdateEnergyLimit.md) | Update the deployer energy limit |

## Witness / governance

| Method | Description |
|---|---|
| [CreateWitness2](witness-and-governance/CreateWitness2.md) | Apply to become an SR candidate |
| [UpdateWitness2](witness-and-governance/UpdateWitness2.md) | Update an SR's URL |
| [ListWitnesses](witness-and-governance/ListWitnesses.md) | List all SR candidates |
| [GetPaginatedNowWitnessList](witness-and-governance/GetPaginatedNowWitnessList.md) | Paginated SR list |
| [VoteWitnessAccount2](witness-and-governance/VoteWitnessAccount2.md) | Vote for SRs |
| [GetBrokerageInfo](witness-and-governance/GetBrokerageInfo.md) | An SR's current brokerage rate |
| [UpdateBrokerage](witness-and-governance/UpdateBrokerage.md) | An SR updates its brokerage |
| [GetRewardInfo](witness-and-governance/GetRewardInfo.md) | Query claimable voter rewards |
| [WithdrawBalance2](witness-and-governance/WithdrawBalance2.md) | Withdraw block-production rewards / voter rewards |
| [ProposalCreate](witness-and-governance/ProposalCreate.md) | Create a chain-parameter proposal |
| [ProposalApprove](witness-and-governance/ProposalApprove.md) | An SR votes on a proposal |
| [ProposalDelete](witness-and-governance/ProposalDelete.md) | Cancel a proposal you created |
| [ListProposals](witness-and-governance/ListProposals.md) | List proposals |
| [GetProposalById](witness-and-governance/GetProposalById.md) | Look up a proposal by ID |
| [GetPaginatedProposalList](witness-and-governance/GetPaginatedProposalList.md) | Paginated proposal list |
| [GetChainParameters](witness-and-governance/GetChainParameters.md) | Current values of all chain parameters |
| [GetNextMaintenanceTime](witness-and-governance/GetNextMaintenanceTime.md) | Time of the next maintenance period |

## Stake 1.0 (unfreeze and query only)

After proposal #70 `UNFREEZE_DELAY_DAYS` was passed (mainnet has activated it), new V1 freeze requests are rejected on chain; the unfreeze and query methods remain so legacy positions can still be wound down.

> The trailing `2` in file names (e.g. `FreezeBalance2`) is a historical proto naming suffix (the V1 method that returns `TransactionExtention`) and is not the same method as Stake 2.0's `FreezeBalanceV2`.

| Method | Description |
|---|---|
| [FreezeBalance2](stake-v1/FreezeBalance2.md) | Freeze TRX for resources (V1, **chain rejects new requests**) |
| [UnfreezeBalance2](stake-v1/UnfreezeBalance2.md) | Unfreeze matured resources (V1, still usable for legacy unfreezing) |
| [GetDelegatedResource](stake-v1/GetDelegatedResource.md) | Look up delegation records (V1, read-only) |
| [GetDelegatedResourceAccountIndex](stake-v1/GetDelegatedResourceAccountIndex.md) | Look up delegation counterparty addresses (V1, read-only) |

## Stake 2.0

| Method | Description |
|---|---|
| [FreezeBalanceV2](stake-v2/FreezeBalanceV2.md) | Freeze TRX for resources |
| [UnfreezeBalanceV2](stake-v2/UnfreezeBalanceV2.md) | Initiate an unfreeze (14-day wait) |
| [WithdrawExpireUnfreeze](stake-v2/WithdrawExpireUnfreeze.md) | Withdraw matured unfreeze |
| [CancelAllUnfreezeV2](stake-v2/CancelAllUnfreezeV2.md) | Cancel all unmatured unfreezes |
| [DelegateResource](stake-v2/DelegateResource.md) | Delegate resources to another account |
| [UnDelegateResource](stake-v2/UnDelegateResource.md) | Undelegate resources |
| [GetDelegatedResourceV2](stake-v2/GetDelegatedResourceV2.md) | Look up delegation records |
| [GetDelegatedResourceAccountIndexV2](stake-v2/GetDelegatedResourceAccountIndexV2.md) | Look up delegation counterparty addresses |
| [GetCanDelegatedMaxSize](stake-v2/GetCanDelegatedMaxSize.md) | Current maximum delegatable amount |
| [GetAvailableUnfreezeCount](stake-v2/GetAvailableUnfreezeCount.md) | Remaining unfreeze slots |
| [GetCanWithdrawUnfreezeAmount](stake-v2/GetCanWithdrawUnfreezeAmount.md) | Withdrawable amount at a given timestamp |

## Node / pricing / tools

| Method | Description |
|---|---|
| [GetNodeInfo](node-and-tools/GetNodeInfo.md) | Node status |
| [ListNodes](node-and-tools/ListNodes.md) | Known peer nodes |
| [GetEnergyPrices](node-and-tools/GetEnergyPrices.md) | Historical energy unit prices |
| [GetBandwidthPrices](node-and-tools/GetBandwidthPrices.md) | Historical bandwidth unit prices |
| [GetBurnTrx](node-and-tools/GetBurnTrx.md) | Cumulative burned TRX |
