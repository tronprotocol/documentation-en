
# Network Governance

The governance of the TRON network is primarily achieved by modifying [network parameters](https://tronscan.org/#/sr/committee), a process also known as **network upgrade**.  
Anyone can propose changes to network parameters within the community, but only **Super Representatives (SR)** or **Super Representative Partners** can formally submit voting requests on-chain. During the voting period, the 27 Super Representatives will vote on the proposal. When the voting deadline is reached and the required number of supporting votes is met, the proposal automatically takes effect.

You can view the history of completed proposals and voting records [here](https://github.com/tronprotocol/tips/tree/master/proposal).

---

## Proposal Voting Process

1. [Initiate Proposal Discussion](#initiate-proposal-discussion)  
2. [Community Discussion](#community-discussion)  
3. [Submit Voting Request](#submit-voting-request)  
4. [Voting and Implementation](#voting-and-implementation)  

---

## Initiate Proposal Discussion

Any TRON network participant can initiate a discussion for a TIP vote.  
Please create an **Issue** in the [TIP repository](https://github.com/tronprotocol/tips/issues), providing detailed information about the proposal, including:

- Proposal motivation  
- Network parameters to be modified and their values  
- Technical specifications  
- Expected impact of the changes  

New proposal discussions can refer to this [example](https://github.com/tronprotocol/tips/issues/789).

### Specification Requirements

#### Title
To facilitate dissemination and community participation, it is recommended to give the proposal a concise and clear name, placed at the beginning of the title, for example:

```
Proposal: Change the unit price of Energy to 100 sun
```

#### Body Content
The Issue body should include the following main sections:

```
## Simple Summary
Briefly describe the TRON network parameters to be modified and their values, along with a summary of the expected impact.

## Motivation
Describe the motivation for the proposal, including the current issues and why certain network parameters need to be modified.

## Timeline
Specify the date for initiating the proposal vote and the estimated time for the proposal to take effect.
Generally, after an Issue is raised, about two weeks are allocated for community discussion, so the formal voting request should be initiated after two weeks.

## How to Initialize the Voting Request
Clearly specify the command to initiate the proposal voting request on-chain.

## Technical Specification / Background
Provide a detailed description of the technical specifications or background information for the proposal.
```

## Community Discussion

After the TIP discussion is initiated, the proposer should actively encourage community users to participate in the discussion, collect opinions and feedback, and make appropriate revisions and updates to the proposal based on the discussion results.

## Submit Voting Request

Typically, two weeks after the proposal is initiated, if the community has fully discussed and reached a basic consensus, a **Super Representative** or **Super Representative Partner** will formally submit the voting request on-chain.

## Voting and Implementation

- The on-chain voting period lasts for **3 days**.  
- During this period, all 27 Super Representatives can vote on the TIP.  
- After the voting deadline, if the number of supporting votes is **greater than or equal to 18**, the proposal is considered passed and automatically takes effect.
