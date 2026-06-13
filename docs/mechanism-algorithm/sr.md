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
 
    When you unstake a portion of your TRX, you lose an equivalent amount of TP. The system retracts TP according to the following rules:
    
    * Unused TP is reclaimed first.
    * If the available TP is insufficient, the system automatically retracts a proportional amount from your existing votes to cover the deficit.
    * If you have voted for multiple SRs, the system will retract votes proportionally from each SR based on your voting distribution.

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

SRs and SR Partners can set a Commission Rate (also known as Brokerage Rate) to determine how rewards are distributed between themselves and their voters.

- Default Rate

    The default commission rate for a newly elected SR or SR Partner is 20%. This means that 20% of the total rewards go to the SR, and the remaining 80% is distributed to their voters in proportion to their votes.

- Customizing the Rate

    SRs and SR Partners can adjust their commission rate at any time via the [`wallet/updateBrokerage`](../api/http/witness-and-governance/updateBrokerage.md) API interface.

    - 100% Commission: All rewards go to the SR/SR Partner.
    - 0% Commission: All rewards are distributed to the voters.

### Block Production Rewards and Voting Rewards

Rewards are divided into block rewards and vote rewards. The differences are as follows:


|  | **Block Production Rewards** | **Voting Rewards** |
| :--- | :--- | :--- |
| **Total Rewards** | On-chain parameter modifiable by proposal, currently 8 TRX | On-chain parameter modifiable by proposal, currently 128 TRX |
| **Related On-chain Parameter ID** | #5 (requires activation of #30 chain parameter) | #31 (requires activation of #30 chain parameter) |
| **Related On-chain Parameter Name** | `getWitnessPayPerBlock` | `getWitness127PayPerBlock` |
| **Rewards Distribution Target** | SRs, their voters | SRs/SR partners, their voters |
| **Rewards Distribution** | **SR**: After producing each block<br><br>**Voters**: Triggered when voters initiate any of these 4 transactions:<br>- `VoteWitnessContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract`<br>- `WithdrawBalanceContract`(unlike the prior 3 transactions: rewards withdrawn to account balance immediately after distribution) | **SRs/SR partners**: After producing each block<br><br>**Voters**: Triggered when  a voter initiates any of the following 4 transactions:<br>- `VoteWitnessContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract`<br>- `WithdrawBalanceContract`(unlike the prior 3 transactions: rewards withdrawn to account balance immediately after distribution) |
| **Rewards Withdrawn to Account Balance** |Triggered when `WithdrawBalanceContract` transaction is initiated  | Triggered when `WithdrawBalanceContract` transaction is initiated|
| **Specific Rewards** | SR: <br>`8 * brokerageRate`<br><br>voter:<br> `8 * (1-brokerageRate) * (votes of this voter) / (total votes received by this SR)` | SR/SR partner:<br> `128 * brokerageRate * (votes received by this SR/SR partner) / (total votes received by all SRs & SR partners)`<br><br>voter:<br> `128 * (1-brokerageRate) * (votes of this voter) / (total votes received by all SRs & SR partners)` |


**Notes:**

- Chain parameter details can be viewed on TRONSCAN's [committee](https://tronscan.org/#/sr/committee) page.
- `brokerageRate` refers to the commission rate.
- SRs and SR Partners are the top 127 SR candidates.
- Candidates ranked beyond 127th remain SR candidates and receive neither block nor vote rewards. Likewise, their voters cannot receive block or vote rewards either.
- If a voter votes for an SR, they are eligible for both block and vote rewards (block rewards only when that SR produces a block). If a voter votes for a Partner, they are only eligible for vote rewards.
- Via the `WithdrawBalanceContract` transaction, withdrawing rewards to the account balance is subject to a 24-hour withdrawal interval limit: if less than 24 hours have passed since the last withdrawal, another withdrawal is rejected during validation.

## Committee

### About the Committee

The Committee is the highest governing body of the TRON network, responsible for modifying the network parameters (eg. transaction fees, block rewards).

- **Composition**: The Committee is composed of the current 27 active Super Representatives (SRs).
- **Powers**: Each committee member has two core powers: 

    - To create a proposal: Initiate a proposal to modify network parameters.
    - To vote on a proposal: Vote on proposals to modify network parameters (including proposals initiated by oneself).

- **Proposal Effective Mechanism**: A proposal is passed when it receives at least 18 approval votes. It will then take effect in the next maintenance period.

**Note**: The Create, Vote on, and Cancel Proposal examples below are wallet-cli client commands. For the corresponding HTTP API interfaces, see [ProposalCreate](../api/http/witness-and-governance/proposalcreate.md), [ProposalApprove](../api/http/witness-and-governance/proposalapprove.md), and [ProposalDelete](../api/http/witness-and-governance/proposaldelete.md).

### Create a Proposal

In the TRON network, all SRs, SR Partners, and SR candidates have the right to initiate proposals to modify network parameters.

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
2.  A proposal is valid for 3 days from its creation by default. This duration is the on-chain parameter `getProposalExpireTime` (#92), which can be modified by proposal (currently 3 days on mainnet). If it does not receive enough approval votes within this period, it will expire.

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

The creator of a proposal can cancel it at any time before it takes effect.

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
