# Super Representatives & Committee

## How to Become a Super Representative

In the TRON network, block producers are called Super Representatives (SRs), and they are elected by a network-wide vote. Any account can apply to become a Super Representative candidate by paying a one-time fee of 9999 TRX, and any TRX holder can vote for SR candidates.

An application to become a candidate can be initiated via the `CreateWitness` command in the wallet-cli client, and requires submitting a URL (used to publish information such as the candidate's homepage).

Based on the final vote rankings, the top 127 candidates take on one of two roles:

- **Super Representatives (SRs)**: The top 27 candidates with the most votes. They are the core nodes of the TRON network, responsible for producing blocks and packing transactions. For this, they receive block rewards and vote rewards.
- **Super Representative Partners (SR Partners)**: Candidates ranking from 28th to 127th. They act as backup nodes for the network, do not participate in block production, but share in the vote rewards.

The TRON network tallies votes once every 6 hours, and the roles of Super Representatives and Partners are updated accordingly in this 6-hour cycle.


## Super Representative Election

All accounts in the TRON network have the right to vote for the Super Representative candidates they support. The core of voting is TRON Power (TP), which determines the weight of your vote.

- Obtaining Voting Power (TRON Power)

    Your amount of TP is directly linked to the amount of TRX you have staked. Calculation Method: For every 1 TRX you stake, you receive 1 TP.

- The Impact of Unstaking on Voting
 
    Under the current mainnet resource model, unstaking TRX reduces your TP. The effect on existing votes depends on the staking version.

    For **Stake 2.0** (`UnfreezeBalanceV2Contract`):

    * If you still have enough TP for all your existing votes, those votes remain unchanged.
    * Otherwise, the system reduces your votes for each candidate in proportion to your remaining TP, rounding each result down to a whole number. This can leave some TP unused.
    * For example, if you have 10 TP and have cast 4 votes for one candidate and 6 for another, unstaking 1 TRX leaves 9 TP and reduces those votes to 3 and 5, respectively.

    For **Stake 1.0** (`UnfreezeBalanceContract`), unstaking clears all your existing votes, even if you still have enough TP for some or all of them. You must vote again using your remaining TP.

**Important Note:**
The TRON network only records the state of your last vote. This means that every new vote you cast will completely overwrite all previous voting effects.

**Example:**

```text
>freezebalancev2 10000000 1 # Stake 10 TRX (the amount is in sun; 1 TRX = 1,000,000 sun, so 10 TRX = 10000000 sun) to get 10 TP. Resource code: 0 for BANDWIDTH, 1 for ENERGY.
>votewitness SR1 4 SR2 6 # Cast 4 votes for SR1 and 6 votes for SR2.
>votewitness SR1 3 SR2 7 # Cast 3 votes for SR1 and 7 votes for SR2.
```

The final result of the commands above is 3 votes for SR1 and 7 votes for SR2.

## Rewards

### Brokerage of SRs and SR Partners

SR candidates can set a Commission Rate (also known as Brokerage Rate) to determine how their rewards are distributed between themselves and their voters.

- Default Rate

    If no commission rate has been set, the default is 20%. This means that 20% of the total rewards go to the SR/SR Partner, and the remaining 80% is distributed to their voters in proportion to their votes. Becoming an SR or SR Partner does not change a rate you have already set.

- Customizing the Rate

    Any SR candidate, including those outside the top 127, can change their commission rate at any time using the [`wallet/updateBrokerage`](../api/http/witness-and-governance/updateBrokerage.md) API. Changes take effect from the next epoch. Until then, rewards use the current epoch's rate.

    - 100% Commission: All rewards go to the SR/SR Partner.
    - 0% Commission: All rewards are distributed to the voters.

### Block Production Rewards and Voting Rewards

Rewards are divided into block rewards and voting rewards. The table below describes their distribution when chain parameter #30 (`getChangeDelegation`) is enabled. This parameter is currently enabled on mainnet.

Allowance is a separate reward balance that must be withdrawn before it can be spent.

|  | **Block Production Rewards** | **Voting Rewards** |
| :--- | :--- | :--- |
| **Total Rewards** | On-chain parameter modifiable by proposal, currently 8 TRX | On-chain parameter modifiable by proposal, currently 128 TRX |
| **Related On-chain Parameter ID** | #5 | #31 |
| **Related On-chain Parameter Name** | `getWitnessPayPerBlock` | `getWitness127PayPerBlock` |
| **Rewards Distribution Target** | SRs, their voters | SRs/SR partners, their voters |
| **Rewards Distribution** | **SR**: Rewards are added to allowance after producing a block.<br><br>**Voters**: Rewards from completed epochs are calculated and added to allowance when any of these transactions is executed:<br>- `VoteWitnessContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract`<br>- `WithdrawBalanceContract` (also transfers allowance to the account balance) | **SRs/SR partners**: Rewards are added to allowance after each block is produced.<br><br>**Voters**: Rewards from completed epochs are calculated and added to allowance when any of these transactions is executed:<br>- `VoteWitnessContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract`<br>- `WithdrawBalanceContract` (also transfers allowance to the account balance) |
| **Rewards Withdrawn to Account Balance** |Triggered when `WithdrawBalanceContract` transaction is initiated  | Triggered when `WithdrawBalanceContract` transaction is initiated|
| **Specific Rewards** | SR: <br>`8 * brokerageRate`<br><br>voter:<br> `8 * (1-brokerageRate) * (votes cast by this voter for this SR) / (total votes received by this SR)` | SR/SR partner:<br> `128 * brokerageRate * (votes received by this SR/SR partner) / (total votes received by all SRs & SR partners)`<br><br>voter:<br> `128 * (1-brokerageRate) * (votes cast by this voter for this SR/SR partner) / (total votes received by all SRs & SR partners)` |


**Notes:**

- Chain parameter details can be viewed on TRONSCAN's [committee](https://tronscan.org/#/sr/committee) page.
- `brokerageRate` refers to the commission rate.
- SRs and SR Partners are the top 127 SR candidates.
- Candidates ranked beyond 127th remain SR candidates and receive neither block nor vote rewards. Likewise, their voters cannot receive block or vote rewards either.
- If a voter votes for an SR, they are eligible for both block and vote rewards (block rewards only when that SR produces a block). If a voter votes for a Partner, they are only eligible for vote rewards.
- Voter rewards from the current epoch cannot be added to allowance or withdrawn until that epoch ends. `WithdrawBalanceContract` collects any unclaimed rewards from completed epochs into allowance, then transfers the full allowance to the spendable account balance.
- Via the `WithdrawBalanceContract` transaction, withdrawing rewards to the account balance is subject to a 24-hour withdrawal interval limit: if less than 24 hours have passed since the last withdrawal, another withdrawal is rejected during validation.

## Committee

### About the Committee

The Committee is the highest governing body of the TRON network, responsible for modifying the network parameters (eg. transaction fees, block rewards).

- **Composition**: The Committee consists of the top 27 candidates by vote count, known as Super Representatives (SRs).
- **Powers**: Each committee member has two core powers: 

    - To create a proposal: Initiate a proposal to modify network parameters.
    - To vote on a proposal: Vote on proposals to modify network parameters (including proposals initiated by oneself).

- **Proposal Effective Mechanism**: A proposal that has not been canceled is evaluated at the first maintenance at or after its expiration time. Only approvals from the SRs who ranked in the top 27 by votes in the most recent election count. If at least 18 of those SRs approve, the proposal passes and its parameter changes take effect. Receiving enough approvals earlier does not make it take effect sooner.

**Note**: The Create, Vote on, and Cancel Proposal examples below are wallet-cli client commands. For the corresponding HTTP API interfaces, see [ProposalCreate](../api/http/witness-and-governance/proposalcreate.md), [ProposalApprove](../api/http/witness-and-governance/proposalapprove.md), and [ProposalDelete](../api/http/witness-and-governance/proposaldelete.md).

### Create a Proposal

In the TRON network, all SRs, SR Partners, and SR candidates have the right to initiate proposals to modify network parameters.

A new proposal cannot be created until the existing proposal expires.

Please refer to [here](https://tronscan.org/#/sr/committee) for TRON network parameters and their values.

**Example**:

```text
>createproposal parameter0 value0 ... parameterN valueN
# parameter0_N: the network parameter number to modify (not the proposal id)
# value0_N: the new value for that parameter
```

**Note**: A single proposal can modify several network parameters at once by supplying multiple `parameter value` pairs.

### Vote on a Proposal

The voting process for proposals follows these core rules:

1.  The governance system only supports approval votes. Not voting is equivalent to disapproving.
2.  The on-chain parameter `getProposalExpireTime` (#92) sets the base duration for calculating when a proposal expires. It is currently 3 days on mainnet and can be changed by proposal. The expiration time is adjusted to fall at a later scheduled maintenance time. With the current 3-day base duration and 6-hour maintenance interval, a proposal expires more than 3 days and no later than 3 days and 6 hours after creation. Here, creation time refers to the proposal's recorded `create_time`, which is the timestamp of the parent block of the block containing the proposal creation transaction.
3.  Once a proposal expires, approvals can no longer be added or removed. At the first maintenance at or after a proposal's expiration time, the proposal is marked `DISAPPROVED` if it has not been canceled and has fewer than 18 approvals from the SRs who ranked in the top 27 by votes in the most recent election.

**Example**:

```text
>approveProposal id is_or_not_add_approval
# id: proposal id
# is_or_not_add_approval: true to add an approval (vote YES), false to cancel a previous approval
```

**Note**: The following two cases are rejected during validation:

- Passing `true` when you have already approved the proposal (you cannot approve the same proposal twice).
- Passing `false` when you have not approved the proposal before (there is no approval to cancel).

### Cancel Proposal

The creator can cancel a proposal only before it expires, as long as it has not already been canceled.

**Example**:

```text
>deleteProposal proposalId
# id: proposal id
```

### Querying Proposals

Proposals can be queried using the following API interfaces:

+ Query all the proposals list ([ListProposals](../api/http/witness-and-governance/listproposals.md))
+ Query all the proposals list by pagination ([GetPaginatedProposalList](../api/http/witness-and-governance/getpaginatedproposallist.md))
+ Query a proposal by proposal id ([GetProposalById](../api/http/witness-and-governance/getproposalbyid.md))
