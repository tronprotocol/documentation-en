# Governance

The governance of the TRON network is accomplished by modifying [the network parameters](https://tronscan.org/#/sr/committee). The modification of network parameters is also called a network upgrade. Anyone can propose a discussion on modifying one or several network parameters, however, only super representatives or super representative partners can submit voting requests on-chain. Before the voting deadline, 27 super representatives can vote on the proposal. After the voting deadline arrives and the number of votes meets the requirement, the proposal will take effect.

You can view the list of the past completed proposals [here](https://github.com/tronprotocol/tips/tree/master/proposal).

Please according to the following process to propose a voting request:

1. [Initiate a discussion on proposal](#initiate-a-discussion-on-a-proposal)
2. [Community discussion](#community-discussion)
3. [Initiate a voting request](#initiate-a-voting-request)
4. [Voting and taking effective](#vote-and-take-effect)

## Initiate a discussion on a proposal
Any TRON network participant can initiate a discussion on a proposal. Please create a proposal discussion issue in [TIP repository](https://github.com/tronprotocol/tips/issues). The Issue is used to introduce the proposal in detail, including the motivation of this proposal, the TRON network parameters to be modified and their values, technical specifications, and the impact of the modification, etc. for a new proposal, please refer to this [example](https://github.com/tronprotocol/tips/issues/232) to create an issue for discussion.

Below are the specifications of how to write an issue for proposal discussion.

### Title
We hope that all users of the TRON ecosystem can participate in network governance. In order to be able to better publicize in the community, it is recommended to name the proposal and put the name at the beginning of the title. Here is an example:

```
Palma Upgrade: proposal to change the unit price of energy to 210 sun
```

### Body
In the issue body, the content of the proposal should be introduced in detail, including motivation, estimated time to initiate the proposal vote and effective time of the proposal, how to initiate a proposal vote, technical specifications or background information of the proposal, etc.

```
# Simple Summary
Briefly introduce the parameters to be modified by this proposal and their values, and summarize the issue it wants to solve

# Motivation
Describe the motivation for the proposal, what is the problem encountered now, that is, why one or some dynamic parameters need to be modified.

# Timeline
Indicate when to initiate the proposal voting request, and the estimated effective date of the proposal. After the issue is proposed, two weeks are generally reserved for community discussion. Therefore, the proposal initiation time set in the Issue should be two weeks after the issue is proposed.

# How to Initialize the Voting Request
Indicates the command to initiate the proposal voting request.

# Technical Specification / Background
The specific technical specifications or background information of the proposal
```

## Community discussion
After the proposal issue is initiated, the initiator of the issue should try his best to promote it in the community, attract community users to participate in the discussion on the proposal, and update the proposal according to the results of the discussion.

## Initiate a voting request
Generally, the initiation time of the voting request set in the proposal is two weeks after the proposed issue is initiated. When the community has already fully discussed on the proposal and formed a community consensus, the super representative or super representative partner will initiate a voting request on the chain.

## Vote and take effect
The validity period of the voting request initiated on-chain is 3 days. During the validity period, all 27 super representatives can vote for the proposal. When the voting deadline is reached, if the number of votes obtained is equal to or greater than 18 votes, the proposal will take effect.

