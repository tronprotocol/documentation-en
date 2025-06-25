# Super Representative

## How to Become a Super Representative

Block producers in the TRON network, also called super representatives, are elected by voting. Any account can apply to become a super representative candidate by paying 9999 TRX and then participate in the super representative election. Any account can vote for super representative candidates, and the top 27 candidates with the most votes become super representatives, and they have the right to produce blocks. Super representative needs to run a TRON node to participate in block production, and will also receive block rewards and voting rewards. Voters who vote to super representatives will receive voting rewards.

The super representative candidates ranked 28th to 127th are also called super representative partners. Super representative partners do not participate in block production and packaging transactions, but will receive voting rewards. Voters who vote to super representative partners will also receive voting rewards.

The votes will be counted every 6 hours, so super representatives and super representative partners will be changed every 6 hours.

## Super Representative Election

To vote, you need to have TRON Power(TP). To get TRON Power, you need to stake TRX. Every 1 staked TRX accounts for one TRON Power(TP). Every account in TRON network has the right to vote for a super representative candidate. After you unstake your staked TRX, you will lose the corresponding TRON Power(TP), so your previous vote will be invalid.

Note: Only your latest vote will be counted in TRON network which means your previous vote will be over written by your latest vote.

Example (Using wallet-cli):

```console
> freezebalancev2 10,000,000 3 // Stake 10 TRX to get 10 TRON Power(TP)
> votewitness SR1 4 SR2 6 // Vote 4 votes for SR1, 6 votes for SR2
> votewitness SR1 3 SR2 7 // Vote 3 votes for SR1, 7 votes for SR2
```

The final output above is: Vote 3 votes for SR1, 7 votes for SR2.

## Rewards 
### Brokerage of SRs and SR partners

The default ratio is 20%. Super representatives and super representative partners can query the brokerage ratio through the `wallet/getBrokerage` interface, and can also modify the brokerage ratio through the `wallet/updateBrokerage` interface.

If a SR(Super Representatives) get 20% of the rewards, and the other 80% will be awarded to the voters. If the brokerage ratio is set to 100%, the rewards are all obtained by the SR; if set to 0, the rewards are all sent to the voters.

### Block Production Rewards and Voting Rewards
Rewards are categorized into block production rewards and voting rewards, with their differences outlined as follows:

|  | **Block Production Rewards** | **Voting Rewards** |
| :--- | :--- | :--- |
| **Total Rewards** | On-chain parameter modifiable by proposal, currently 8 TRX | On-chain parameter modifiable by proposal, currently 128 TRX |
| **Related On-chain Parameter ID** | #5 (requires activation of #30 chain parameter) | #31 (requires activation of #30 chain parameter) |
| **Related On-chain Parameter Name** | getWitnessPayPerBlock | getWitness127PayPerBlock |
| **Rewards Distribution Target** | SR, its voters | SRs/SR partners, their voters |
| **Rewards Distribution Time** | SR: After producing each block<br>Voters: Triggered when voters initiate any of these 4 transactions:<br>- VoteWitnessContract<br>- WithdrawBalanceContract<br>- UnfreezeBalanceContract<br>- UnfreezeBalanceV2Contract | SRs/SR partners: After producing each block<br>Voters: Triggered when voters initiate any of these 4 transactions:<br>- VoteWitnessContract<br>- WithdrawBalanceContract<br>- UnfreezeBalanceContract<br>- UnfreezeBalanceV2Contract |
| **Specific Rewards** | SR: 8 * brokerageRate<br>voter: 8 * (1-brokerageRate) * (votes of this voter) / (total votes received by this SR) | SR/SR partner: 128 * brokerageRate * (votes received by this SR/SR partner) / (total votes received by all SRs & SR partners)<br>voter: 128 * (1-brokerageRate) * (votes of this voter) / (total votes received by all SRs & SR partners) |

**Notices**:

- on-chain parameter's ID and name can be seen [here](https://tronscan.org/#/sr/committee)
- SRs and SR partners: Top 127 witnesses
- Voters for SRs receive both block production and voting rewards, but block production rewards are only earned when the SR they voted for is scheduled to produce block. Voters for SR partners only receive voting rewards.


## Committee

### What is Committee

Committee can modify the TRON network parameters, like transacton fees, block producing reward amount, etc. Committee is composed of the current 27 super representatives. Every SR has the right to create and vote a proposal. The proposal will be passed after it gets at least 18 approves from the super representatives and will become valid in the next maintenance period.

### Create a Proposal

In addition to SR, SR Partner and SR Candidate also have the right to create a proposal, and only they have this right.

Please refer to [here](https://tronscan.org/#/sr/committee) for TRON network dynamic parameters and their values.

Example (Using wallet-cli):

```console
> createproposal id value
# id: the serial number
# value: the parameter value
```


### Vote for a Proposal

Proposal only support YES vote. Since the creation time of the proposal, the proposal is valid within 3 days. If the proposal does not receive enough YES votes within the period of validity, the proposal will be invalid beyond the period of validity. Yes vote can be cancelled.

Example (Using wallet-cli):

```console
> approveProposal id is_or_not_add_approval
# id: proposal id
# is_or_not_add_approval: YES vote or cancel YES vote
```

### Cancel Proposal

Proposal creator can cancel the proposal before it is passed.

Example (Using wallet-cli):

```console
> deleteProposal id
# id: proposal id
```

### Query Proposal

- Query all the proposals list (ListProposals)
- Query all the proposals list by pagination (GetPaginatedProposalList)
- Query a proposal by proposal id (GetProposalById)

For more API detail, please refer to [HTTP API](../api/http.md).
