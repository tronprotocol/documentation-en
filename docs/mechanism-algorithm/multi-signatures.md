# Account Permission Management 

The TRON network supports fine-grained control of account permissions. By configuring permissions (owner, witness, active), joint control of accounts, secure delegation, and functional permission separation can be achieved. The following document details the account permission model, contract structure, configuration methods, and common interface calls.



## Function Overview

Account permission management allows:

- Setting permission levels for an account.
- Associating each permission with a group of addresses and weights.
- Implementing permission control through a threshold mechanism.
- Flexibly configuring which addresses can execute which contract types.

For detailed specifications, see [TIP-16: Account Permission Management](https://github.com/tronprotocol/tips/blob/master/tip-16.md).



## Permission Level Concepts

TRON supports three types of permission:

| Permission Type | Description                          |
|-----------------|--------------------------------------|
| owner           | Highest account permission, controls ownership and permission structure |
| witness         | Super Representative permission, used only for block production |
| active          | Custom permission, can specify functional permission combinations |

---

## Permission Structure Definition

### 1. Account Structure: `Account`

```
message Account {
  ...
  Permission owner_permission = 31;
  Permission witness_permission = 32;
  repeated Permission active_permission = 33;
}
```

Explanation:

- `owner_permission`: `owner` permission (only one).
- `witness_permission`: Super Representative permission (only one).
- `active_permission`: `active` permission list, supports up to 8.

### 2. Permission Configuration: `Permission`

```
message Permission {
  enum PermissionType {
    Owner = 0;
    Witness = 1;
    Active = 2;
  }
  PermissionType type = 1;
  int32 id = 2;
  string permission_name = 3;
  int64 threshold = 4;
  int32 parent_id = 5;
  bytes operations = 6;
  repeated Key keys = 7;
}
```

Explanation:

- `type`: Permission type (owner/witness/active).
- `id`: Permission ID, automatically assigned by the system.
    - `owner` = 0, `witness` = 1, `active` starts from 2 and increments.
- `permission_name`: Permission name, maximum 32 characters.
- `threshold`: Permission threshold, operation is allowed only when the combined weight of the signing key ≥ this value.
- `operations`: Used only for Active permissions, specifies executable contract types.
- `keys`: Addresses and weights with this permission (up to 5).

### 3. Permission Key Structure: `Key`

```
message Key {
  bytes address = 1;
  int64 weight = 2;
}
```

- `address`: Address with permission.
- `weight`: Weight of this address under this permission.

### 4. Permission Update Transaction: `AccountPermissionUpdateContract`

```
message AccountPermissionUpdateContract {
  bytes owner_address = 1;
  Permission owner = 2;
  Permission witness = 3;
  repeated Permission actives = 4;
}
```

- This contract is used to **update all account permission structures at once**.
- Even if only one permission is modified, all other existing permissions must be fully specified in the contract.

### 5. Contract Type Enumeration: `ContractType`

```
enum ContractType {
  AccountCreateContract = 0;
  ...
  AccountPermissionUpdateContract = 46;
}
```

The detailed information of `ContractType` is as follows (including Proto Message, Actuator, status, and business Triggered):

| # | ContractType | Proto Message | Actuator | Status | Business Triggered |
|---|---|---|---|---|---|
| 0 | AccountCreateContract | AccountContract.AccountCreateContract | CreateAccountActuator | ✅ Enabled | Create an on-chain account |
| 1 | TransferContract | BalanceContract.TransferContract | TransferActuator | ✅ Enabled | TRX Transfer |
| 2 | TransferAssetContract | AssetIssueContractOuterClass.TransferAssetContract | TransferAssetActuator | ✅ Enabled | TRC10 Token Transfer |
| 3 | VoteAssetContract | | | 🚫 Disabled (Actuator not implemented) | |
| 4 | VoteWitnessContract | WitnessContract.VoteWitnessContract | VoteWitnessActuator | ✅ Enabled | Vote for SRs using account's TronPower; refresh voting records (takes effect at next maintenance) |
| 5 | WitnessCreateContract | WitnessContract.WitnessCreateContract | WitnessCreateActuator | ✅ Enabled | Apply to become a Super Representative (SR) candidate; write to witness store |
| 6 | AssetIssueContract | AssetIssueContractOuterClass.AssetIssueContract | AssetIssueActuator | ✅ Enabled | Issue TRC10 tokens; freeze balance during recruitment period according to ICO rules |
| 8 | WitnessUpdateContract | WitnessContract.WitnessUpdateContract | WitnessUpdateActuator | ✅ Enabled | Update the official website URL of an SR |
| 9 | ParticipateAssetIssueContract | AssetIssueContractOuterClass.ParticipateAssetIssueContract | ParticipateAssetIssueActuator | ✅ Enabled | Subscribe to TRC10 tokens with TRX during the ICO period |
| 10 | AccountUpdateContract | AccountContract.AccountUpdateContract | UpdateAccountActuator | ✅ Enabled | Modify account name (subject to AllowUpdateAccountName constraint) |
| 11 | FreezeBalanceContract | BalanceContract.FreezeBalanceContract | FreezeBalanceActuator | 🚫 Disabled (rejected by chain after `supportUnfreezeDelay` is enabled) | Stake 1.0: Freeze TRX to gain Bandwidth/Energy; can be delegated to others |
| 12 | UnfreezeBalanceContract | BalanceContract.UnfreezeBalanceContract | UnfreezeBalanceActuator | ✅ Enabled | Stake 1.0: Unfreeze TRX after expiration; release resources and clear votes |
| 13 | WithdrawBalanceContract | BalanceContract.WithdrawBalanceContract | WithdrawBalanceActuator | ✅ Enabled | Withdraw SR block/voting rewards to account balance |
| 14 | UnfreezeAssetContract | AssetIssueContractOuterClass.UnfreezeAssetContract | UnfreezeAssetActuator | ✅ Enabled | Issuer unfreezes TRC10 token shares frozen during ICO |
| 15 | UpdateAssetContract | AssetIssueContractOuterClass.UpdateAssetContract | UpdateAssetActuator | ✅ Enabled | Update TRC10 token description / url / free bandwidth quota |
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

Active permissions configure which `ContractType` can be executed through the `operations` field. For details on how to calculate the value of `operations`, please see [Operations Value Calculation Example](#2-operations-value-calculation-example).

## Explanation of Each Permission Type

### `owner` Permission (Account Master Control)

- Holds full control over the account.
- Can modify any permission structure (including itself).
- Automatically set when creating an account, default threshold is 1, includes the account's own address.
- By default, transactions without a specified `Permission_id` use the Owner permission.

### `witness` Permission (Block Production Permission)

- Available only for Super Representative, Super Representative Partner, and Super Representative Candidate accounts.
- Controls block-producing nodes, does not have permissions for fund transfers or other operations.
- Can delegate block production permission to other addresses to enhance account security.
- Must contain exactly one key.

#### Super Representative Node Configuration Example:

```
# config.conf
//localWitnessAccountAddress = TMK5c1jd...m6FXFXEz  # TRON Address
localwitness = [
  xxx  # Private key of TMK5c1jd...m6FXFXEz
]
```

If the `witness` permission is modified, then:

```
localWitnessAccountAddress = TSMC4YzU...PBebBk2E
localwitness = [
  yyy  # Private key of TSMC4YzU...PBebBk2E
]
```

>**Note**: Only one private key is allowed in `localwitness`.

### Active Permission (Functional Permission Combination)

- Can combine contract permissions, assigning sub-permissions to different roles.
- Supports up to 8 `active` permission configurations.
- Permission IDs start from 2 and increment.
- When creating an account by default, one `active` permission is generated, with a default threshold of 1, containing only the account's own address.

## Operation Fees

| Operation                  | Fee Standard |
| -------------------------- | ------------ |
| Modify Account Permission  | 100 TRX      |
| Transaction (2 or more signatures) | Additional 1 TRX |

The above fees can be adjusted through proposals.

## Interfaces and Operation Examples

### 1. Permission Modification Operation Process

1. Use `getaccount` to query the current account permission structure.
2. Construct the new permission configuration.
3. Call `AccountPermissionUpdateContract`.
4. Sign and broadcast the transaction.

**Note**: When a block contains transactions that modify account permissions, no further transactions from this account will be included in this block to ensure that such account permission modify transactions actually take effect starting from the next block.

#### Example Request:

```
POST http://{{host}}:{{port}}/wallet/accountpermissionupdate

{
  "owner_address": "41ffa946...",
  "owner": {
    "type": 0,
    "id": 0,
    "permission_name": "owner",
    "threshold": 2,
    "keys": [...]
  },
  "witness": {
    "type": 1,
    "id": 1,
    "permission_name": "witness",
    "threshold": 1,
    "keys": [...]
  },
  "actives": [
    {
      "type": 2,
      "id": 2,
      "permission_name": "active0",
      "threshold": 3,
      "operations": "7fff1fc0037e...",
      "keys": [...]
    }
  ]
}
```

### 2. Operations Value Calculation Example

`operations` is a 32-byte hexadecimal string (little-endian) representing executable contract permissions.
The following Java example generates permissions for contracts (ID=0-45):

```
Integer[] contractId = {0, 1, 2, ..., 45};
byte[] operations = new byte[32];
for (int id : contractId) {
  operations[id / 8] |= (1 << id % 8);
}
System.out.println(ByteArray.toHexString(operations));
```

>**Note**: The `contractId` above only illustrates the bit-setting logic. `ContractType` IDs are not contiguous (7, 21-29, 34-40, etc. are gaps), and a bit can only be set for a contract type already present in the on-chain `AVAILABLE_CONTRACT_TYPE` bitmap; otherwise the transaction is rejected during validation. `AVAILABLE_CONTRACT_TYPE` roughly corresponds to the `#` column in the table above, except it does not include ShieldedTransferContract(51).

### 3. Transaction Execution Process

1. Create the transaction.
2. Set `Permission_id` (default is 0, i.e., `owner` permission).
3. User A signs and forwards to B.
4. User B signs and forwards to C.
5. ...
6. The last user signs and broadcasts.
7. The node verifies if the total signature weight ≥ `threshold`; if yes, accepts the transaction.

>Example code reference: [wallet-cli Example](https://github.com/tronprotocol/wallet-cli/blob/develop/src/main/java/org/tron/common/utils/TransactionUtils.java)

## Auxiliary Interfaces

### Query Signed Addresses

```
POST /wallet/getapprovedlist

rpc GetTransactionApprovedList(Transaction) returns (TransactionApprovedList) {}
```

### Query Signature Weight

```
POST /wallet/getsignweight

rpc GetTransactionSignWeight(Transaction) returns (TransactionSignWeight) {}
```

## References

- [TIP-16 Permission Management Proposal](https://github.com/tronprotocol/tips/blob/master/tip-16.md)
- [Tron.proto Contract Type Definitions](https://github.com/tronprotocol/java-tron/blob/master/protocol/src/main/protos/core/Tron.proto)
