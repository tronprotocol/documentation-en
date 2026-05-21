# System Contracts
The TRON network supports many different types of transactions, such as TRX transfers, TRC-10 transfers, smart contract creation and triggering and TRX staking. To create different types of transactions, you need to call different APIs. For example, the transaction type for smart contract deployment is `CreateSmartContract`, which requires calling the `wallet/deploycontractAPI`.The transaction type of stake TRX is `FreezeBalanceV2Contract`, which requires calling the ` wallet/freezebalancev2API`. We collectively refer to the implementation of these different transaction types as system contracts.

## ContractType Overview

Every system contract is identified by a `ContractType` enum value defined in [`Tron.proto`](https://github.com/tronprotocol/java-tron/blob/master/protocol/src/main/protos/core/Tron.proto). The table below lists each `ContractType` together with its Proto Message, Actuator, current status, and the business it triggers.

| # | ContractType | Proto Message | Actuator | Status | Business Triggered |
|---|---|---|---|---|---|
| 0 | AccountCreateContract | AccountContract.AccountCreateContract | CreateAccountActuator | ✅ Enabled | Create an on-chain account |
| 1 | TransferContract | BalanceContract.TransferContract | TransferActuator | ✅ Enabled | TRX Transfer |
| 2 | TransferAssetContract | AssetIssueContractOuterClass.TransferAssetContract | TransferAssetActuator | ✅ Enabled | TRC-10 token transfer |
| 3 | VoteAssetContract | | | 🚫 Disabled (Actuator not implemented) | |
| 4 | VoteWitnessContract | WitnessContract.VoteWitnessContract | VoteWitnessActuator | ✅ Enabled | Vote for SRs using account's TronPower; refresh voting records (takes effect at next maintenance) |
| 5 | WitnessCreateContract | WitnessContract.WitnessCreateContract | WitnessCreateActuator | ✅ Enabled | Apply to become a Super Representative (SR) candidate; write to witness store |
| 6 | AssetIssueContract | AssetIssueContractOuterClass.AssetIssueContract | AssetIssueActuator | ✅ Enabled | Issue TRC-10 tokens; freeze balance during recruitment period according to ICO rules |
| 8 | WitnessUpdateContract | WitnessContract.WitnessUpdateContract | WitnessUpdateActuator | ✅ Enabled | Update the official website URL of an SR |
| 9 | ParticipateAssetIssueContract | AssetIssueContractOuterClass.ParticipateAssetIssueContract | ParticipateAssetIssueActuator | ✅ Enabled | Participate in a TRC-10 token issuance with TRX during the ICO period |
| 10 | AccountUpdateContract | AccountContract.AccountUpdateContract | UpdateAccountActuator | ✅ Enabled | Modify account name (subject to AllowUpdateAccountName constraint) |
| 11 | FreezeBalanceContract | BalanceContract.FreezeBalanceContract | FreezeBalanceActuator | 🚫 Disabled (rejected by chain after `supportUnfreezeDelay` is enabled) | Stake 1.0: Freeze TRX to gain Bandwidth/Energy; can be delegated to others |
| 12 | UnfreezeBalanceContract | BalanceContract.UnfreezeBalanceContract | UnfreezeBalanceActuator | ✅ Enabled | Stake 1.0: Unfreeze TRX after expiration; release resources and clear votes |
| 13 | WithdrawBalanceContract | BalanceContract.WithdrawBalanceContract | WithdrawBalanceActuator | ✅ Enabled | Withdraw SR block/voting rewards to account balance |
| 14 | UnfreezeAssetContract | AssetIssueContractOuterClass.UnfreezeAssetContract | UnfreezeAssetActuator | ✅ Enabled | Issuer unfreezes TRC-10 token shares frozen during ICO |
| 15 | UpdateAssetContract | AssetIssueContractOuterClass.UpdateAssetContract | UpdateAssetActuator | ✅ Enabled | Update TRC-10 token description / url / free bandwidth quota |
| 16 | ProposalCreateContract | ProposalContract.ProposalCreateContract | ProposalCreateActuator | ✅ Enabled | SR creates an on-chain parameter proposal; written to ProposalStore for voting |
| 17 | ProposalApproveContract | ProposalContract.ProposalApproveContract | ProposalApproveActuator | ✅ Enabled | SR approves or cancels a vote on a proposal |
| 18 | ProposalDeleteContract | ProposalContract.ProposalDeleteContract | ProposalDeleteActuator | ✅ Enabled | Proposal creator withdraws their own created proposal |
| 19 | SetAccountIdContract | AccountContract.SetAccountIdContract | SetAccountIdActuator | ✅ Enabled | Set a unique account_id for the account (can only be set once) |
| 20 | CustomContract | | | 🚫 Disabled (Actuator not implemented) | |
| 30 | CreateSmartContract | SmartContractOuterClass.CreateSmartContract | VMActuator | ✅ Enabled | Deploy a smart contract |
| 31 | TriggerSmartContract | SmartContractOuterClass.TriggerSmartContract | VMActuator | ✅ Enabled | Call/Trigger a smart contract |
| 32 | GetContract | | | 🚫 Disabled (Actuator not implemented) | |
| 33 | UpdateSettingContract | SmartContractOuterClass.UpdateSettingContract | UpdateSettingContractActuator | ✅ Enabled | Contract owner modifies `consume_user_resource_percent` (percentage of energy borne by the user) |
| 41 | ExchangeCreateContract | ExchangeContract.ExchangeCreateContract | ExchangeCreateActuator | ✅ Enabled | Create a Bancor exchange pair; inject initial liquidity for two assets |
| 42 | ExchangeInjectContract | ExchangeContract.ExchangeInjectContract | ExchangeInjectActuator | ✅ Enabled | Inject liquidity into an existing exchange pair; deduct assets based on Bancor algorithm |
| 43 | ExchangeWithdrawContract | ExchangeContract.ExchangeWithdrawContract | ExchangeWithdrawActuator | ✅ Enabled | Exchange pair creator redeems both assets from the pair proportionally |
| 44 | ExchangeTransactionContract | ExchangeContract.ExchangeTransactionContract | ExchangeTransactionActuator | 🚫 Disabled | Asset exchange via Bancor exchange pair |
| 45 | UpdateEnergyLimitContract | SmartContractOuterClass.UpdateEnergyLimitContract | UpdateEnergyLimitContractActuator | ✅ Enabled | Contract owner updates `origin_energy_limit` (max energy consumption owner is willing to pay per call) |
| 46 | AccountPermissionUpdateContract | AccountContract.AccountPermissionUpdateContract | AccountPermissionUpdateActuator | ✅ Enabled | Update account permissions: owner/witness/active |
| 48 | ClearABIContract | SmartContractOuterClass.ClearABIContract | ClearABIContractActuator | ✅ Enabled | Contract owner clears contract ABI |
| 49 | UpdateBrokerageContract | StorageContract.UpdateBrokerageContract | UpdateBrokerageActuator | ✅ Enabled | SR adjusts the brokerage ratio (0-100%) for voters |
| 51 | ShieldedTransferContract | ShieldContract.ShieldedTransferContract | ShieldedTransferActuator | 🚫 Disabled (`getAllowShieldedTransaction` not enabled) | ZK-SNARK anonymous transfer (transparent in + shielded spend/receive + transparent out) |
| 52 | MarketSellAssetContract | MarketContract.MarketSellAssetContract | MarketSellAssetActuator | 🚫 Disabled (`getAllowMarketTransaction` not enabled) | Place a limit sell order on the built-in order book (sell/buy two assets + price) |
| 53 | MarketCancelOrderContract | MarketContract.MarketCancelOrderContract | MarketCancelOrderActuator | 🚫 Disabled (`getAllowMarketTransaction` not enabled) | Cancel own unexecuted market order; refund remaining assets |
| 54 | FreezeBalanceV2Contract | BalanceContract.FreezeBalanceV2Contract | FreezeBalanceV2Actuator | ✅ Enabled | Stake 2.0: Freeze TRX to gain Bandwidth/Energy; decouples resources from TronPower |
| 55 | UnfreezeBalanceV2Contract | BalanceContract.UnfreezeBalanceV2Contract | UnfreezeBalanceV2Actuator | ✅ Enabled | Stake 2.0: Initiate unstaking; enters unfreeze waiting period |
| 56 | WithdrawExpireUnfreezeContract | BalanceContract.WithdrawExpireUnfreezeContract | WithdrawExpireUnfreezeActuator | ✅ Enabled | Withdraw unfrozen TRX that has passed the waiting period to account balance |
| 57 | DelegateResourceContract | BalanceContract.DelegateResourceContract | DelegateResourceActuator | ✅ Enabled | Stake 2.0: Delegate own staked Bandwidth/Energy to other addresses (lock-up period optional) |
| 58 | UnDelegateResourceContract | BalanceContract.UnDelegateResourceContract | UnDelegateResourceActuator | ✅ Enabled | Stake 2.0: Reclaim previously delegated resources from others |
| 59 | CancelAllUnfreezeV2Contract | BalanceContract.CancelAllUnfreezeV2Contract | CancelAllUnfreezeV2Actuator | ✅ Enabled | Cancel all pending Stake 2.0 unfreezing requests; remaining shares are re-staked |

The protobuf message definition and field-level documentation of each contract are listed in the sections below.

## AccountCreateContract
```
    message AccountCreateContract {
      bytes owner_address = 1;
      bytes account_address = 2;
      AccountType type = 3;
    }
```

- `owner_address`: The address of the account creating the new account.
- `account_address`: The target address to create.
- `type`: Account type. 0 means normal account; 1 means the Genesis account; 2 means smart contract account.

## TransferContract
```
    message TransferContract {
      bytes owner_address = 1;
      bytes to_address = 2;
      int64 amount = 3;
    }
```

- `owner_address`: The address of the account sending TRX.
- `to_address`: The target address to receive the transfer.
- `amount`: The amount of TRX to transfer.

## TransferAssetContract
```
    message TransferAssetContract {
      bytes asset_name = 1;
      bytes owner_address = 2;
      bytes to_address = 3;
      int64 amount = 4;
    }
```

- `asset_name`: The TRC-10 token ID to transfer.
- `owner_address`: The address of the account sending the TRC-10 token.
- `to_address`: The target address to receive the transfer.
- `amount`: The amount of token to transfer.

## VoteWitnessContract
```
    message VoteWitnessContract {
      message Vote {
        bytes vote_address = 1;
        int64 vote_count = 2;
      }
      bytes owner_address = 1;
      repeated Vote votes = 2;
      bool support = 3;
    }
```

- `owner_address`: The address of the voter account.
- `vote_address`: The SR or candidate's address.
- `vote_count`: The votes number.
- `support`: Constant true, not used.

## WitnessCreateContract
```
    message WitnessCreateContract {
      bytes owner_address = 1;
      bytes url = 2;
    }
```

- `owner_address`: The address of the account applying to become a Witness.
- `url`: The website url of the witness.

## AssetIssueContract
```
    message AssetIssueContract {
      message FrozenSupply {
        int64 frozen_amount = 1;
        int64 frozen_days = 2;
      }
      bytes owner_address = 1;
      bytes name = 2;
      bytes abbr = 3;
      int64 total_supply = 4;
      repeated FrozenSupply frozen_supply = 5;
      int32 trx_num = 6;
      int32 precision = 7;
      int32 num = 8;
      int64 start_time = 9;
      int64 end_time = 10;
      int64 order = 11; // useless
      int32 vote_score = 16;
      bytes description = 20;
      bytes url = 21;
      int64 free_asset_net_limit = 22;
      int64 public_free_asset_net_limit = 23;
      int64 public_free_asset_net_usage = 24;
      int64 public_latest_free_net_time = 25;
      string id = 41;
    }
```

- `owner_address`: The address of the account issuing the TRC-10 token.
- `name`: The token name to issue.
- `abbr`: The abbreviation of the token name.
- `total_supply`: The amount of token to issue.
- `frozen_supply`: The amount of token and staked days to stake.
- `trx_num`: trx_num/num defines the token price.
- `num`: trx_num/num defines the token price.
- `start_time`: ICO starts time.
- `end_time`: ICO ends time.
- `order`: Deprecated.
- `vote_score`: Deprecated.
- `description`: The description of the token.
- `url`: The website url of the token.
- `free_asset_net_limit`: The free bandwidth limit each account owns when transfers asset.
- `public_free_asset_net_limit`: The free bandwidth limit all the accounts can use.
- `public_free_asset_net_usage`: The free bandwidth usage of all the accounts.
- `public_latest_free_net_time`: The latest bandwidth consumption time of token transfer.
- `id`: The unique token ID, generated sequentially by the system at issuance (incrementing from 1000001).

## WitnessUpdateContract
```
    message WitnessUpdateContract {
      bytes owner_address = 1;
      bytes update_url = 12;
    }
```

- `owner_address`: The Witness account address.
- `update_url`: The website url of the witness.

## ParticipateAssetIssueContract
```
    message ParticipateAssetIssueContract {
      bytes owner_address = 1;
      bytes to_address = 2;
      bytes asset_name = 3;
      int64 amount = 4;
    }
```

- `owner_address`: The address of the account participating in the asset issue.
- `to_address`: The token owner's address.
- `asset_name`: The token id.
- `amount`: The amount of token to purchase.

## AccountUpdateContract
```
    // Update account name. Account name is unique now.
    message AccountUpdateContract {
      bytes account_name = 1;
      bytes owner_address = 2;
    }
```

- `owner_address`: The address of the account to update.
- `account_name`: Account name.

## FreezeBalanceContract
```
    message FreezeBalanceContract {
      bytes owner_address = 1;
      int64 frozen_balance = 2;
      int64 frozen_duration = 3;
      ResourceCode resource = 10;
      bytes receiver_address = 15;
    }
```

- `owner_address`: The address of the account staking TRX.
- `frozen_balance`: The amount of TRX to stake.
- `frozen_duration`: The stake duration.
- `resource`: The type of resource get by staking TRX.
- `receiver_address`: The account address to receive resource.

## UnfreezeBalanceContract
```
    message UnfreezeBalanceContract {
      bytes owner_address = 1;
      ResourceCode resource = 10;
      bytes receiver_address = 15;
    }
```

- `owner_address`: The address of the account unstaking TRX.
- `resource`: The type of resource to unfree.
- `receiver_address`: The account address to receive resource.

## WithdrawBalanceContract
```
    message WithdrawBalanceContract {
      bytes owner_address = 1;
    }
```

- `owner_address`: The address of the account withdrawing rewards.

## UnfreezeAssetContract
```
    message UnfreezeAssetContract {
      bytes owner_address = 1;
    }
```

- `owner_address`: The address of the token issuer.

## UpdateAssetContract
```
    message UpdateAssetContract {
      bytes owner_address = 1;
      bytes description = 2;
      bytes url = 3;
      int64 new_limit = 4;
      int64 new_public_limit = 5;
    }
```

- `owner_address`: The address of the token issuer.
- `description`: The description of the token.
- `url`: The website url of the token.
- `new_limit`: The bandwidth consumption limit of each account when transfers asset.
- `new_public_limit`: The bandwidth consumption limit of the accounts.

## ProposalCreateContract
```
    message ProposalCreateContract {
      bytes owner_address = 1;
      map<int64, int64> parameters = 2;
    }
```

- `owner_address`: The address of the account creating the proposal.
- `parameters`: The proposal.

## ProposalApproveContract
```
    message ProposalApproveContract {
      bytes owner_address = 1;
      int64 proposal_id = 2;
      bool is_add_approval = 3; // add or remove approval
    }
```

- `owner_address`: The address of the account approving the proposal.
- `proposal_id`: The proposal id.
- `is_add_approval`: Whether to approve.

## ProposalDeleteContract
```
    message ProposalDeleteContract {
      bytes owner_address = 1;
      int64 proposal_id = 2;
    }
```

- `owner_address`: The address of the account deleting the proposal.
- `proposal_id`: The proposal id.

## SetAccountIdContract
```
    // Set account id if the account has no id. Account id is unique and case insensitive.
    message SetAccountIdContract {
      bytes account_id = 1;
      bytes owner_address = 2;
    }
```

- `owner_address`: The address of the account setting the account id.
- `account_id`: The account id.

## CreateSmartContract
```
    message CreateSmartContract {
      bytes owner_address = 1;
      SmartContract new_contract = 2;
      int64 call_token_value = 5;
      int64 token_id = 6;
    }
```

- `owner_address`: The address of the account deploying the contract.
- `new_contract`: the smart contract.
- `call_token_value` : The amount of TRC-10 token to send to the contract when triggers.
- `token_id` : The id of the TRC-10 token to be sent to the contract.

## TriggerSmartContract
```
    message TriggerSmartContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
      int64 call_value = 3;
      bytes data = 4;
      int64 call_token_value = 5;
      int64 token_id = 6;
    }
```

- `owner_address`: The address of the account calling the contract.
- `contract_address`: The contract address.
- `call_value`: The amount of TRX to send to the contract when triggers.
- `data`: The parameters to trigger the contract.
- `call_token_value` : The amount of TRC-10 token to send to the contract when triggers.
- `token_id` : The id of the TRC-10 token to be sent to the contract.

## UpdateSettingContract
```
    message UpdateSettingContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
      int64 consume_user_resource_percent = 3;
    }
```

- `owner_address`: The address of the contract deployer.
- `contract_address`: The address of the smart contract.
- `consume_user_resource_percent`: The percentage of resource consumption ratio.

## ExchangeCreateContract
```
    message ExchangeCreateContract {
      bytes owner_address = 1;
      bytes first_token_id = 2;
      int64 first_token_balance = 3;
      bytes second_token_id = 4;
      int64 second_token_balance = 5;
    }
```

- `owner_address`: The address of the account creating the exchange.
- `first_token_id`: First token id.
- `first_token_balance`: First token balance.
- `second_token_id`: Second token id.
- `second_token_balance`: Second token balance.

## ExchangeInjectContract
```
    message ExchangeInjectContract {
      bytes owner_address = 1;
      int64 exchange_id = 2;
      bytes token_id = 3;
      int64 quant = 4;
    }
```

- `owner_address`: The address of the account injecting liquidity.
- `exchange_id`: The token pair id.
- `token_id`: The token id to inject.
- `quant`: The token amount to inject.

## ExchangeWithdrawContract
```
    message ExchangeWithdrawContract {
      bytes owner_address = 1;
      int64 exchange_id = 2;
      bytes token_id = 3;
      int64 quant = 4;
    }
```

- `owner_address`: The address of the account withdrawing liquidity.
- `exchange_id`: The token pair id.
- `token_id`: The token id to withdraw.
- `quant`: The token amount to withdraw.

## ExchangeTransactionContract
```
    message ExchangeTransactionContract {
      bytes owner_address = 1;
      int64 exchange_id = 2;
      bytes token_id = 3;
      int64 quant = 4;
      int64 expected = 5;
    }
```

- `owner_address`: The address of the trading account.
- `exchange_id`: The token pair id.
- `token_id`: The token id to sell.
- `quant`: The token amount to sell.
- `expected`: The expected token amount to buy, if the calculated actual token amount that can be bought is less than this value, the transaction will fail.

## UpdateEnergyLimitContract
```
    message UpdateEnergyLimitContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
      int64 origin_energy_limit = 3;
    }
```

- `owner_address`: The address of the contract deployer.
- `contract_address`: The contract address.
- `origin_energy_limit`: The target energy limit to change.

## AccountPermissionUpdateContract
```
    message AccountPermissionUpdateContract {
      bytes owner_address = 1;
      Permission owner = 2;             //Empty is invalidate
      Permission witness = 3;           //Can be empty
      repeated Permission actives = 4;  //Empty is invalidate
    }
```

- `owner_address`: The address of the account whose permissions will be updated.
- `owner`: The owner permission of the account. Cannot be empty.
- `witness`: The witness permission. Required for SR (witness) accounts; must be empty for non-witness accounts.
- `actives`: The list of active permissions. Cannot be empty; at most 8 entries.

For more details, see [Account Permission Management](./multi-signatures.md).

## ClearABIContract
```
    message ClearABIContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
    }
```

- `owner_address`: The address of the contract deployer.
- `contract_address`: The target contract address to clear ABI.

## UpdateBrokerageContract
```
    message UpdateBrokerageContract {
      bytes owner_address = 1;
      int32 brokerage = 2;
    }
```

- `owner_address`: The Witness account address.
- `brokerage`: Commission rate, from 0 to 100,1 mean 1%.

## ShieldedTransferContract
```
    message ShieldedTransferContract {
      bytes transparent_from_address = 1;
      int64 from_amount = 2;
      repeated SpendDescription spend_description = 3;
      repeated ReceiveDescription receive_description = 4;
      bytes binding_signature = 5;
      bytes transparent_to_address = 6;
      int64 to_amount = 7;
    }
```

- `transparent_from_address`: The transparent address of the sender.
- `from_amount`: The amount to send.
- `spend_description`: Shielded spend information.
- `receive_description`: Shielded receive information.
- `binding_signature`: The binding signature.
- `transparent_to_address`: The transparent address of the receiver.
- `to_amount`: The amount to receive.

```
message SpendDescription {
  bytes value_commitment = 1;
  bytes anchor = 2;
  bytes nullifier = 3;
  bytes rk = 4;
  bytes zkproof = 5;
  bytes spend_authority_signature = 6;
}
```

- `value_commitment`: _value commitment_ of spender's transfer amount.
- `anchor`: root of the note commitment Merkle tree at some block.
- `nullifier`: _nullifier_ of spender's note, to prevent double-spent.
- `rk`: public key, to verify spender's _Spend Authorization Signature_.
- `zkproof`: zero-knowledge proof of spender's note, prove that this note exists and could be spent.
- `spend_authority_signature`: the spender's _Spend Authorization Signature_.

```
message ReceiveDescription {
  bytes value_commitment = 1;
  bytes note_commitment = 2;
  bytes epk = 3;
  bytes c_enc = 4;
  bytes c_out = 5;
  bytes zkproof = 6;
}
```

- `value_commitment`: _value commitment_ of receiver's transfer amount.
- `note_commitment`: commitment of the receiver's note.
- `epk`: ephemeral public key, in order to generate note's decryption key.
- `c_enc`: part of note ciphertext, encryption of diversifier, receiver's transfer amount, rcm, and memo.
- `c_out`: part of note ciphertext, encryption of the receiver's public key and ephemeral private key.
- `zkproof`: zero-knowledge proof of the receiver's note.

## MarketSellAssetContract
```
    message MarketSellAssetContract {
      bytes owner_address = 1;
      bytes sell_token_id = 2;
      int64 sell_token_quantity = 3;
      bytes buy_token_id = 4;
      int64 buy_token_quantity = 5; // min to receive
    }
```

- `owner_address`: The address of the account placing the order.
- `sell_token_id`: The id of the token to sell.
- `sell_token_quantity`: The amount of the token to sell.
- `buy_token_id`: The id of the token to buy.
- `buy_token_quantity`: The minimum amount of the buy token to receive. If the actual amount obtained when matching is less than this value, the order will be placed on the order book waiting to be matched at a better price.

## MarketCancelOrderContract
```
    message MarketCancelOrderContract {
      bytes owner_address = 1;
      bytes order_id = 2;
    }
```

- `owner_address`: The address of the account that placed the order.
- `order_id`: The id of the market order to cancel.

## FreezeBalanceV2Contract

```protobuf
     message FreezeBalanceV2Contract {
      bytes owner_address = 1;
      int64 frozen_balance = 2;
      ResourceCode resource = 3;
      }
```

* `owner_address`: The address of the account staking TRX.
* `frozen_balance`：TRX stake amount, the unit is sun
* `resource`： Resource type

## UnfreezeBalanceV2Contract

```protobuf
      message UnfreezeBalanceV2Contract {
       bytes owner_address = 1;
       int64 unfreeze_balance = 2;
       ResourceCode resource = 3;
      }
```

* `owner_address`: The address of the account unstaking TRX.
* `unfreeze_balance`：The amount of TRX to unstake, in sun
* `resource`： Resource type
   

## WithdrawExpireUnfreezeContract

```protobuf
      message WithdrawExpireUnfreezeContract {
        bytes owner_address = 1;
      }
```

* `owner_address`: The address of the account withdrawing expired unstaked TRX.
   
## DelegateResourceContract

```protobuf
      message DelegateResourceContract {
      bytes owner_address = 1;
      ResourceCode resource = 2;
      int64 balance = 3;
      bytes receiver_address = 4;
      bool  lock = 5;
      int64 lock_period = 6;
      }
```

* `owner_address`: The address of the resource delegator.
* `resource`： Resource type
* `balance`： Amount of TRX staked for resources to be delegated, unit is sun
* `receiver_address`：Resource receiver address
* `lock`：Whether to lock this delegation.
* `lock_period`：The lock duration when `lock=true`, in blocks (3 seconds per block). User-supplied values are only accepted after the `MAX_DELEGATE_LOCK_PERIOD` proposal takes effect; in that case `0` means use the default of 86400 blocks (3 days), and the upper bound is determined by the chain parameter `getMaxDelegateLockPeriod`. Before the proposal takes effect this field is ignored and the lock duration is fixed at 86400 blocks.
   
   
## UnDelegateResourceContract

```protobuf
      message UnDelegateResourceContract {
      bytes owner_address = 1;
      ResourceCode resource = 2;
      int64 balance = 3;
      bytes receiver_address = 4;
      }
```

* `owner_address`: The address of the account canceling the delegation.
* `resource`： Resource type
* `balance`：undelegated TRX, unit is sun
* `receiver_address`：Resource receiver address


## CancelAllUnfreezeV2Contract

```protobuf
      message CancelAllUnfreezeV2Contract {
        bytes owner_address = 1;
      }
```

* `owner_address`: The address of the account canceling all pending Stake 2.0 unfreezing requests.



