# Super Representatives & Committee

## How to Become a Super Representative

In the TRON network, block producers are called Super Representatives (SRs), and they are elected by a network-wide vote. Any account can apply to become a Super Representative candidate and participate in the election by paying a fee of 9999 TRX.

Based on the final vote rankings, candidates are divided into two categories:

 - **Super Representatives (SRs)**: The top 27 candidates with the most votes. They are the core nodes of the TRON network, responsible for producing blocks and packing transactions. For this, they receive block rewards and vote rewards.
 - **Super Representative Partners (SR Partners)**: Candidates ranking from 28th to 127th. They act as backup nodes for the network, do not participate in block production, but share in the vote rewards.

Voters who cast their ballots for both Super Representatives (SRs) and Partners can receive corresponding voting rewards proportional to their votes.

The TRON network tallies votes once every 6 hours, and the roles of Super Representatives and Partners are updated accordingly in this 6-hour cycle.


## Super Representative Election

All accounts in the TRON network have the right to vote for the Super Representative candidates they support. The core of voting is TRON Power (TP), which determines the weight of your vote.

 - Obtaining Voting Power (TRON Power)
Your amount of TP is directly linked to the amount of TRX you have staked.
Calculation Method: For every 1 TRX you stake, you receive 1 TP.
 - The Impact of Unstaking on Voting
    When you unstake a portion of your TRX, you lose an equivalent amount of TP. The system reclaims TP according to the following rules:
    
    * Unused TP is reclaimed first.
    * If the available TP is insufficient, the system automatically retracts a proportional amount from your existing votes to cover the deficit.
    * If you have voted for multiple SRs, the system will retract votes proportionally from each SR based on your voting distribution.

**Important Note:**
The TRON network only records the state of your last vote. This means that every new vote you cast will completely overwrite all previous voting effects.

 + **Example:：** 

```shell
>freezebalancev2 10000000 1 # Stake 10 TRX to get 10 TP. Resource code: 0 for BANDWIDTH, 1 for ENERGY.
>votewitness SR1 4 SR2 6 # Cast 4 votes for SR1 and 6 votes for SR2.
>votewitness SR1 3 SR2 7 # Cast 3 votes for SR1 and 7 votes for SR2.
```
The final result of the commands above is 3 votes for SR1 and 7 votes for SR2.

## Rewards

### Brokerage of SRs and SR partners

Super Representatives (SRs) and Super Representative Partners can set a Commission Rate (also known as Brokerage Rate) to determine how rewards are distributed between themselves and their voters.

- Default Rate
The default commission rate for a newly elected SR or Partner is 20%. This means that 20% of the total rewards go to the SR, and the remaining 80% is distributed to their voters in proportion to their votes.
- Customizing the Rate
SRs and Partners can adjust their commission rate at any time via the wallet/updateBrokerage API interface.
  - 100% Commission: All rewards go to the SR/Partner.
  - 0% Commission: All rewards are distributed to the voters.

### Block Production Rewards and Voting Rewards

Rewards are divided into block rewards and vote rewards. The differences are as follows:


|  | **Block Production Rewards** | **Voting Rewards** |
| :--- | :--- | :--- |
| **Total Rewards** | On-chain parameter modifiable by proposal, currently 8 TRX | On-chain parameter modifiable by proposal, currently 128 TRX |
| **Related On-chain Parameter ID** | #5 (requires activation of #30 chain parameter) | #31 (requires activation of #30 chain parameter) |
| **Related On-chain Parameter Name** | `getWitnessPayPerBlock` | `getWitness127PayPerBlock` |
| **Rewards Distribution Target** | SRs, their voters | SRs/SR partners, their voters |
| **Rewards Distribution Time** | **SR**:<br> After producing each block<br><br>**Voters**:<br> Triggered when voters initiate any of these 4 transactions:<br>- `VoteWitnessContract`<br>- `WithdrawBalanceContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract` | **SRs/SR partners**: <br>After producing each block<br><br>**Voters**: <br>Triggered when voters initiate any of these 4 transactions:<br>- `VoteWitnessContract`<br>- `WithdrawBalanceContract`<br>- `UnfreezeBalanceContract`<br>- `UnfreezeBalanceV2Contract` |
| **Specific Rewards** | SR: <br>`8 * brokerageRate`<br><br>voter:<br> `8 * (1-brokerageRate) * (votes of this voter) / (total votes received by this SR)` | SR/SR partner:<br> `128 * brokerageRate * (votes received by this SR/SR partner) / (total votes received by all SRs & SR partners)`<br><br>voter:<br> `128 * (1-brokerageRate) * (votes of this voter) / (total votes received by all SRs & SR partners)` |


**Notes:**
 - Chain parameter details can be viewed on TRONSCAN's committee page.
 - `brokerageRate` refers to the commission rate.
 - Super Representatives and Partners are the top 127 witnesses.
 - If a voter votes for an SR, they are eligible for both block and vote rewards (block rewards only when that SR produces a block). If a voter votes for a Partner, they are only eligible for vote rewards.

## Committee

### What is Committee

The Committee is the highest governing body of the TRON network, responsible for modifying the network's core dynamic parameters (such as transaction fees, block rewards, etc.).
 - Composition: The Committee is composed of the current 27 active Super Representatives (SRs).
 - Powers: Each committee member has two core powers: 
   - To create a proposal.
   - To vote on a proposal.
 - Effective Mechanism: A proposal is passed when it receives at least 18 approval votes. It will then take effect in the next maintenance period.

### Create a Proposal

In the TRON network, all Super Representatives, Partners, and candidates have the right to initiate proposals to modify network parameters.

Please refer to [here](https://tronscan.org/#/sr/committee) for TRON network dynamic parameters and their values.

+ Example:

```shell
>createproposal id0 value0 ... idN valueN
# id0_N: Parameter number
# value0_N: New parameter value
```

### Vote for a Proposal

The voting process for proposals follows these core rules:
1.  The governance system only supports approval votes. Not voting is equivalent to disapproving.
2.  A proposal is valid for 3 days from its creation. If it does not receive enough approval votes within this period, it will expire.

+ Example:

```shell
>approveProposal id is_or_not_add_approval
# id: proposal id
# is_or_not_add_approval: YES vote or cancel YES vote
```

### Cancel Proposal

The creator of a proposal can cancel it at any time before it takes effect.
+ Example:
```shell
>deleteProposal proposalId
# id: proposal id
```

### Query Proposal

Proposals can be queried using the following API interfaces:
+ Query all the proposals list ([ListProposals](https://tronprotocol.github.io/documentation-en/api/http/#walletlistproposals))
+ Query all the proposals list by pagination ([GetPaginatedProposalList](https://tronprotocol.github.io/documentation-en/api/http/#walletgetpaginatedproposallist))
+ Query a proposal by proposal id ([GetProposalById](https://tronprotocol.github.io/documentation-en/api/http/#walletgetproposalbyid))