## Overview
Blockchain is a distributed bookkeeping system. There can be thousands of nodes in a blockchain system. Each of them independently stores the same ledger. For new transaction data to be written into the ledger, approvals from these nodes are needed. Achieving this goal in an untrusted distributed environment is a systematic, complicated quest. For a blockchain system to operate normally, that is, each node in the blockchain can always keep the same ledger, an absolute majority of the nodes in the system have to be honest and reliable. In order to ensure that honest and reliable nodes can jointly supervise the process of transaction data being written into the ledgers, each blockchain system needs to build its own consensus, which is equivalent to a constitution on the blockchain. Consensus guarantees that even in an untrusted distributed environment, as long as the vast majority of nodes comply with the consensus requirements, the results will certainly be credible. Therefore, the significance of the consensus is that the honest nodes in the blockchain can ultimately achieve the agreement of the ledgers as long as they strictly abide by this consensus.

There are several types of consensus, and the most used ones are POW, POS, and DPOS. Of course, different blockchain systems will have their own unique way of implementation. The article will mainly introduce the DPOS consensus on which TRON bases itself. We will also explain the basic components and mechanism of DPOS.

## Bookkeeping process
The bookkeeper of the blockchain system collects the newly generated transactions in the blockchain network and verifies the legality of these transactions, then packages the transactions in a block, records them as a new page on the ledger, and broadcasts the page to the entire blockchain network. Other nodes will receive the new page and verify the legality of the transaction data on the page and add it to their own ledger. The bookkeeper will repeat this process so all new transaction data in the blockchain system can be recorded in the ledger.

## DPOS overview
The role of consensus is to select the bookkeepers in the blockchain system. The bookkeepers verify the transaction data and keep the account in order to broadcast new accounts to other nodes in the network and obtains the approval of the new accounts from other nodes. As a specific implementation of consensus, DPOS works in the following way:

The DPOS consensus selects some nodes as bookkeepers in the blockchain system based on the number of votes they receive. First, when the blockchain system starts to operate, a certain number of tokens will be issued, and then the tokens will be given to nodes in the blockchain system. A node can apply to be a bookkeeper candidate in the blockchain system with a portion of the tokens. Any token-holding node in the blockchain system can vote for these candidates. Every t period of time, the votes for all the candidates will be counted. Top N candidate nodes with the most votes will become bookkeepers for the next t period. After t period of time, the votes will be counted again to elect the new bookkeepers, and the cycle continues.

Let's see how it's realized in the context of TRON:

## Definition
TRON: refers to the TRON network. The document does not distinguish between TRON, TRON blockchain, TRON blockchain system, etc.

TRON token: refers to the equity token issued by and circulating in TRON, known as TRX.

Bookkeeper candidates: nodes eligible for becoming bookkeepers in TRON.

Bookkeeper: nodes in TRON qualified for bookkeeping. They are usually called witness in DPOS consensus. In TRON, the 27 bookkeepers are also called super nodes (or SR). We will not distinguish between bookkeeper, witness, supernode, SR, etc.

Bookkeeping: the process of verifying transactions and recording them in a ledger. Because ledgers in TRON are carried by blocks, the bookkeeping process is also called block generation. We will not distinguish between bookkeeping and block generation in the document.

Bookkeeping order: block generation order. The descending order of the 27 bookkeepers based on the number of votes they receive.

Block time: TRON sets block time to be 3 seconds. This means a block is generated every 3 seconds.

Slot: after each block is generated, it can be put into a slot; and each generated block will take up a slot. For example, there are 20 slots for every minute. When a block is generated during the block time, the corresponding slot will be filled. If a block is not generated, then the corresponding slot will be empty. The next block generated will fill in a new corresponding slot.

Epoch: TRON sets an Epoch to be 6 hours. The last 2 block time of an Epoch is the maintenance period, during which block generating order for the next Epoch will be decided.

The maintenance period: TRON sets the period to be 2 block time, which is 6 seconds. This period of time is used to count the votes for candidates. There are 4 Epoch in 24 hours, and naturally, 4 maintenance periods. During the maintenance period, no block is generated and block generation order for the next Epoch is decided.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/sequence.png)

## Election mechanism
1. Votes

In TRON, 1 TRX equals 1 vote.

2. Voting process

In TRON, voting for candidates is a special transaction. Nodes can vote for candidates through generating a voting transaction.

3. Vote counting

During each maintenance period, the votes for candidates will be counted. The top 27 candidates with the most votes will be the bookkeepers for the next Epoch.

## Block generation mechanism
During each Epoch, the 27 bookkeepers will take turns to generate blocks according to the bookkeeping order. Each bookkeeper can only generate blocks when it is their turn. Bookkeepers package the data of multiple verified transactions into each block. The hash of the previous block will be included into each new block as the parentHash. The bookkeeper will sign the data of this block with his/her private key and fill in witness_signature, along with the address of the keeper, the block height, and the time the block is generated, etc.

Through storing the hash of the previous block, blocks are logically connected. Eventually, they form a chain. A typical blockchain structure is shown in the following picture:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/blockchain_structure.png)


In ideal circumstances, the bookkeeping process in a DPOS consensus-based blockchain system proceeds according to the bookkeeping order calculated in advance. Blocks are generated by witnesses in turn (see figure a). However, in reality, the blockchain network is a distributed and untrusted complex system in the following three ways. Firstly, due to poor network environment, blocks generated by witnesses cannot be received by other witnesses in valid time (see figure b1 and b2). Secondly, the normal operation of a certain witness cannot always be guaranteed (see figure c). Thirdly, some malicious witnesses will generate fork blocks in order to fork the chain (see figure d).

![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/longest_chain1.png)

![image](https://raw.githubusercontent.com/tronprotocol/documentation-EN/master/imags/longest_chain2.png)

As mentioned above, the basis for the blockchain system to operate normally is that most of the nodes in the system are honest and reliable. Furthermore, the primary guarantee for the security of the blockchain system is the security of the ledger, meaning that illegal data cannot be written into the ledger maliciously and ledger copies saved on each node should be consistent as well. Based on DPOS consensus, the bookkeeping process is carried out by witnesses. Therefore, the safety of TRON depends on the reliability of the majority of the witnesses. TRON has put confirmed blocks in the system which are irreversible. At the same time, in order to resist the malicious behaviors of a small number of bookkeeping nodes, TRON recognize the longest chain as the main chain based on "the longest chain principle".




The confirmed block principle

A block "approved" by more than two thirds of the 27 witnesses (27 * 2/3 + 1 = 19) is called a confirmed block, meaning that the transaction data in this block is confirmed by the entire TRON blockchain. "Approved" means that the block produced by the witness follows the approval-pending block. For example, block No.103 in figure d is produced by witness C; Witness E produced block No.104 after No.103. Then No. 105, 106, 107 produced by witness G, A, B are all following blocks that come after block No.103, making them the approval blocks for block No. 103 by witness C.

 

The longest chain principle

When a fork occurs, an honest witness would always choose to produce blocks on the longest chain.

## Incentive model
To ensure safe and efficient operation of the blockchain system, TRON sets up an incentive model to encourage node participation and network expansion. Bookkeepers who complete block production tasks will be rewarded with TRX. The model also specifies that for every confirmed block produced by a witness, the witness will receive 32 TRX; For the first 127th witnesses (including bookkeeper candidates) with the most votes, they will receive proportional rewards during the maintenance period of each Epoch.

## Proposal-based parameter adjustment
One important characteristics of DPOS is that any parameter adjustment can be proposed on the chain, and bookkeepers will decide whether to approve the proposal by starting a vote. A benefit to this method is that it avoids hard fork upgrades when adding new features. Currently, TRON supports the following parameter adjustments:

1. The interval between two maintenance periods

2. The TRX cost of applying to be a bookkeeper candidate.

3. The TRX cost of account activation

4. The bandwidth cost for one byte in each transaction

5. The TRX cost of issuing tokens on TRON

6. The rewards for producing each block

7. The total amount of TRX that is proportionately awarded to the first 127th bookkeepers (including bookkeeper candidates) with the most votes

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
To be continued

Appendix: Reference Documentations

[https://www.coinbureau.com/education/delegated-proof-stake-dpos/](https://www.coinbureau.com/education/delegated-proof-stake-dpos/)  

[https://www.nichanank.com/blog/2018/6/4/consensus-algorithms-pos-dpos](https://www.nichanank.com/blog/2018/6/4/consensus-algorithms-pos-dpos)  

[http://docs.bitshares.org/en/master/technology/dpos.html#role-of-delegates](http://docs.bitshares.org/en/master/technology/dpos.html#role-of-delegates)  

[https://hackernoon.com/what-is-delegated-proof-of-stake-897a2f0558f9](https://hackernoon.com/what-is-delegated-proof-of-stake-897a2f0558f9)   
