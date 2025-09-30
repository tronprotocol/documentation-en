# Resource Model

## Introduction to the Resource Model

The TRON network's core system resources consist of three components: TRON Power (TP), Bandwidth, and Energy. Their definitions and functions are as follows:

  - **TRON Power (TP):** Used exclusively for voting for Super Representatives (SRs) and Super Representative Partners. It serves as the credential for users to participate in network governance and is obtained by staking TRX.
  - **Bandwidth:** Measures the byte size of a transaction on the blockchain. Every type of transaction, from a simple transfer to a contract interaction, must consume Bandwidth.
  - **Energy:** Measures the computational resources consumed by the TRON Virtual Machine (TVM) to execute a smart contract. It can be understood as a "CPU processing fee." Energy is only consumed when deploying or triggering a smart contract.

## TRON Power (TP)

Before voting for Super Representatives, an account must first acquire TRON Power (TP).

  * **How to Obtain:** When you stake TRX for either Bandwidth or Energy, you simultaneously receive an equivalent amount of TRON Power. This is the only way to get TP. For staking instructions, refer to the [Staking on TRON](#staking-on-tron) section.
  * **Conversion Ratio:** The staking-to-TP ratio is 1:1. Staking 1 TRX grants you 1 TP.
  * **Accumulation:** You can stake TRX in multiple, separate transactions. The TP acquired from all stakes is automatically added to your account's total TP pool.
  * **Querying:** You can check your account's total and used TP at any time using the `wallet/getaccountresource` API endpoint.

## Bandwidth

Transactions are transmitted and stored on the network as byte arrays. The Bandwidth consumed by a transaction is calculated as `Transaction Size (bytes) * Bandwidth Rate`. The current Bandwidth rate is 1.

For example, a transaction with a size of 200 bytes will consume 200 Bandwidth.

> **Note:** Because the total staked funds in the network and an individual account's staked funds can change at any time, the amount of Bandwidth an account possesses is not a fixed value.

### 1\. Obtaining Bandwidth

There are three ways to obtain Bandwidth:

  * **Staking TRX:**
    Users share a fixed total Bandwidth pool in proportion to the amount of TRX they have staked for Bandwidth.

    ```
    Bandwidth Share = (TRX Staked for Bandwidth / Total TRX Staked for Bandwidth Network-Wide) * Total Bandwidth Limit
    ```

    **Total Bandwidth** is a network parameter that can be modified through a committee proposal ([\#62](https://tronscan.io/#/sr/committee)) and is currently set to 43,200,000,000.

    Staking for Bandwidth (`wallet-cli` example):

    ```
    freezeBalanceV2 frozen_balance [ResourceCode:0 BANDWIDTH,1 ENERGY]
    ```

  * **Delegation from Others:**
    Another account can delegate their Bandwidth to you. 
    
    Delegating Bandwidth (`wallet-cli` example):

    ```
    delegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress [lock]
    ```
    
  * **Daily Free Allowance:**
    Every account receives a fixed daily allowance of free Bandwidth, which can be modified through a committee proposal [#61](https://tronscan.io/#/sr/committee) and is currently set to 600.

### 2\. How Bandwidth is Consumed

All transactions, except for query operations, consume Bandwidth. When you initiate a transaction, the system deducts the Bandwidth fee according to a strict priority order based on the transaction type.

**Scenario 1: Standard Transactions**

The system attempts to pay the Bandwidth fee in the following order:

1.  **Staked Bandwidth:** Consumes the Bandwidth obtained by the transaction initiator from staking TRX.
2.  **Free Bandwidth:** If staked Bandwidth is insufficient, consumes the initiator's 600 daily free allowance.
3.  **TRX Burning:** If both staked and free Bandwidth are insufficient, burns the initiator's TRX to cover the fee.
      * *Burn Fee = Transaction Size (bytes) × 1,000 sun*

**Scenario 2: New Account Creation Transactions**

Transactions that create a new account follow a special rule and do not use the daily free allowance:

1.  **Staked Bandwidth:** First, attempts to consume the Bandwidth obtained by the transaction initiator from staking TRX.
2.  **TRX Burning:** If staked Bandwidth is insufficient, directly burns 0.1 TRX to complete the account creation.

**Scenario 3: TRC-10 Token Transfers**

TRC-10 token transfers have a unique consumption logic that introduces the "token issuer" as a potential fee payer:

1.  **Issuer's Bandwidth (Highest Priority):** The system first attempts to consume the Bandwidth prepaid by the token issuer. This requires all three of the following conditions to be met (only if all three checks pass will the issuer's Bandwidth be deducted; otherwise, the cost falls to the transaction initiator):
      * The token issuer has a sufficient total free Bandwidth allowance.
          * Query Method: /wallet/getassetissuebyaccount
          * Formula: `public_free_asset_net_limit - public_free_asset_net_usage`
          * Description: The remaining quota the token issuer can pay for this token's transfers.
      * The transaction initiator has a sufficient Bandwidth allowance for that specific token.
          * Query Method: /wallet/getaccountnet
          * Formula: `assetNetLimit['assetID'] - assetNetUsed['assetID']`
          * Description: The free Bandwidth quota provided by the issuer that the token holder can still use.
      * The token issuer has sufficient staked Bandwidth. 
          * Query Method: /wallet/getaccountnet
          * Formula: `NetLimit - NetUsed`
          * Description: The amount of available Bandwidth the issuer has obtained through staking.
2.  **Initiator's Staked Bandwidth:** Attempts to consume the initiator's staked Bandwidth.
3.  **Initiator's Free Bandwidth:** If staked Bandwidth is insufficient, consumes the initiator's free Bandwidth allowance.
4.  **TRX Burning:** If all the above resources are insufficient, burns the initiator's TRX to pay the fee.
      * *Burn Fee = Transaction Size (bytes) × 1,000 sun*

### 3\. Automatic Bandwidth Recovery

An account's consumed free Bandwidth and staked Bandwidth will gradually recover over a 24-hour period.

### 4\. Querying Bandwidth Balance

You can query an account's current resource status by calling the `wallet/getaccountresource` HTTP endpoint. In the returned JSON data, use the following formulas to calculate the remaining Bandwidth:

```
Remaining Free Bandwidth = freeNetLimit - freeNetUsed
Remaining Staked Bandwidth = NetLimit - NetUsed
```

*Note: If any of these parameters are absent from the API response, their value is `0`.*

## Energy

Energy is the unit of measurement for the computational resources consumed by the TRON Virtual Machine (TVM) when executing the instructions of a smart contract. This section provides a comprehensive overview of Energy focusing on the following three aspects:

- [The acquisition, consumption, and recovery of Energy](#get-energy)
- [How to set the key parameter, `fee_limit`](#set-fee-limit)
- [The TRON network's overall consumption mechanism](#energy-mechanism)

<a id="get-energy"></a>
### 1\. Acquiring and Consuming Energy

Energy can be acquired in two primary ways:

- By Staking TRX: Users can obtain Energy by staking the TRX they hold.
- By Receiving Delegation: Users can receive Energy delegated to them from other accounts.

#### Staking for Energy (`wallet-cli` example)

```
freezeBalanceV2 frozen_balance [ResourceCode:0 BANDWIDTH,1 ENERGY]
```

#### Delegating Energy (`wallet-cli` example)

```
delegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress [lock]
```

#### Querying Energy Balance

You can query an account's current Energy status using the `wallet/getaccountresource` HTTP endpoint. In the returned JSON data, calculate the remaining Energy using the following formula:

```
Remaining Energy = EnergyLimit - EnergyUsed
```

*Note: If these parameters are absent from the API response, their value is `0`.*

#### Calculating your Energy Share

The amount of Energy you receive is a dynamic value calculated in real-time based on your stake relative to the total network stake for Energy:

```
Your Energy Share = (TRX Staked for Energy / Total TRX Staked for Energy Network-Wide) * Total Energy Limit
```

Total Energy Limit is a network parameter set by the committee ([\#19](https://tronscan.io/#/sr/committee)), currently at 180,000,000,000, and can be modified via proposals.

##### Calculation Example

Because your share is tied to the network's total stake, your available Energy will fluctuate as other users stake or unstake.

```
Assume only two users, A and B, have staked 2 TRX each.

Their respective Energy shares are:
A: 90,000,000,000
B: 90,000,000,000

When a third user, C, stakes 1 TRX, the shares are adjusted:
A: 72,000,000,000
B: 72,000,000,000
C: 36,000,000,000
```

#### Energy Consumption

##### Payment Priority

When a contract transaction consumes Energy, the system deducts the cost in the following order:

1.  **Staked Energy:** First, the system consumes the Energy obtained by the transaction initiator from staking TRX.
2.  **TRX Burning:** If staked Energy is insufficient to cover all instructions, the system automatically burns the initiator's TRX to cover the difference. The current price is 0.0001 TRX per unit of Energy.

##### Fee Deduction for Exceptions

Contract execution can be interrupted for various reasons, with different rules for Energy deduction:

  * **Normal Interruption (`REVERT`):** If a contract exits due to a `REVERT` instruction, only the Energy for the instructions executed up to that point is deducted.
  * **Unexpected Interruption (bug or Timeout):** If a contract crashes due to a code bug, timeout, or another unexpected error, the system will deduct all available Energy for the transaction as a penalty. Users can limit this penalty by setting the `fee_limit` parameter for the transaction.

#### Energy Recovery

Consumed Energy resources gradually recover over a 24-hour period.

<a id="set-fee-limit"></a>
### 2\. How to Set `fee_limit` (Essential for Users)

> In this section, "developer" refers to the person who develops and deploys the contract, while "caller" refers to the user or contract that invokes it.
>
> Since the Energy consumed by a contract can be converted to TRX (or sun), this section uses "Energy" and "TRX" interchangeably to refer to the resource cost. The terms are distinguished only when referring to specific numerical units.

`fee_limit` is a critical safety parameter when calling a smart contract. A properly set `fee_limit` ensures that a transaction can execute successfully while preventing excessive TRX consumption if the contract requires unexpectedly high Energy.

Before setting `fee_limit`, understand these concepts:

1.  A valid `fee_limit` is an integer ranging from 0 to 15,000,000,000 sun (equivalent to 15,000 TRX). The `fee_limit` upper bound is a network parameter that can be modified by committee proposals ([#47](https://tronscan.io/#/sr/committee)), and its current value is 15,000 TRX.
2.  Contracts of varying complexity consume different amounts of Energy. The same contract generally consumes a similar amount of Energy per execution[^1], but with the dynamic energy model, popular contracts may require more Energy at different times. For details, see the [Dynamic Energy Model](#dynamic-energy-model) section. During execution, Energy is deducted instruction by instruction. If the cost exceeds the `fee_limit`, the execution fails, and the consumed Energy is not refunded.
3.  The `fee_limit` currently specifies the maximum amount of TRX the **caller** is willing to pay to execute a contract[^2]. Note that the total Energy consumed by the contract's execution can be a combination of what the caller pays and what the developer covers for the contract.
4.  If a contract execution times out or crashes due to a bug, all the Energy allowed for the current transaction will be consumed. This total energy pool is the sum of the following components: `Total Consumed Energy = Energy from Caller's Stake + Energy from Developer's Share + Energy from Burned TRX`. The "Energy from Burned TRX" component is capped by `fee_limit`.
5.  Through the [Energy sharing mechanism](https://developers.tron.network/docs/energy-consumption-mechanism#tron-energy-sharing-mechanism), a developer may cover a percentage of the Energy cost (e.g., 90%). However, if the developer's account has insufficient Energy, the remaining cost falls entirely to the caller. Within the `fee_limit`, if the caller's Energy is also insufficient, an equivalent amount of TRX will be burned.

**Example:**
Here's how to estimate the `fee_limit` for executing a contract `C`:

  - Assume contract C consumed 18,000 Energy during its last successful execution. By calling the [estimateenergy](https://developers.tron.network/reference/estimateenergy) API to get a pre-execution estimate, let's assume the upper limit of Energy consumption for this transaction is approximately 20,000 Energy.
  - When burning TRX, since the unit price of Energy is currently 100 sun, 10 TRX can be exchanged for a fixed 100,000 Energy units.
  - Assume the developer has committed to covering 90% of the Energy cost and has sufficient Energy.

The `fee_limit` estimation method is as follows:

- **Step 1: Calculate the Total Transaction Fee**
First, calculate the total potential cost of the transaction by multiplying the estimated maximum Energy consumption by the current Energy price: `20,000 Energy * 100 sun = 2,000,000 sun (equivalent to 2 TRX)`.
- **Step 2: Determine the User's Share**
Next, calculate the portion of the fee the user is responsible for. Given the developer commits to covering 90%, the user's share is 10%: `2,000,000 sun * 10% = 200,000 sun`.
- **Step 3: Set the Final `fee_limit`**
Therefore, the recommended `fee_limit` for the user to set is 200,000 sun.

<a id="energy-mechanism"></a>
### 3\. Energy Consumption Mechanism

**Basic Energy Consumption Rules**

When executing smart contract transactions, the system calculates and deducts the Energy required for each instruction sequentially. The consumption of Energy in an account follows these priority principles:

1. Available Energy (obtained through staking or renting) in the account is first used.
2. If that part of Energy is insufficient, the remaining part will be covered by burning TRX from the account at a fixed rate (0.0001 TRX per Energy unit).

**Contract Energy Sharing Mechanism**

For smart contract calls, to reduce the caller's costs, TRON allows contract deployers to bear a portion of the Energy consumption. For specific details, please refer to the Contract Energy Sharing Mechanism section.

Energy Deduction Rules:

- Portion borne by the contract deployer:
    - Directly deducted from the available Energy in the deployer's account. TRX in the deployer's account will not be burned.
- Portion borne by the contract caller:
    - Available Energy in the caller’s account is consumed first.
    - If insufficient, the remaining part will be covered by burning TRX from the caller's account at a fixed rate.

<a id="dynamic-energy-model"></a>
## Dynamic Energy Model

The Dynamic Energy Model is a resource-balancing mechanism on the TRON network. It dynamically adjusts the Energy consumption of each contract based on its resource usage, promoting a more equitable distribution of Energy and preventing network resources from being excessively concentrated on a few popular contracts. For more details, see the [Introduction to Dynamic Energy Model](https://medium.com/tronnetwork/introduction-to-dynamic-energy-model-31917419b61a).

### How It Works

If a contract consumes an excessive amount of Energy within a maintenance period (currently 6 hours), transactions calling that same contract will incur additional Energy costs in the next period. When the contract's resource usage returns to a reasonable level, the Energy cost for calling it will gradually return to normal.

Each contract has an `energy_factor`, which is a multiplier for its base Energy consumption. The initial value is `0`.

  - An `energy_factor` of `0` means the contract is using resources reasonably, and calls will incur no extra Energy cost.
  - An `energy_factor` greater than `0` indicates it is a popular contract, and calls will consume additional Energy. You can query a contract's `energy_factor` via the `getcontractinfo` API endpoint.

The final Energy consumption for a contract call is calculated as:

```
Contract Transaction Energy Consumption = Base Energy Consumption Generated by the Contract Call Transaction * (1 + energy_factor)
```

The dynamic energy model introduces three network parameters that control the `energy_factor`:

  * `threshold`: The threshold for a contract's base Energy consumption. If a contract exceeds this threshold in a maintenance period, its Energy cost will increase in the next period.
  * `increase_factor`: The rate at which `energy_factor` increases when the threshold is exceeded.
  * `max_factor`: The maximum possible value for `energy_factor`.

There is also a `decrease_factor` used to lower the `energy_factor`:

  * `decrease_factor`: Set to **one-fourth** of the `increase_factor`. When a contract's base Energy consumption falls below the threshold, its `energy_factor` is reduced by this rate.

**`energy_factor` Adjustment Formulas:**

  - When the base energy consumption of a contract exceeds the `threshold` within a maintenance period, its `energy_factor` will increase during the next maintenance period, but will not exceed `max_factor`. The formula for this calculation is:
    ```
    energy_factor = min((1 + energy_factor) * (1 + increase_factor) - 1, max_factor)
    ```
  - When the base energy consumption of a contract falls to or below the `threshold` within a maintenance period, its `energy_factor` will decrease during the next maintenance period, but not below a minimum of `0`. The formula for this calculation is:
    ```
    energy_factor = max((1 + energy_factor) * (1 - decrease_factor) - 1, 0)
    ```

The dynamic energy model is active on Mainnet with the following parameters:

  * `threshold`: 5,000,000,000
  * `increase_factor`: 0.2
  * `max_factor`: 3.4

Since the Energy cost for popular contracts can vary between maintenance periods, it is crucial to set an appropriate `fee_limit` for transactions.

<a id="staking-on-tron"></a>
## Staking on TRON

### How to Stake for System Resources

On the TRON network, staking TRX is the unified mechanism for obtaining the three core resources: Energy, Bandwidth, and TRON Power (TP).

#### How to Stake

  * **HTTP API:** Call the `wallet/freezebalancev2` endpoint.
  * **Smart Contract:** Use the [Stake 2.0 Solidity API](https://developers.tron.network/docs/stake-20-solidity-api) within a contract.

When you unstake, the corresponding resources (Energy/Bandwidth) and TP are released and reclaimed simultaneously.

### How to Delegate Resources

After an account obtains Energy or Bandwidth through staking, it can choose to delegate these resources to other TRON accounts. This allows accounts with a surplus of resources to help those with insufficient resources complete transactions.

**Delegation Rules and Key Restrictions**

  * **Delegable Resources:** Only Energy and Bandwidth can be delegated. TP cannot.
  * **Source of Resources:** Only available resources obtained through Stake 2.0 are eligible for delegation.
  * **Recipient:** The recipient must be an activated external account, not a contract address.

**Time Lock Option**

When delegating, you can choose to enable a time lock, which affects when you can reclaim the resources.

  * **With Time Lock:** The resources are locked for a period. You must wait for this period to end before you can undelegate. 
      > **Important:** If you delegate to the same address again during this period, the pending period resets.
  * **Without Time Lock:** You can undelegate at any time and reclaim the resources immediately.

**Related API Endpoints**

  * `delegateresource`: Delegate resources.
  * `undelegateresource`: Undelegate (reclaim) resources.
  * `getcandelegatedmaxsize`: Query the maximum amount of a resource you can delegate.

### How to Unstake

After staking TRX, you can initiate an unstake operation at any time using the `unfreezebalancev2` API. However, this process has a time delay and follows specific rules.

**Core Rule: 14-Day Pending Period**

  * **Pending Period:** After initiating an unstake, your TRX funds enters a 14-day pending period.
  * **Fund Availability:** You can only withdraw the funds to your account balance after the 14-day period has ended.
  * **Network Parameter:** This pending period is TRON network parameter [#70](https://tronscan.io/#/sr/committee) and may be changed in the future through network governance.

**Important Notes**

  * **Delegated Resources Cannot Be Unstaked:** 
You cannot unstake TRX corresponding to resources that are currently delegated. You must first reclaim the resources using `undelegateresource` before you can unstake that portion of TRX.
  * **Resource Reclamation:** 
      Unstaking will cause the resources (Energy or Bandwidth) and TRON Power (TP) corresponding to the staked TRX to be synchronously reclaimed by the system. As a result, you will lose the respective Energy or Bandwidth and an equivalent amount of TP.
  * **Concurrent Operation Limit:** 
You can have a maximum of 32 unstake operations in the 14-day pending period at any one time. Use the `getavailableunfreezecount` endpoint to check your remaining unstake capacity.

**Automatic Effects of Unstaking**

Calling `unfreezebalancev2` not only initiates a new unstaking process, but it also automatically withdraws any TRX that has already completed its 14-day pending period.


**How to Verify Withdrawn Amount**

To find out exactly how much unstaked TRX was automatically withdrawn during a specific unstaking operation, you can query the details of that unstake transaction using the `gettransactioninfobyid` API and look for the following field:

- `withdraw_expire_amount`: This field shows the amount of matured unstaked TRX that was automatically withdrawn in this transaction.

#### Reclaiming TRON Power

Under Stake 2.0, unstaking TRX simultaneously reclaims an equivalent amount of TRON Power (TP). If the amount of TP to be reclaimed exceeds your account's idle (unvoted) TP, the system will proportionally revoke your cast votes.

**TP Reclamation Priority**

When the system reclaims TP, it follows the following two-step process:

1.  **Reclaim Idle TP First:** The system first reclaims all of your account's TP that is not currently being used for voting.
2.  **Cancel Votes as Needed:** If the idle TP is insufficient to meet the reclamation demand, the system will begin to revoke your cast votes to reclaim the remaining required TP.

**Rules for Calculating Vote Revocation**

The revocation operation is not random. Instead, votes are revoked proportionally and fairly from every Super Representative (SR) and Super Representative Partner you have voted for.

*Formula:*

```
Votes Revoked from a Given SR = Total Votes to Revoke * (Votes Cast for that SR or SR Partner / Total Votes Cast by the Account)
```

*Example:*

Assume User `A`'s account state is:

  * **Total Staked:** 2,000 TRX
  * **Total TP:** 2,000 TP
  * **Votes Cast:** 1,000 TP (600 for SR1, 400 for SR2)
  * **Unused TP:** 1,000 TP

Now, User `A` unstakes **1,500 TRX**.

*System Process:*

1.  **Reclamation Demand:** The system needs to reclaim 1,500 TP.
2.  **Reclaim Unused TP:** First, it reclaims all 1,000 idle TP.
3.  **Calculate Shortfall:** A remaining `1,500 - 1,000 = 500 TP` must be reclaimed by revoking votes.
4.  **Proportional revocation:**
      * Votes revoked for SR1: `500 * (600 / 1000) = 300` votes.
      * Votes revoked for SR2: `500 * (400 / 1000) = 200` votes.
5.  **Final State:** User A successfully unstakes 1,500 TRX. Their voting state is updated to: 300 votes for SR1 and 200 votes for SR2.

> **Important Distinction: Stake 1.0 vs. Stake 2.0**
>
> Although Stake 2.0 is the current standard, TRX staked via the legacy Stake 1.0 system is still valid and can be redeemed using its corresponding `wallet/unfreezebalance` API.

**Note:** Unstaking TRX from Stake 1.0 will revoke **all** of the account's votes.

### How to Cancel All Unstaking Requests

If you initiate an unstake but change your mind, Stake 2.0 provides an efficient "cancel" feature. You can use the `cancelallunfreezev2` API to immediately cancel all pending unstake requests, bypassing the 14-day pending period and get your resources back immediately.

**Please note**: this endpoint cancels all of your account's unstaking requests that are currently in the 14-day pending period.

  * **TRX Status:** The canceled TRX is immediately re-staked.
  * **Resource Type:** The re-staked funds will acquire the same resource type (Energy or Bandwidth) as the original stake.

**Additional Effect: Automatic Withdrawal**

This operation will also automatically withdraw any unstaked fund that has already completed its 14-day pending period and is awaiting withdrawal.

**How to Verify the Result**

You can query the transaction details using `gettransactioninfobyid` and check the following fields:

  * `cancel_unfreezeV2_amount`: The total amount of TRX that was successfully canceled and re-staked.
  * `withdraw_expire_amount`: The total amount of matured unstaked TRX that was automatically withdrawn to your account balance.

### API Summary

| Description                                                   | API Endpoint                                |
| ------------------------------------------------------------- | ------------------------------------------- |
| Stake TRX.                                                    | `wallet/freezebalancev2`                    |
| Unstake TRX.                                                  | `wallet/unfreezebalancev2`                  |
| Delegate resources.                                           | `wallet/delegateresource`                   |
| Undelegate resources.                                         | `wallet/undelegateresource`                 |
| Withdraw unstaked TRX that has passed the pending period.     | `wallet/withdrawexpireunfreeze`             |
| Check the remaining number of unstake operations allowed.     | `wallet/getavailableunfreezecount`          |
| Check the amount of withdrawable unstaked TRX.                | `wallet/getcanwithdrawunfreezeamount`       |
| Check the maximum amount of delegable resources.              | `wallet/getcandelegatedmaxsize`             |
| Check resources delegated from one address to another.        | `wallet/getdelegatedresourcev2`             |
| Check an account's delegation and received delegation status. | `wallet/getdelegatedresourceaccountindexv2` |
| Check account stake, resources, unstake, and voting status.   | `wallet/getaccount`                         |
| Check resource totals, usage, and available amounts.          | `wallet/getaccountresource`                 | Cancel all pending unstake requests.                        |

[^1]:
    If a developer is unsure about a contract's stability, they should not set the user's cost share to 0%. Otherwise, if the execution is deemed malicious, all of the developer's Energy will be deducted.

[^2]:
    Therefore, it is recommended that developers set the user's share of the cost to be between 10% and 100%.
