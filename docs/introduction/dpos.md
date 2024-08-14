# DPoS

## Overview
Blockchain is a distributed accounting system. In a blockchain system, there can be thousands of nodes, each of which independently stores the same ledger. If new transaction data is to be written into the ledger,  approvals from these nodes are needed. Achieving this goal in an untrusted distributed environment is a complicated systematic quest. The blockchain system operates normally means each node in the blockchain can always keep the same ledger, provided that most nodes in the system are honest and reliable. In order to ensure that honest and reliable nodes can jointly supervise the transaction data written into the ledgers, each blockchain system needs to build its own consensus, which is equivalent to the constitution of the blockchain. As long as the vast majority of nodes comply with the consensus requirements, it is able to guarantee the results will certainly be credible, even in an untrusted distributed environment. Therefore, the significance of the consensus is that the honest nodes in the blockchain can ultimately achieve the agreement of the ledgers as long as they strictly abide by this consensus.

There are several types of consensus, and the most commonly used are POW, POS, and DPoS. Definitely, different blockchain systems will have a unique way of implementation. This article will mainly introduce the DPoS consensus on which TRON based. We will also explain the basic components and mechanisms of DPoS.

## Block Producing Process
The witnesses of the blockchain network collect the newly generated transactions in the blockchain network and verify the legality of these transactions, then package the transactions in a block, record them as a new page on the ledger, and broadcast the page to the entire blockchain network. Other nodes will receive the new page and verify the legality of the transaction data on the page and add it to their own ledger. The witnesses will repeat this process so all new transaction data in the blockchain system can be recorded in the ledger.

## DPoS overview
The role of consensus is to select the witnesseses in the blockchain system. The witnesseses verify the transaction data and keep the account in order to broadcast new accounts to other nodes in the network and obtains the approval of the new accounts from other nodes. As a specific implementation of consensus, DPoS works in the following way:

The DPoS consensus selects some nodes as witnesseses in the blockchain system based on the number of votes they receive. First, when the blockchain system starts to operate, a certain number of tokens will be issued, and then the tokens will be given to nodes in the blockchain system. A node can apply to be a witnesses candidate in the blockchain system with a portion of the tokens. Any token-holding node in the blockchain system can vote for these candidates. Every t period of time, the votes for all the candidates will be counted. Top N candidate nodes with the most votes will become witnesseses for the next t period. After t period of time, the votes will be counted again to elect the new witnesseses, and the cycle continues.

Let's see how it's realized in the context of TRON:

## Definition
- TRON: refers to the TRON network. The document does not distinguish between TRON, TRON blockchain, TRON blockchain system, etc.

- TRON token: refers to the equity token issued by and circulating in TRON, known as TRX.

- Witnesses candidates: nodes eligible for becoming witnesseses in TRON.

- Witnesses: nodes in TRON qualified for book-keeping. They are usually called witnesses in DPoS consensus. In TRON, there will be 27 witnesseses, which are also called super nodes (or SR). Here, we will not distinguish between bookkeeper, witness, supernode, SR, etc.

- Bookkeeping: the process of verifying transactions and recording them in a ledger. Because ledgers in TRON are carried by blocks, the bookkeeping process is also called block generation. We will not distinguish between bookkeeping and block generation in the document.

- Bookkeeping order: block generation order. The descending order of the 27 witnesseses based on the number of votes they receive.

- Slot: In TRON, every three seconds is regarded as one slot. Under normal circumstances, each SR will produce a block within the corresponding slot time. Therefore, the average block interval of TRON is approximately three seconds. If an SR fails to produce a block for some reasons, the corresponding slot will be vacant and the next SR will produce a block in the following slot. During the maintenance period, block production will skip two slots.

- Epoch: TRON sets an Epoch to be 6 hours. The last 2 block time of an Epoch is the maintenance period, during which block generating order for the next Epoch will be decided.

- The maintenance period: TRON sets the period to be 2 block time, which is 6 seconds. This period of time is used to count the votes for candidates. There are 4 Epochs in 24 hours, and naturally, 4 maintenance periods. During the maintenance period, no block is generated and block generation order for the next Epoch is decided.

![image](https://github.com/tronprotocol/documentation-en/raw/master/images/sequence_en.jpg)

## Election mechanism
1. Votes

In TRON, 1 TRX equals 1 vote.

2. Voting process

In TRON, voting for candidates is a special transaction. Nodes can vote for candidates through generating a voting transaction.

3. Vote counting

During each maintenance period, the votes for candidates will be counted. The top 27 candidates with the most votes will be the witnesses for the next Epoch.

## Block generation mechanism
During each Epoch, the 27 witnesses will take turns to generate blocks according to the bookkeeping order. Each witness can only generate blocks when it is their turn. Witnesses package the data of multiple verified transactions into each block. The hash of the previous block will be included in each new block as the parentHash. The witness will sign the data of this block with his/her private key and fill in witness_signature, along with the address of the witness, the block height, and the time that block is generated, etc.

Through storing the hash of the previous block, blocks are logically connected. Eventually, they form a chain. A typical blockchain structure is shown in the following picture:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/blockchain_structure.png)


In ideal circumstances, the bookkeeping process in a DPoS consensus-based blockchain system proceeds according to the bookkeeping order calculated in advance. Blocks are generated by witnesses in turn (see figure a). However, in reality, the blockchain network is a distributed and untrusted complex system in the following three ways.
- Due to poor network environment, blocks generated by some witnesses cannot be received by other witnesses in valid time (see figure b1 and b2).
- The normal operation of a certain witness cannot always be guaranteed (see figure c).
- Some malicious witnesses will generate fork blocks in order to fork the chain (see figure d).

![image](https://github.com/tronprotocol/documentation-en/raw/master/images/longest_chain1_en.jpg)

![image](https://github.com/tronprotocol/documentation-en/raw/master/images/longest_chain2_en.jpg)

As mentioned above, the basis for the blockchain system to operate normally is that most of the nodes in the system are honest and reliable. Furthermore, the primary guarantee for the security of the blockchain system is the security of the ledger, meaning that illegal data cannot be written into the ledger maliciously and ledger copies saved on each node should be consistent as well. Based on the DPoS consensus, the bookkeeping process is carried out by witnesses. Therefore, the safety of TRON depends on the reliability of the majority of the witnesses. TRON has put confirmed blocks in the system which are irreversible. At the same time, in order to resist the malicious behaviors of a small number of witness nodes, TRON recognizes the longest chain as the main chain based on "the longest chain principle".

**The confirmed block principle**

The newly produced blocks are in unconfirmed state, and only those blocks that are "approved" by more than 70% (i.e. 27 * 70% = 19, rounded down) of the 27 Witnesses are considered to be irreversible blocks, commonly referred to as solidified blocks, and the transactions contained in the solidified blocks have been confirmed by the entire blockchain network.  The way to "approve" the unconfirmed state block is that the Witness producing subsequent blocks after it, as shown in Figure d, the Witness C produces block 103, the Witness E produces 104' on the basis of block 103, the block 105', 106', and 107' produced respectively by the Witness G, A and B, are also subsequent blocks of the 103rd block, which means these four blocks approve the 103rd block. It can be seen that when the block of height 121 is produced, the 103rd block becomes a solidified block, since by this time the 103rd block has 19 subsequent blocks, and the point to be emphasized here is that the Witnesses producing these 19 blocks must be different from each other and from the Witnesses producing the 103rd block.

**The longest chain principle**

When a fork occurs, an honest witness would always choose to produce blocks on the longest chain.

## Incentive model

To ensure the safe and efficient operation of the blockchain system, TRON sets up an incentive model to encourage more nodes to join the network, thereby expanding the scale of the network. Every time a block is generated by the TRON network, a block reward of 16 TRX will be awarded to the super representative who produced the block, and a voting reward of 160 TRX will be awarded to all super representatives and super partners (super representative candidates who ranking 28th~ 127th are also called super partners), and they share the voting rewards proportionally according to the number of votes they get. At the same time, super representatives and partners will also deduct the rewards according to their commission ratio, and distribute the remaining part to voters according to the voter voting ratio.

## Proposal-based parameter adjustment
An important characteristic of DPoS is that any parameter adjustment can be proposed on the chain, and witnesses will decide whether to approve the proposal by starting a vote. The advantage of this method is that it avoids hard fork upgrades when adding new features. Currently, TRON supports the following parameter adjustments:

1. The interval between two maintenance periods

2. The TRX cost of applying to be a bookkeeper candidate

3. The TRX cost of account activation

4. The bandwidth cost for one byte in each transaction

5. The TRX cost of issuing tokens on TRON

6. The rewards for producing each block

7. The total amount of TRX that is proportionately awarded to the first 127th witnesses (including bookkeeper candidates) with the most votes

8. The TRX cost of account activation through system contract

9. The bandwidth cost for account activation

10. The exchange rate between Energy and Sun

11. The TRX cost for building a TRC-10 token-based decentralized trading pair

12. The maximum CPU time allowed for a single transaction execution

13. Whether to allow changes of account names

14. Whether to allow the issuance of assets with duplicate names

15. Whether to allow resource delegation

16. The upper limit for Energy in TRON blockchain

17. Whether to allow TRC-10 asset transfer in smart contracts

18. Whether to allow adjustment to Energy upper limit

19. Whether to allow multi-signature

20. The TRX cost of updating account access

21. The TRX cost of multi-signature transactions

22. Whether to verify block and transaction protobuf message

## Bandwidth and energy mechanism
To be continued...

## Appendix: Reference Documentations

- [Delegated Proof of Stake (DPoS) – Total Beginners Guide](https://www.coinbureau.com/education/delegated-proof-stake-dpos/)
- [Consensus Algorithms: Proof-of-Stake & Cryptoeconomics](https://www.nichanank.com/blog/2018/6/4/consensus-algorithms-pos-dpos)
- [Role of Delegates](http://docs.bitshares.org/en/master/technology/dpos.html#role-of-delegates)
- [What is Delegated Proof of Stake?](https://hackernoon.com/what-is-delegated-proof-of-stake-897a2f0558f9)
