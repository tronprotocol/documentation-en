# TRON DPoS Consensus Mechanism

## Overview

As a distributed ledger system, a blockchain boasts thousands, even tens of thousands, of independent nodes globally, each maintaining an identical copy of the ledger. To record new transaction data onto this shared ledger, universal agreement from these nodes is essential. Achieving this in an inherently untrustworthy distributed environment is a complex engineering challenge.

A blockchain system functions correctly (i.e., all nodes can consistently maintain a coherent ledger) provided that the vast majority of nodes in the system are honest and reliable. To ensure that honest nodes can collectively oversee the recording of transaction data, every blockchain system needs to establish its own **consensus mechanism**. 

The consensus mechanism acts like the blockchain's "constitution," guaranteeing that even in an untrustworthy distributed environment, as long as the majority of nodes adhere to the consensus rules, the system can achieve deterministic and trustworthy results. Therefore, the significance of a consensus mechanism lies in its ability to enable honest nodes within the blockchain to ultimately agree on the ledger's content.

Currently, mainstream consensus mechanisms include Proof of Work (PoW), Proof of Stake (PoS), and Delegated Proof of Stake (DPoS), and each mechanism has its unique specific implementation in different blockchain systems. This document will focus on the DPoS consensus mechanism adopted by the **TRON network** and elaborate on its core components and operational principles.

### DPoS Consensus Mechanism

The core role of the DPoS consensus mechanism in a blockchain system is to elect **Super Representatives (SRs)**, which are the designated Block Producers for the network. These SRs are responsible for validating transaction data and recording it onto the ledger, subsequently broadcasting the new block containing the new entries to the entire network, and gaining recognition from other nodes.

In DPoS consensus, the system selects a subset of nodes as SRs based on the number of votes they receive. The election process is as follows:

1. **Initial Setup:** When the blockchain system launches, a certain amount of **tokens** (e.g., TRON's TRX) are issued.
2. **Becoming a Candidate:** Nodes can spend a portion of these tokens to apply to become a SR **candidate**.
3. **Community Voting:** Any node in the network holding tokens can vote for these candidates.
4. **Vote Tallying and Election:** After a preset **time period** (e.g., `t`), the system tallies the votes for all candidates, and the top `N` candidates by vote count become the SRs for the next time period.
5. **Cycle Rotation:** After the time period ends, the system re-tallies votes and elects new SRs, and so on.

The following will provide a detailed explanation, integrating the specific implementation within the TRON network.

## Core Concept Definitions

| Concept | Definition |
| -------- | -------- |
| TRON     | The TRON blockchain network. This document does not distinguish between TRON, TRON blockchain, TRON blockchain system, etc.|
|TRX| The equity token issued and circulated within the TRON blockchain system, with the ticker symbol **TRX**.|
|Super Representative (SR) |A node in the TRON network that has obtained block production qualifications. TRON sets the number of SRs at **27**. This document does not distinguish between block producer, Witness, SuperNode, SR, etc.|
|Super Representative Candidate| A node in the TRON network that is eligible to become an SR.|
|Super Representative Partner (SRP)| SR candidates ranked from **28th** to **127th** by vote count. They do not participate in block production or transaction packaging but can receive voting rewards. Voters who vote for SRPs will also receive voting rewards.|
|Block Production / Producing Blocks|The process of validating transactions and recording them as entries. Since entries in TRON are carried by blocks, the block production process is also referred to as "producing blocks." This document does not distinguish between block production and producing blocks.|
|Block Production Order (Block Generation Order)|The 27 SRs are ranked from highest to lowest by vote count, which determines their block production order.|
|Slot|In the TRON network, every **3 seconds** is counted as a slot. Under normal circumstances, each SR producing a block will complete block generation within its corresponding slot time. Therefore, TRON's average block generation interval is approximately 3 seconds. If an SR fails to produce a block for some reason, the corresponding slot will be empty, and the next SR will produce a block in the subsequent slot. During maintenance periods, block production skips 2 slots.|
|Epoch|TRON defines every **6 hours** as an epoch. The last two block generation times in each epoch are **maintenance periods**. The maintenance period of each epoch will determine the block generation order for the next epoch.|
|Maintenance Period|TRON sets this at **2 block times**, which is **6 seconds**. This period is used to tally the votes for candidates. Since there are 4 epochs in 24 hours, there are naturally 4 maintenance periods. No blocks are produced during the maintenance period; its primary purpose is to determine the block production order for the next epoch.|

![Epoch](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/sequence_en.jpg)

## Block Production Process

SRs in the TRON blockchain system continuously execute the following process:

1. **Collect Transactions:** SRs collect newly generated transactions from the blockchain network.
2. **Validate Transactions:** The legitimacy of these transactions is verified.
3. **Package Blocks:** Validated transactions are packaged into a **block** in order to record them as a new page of entries to the ledger.
4. **Broadcast Blocks:** The newly generated block is broadcast throughout the entire blockchain network.
5. **Other Node Verification:** Upon receiving the new block, other nodes also verify the legitimacy of the transaction data within it and add it to their own ledgers.

SRs continuously repeat this process to ensure that all new transaction data in the TRON system is promptly recorded onto the ledger.

## Super Representative Election Mechanism

### Votes

Before voting for SRs, an account needs to acquire **voting power**, specifically **TRON Power (TP)**. Voting power is obtained by **staking TRX**. In addition to obtaining Bandwidth or Energy, staking TRX simultaneously grants users voting power. For every **1 TRX** staked, a user receives **1 TP**.

When an account unstakes TRX, it loses the corresponding amount of TP, and its current votes become invalid. Votes are tallied every **6 hours**, and SRs and SRPs are also updated every 6 hours. If an account casts multiple votes before the vote tally, the TRON network will only record the account's **latest vote**, and previous votes will be overwritten.

### Voting Process

In TRON, voting for candidates is defined as a special type of **transaction**. Nodes can vote for candidates by generating a voting transaction.

### Tallying Votes

During each **maintenance period**, the system tallies the votes for all candidates and selects the **27** candidates with the most votes to be the SRs for the next block production cycle.

## Block Production Mechanism

In an **epoch**, the 27 SRs will produce blocks sequentially according to their **block production order**. Each SR can only produce blocks when it is their turn.

SRs package multiple valid transaction data into each block. At the same time, each block fills in the **hash value** (`hash`) of the previous block as its **parent hash value** (`parentHash`). Furthermore, the SR uses their private key to sign the current block's data, and the **signature result** (`witness_signature`), along with the SR's address, block height, block generation time, and other data, are also filled into the block.

In this way, each block stores the hash value of the previous block, thereby logically linking the blocks together and ultimately forming the blockchain's chain structure. A typical blockchain structure diagram is as follows:

![blockchain_structure](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/blockchain_structure.png)

Ideally, in a blockchain system adopting DPoS consensus, the block production process should strictly follow a pre-calculated block production order, with SRs taking turns to produce blocks sequentially (as shown in Figure a below). However, a real blockchain network is a distributed, untrustworthy, and complex system, and the following situations may occur:

1. **Network Latency:** Due to poor network link conditions, a block produced by an SR might not be received by other SRs within the effective time (as shown in Figures b1, b2 below).
2. **Node Failure:** Some SRs may not always operate normally (as shown in Figure c).
3. **Malicious Behavior:** A few SRs might maliciously produce fork blocks, attempting to split the main chain (as shown in Figure d).

![longest_chain1](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/longest_chain1_en.jpg)
![longest_chain2](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/longest_chain2_en.jpg)

As mentioned earlier, the normal operation of a blockchain system is predicated on the vast majority of nodes in the system being honest and reliable. To further delve into this issue, the primary guarantee for blockchain system security is ledger security: the ledger cannot be maliciously written with illegal data, and the copies of the ledger stored on various nodes should remain consistent. From the perspective of DPoS consensus, the block production process is completed by SRs, so TRON's security depends on the reliability of the majority of SRs.

TRON has established an **irreversible block** (or **solidified block**) mechanism, and to resist malicious behavior from a few block-producing nodes, TRON adopts the **longest chain principle** to confirm the main chain.

### Solidified Block Principle

Newly produced blocks initially remain in an unconfirmed state. When a block is acknowledged by at least **70%** (i.e., $27 \times 70\% \approx 19$ (rounded up) SRs), that block is considered an **irreversible block**, commonly referred to as a **solidified block**. At this point, the transactions contained within the solidified block have been confirmed by the entire blockchain network.

The "acknowledgment" of an unconfirmed block here occurs when other SRs produce subsequent blocks after that block. For example, as shown in Figure d, when SR C produces block 103, SR E produces block 104' based on block 103, and SR G, A, and B produce blocks 105', 106', and 107' respectively. These are essentially subsequent blocks to block 103, and therefore, they signify acknowledgment of block 103 produced by C.

Thus, when block 121 is produced, block 103 becomes a solidified block because it now has 19 subsequent blocks. It's important to emphasize that the SRs who produced these 19 blocks must be **different from each other** and **different** from the SR who produced block 103.

### Longest Chain Principle

When a blockchain forks, honest SRs will always choose to continue producing blocks on the currently **longest** fork chain.

## Incentive Model

To ensure the secure and efficient operation of the TRON blockchain system, TRON has designed an incentive model to encourage more nodes to join the TRON network, thereby expanding network scale.

* **Block Production Rewards:** For every block successfully produced in the TRON network, the corresponding SR is rewarded with **8 TRX**. After deducting their commission based on a self-defined commission rate, this SR distributes the remaining portion to the voters who supported them, based on their voting weight.
* **Voting Rewards:** With the generation of each block, the TRON network also awards an additional **128 TRX** to all SRs and SRPs. This reward is distributed based on their respective vote proportions. Similarly, after deducting their commission based on their set commission rate, SRs and SRPs distribute the remaining voting rewards to their respective voters based on the voters' voting weight.

## Proposal-Based Parameter Adjustment

An important feature of DPoS is that any system parameter adjustment can be initiated through an **on-chain proposal**. SRs decide whether a proposal takes effect by voting on it. The benefit of this mechanism is that **no hard fork upgrade is required** when adjusting parameters on-chain.

For current dynamic parameters and their values in the TRON network, as well as past proposal records, please refer to the [TRONSCAN Committee Page](https://tronscan.org/#/sr/committee).

## References

* [The Basics of TRON’s DPoS Consensus Algorithm](https://medium.com/tronnetwork/the-basics-of-trons-dpos-consensus-algorithm-db12c52f1e03)