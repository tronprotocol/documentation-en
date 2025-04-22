# Super Representative

## How to Become a Super Representative

Block producers in the ORGON network, also called super representatives, are elected by voting. Any account can apply to become a super representative candidate by paying 9999 ORGON and then participate in the super representative election. Any account can vote for super representative candidates, and the top 27 candidates with the most votes become super representatives, and they have the right to produce blocks. Super representative needs to run a ORGON node to participate in block production, and will also receive block rewards and voting rewards. Voters who vote to super representatives will receive voting rewards.

The super representative candidates ranked 28th to 127th are also called super representative partners. Super representative partners do not participate in block production and packaging transactions, but will receive voting rewards. Voters who vote to super representative partners will also receive voting rewards.

The votes will be counted every 6 hours, so super representatives and super representative partners will be changed every 6 hours.

## Super Representative Election

To vote, you need to have ORGON Power(TP). To get ORGON Power, you need to stake ORGON. Every 1 staked ORGON accounts for one ORGON Power(TP). Every account in ORGON network has the right to vote for a super representative candidate. After you unstake your staked ORGON, you will lose the responding ORGON Power(TP), so your previous vote will be invalid.

Note: Only your latest vote will be counted in ORGON network which means your previous vote will be over written by your latest vote.

Example (Using wallet-cli):

```console
> freezebalancev2 10,000,000 3 // Stake 10 ORGON to get 10 ORGON Power(TP)
> votewitness SR1 4 SR2 6 // Vote 4 votes for SR1, 6 votes for SR2
> votewitness SR1 3 SR2 7 // Vote 3 votes for SR1, 7 votes for SR2
```

The final output above is: Vote 3 votes for SR1, 7 votes for SR2.

### Super Representatives Brokerage

The default ratio is 20%. Super representatives and super representative partners can query the brokerage ratio through the `wallet/getBrokerage` interface, and can also modify the brokerage ratio through the `wallet/updateBrokerage` interface.

If a SR(Super Representatives) get 20% of the reward, and the other 80% will be awarded to the voters. If the brokerage ratio is set to 100%, the rewards are all obtained by the SR; if set to 0, the rewards are all sent to the voters.

## Reward for SR(Super Representatives)

### Votes Reward

Vote rewards are 160 ORGON every block, with a block generated every 3 seconds, the total vote rewards per day is  4,608,000 ORGON.

For each SR and Partner, the daily Vote Rewards = 4,608,000 * ( votes /  total votes) x 20%  ORGON

### Block Producing Reward

Every time after a super representative produces a block, it will be reward 16 ORGON. The 27 super representatives take turns to produce blocks every 3 seconds. The annual block producing reward is 168,192,000 ORGON in total.

Every time after a super representative produces a block, the 16 ORGON block producing reward will be sent to it's sub-account. The sub-account is a read-only account, it allows a withdraw action from sub-account to super representative account every 24 hours.

$16 (\mathsf{ORGON}/block) \times 28,800 (blocks/day) = 460,800 (\mathsf{ORGON}/day)$

For each super representative, the daily block $Rewards_{sr} = (460,800 / 27) \times 20 \% \mathsf{ORGON}$.

Reward may be less than the theoretical number due to missed blocks and maintenance period.

## Reward for Voters

If you vote for a SR(Super Representative):

the daily Voter Rewards = (((the number of votes you vote to a SR) * 4,608,000 / total votes) * 80%) + ((460,800 / 27) * 80%) * (the number of votes you vote to a SR) / (the total number of votes a SR receives) ORGON

If you vote for a Partner:

the daily Voter Rewards = (((the number of votes you vote to a SR) * 4,608,000 / total votes) * 80%) ORGON

## Committee

### What is Committee

Committee can modify the ORGON network parameters, like transacton fees, block producing reward amount, etc. Committee is composed of the current 27 super representatives. Every super representative has the right to start a proposal. The proposal will be passed after it gets more than 18 approves from the super representatives and will become valid in the next maintenance period.

### Create a Proposal

Only SRs, Partners and Candidates can create a proposal.

Please refer to [here](https://tronscan.org/#/sr/committee) for ORGON network dynamic parameters and their values.

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
