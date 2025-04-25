# DPoS

## Overview
Blockchain is a distributed accounting system. In a blockchain system, there can be thousands of nodes, each of which independently stores the same ledger. If new transaction data is to be written into the ledger,  approvals from these nodes are needed. Achieving this goal in an untrusted distributed environment is a complicated systematic quest. The blockchain system operates normally means each node in the blockchain can always keep the same ledger, provided that most nodes in the system are honest and reliable. In order to ensure that honest and reliable nodes can jointly supervise the transaction data written into the ledgers, each blockchain system needs to build its own consensus, which is equivalent to the constitution of the blockchain. As long as the vast majority of nodes comply with the consensus requirements, it is able to guarantee the results will certainly be credible, even in an untrusted distributed environment. Therefore, the significance of the consensus is that the honest nodes in the blockchain can ultimately achieve the agreement of the ledgers as long as they strictly abide by this consensus.

There are several types of consensus, and the most commonly used are POW, POS, and DPoS. Definitely, different blockchain systems will have a unique way of implementation. This article will mainly introduce the DPoS consensus on which TRON based. We will also explain the basic components and mechanisms of DPoS.

The role of consensus is to select SRs(Super Representatives) in the blockchain system. SRs(Super Representatives) verify the transaction data and keep it in a leger, then broadcast the leger to other nodes in the network and obtain the approval of the leger from other nodes. As a specific implementation of consensus, DPoS works in the following way:

The DPoS consensus selects some nodes as SRs(Super Representatives) in the blockchain system based on the number of votes they obtain. First, when the blockchain system starts to operate, a certain number of tokens will be issued, and then the tokens will be given to nodes in the blockchain system. A node can apply to be a super representative candidate in the blockchain system with a portion of the tokens. Any token-holding node in the blockchain system can vote for these candidates. Every t period of time, the votes for all the candidates will be counted. Top N candidate nodes with the most votes will become SR(Super Representatives) for the next t period. After t period of time, the votes will be counted again to elect the new SR(Super Representatives), and the cycle continues.

Let's see how it's implemented in the context of TRON:

## Definition
- TRON: refers to the TRON network. The document does not distinguish between TRON, TRON blockchain, TRON blockchain system, etc.

- TRON token: refers to the equity token issued by and circulating in TRON, known as TRX.

- super representative candidates: nodes eligible for becoming super representatives in TRON.

- SR(Super Representatives): nodes in TRON qualified for book-keeping. They are usually called super representatives in DPoS consensus. In TRON, there will be 27 super representatives, which are also called super nodes (or SR). Here, we will not distinguish between bookkeeper, witness, supernode, SR, etc.

- Bookkeeping: the process of verifying transactions and recording them in a ledger. Because ledgers in TRON are carried by blocks, the bookkeeping process is also called block generation. We will not distinguish between bookkeeping and block generation in the document.

- Bookkeeping order: block generation order. The descending order of the 27 super representatives based on the number of votes they receive.

- Slot: In TRON, every 3 seconds is regarded as one slot. Under normal circumstances, each SR will produce a block within the corresponding slot time. Therefore, the average block interval of TRON is approximately 3 seconds. If an SR fails to produce a block for some reasons, the corresponding slot will be vacant and the next SR will produce a block in the following slot. During the maintenance period, block production will skip two slots.

- Epoch: TRON sets an Epoch to be 6 hours. The last 2 block time of an Epoch is the maintenance period, during which block generating order for the next Epoch will be decided.

- The maintenance period: TRON sets the period to be 2 block time, which is 6 seconds. This period of time is used to count the votes for candidates. There are 4 Epochs in 24 hours, and naturally, 4 maintenance periods. During the maintenance period, no block is generated and block generation order for the next Epoch is decided.

![image](https://github.com/tronprotocol/documentation-en/raw/master/images/sequence_en.jpg)


## Block Production Process
The SR(Super Representatives) of the blockchain network collect the newly generated transactions in the blockchain network and verify the legality of these transactions, then package the transactions in a block, record them as a new page on the ledger, and broadcast the page to the entire blockchain network. Other nodes will receive the new page and verify the legality of the transaction data on the page and add it to their own ledger. The SR(Super Representatives) will repeat this process so all new transaction data in the blockchain system can be recorded in the ledger.

## SR Election Mechanism
- Vote

In TRON, 1 TRX equals 1 vote.

- Voting process

In TRON, voting for candidates is a special transaction. Nodes can vote for candidates through generating a voting transaction.

- Vote counting

During each maintenance period, the votes for candidates will be counted. The top 27 candidates with the most votes will be the super representatives for the next Epoch.

## Block Generation Mechanism
During each Epoch, the 27 super representatives will take turns to generate blocks according to the bookkeeping order. Each super representative can only generate blocks when it is their turn. Super representatives package the data of multiple verified transactions into each block. The hash of the previous block will be included in each new block as the parentHash. The super representative will sign the data of this block with his/her private key and fill in witness_signature, along with the address of the super representative, the block height, and the time that block is generated, etc.

Through storing the hash of the previous block, blocks are logically connected. Eventually, they form a chain. A typical blockchain structure is shown in the following picture:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/blockchain_structure.png)


In ideal circumstances, the bookkeeping process in a DPoS consensus-based blockchain system proceeds according to the bookkeeping order calculated in advance. Blocks are generated by super representatives in turn (see figure a). However, in reality, the blockchain network is a distributed and untrusted complex system in the following three ways.
- Due to poor network environment, blocks generated by some super representatives cannot be received by other super representatives in valid time (see figure b1 and b2).
- The normal operation of a certain super representative cannot always be guaranteed (see figure c).
- Some malicious super representatives will generate fork blocks in order to fork the chain (see figure d).

![image](https://github.com/tronprotocol/documentation-en/raw/master/images/longest_chain1_en.jpg)

![image](https://github.com/tronprotocol/documentation-en/raw/master/images/longest_chain2_en.jpg)

As mentioned above, the basis for the blockchain system to operate normally is that most of the nodes in the system are honest and reliable. Furthermore, the primary guarantee for the security of the blockchain system is the security of the ledger, meaning that illegal data cannot be written into the ledger maliciously and ledger copies saved on each node should be consistent as well. Based on the DPoS consensus, the bookkeeping process is carried out by super representatives. Therefore, the safety of TRON depends on the reliability of the majority of the super representatives. TRON has put confirmed blocks in the system which are irreversible. At the same time, in order to resist the malicious behaviors of a small number of super representatives nodes, TRON recognizes the longest chain as the main chain based on "the longest chain principle".

### The Confirmed Block Principle
The newly produced blocks are in unconfirmed state, and only those blocks that are "approved" by at least 70% of the 27 super representatives(i.e. 27 * 70% = 19, rounded up)) are considered to be irreversible blocks, commonly referred to as solidified blocks, and the transactions contained in the solidified blocks have been confirmed by the entire blockchain network.  The way to "approve" the unconfirmed state block is that the SR producing subsequent blocks after it, as shown in Figure d, the SR C produces block 103, the SR E produces 104' on the basis of block 103, the block 105', 106', and 107' produced respectively by the SR G, A and B, are also subsequent blocks of the 103rd block, which means these four blocks approve the 103rd block. It can be seen that when the block of height 121 is produced, the 103rd block becomes a solidified block, since by this time the 103rd block has 19 subsequent blocks, and the point to be emphasized here is that the super representatives producing these 19 blocks must be different from each other and from the super representatives producing the 103rd block.

### The Longest Chain Principle
When a fork occurs, an honest super representative would always choose to produce blocks on the longest chain.

## Incentive Model

To ensure the safe and efficient operation of the blockchain system, TRON sets up an incentive model to encourage more nodes to join the network, thereby expanding the scale of the network. Every time a block is generated by the TRON network, a block reward of 16 TRX will be awarded to the super representative who produced the block, and a voting reward of 160 TRX will be awarded to all super representatives and super partners (super representative candidates who ranking 28th~ 127th are also called super partners), and they share the voting rewards proportionally according to the number of votes they get. At the same time, super representatives and partners will also deduct the rewards according to their commission ratio, and distribute the remaining part to voters according to the voter voting ratio.

## Proposal-based Parameter Adjustment
An important characteristic of DPoS is that any parameter adjustment can be proposed on the chain, and super representatives will decide whether to approve the proposal by starting a vote. The advantage of this method is that it avoids hard fork upgrades when adding new features. For the current dynamic parameters and values ​​of the TRON network, as well as past proposals, please refer to [here](https://tronscan.org/#/sr/committee).


## Reference Documentations

- [The Basics of TRON’s DPoS Consensus Algorithm](https://medium.com/tronnetwork/the-basics-of-trons-dpos-consensus-algorithm-db12c52f1e03)
