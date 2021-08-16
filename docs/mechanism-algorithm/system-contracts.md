# System Contracts

## AccountCreateContract

    message AccountCreateContract {
      bytes owner_address = 1;
      bytes account_address = 2;
      AccountType type = 3;
    }

- `owner_address`: The owner of the current account.
- `account_address`: The target address to create.
- `type`: Account type. 0 means normal account; 1 means the Genesis account; 2 means smart contract account.

## TransferContract

    message TransferContract {
      bytes owner_address = 1;
      bytes to_address = 2;
      int64 amount = 3;
    }

- `owner_address`: The owner of the current account.
- `to_address`: The target address to transfer.
- `amount`: The amount of TRX to transfer.

## TransferAssetContract

    message TransferAssetContract {
      bytes asset_name = 1;
      bytes owner_address = 2;
      bytes to_address = 3;
      int64 amount = 4;
    }

- `asset_name`: The token id to transfer.
- `owner_address`: The owner of the current account.
- `to_address`: The target address to transfer.
- `amount`: The amount of token to transfer.

## VoteWitnessContract

    message VoteWitnessContract {
      message Vote {
        bytes vote_address = 1;
        int64 vote_count = 2;
      }
      bytes owner_address = 1;
      repeated Vote votes = 2;
      bool support = 3;
    }

- `owner_address`: The owner of the current account.
- `vote_address`: The SR or candidate's address.
- `vote_count`: The votes number.
- `support`: Constant true, not used.

## WitnessCreateContract

    message WitnessCreateContract {
      bytes owner_address = 1;
      bytes url = 2;
    }

- `owner_address`: The owner of the current account.
- `url`: The website url of the witness.

## AssetIssueContract

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
      int32 num = 8;
      int64 start_time = 9;
      int64 end_time = 10;
      int64 order = 11; // the order of tokens of the same name
      int32 vote_score = 16;
      bytes description = 20;
      bytes url = 21;
      int64 free_asset_net_limit = 22;
      int64 public_free_asset_net_limit = 23;
      int64 public_free_asset_net_usage = 24;
      int64 public_latest_free_net_time = 25;
    }

- `owner_address`: The owner of the current account.
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

## WitnessUpdateContract

    message WitnessUpdateContract {
      bytes owner_address = 1;
      bytes update_url = 12;
    }

- `owner_address`: The owner of the current account.
- `update_url`: The website url of the witness.

## ParticipateAssetIssueContract

    message ParticipateAssetIssueContract {
      bytes owner_address = 1;
      bytes to_address = 2;
      bytes asset_name = 3;
      int64 amount = 4;
    }

- `owner_address`: The owner of the current account.
- `to_address`: The token owner address.
- `account_name`: The token id.
- `amount`: The amount of token to purchase.

## AccountUpdateContract

    // Update account name. Account name is unique now.
    message AccountUpdateContract {
      bytes account_name = 1;
      bytes owner_address = 2;
    }

- `owner_address`: The owner of the current account.
- `account_name`: Account name.

## FreezeBalanceContract

    message FreezeBalanceContract {
      bytes owner_address = 1;
      int64 frozen_balance = 2;
      int64 frozen_duration = 3;
      ResourceCode resource = 10;
      bytes receiver_address = 15;
    }

- `owner_address`: The owner of the current account.
- `frozen_balance`: The amount of TRX to stake.
- `frozen_duration`: The stake duration.
- `resource`: The type of resource get by staking TRX.
- `receiver_address`: The account address to receive resource.

## UnfreezeBalanceContract

    message UnfreezeBalanceContract {
      bytes owner_address = 1;
      ResourceCode resource = 10;
      bytes receiver_address = 13;
    }

- `owner_address`: The owner of the current account.
- `resource`: The type of resource to unfree.
- `receiver_address`: The account address to receive resource.

## WithdrawBalanceContract

    message WithdrawBalanceContract {
      bytes owner_address = 1;
    }

- `owner_address`: The owner of the current account.

## UnfreezeAssetContract

    message UnfreezeAssetContract {
      bytes owner_address = 1;
    }

- `owner_address`: The owner of the current account.

## UpdateAssetContract

    message UpdateAssetContract {
      bytes owner_address = 1;
      bytes description = 2;
      bytes url = 3;
      int64 new_limit = 4;
      int64 new_public_limit = 5;
    }

- `owner_address`: The owner of the current account.
- `description`: The description of the token.
- `url`: The website url of the token.
- `new_limit`: The bandwidth consumption limit of each account when transfers asset.
- `new_public_limit`: The bandwidth consumption limit of the accounts.

## ProposalCreateContract

    message ProposalCreateContract {
      bytes owner_address = 1;
      map<int64, int64> parameters = 2;
    }

- `owner_address`: The owner of the current account.
- `parameters`: The proposal.

## ProposalApproveContract

    message ProposalApproveContract {
      bytes owner_address = 1;
      int64 proposal_id = 2;
      bool is_add_approval = 3; // add or remove approval
    }

- `owner_address`: The owner of the current account.
- `proposal_id`: The proposal id.
- `is_add_approval`: Whether to approve.

## ProposalDeleteContract

    message ProposalDeleteContract {
      bytes owner_address = 1;
      int64 proposal_id = 2;
    }

- `owner_address`: The owner of the current account.
- `proposal_id`: The proposal id.

## SetAccountIdContract

    // Set account id if the account has no id. Account id is unique and case insensitive.
    message SetAccountIdContract {
      bytes account_id = 1;
      bytes owner_address = 2;
    }

- `owner_address`: The owner of the current account.
- `account_id`: The account id.

## CreateSmartContract

    message CreateSmartContract {
      bytes owner_address = 1;
      SmartContract new_contract = 2;
      int64 call_token_value = 5;
      int64 token_id = 6;
    }

- `owner_address`: The owner of the current account.
- `new_contract`: the smart contract.
- `call_token_value` : The amount of TRC-10 token to send to the contract when triggers.
- `token_id` : The id of the TRC-10 token to be sent to the contract.

## TriggerSmartContract

    message TriggerSmartContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
      int64 call_value = 3;
      bytes data = 4;
      int64 call_token_value = 5;
      int64 token_id = 6;
    }

- `owner_address`: The owner of the current account.
- `contract_address`: The contract address.
- `call_value`: The amount of TRX to send to the contract when triggers.
- `data`: The parameters to trigger the contract.
- `call_token_value` : The amount of TRC-10 token to send to the contract when triggers.
- `token_id` : The id of the TRC-10 token to be sent to the contract.

## UpdateSettingContract

    message UpdateSettingContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
      int64 consume_user_resource_percent = 3;
    }

- `owner_address`: The owner of the current account.
- `contract_address`: The address of the smart contract.
- `consume_user_resource_percent`: The percentage of resource consumption ratio.

## ExchangeCreateContract

    message ExchangeCreateContract {
      bytes owner_address = 1;
      bytes first_token_id = 2;
      int64 first_token_balance = 3;
      bytes second_token_id = 4;
      int64 second_token_balance = 5;
    }

- `owner_address`: The owner of the current account.
- `first_token_id`: First token id.
- `first_token_balance`: First token balance.
- `second_token_id`: Second token id.
- `second_token_balance`: Second token balance.

## ExchangeInjectContract

    message ExchangeInjectContract {
      bytes owner_address = 1;
      int64 exchange_id = 2;
      bytes token_id = 3;
      int64 quant = 4;
    }

- `owner_address`: The owner of the current account.
- `exchange_id`: The token pair id.
- `token_id`: The token id to inject.
- `quant`: The token amount to inject.

## ExchangeWithdrawContract

    message ExchangeWithdrawContract {
      bytes owner_address = 1;
      int64 exchange_id = 2;
      bytes token_id = 3;
      int64 quant = 4;
    }

- `owner_address`: The owner of the current account.
- `exchange_id`: The token pair id.
- `token_id`: The token id to withdraw.
- `quant`: The token amount to withdraw.

## ExchangeTransactionContract

    message ExchangeTransactionContract {
      bytes owner_address = 1;
      int64 exchange_id = 2;
      bytes token_id = 3;
      int64 quant = 4;
    }

- `owner_address`: The owner of the current account.
- `exchange_id`: The token pair id.
- `token_id`: The token id to sell.
- `quant`: The token amount to sell.

## ShieldedTransferContract

    message ShieldedTransferContract {
      bytes transparent_from_address = 1;
      int64 from_amount = 2;
      repeated SpendDescription spend_description = 3;
      repeated ReceiveDescription receive_description = 4;
      bytes binding_signature = 5;
      bytes transparent_to_address = 6;
      int64 to_amount = 7;
    }

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
- `note_commitment`: commitment of the receiver's not.
- `epk`: ephemeral public key, in order to generate note's decryption key.
- `c_enc`: part of note ciphertext, encryption of diversifier, receiver's transfer amount, rcm, and memo.
- `c_out`: part of note ciphertext, encryption of the receiver's public key and ephemeral private key.
- `zkproof`: zero-knowledge proof of the receiver's note.

## Multi Signature

[Multi-Signature](./multi-signatures.md)

## ClearABIContract

    message ClearABIContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
    }

- `owner_address`: The owner of the current account.
- `account_address`: The target contract address to clear ABI.

## UpdateBrokerageContract

    message UpdateBrokerageContract {
      bytes owner_address = 1;
      int32 brokerage = 2;
    }

- `owner_address`: The owner of the current account.
- `brokerage`: Commission rate, from 0 to 100,1 mean 1%.

## UpdateEnergyLimitContract

    message UpdateEnergyLimitContract {
      bytes owner_address = 1;
      bytes contract_address = 2;
      int64 origin_energy_limit = 3;
    }

- `owner_address`: The owner of the current account.
- `contract_address`: The contract address.
- `origin_energy_limit`: The target energy limit to change.
