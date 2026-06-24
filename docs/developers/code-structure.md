# java-tron Core Modules
## Code Structure
java-tron is a TRON network client developed based on the Java language. It implements all the functions mentioned in the TRON white paper, including consensus mechanism, cryptography, database, TVM virtual machine, network management, etc. Starting java-tron runs a TRON node. This document details the code structure of java-tron and introduces the functions of its various modules to facilitate code analysis and development.

java-tron adopts a modular code structure; the code structure is clear and easy to maintain and expand. The core of java-tron consists of 7 modules: [Protocol](#protocol), [Common](#common), [Chainbase](#chainbase), [Consensus](#consensus), [Actuator](#actuator), [Crypto](#crypto), [Framework](#framework). This document introduces the functions of these 7 core modules and their code organization. In addition, java-tron includes two auxiliary modules:

* `plugins` - A set of node maintenance tools (Toolkit), providing offline database operations such as lite, convert, copy, move, and archive
* `platform` - CPU architecture adaptation module, providing architecture-specific implementations (such as math operations and market order comparators) under the `common`/`x86`/`arm` directories respectively



### Protocol

In a distributed network like a blockchain, a concise and efficient data interaction protocol is essential. 
The protocol module defines:

* Inter-node communication protocol
* Communication protocol between modules within the node
* Protocols for externally provided services

The above protocols adopt the [`Google Protobuf`](https://developers.google.com/protocol-buffers) data exchange format. Compared with JSON and XML, the `Google Protobuf` format is more efficient and flexible and can be compiled by the ProtoBuf compiler to generate language-specific source code for serialization and deserialization based on the defined protocol files. Protobuf is the basis for java-tron to achieve cross-language and cross-platform.

[protocol](https://github.com/tronprotocol/java-tron/tree/develop/protocol) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/protocol` , its directory structure is as follows:

```
|-- protocol/src/main/protos
    |-- api
    |   |-- api.proto
    |   |-- zksnark.proto
    |-- core
        |-- Discover.proto
        |-- Tron.proto
        |-- TronInventoryItems.proto
        |-- contract
```

* `api/` - The gRPC interface and data structure provided by the java-tron node externally
* `core/` - Data structure for communication between nodes and between modules within nodes
    * `Discover.proto` - Node discovers related data structures
    * `TronInventoryItems.proto` - Data structure related to block transferring between nodes
    * `contract/` - Contract related data structures
    * `Tron.proto` - Other important data structures, including accounts, blocks, transactions, resources, super representatives, voting, and proposals...



### Common

The common module encapsulates common components and tools, such as exception handling and metrics monitoring tools, making them easily accessible for use by other modules.

[common](https://github.com/tronprotocol/java-tron/tree/develop/common) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/common`, its directory structure is as follows:

```
|-- common/src/main/java/org/tron
    |-- common
    |   |-- args
    |   |-- cache
    |   |-- config
    |   |-- cron
    |   |-- entity
    |   |-- es
    |   |-- exit
    |   |-- log
    |   |-- logsfilter
    |   |-- math
    |   |-- parameter
    |   |-- prometheus
    |   |-- runtime
    |   |-- setting
    |   |-- utils
    |-- core
        |-- config
        |-- db
        |-- db2
        |-- exception
        |-- vm
```


* `common/prometheus` - Prometheus metrics monitoring
* `common/utils` - The wrapper class of basic data type
* `core/config` - Node configuration related classes
* `core/exception` - All exception handling related classes




### Chainbase

Chainbase is a database module. For probabilistic consensus algorithms such as PoW, PoS and DPoS, situations of switching to a new chain, however unlikely, are inevitable. To address this, Chainbase defines an interface standard that supports rollbackable databases. This interface requires databases to implement a state rollback mechanism, a checkpoint-based disaster tolerance mechanism, and other relevant features. 

In addition, the Chainbase module features a well-designed abstract interface. Any database that implements the interface can be used for underlying storage on the blockchain, granting more flexibility to developers. LevelDB and RocksDB are two default implementations.

[chainbase](https://github.com/tronprotocol/java-tron/tree/develop/chainbase) module's source code is located at: `https://github.com/tronprotocol/java-tron/tree/develop/chainbase`, its directory structure is as follows:
```
|-- chainbase/src/main/java/org/tron
    |-- common
    |   |-- bloom
    |   |-- error
    |   |-- overlay
    |   |-- runtime
    |   |-- storage
    |   |   |-- leveldb
    |   |   |-- rocksdb
    |   |-- utils
    |   |-- zksnark
    |-- core
        |-- actuator
        |-- capsule
        |-- db
        |   |-- RevokingDatabase.java
        |   |-- TronStoreWithRevoking.java
        |   |-- ......
        |-- db2
        |   |-- common
        |   |-- core
        |       |-- SnapshotManager.java
        |       |-- ......
        |-- net
        |-- service
        |-- store
```


* `common/` - Common components, such as exception handling, tools, etc
    * `storage/leveldb/` Implemented the use of LevelDB as the underlying storage database
    * `storage/rocksdb/` Implemented the use of RocksDB as the underlying storage database
* `core/` - The core code of the chainbase module
    * `capsule/` 

        The encapsulation class of each data structure, such as AccountCapsule, BlockCapsule, etc. AccountCapsule is the encapsulation class of Account data structure, which provides modification and query of account data; BlockCapsule is the encapsulation class of Block data structure, which provides modification and query of block data.

    * `store/` 

        Various databases, such as `AccountStore`, `ProposalStore`, etc. `AccountStore` is the account database, the database name is `account`, which stores all account information in the TRON network; `ProposalStore` is the proposal database, and the database name is `proposal`, which stores all the proposal information in the TRON network.

    * `db/` and `db2/` 
    
        Implemented the rollbackable database. The `db/` directory provides the core interface and base class (such as `RevokingDatabase` and `TronStoreWithRevoking`), while the actual rollback implementation is `SnapshotManager` located in the `db2/` directory. `SnapshotManager` provides a stable data rollback mechanism and supports the extension of the underlying database, and is the implementation java-tron uses to roll back the database. Several important interfaces and implementation classes are as follows:

        * `RevokingDatabase.java` - It is the interface of the database container, used to manage all rollbackable databases, `SnapshotManager` is an implementation of this interface
        * `TronStoreWithRevoking.java` - It is the base class that supports rollbackable databases. All rollbackable databases are their implementations, such as `BlockStore`, `TransactionStore`, etc
    

### Consensus

The consensus mechanism is a crucial module in blockchains. Common ones are PoW, PoS, DPoS and PBFT, etc. Conversely, algorithms like Paxos and Raft are typically applied to consortium blockchains and other trusted networks. The consensus mechanism should match the business scenario. For instance, PoW is not suitable for real-time games that are sensitive to consensus efficiency, while PBFT can make an optimized choice for exchanges demanding high real-time capability. Therefore, a replaceable consensus mechanism is an essential innovation for building application-specific blockchains. The ultimate goal of the consensus module is to make consensus switch as easy as configuring parameters for application developers.

[consensus](https://github.com/tronprotocol/java-tron/tree/develop/consensus) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/consensus`, its directory structure is as follows:
```
|-- consensus/src/main/java/org/tron/consensus
    |-- Consensus.java
    |-- ConsensusDelegate.java
    |-- base
    |   |-- ConsensusInterface.java
    |   |-- ......
    |-- dpos
    |-- pbft
```
Consensus module divides the consensus process into several important parts that are defined in `ConsensusInterface`:

1. `start` - start the consensus service with customizable startup parameters
2. `stop` - stop the consensus service
3. `receiveBlock` - define the consensus logic of receiving blocks
4. `validBlock` - define the consensus logic of validating blocks
5. `applyBlock` - define the consensus logic of processing blocks

Currently, java-tron implements DPOS consensus and PBFT consensus based on the `ConsensusInterface` interface, which is located in the `dpos/` and `pbft/` directories respectively. Developers can also implement the `ConsensusInterface` interface according to their own business needs to customize the consensus mechanism.


### Actuator

Ethereum was the first to introduce the virtual machine and define the smart contract. However, smart contracts are constrained in terms of their functions and not flexible enough to accommodate the needs of complex applications. To address these limitations and support the creation of application-specific chains, java-tron includes a separate module called Actuator, offering developers a novel approach to application development. They can choose to implant their application codes into a chain instead of running them on virtual machines. 

Actuator is the executor of transactions, while applications can be viewed as a cluster of different types of transactions, each of which is executed by a corresponding actuator.

[actuator](https://github.com/tronprotocol/java-tron/tree/develop/actuator) module's source code is located at: `https://github.com/tronprotocol/java-tron/tree/develop/actuator`, its directory structure is as follows:
```
|-- actuator/src/main/java/org/tron/core
    |-- actuator
    |   |-- AbstractActuator.java
    |   |-- ActuatorCreator.java
    |   |-- ActuatorFactory.java
    |   |-- TransferActuator.java
    |   |-- VMActuator.java
    |   |-- ......
    |-- utils
    |-- vm
```

* `actuator/` - The executors of various types of transactions in the TRON network which define the processing logic of different types of transactions. For example, `TransferActuator` is the processing class for transferring TRX, and `FreezeBalanceV2Actuator` is the processing class for staking TRX to obtain resource
* `utils/` - tools needed to execute transaction
* `vm/` - TRON virtual machine related code

Actuator module defines the `Actuator` interface, which includes 4 different methods:

* `execute` - execute specific actions of transactions, such as state modification, process redirection, logic execution, etc.
* `validate` - validate authenticity of transactions
* `getOwnerAddress` - acquire the address of transaction initiators
* `calcFee` - define the logic of calculating transaction fees

Depending on their businesses, developers may set up Actuator accordingly and customize the processing of different types of transactions.
 
### Crypto
The Crypto module is relatively independent yet crucial to the system. Data security in java-tron is almost entirely guaranteed by this module. Currently, SM2 and ECKey encryption algorithms are supported.

[crypto](https://github.com/tronprotocol/java-tron/tree/develop/crypto) module's source code is located at: `https://github.com/tronprotocol/java-tron/tree/develop/crypto`, its directory structure is as follows:
```
|-- crypto/src/main/java/org/tron/common/crypto
    |-- Blake2bfMessageDigest.java
    |-- ECKey.java
    |-- Hash.java
    |-- SignInterface.java
    |-- SignUtils.java
    |-- SignatureInterface.java
    |-- cryptohash
    |-- jce
    |-- sm2
    |-- zksnark
```

* `sm2` and `jce` - Provide SM2 and ECKey encryption algorithm and signature algorithm
* `zksnark` - Provide a zero-knowledge proof algorithm

### Framework

The Framework module serves as the core of java-tron and the primary entry point for the node. It manages the initialization of all other modules and handles the core business logic. The framework module includes the services provided externally as well as the block broadcasting and processing procedures; low-level peer discovery and connection transport are provided by the external libp2p dependency, while the TRON protocol layer (handshake, keep-alive, message dispatch, synchronization, and broadcast) is still handled by the framework's `core/net`.

[framework](https://github.com/tronprotocol/java-tron/tree/develop/framework) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/framework`, its directory structure is as follows:

```
|-- framework/src/main/java/org/tron
    |-- common
    |   |-- application
    |   |-- backup
    |   |-- client
    |   |-- logsfilter
    |   |-- runtime
    |   |-- zksnark
    |-- core
    |   |-- Wallet.java
    |   |-- capsule
    |   |-- config
    |   |-- consensus
    |   |-- db
    |   |-- metrics
    |   |-- net
    |   |-- services
    |   |-- trie
    |   |-- zen
    |-- keystore
    |-- program
    |   |-- FullNode.java
```

* `program/FullNode.java` - It is the entry point of the program and initializes external HTTP, gRPC and json-rpc interface services
* `core/services` - Defines the externally provided services, its subdirectory `http/` contains all http interface processing classes, `jsonrpc/` contains all json-rpc interface processing classes
* `core/net` - Message processing and network business logic, its subdirectory `service/` handles transaction and block broadcasting, block fetching and synchronization logic
* `core/db/Manager.java` - Transaction and block verification and processing logic

> **Note**: In earlier versions, the underlying implementations of node discovery and node connection management were located in the `common/overlay` directory (with subdirectories such as `discover` and `server`) of the framework module. This underlying P2P network layer has since been extracted into a standalone external dependency, [`io.github.tronprotocol:libp2p`](https://github.com/tronprotocol/libp2p), and the framework module no longer contains the `common/overlay` and `common/net` directories. Low-level peer discovery and connection transport are now provided by the libp2p library, which the framework integrates with through `core/net` (e.g. `TronNetService`). The TRON protocol layer above it — handshake, keep-alive, message dispatch, synchronization, broadcast, and peer business-state management — remains in `core/net`.

### Summary
This article mainly introduces the code structure of java-tron, as well as the function, location and directory structure of each functional module. Through this article, you will have a general understanding of the overall structure and key interfaces of java-tron, which is helpful for subsequent code analysis and development.



## ChainBase
### Introduction
As we all know, the blockchain is essentially a non-tamperable distributed ledger, which is very suitable for solving the problem of trust. Blockchains are frequently used for secure bookkeeping and transaction processing. For example, applications utilize cryptocurrencies like BTC, ETH, and TRX to conduct economic activities while ensuring financial transparency.

The realization of such an immutable distributed ledger is a very complex system engineering, involving many technical fields: such as p2p networks, smart contracts, databases, cryptography, consensus mechanisms, etc. Among them, the database is the basis of the underlying storage, and various blockchain teams are exploring the design and optimization of the database level.

The Database module of java-tron is also called the ChainBase module. This article mainly introduces some background knowledge and shows developers the implementation details of the ChainBase module by introducing logic such as transaction processing, state rollback, and data persistence.



### Prerequisites
The database is an important part of the blockchain system. It stores all the data on the blockchain and is the basis for the normal operation of the blockchain system. Each fullnode stores a full amount of data, including block data, state data, etc. java-tron uses the Account model to save the user's account state.

#### Account Models
There are currently two mainstream account models,

- [UTXO](https://en.wikipedia.org/wiki/Unspent_transaction_output)
- Account Model

The UTXO model is stateless, makes it easier to process transactions concurrently, and has better privacy, but it is not programming-friendly.

In the Account Model, user data is stored in the corresponding account, and smart contracts are also stored in the account in the form of code. This model is more intuitive and easier for developers to understand. For programmability, flexibility, and other considerations, java-tron adopts the Account Model.

#### Consensus

The current mainstream consensus is PoW, PoS, DPoS, etc. PoW is proof of work, all nodes participate in the calculation of an expected hash result, and the node that first calculates the result has the right to produce a block, but as the computing power continues to increase, the energy consumption required to calculate the hash is also increasing. Moreover, large mining farms monopolize most of the computing power, which also goes against the original intention of decentralization.

To solve the problems faced by PoW, some people proposed PoS (Proof of Stake), which is simply understood as the more coins that the node holds, the greater the probability of obtaining the right to produce blocks, but this will lead to monopoly problems as well. In order to improve, DPoS (Delegated Proof of Stake) is proposed: the decentralization feature is guaranteed by the elected super representative, and the super representative is responsible for the block production in turn to improve the efficiency. java-tron currently adopts the DPoS consensus mechanism.

To learn more, please refer to [Delegated Proof of Stake](https://en.bitcoinwiki.org/wiki/DPoS).

#### Persistent Storage
There are certain differences between blockchain and traditional Internet business. The blockchain does not have particularly complex processing logic at the database level, but there are a large number of key-value read and write operations in the blockchain so there are higher requirements for data read and write performance.

Based on this consideration, java-tron uses LevelDB as the underlying data storage by default (on ARM64 architecture, RocksDB is forced regardless of the configuration, since LevelDB is deprecated on ARM), and java-tron has a good architecture design. The interface-oriented programming mode makes the Chainbase module have better scalability. All databases implemented the chainbase interface can be used as the underlying storage engine of java-tron. For example, in the chainbase v2 version, a database implementation based on RocksDB is provided.


#### Transaction Validation
As we all know, the blockchain mainly stores transaction data. Before introducing the Chainbase module, you need to understand the transaction processing logic in java-tron.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_1.png)


The transaction will be distributed to each node through network broadcast. After receiving the transaction, the node will first validate the signature of the transaction. If successful, the transaction needs to be pre-executed to determine whether the transaction is legal.

**Note: The specific implementation in java-tron may deviate slightly from the simplified figure above. For convenience, this article collectively refers to FullNodes and Super Representatives (SRs) simply as 'nodes'.**

For example, to process a transfer transaction: user A transfers 100 TRX to user B, and it needs to validate whether user A has enough balance to make the transfer.

The account library in the database stores the account information of all users, including the user's balance information. How to judge whether this transfer transaction is legal? The logic of java-tron is: when a transaction is received from the network, the transaction operation will be executed immediately, that is, the account information will be modified in the local database: (accountA - 100TRX, accountB + 100TRX). If this operation can be executed successfully, it means that the transaction is legal at least in the current state, and can be packed into the block.


#### Glossary
SR： Super Representative, is responsible for block production.

FullNode： stores all block data, is responsible for transactions, block broadcasting and validation, and provides query services.

TRX： TRON native token.


### State Rollback
Above we mentioned that java-tron validates whether the transaction is legal through pre-execution, but what we need to know is that the transaction is successfully validated on a certain node does not mean that the transaction has been successfully chained because the transaction has not been packed into the consensus blocks, there is a risk of being rolled back.

The consensus of java-tron follows a principle: that is, the transactions in the blocks that are approved by more than 2/3 of the SRs are the ones that are really successful on the chain. can also be understood as below,


- transactions are packed into a block
- the block is approved by more than 2/3 of the SRs

A transaction that satisfies the above two points is a successful transaction on the chain. A transaction in java-tron is finally confirmed through three stages,

- transaction validating
- transaction packing into the block
- block being accepted, applied, and eventually solidified

This also leads to a problem: in the implementation of java-tron, if a node validates the transaction, its database state changes accordingly. If the transaction is not packed into the block yet or the block it is packed into has not been approved by more than 2/3 of SR, the state of this node will be inconsistent with the state of the entire network.


**Therefore, except for the processing transaction data in blocks approved by more than 2/3 SRs, all other data state changes resulting from transaction processing may need to be rolled back.** There are three kinds of scenarios in total:

- after receiving a new block, roll back the state changes generated by transaction validation
- after producing a block, roll back the state changes generated by transaction validation
- if a forked takes place, roll back the state changes generated by the transactions of the blocks in the forked chain

The data state changes caused by these three scenarios may need to be rolled back and the following section explains why.


#### Rollback after Receiving a New Block
When receiving a new block, the node needs to roll back to the state at the end of the previous block and roll back all transactions validated afterward. As shown below,

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_2.png)




If the account balance of accountA is 100 at the block height is 1000, the node receives and validates a transaction 't1', in which accountA transfers 100TRX to accountB. After receiving the new block1001, the block contains a transaction 't2', in which accountA transfers 50TRX to accountC. In theory, t2 has been packed into the block, and the priority is higher than t1. However, if no operation is done, the validation of t2 will fail because accountA does not have enough balance. Therefore, after receiving the new block 1001, the state change generated by transaction t1 needs to be rolled back.


#### Rollback after Producing a New Block
First of all, readers may have a question: the validated transaction can be directly packed into the block, and it will not change the database state. Why is there a change in the database state?

Because java-tron does a secondary validation of the transaction when it is packed into the block. The secondary validation is due to the timeliness of the transaction. Still taking the above figure as an example, it can be seen from the figure, that after 1001 is received, the transaction t1 was rolled back, and the balance of accountA was deducted by 50. And then, it was the node's turn to produce a block, but t1 had become an illegal transaction at this time because the balance in accountA was not enough to transfer 100 TRX, it is not advisable to directly pack t1 into the block. So the transaction needs to be validated again, which is why the transaction needs to be validated twice when producing a block.

After the block is packed successfully, the node will broadcast the block to the network and apply the block locally. And the logic of applying will re-check the transactions in the block. So after the block is packed, a rollback operation still needs to be performed.


#### Rollback when Forking
This is the last rollback situation, and the blockchain will inevitably fork, especially the blockchain system based on DPoS with a faster block production speed that is more prone to fork.

java-tron maintains a data structure in memory as below,

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_3.png)



java-tron holds all blocks that have not reached consensus recently. When a forked chain occurs, according to the longest chain principle: if the block height of the forked chain is greater than the current main chain block height, the forked chain needs to be switched to the main chain. Part of the blocks on the previous main chain needs to roll back up to their common parent blocks when switching, and then apply new main chain blocks sequentially from the parent block.

As shown in the figure, fork A in the dark part was originally the main chain. Because the height of fork B continues to grow and eventually exceeds the height of A, it is necessary to roll back the data in those three blocks with heights 1003, 1002, and 1001 in fork A. Then apply fork blocks 1001', 1002', 1003', and 1004' in B in sequence.



### State Rollback Implementation
This chapter explains receiving and validating transactions, block production, validating and saving blocks from the perspective of code, to further analyze the chainbase module of java-tron. If there is no further declaration, the default description is dedicated to all the Fullnode (including SR).


#### Receiving Transactions
![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_4.png)


After the node receives a transaction, it puts the transaction into the local pushTransactionQueue cache queue by calling the `pushTransaction(final TransactionCapsule trx)` function of the manager class and validates the transaction at the same time. And the return of this method is sort of elegant:


1. if validation is successful, ‘true' is returned
2. for the transaction sent by the user to the node through the API, if the transaction validation fails, an exception will be returned to the user; for transactions received from other nodes through the network, exceptions will only be recorded locally

After the transaction validation is successful, the transactions without problems will be put into the pendingTransactionQueue, and the pendingTransactionQueue is responsible for providing the transaction set when producing blocks. If the node is an SR node, when producing a block, it will take out all or part of it from the pendingTransactionQueue (depending on how many transactions are in the pendingTransactionQueue) to generate a block.




#### Rollback when Receiving Blocks

A node would receive transactions broadcasted from other nodes before receiving a new block, the transactions need to be validated to determine whether they can be executed correctly. Validation means that the state needs to be changed, and a successful validation does not mean that the transaction will be finally executed, and it will be considered successful after packing into a block and the block become solidified. This step can be considered to filter out those obviously wrong transactions in advance. This is just validation. When a new block arrives, the state changed by transaction validations should be rolled back. The state produced by applying new blocks will not be rolled back during this pending-transaction cleanup step; however, before a block is solidified, its applied state may still be rolled back when a fork switch occurs.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_5.png)


When rolling back, java-tron move the transactions in the pendingTransactionQueue to rePushTransactions, and clear the pendingTransactionQueue, see the figure for a detailed explanation.

Why does the pendingTransactionQueue need to be emptied after a new block arrives? First of all, it is clear that the pendingTransactionQueue queue is responsible for providing transaction data when generating blocks, that is to say, it stores validated transactions that can be directly packed into blocks. Since the new block will also change the account state, those validated transactions in pendingTransactionQueue may not pass the validation after applying the new block (the simplest example: a transaction in the new block is that accountA spends a part of the token, resulting in a transaction amount of accountA in the queue that is not enough to pay ). After the transaction is moved to rePushTransactions, a background thread will be responsible for re-validating the transaction in the queue. If nothing is wrong, it will be put into the pendingTransactionQueue again to provide data for block production.

There is a session object in java-tron. A session represents the change in the state of a block. The session object is mainly used for rollback. For example,rolling back the state to the state of the previous block needs to be operated throughout the session, as shown in the following figure,

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_6.png)


In the above figure, you can see that there are many different types of databases in persistent storage. These data are jointly organized into a complete blockchain. For example, blocks are stored in khasodb and blockStore, and account information is stored in accountStore... 

The node maintains a session chain table, which stores the change information corresponding to the block/transaction, and the node can roll back through the change information. In the above figure, session1 is the status change of the current highest block. When a transaction is received, a new session2 will be generated. Each transaction that comes later will generate a temporary tmpSession, and after the transaction is validated, the tmpSession corresponded will be merged to session2. Before a new block is received again, all status changes generated by transaction validation will be saved in session2. When a new block arrives, directly execute the reset method of the session2 to roll back the state to the previous block.


#### Rollback when Producing Blocks

SR needs to roll back before producing blocks. The reasons are more complicated. Let's consider a scenario first:

- The pendingTransactionQueue stores the currently validated transactions, so when an SR node produces a block, it only needs to directly pack the transactions in the pendingTransactionQueue into the block, and then roll back the state to the state of the previous block after packing.

However, there is a problem with this scheme: if the SR node has just received and applied a new block, the pendingTransactionQueue will be cleared. At this time, it is the turn of the SR to pack the block, but there is no transaction in pendingTransactionQueue. Therefore, the real implementation is that not only reads transactions from pendingTransactionQueue when generating blocks but also reads transactions from rePushTransactions and puts them into blocks if there are few transactions in pendingTransactionQueue. The above analysis shows that transactions in rePushTransactions may not be possible to pass the validation, so the transactions need to be validated again. Due to this validation logic, the state needs to be rolled back before the block is produced.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_7.png)

In the process of producing the block, the transaction will be validated again, so there will be a state change, but this is just block production, and the block needs to be broadcast as well, and those blocks who received the broadcast will actually change the state, so the state changes incurred by block production also need to be rolled back. As shown in the figure above, when the block production is completed, session2" needs to be rolled back.



### Block Solidity
java-tron adopts the DPoS consensus mechanism. The DPoS of java-tron is to vote for 27 nodes as block producers (also known as SR), SR has the right and obligation to produce blocks, and blocks approved by more than 2/3 of SR are considered to reach a consensus. These blocks, which are no longer rolled back are called solidified blocks. The state of non-solidified blocks is first written into rollbackable in-memory snapshot layers (sessions); only solidified snapshot layers are flushed and merged into the persistent storage.

SnapshotManager in java-tron is the key entry to the storage module, holds references to all current business databases, and stores database references in a list. Each database instance supports adding a new layer of state set on its own called SnapshotImpl. It is an in-memory hashmap, multiple SnapshotImpl are associated in the form of a linked list, and one SnapshotImpl retains the data modification (in-merging or merging) involved in one state change, and SnapshotImpl is independent of each other. They are separated through this data structure, as shown in the following figure,

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_8.png)


The SnapshotRoot in the above figure is the encapsulation class for the persistent database, which is responsible for storing the solidified data.

In the previous chapters, we talked about sessions. A session represents the changes of state in a block. In fact, a session contains the SnapshotImpl corresponding to each database. For example, all SnapshotImpl in the layer of block 5 in the above figure together constitutes the changes of block 5 to the entire database.

The changes generated after the node receives a new block will not be directly stored in the persistent storage (SnapshotRoot), but will first be stored in snapshotImpl. Each block received corresponds to a snapshotImpl. Continuously receiving blocks will lead to more and more snapshotImpl. When will they be written to persistent storage?

There are two variables in SnapshotManager: 'size' and 'maxSize'. Here we simply understand 'size' as how many layers of snapshotImpl are there currently in memory, and 'maxSize' represents the difference between the height of the current solidified block and the latest block.

This is obvious. If 'size' > 'maxSize', it means that the blocks corresponding to the first (size-maxSize) snapshotImpl are already solidified blocks, they can be placed on the disk, and then the snapshotImpl will be merged into the persistent storage. This ensures that snapshotImpl does not occupy too much memory, and also ensures that the solidified block can be persisted in time.


#### Atomicity

The database storage of java-tron is slightly different from other public chains. For example, the Ethereum persistence layer uses only one database instance, and different types of data in Ethereum are distinguished by prefixes and stored in one database instance. However, java-tron currently stores data of different business types in its own database instances.

The two implementations have their own advantages. A single instance is easy to maintain and can be written uniformly, but the disadvantages are also obvious. For example, the amount of data in a single database continues to grow over time, and frequent access to some business databases may drag down the read-and-write performance of other businesses. 

Multi-instance does not have the problem of the mutual influence of each business data read and write, and can configure different parameters according to their respective data volume and performance requirements to maximize performance, and can also independently split the database with a large amount of data. Alleviate data bloat problems. But there is a serious problem with multiple database instances: there is no native tool to support atomic writes among multiple database instances.

In order to ensure the atomic writing of multiple database instances, java-tron has added a checkpoint mechanism, which writes the changed data to the checkpoint uniformly before the multiple instances are placed on the disk. If an accident occurs in writing to multiple database instances, the changed data will be recovered from the checkpoint when the service is restarted to ensure the atomicity of writing.

The process of writing the snapshotImpl of the solidified block to the database in the previous section mainly includes two steps,


1. create a checkpoint
2. place snapshotImpl on disk

The operation of creating a checkpoint is more critical. A checkpoint is to persistently store the snapshotImpl in memory that needs to be written to the database in a tmp database (currently, the underlying implementation is leveldb and rocksdb). After the checkpoint is successfully created, the snapshotImpl will place on the disk. If the machine is down while placing, it will first search for the existence of tmp checkpoint data when the node restart. And if so, the data in the checkpoint will be played back to snapshotRoot.


A checkpoint data structure,

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/chainbase_9.png)



Checkpoint stores all data of a state change in one database. Different types of data are distinguished by prefixes. In order to ensure that all changed data can be placed on disk this time, the bottom layer of the database calls writeBatch() when writing. 


This solution can be summarized as,

- the atomicity of writes cannot be guaranteed among multiple database instances, but a single database (most mainstream databases) supports atomic writes
- the data set that needs to be guaranteed to be written atomically is first written to a temporary database by atomic writing, and then the data is written to different database instances; if an accident occurs, it can be recovered through the data of the temporary database

### Summary
This article analyzes the implementation details of rollback and database writing in the chainbase module through the processing flow of transactions and blocks and also analyzes the principle of atomic writing among multiple instances of the database to prevent database damage caused by accidental downtime. We hope that reading this article can help developers to further understand and develop the java-tron database.





## Network
### Overview
A Peer-to-Peer (P2P) network is a distributed architecture where participants share a portion of their hardware resources, such as processing power, storage capacity, network connection capacity, printers, etc. These shared resources need to be provided services and content by the network, which can be accessed by other peers directly without going through an intermediate entity. Participants in this network are both providers and acquirers of service and content.

Unlike traditional Client/Server architectures, all nodes in a P2P network have equal status. While serving as a client, each node can also serve as a server to provide services to other nodes, which greatly improves the utilization of resources.


#### Blockchain Network
P2P is the network layer in the blockchain structure. The main purpose of the network layer is to realize information broadcast, verification and communication between nodes. The blockchain network is essentially a P2P network, and each node can both receive and generate information. Nodes keep communication by maintaining common blockchain data.

As the foundation of the blockchain, the P2P network brings the following advantages to the blockchain:

* Prevent single-point attack
* High fault tolerance
* Better compatibility and scalability


#### TRON Network
The architecture diagram of TRON is as follows:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_architecture.png)

As the most fundamental module of TRON, the P2P network directly determines the stability of the entire blockchain network. The network module can be divided into the following four parts according to the function:

* Node Discovery
* Node Connection
* [Block Synchronization](#block-synchronization)
* [Block and Transaction Broadcast](#block-and-transaction-broadcast)

The underlying implementations of **Node Discovery** and **Node Connection** have been extracted from the java-tron repository into a standalone external dependency, [`io.github.tronprotocol:libp2p`](https://github.com/tronprotocol/libp2p). This library is responsible for low-level node discovery (based on the Kademlia algorithm) and connection transport, and it adds capabilities such as DNS-based node discovery. The TRON protocol layer above it — including the P2P_HELLO handshake, P2P_PING/P2P_PONG keep-alive, peer business-state management, message dispatch, synchronization, and broadcast — is still implemented in java-tron's `core/net`, which integrates with libp2p through `TronNetService`. For the low-level discovery and connection implementation details, please refer to the libp2p repository; they are no longer covered in this document.

**Block Synchronization** and **Block and Transaction Broadcast** are still implemented in java-tron's `core/net`, and are introduced separately below.

### Block Synchronization

After completing the handshake with the peer node, if the peer node's blockchain is longer than the local blockchain, the block synchronization process `syncService.startSync` will be triggered according to the longest chain principle. The message interaction during the synchronization process is as follows:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_syncflow.png)

Node A sends an `SYNC_BLOCK_CHAIN` message to peer node B to announce the blockchain summary information of the local chain. After the peer node B receives it, it calculates the list of missing blocks of node A, and sends the lost block ID list to node A through the `BLOCK_CHAIN_INVENTORY` message, carrying a maximum of 2000 block ids at a time.

After node A receives the `BLOCK_CHAIN_INVENTORY` message, it gets the missing block id, and sends a `FETCH_INV_DATA` message to node B asynchronously to request the missing block, up to 100 blocks at a time. If there are still blocks that need to be synchronized (that is, the remain_num in the `BLOCK_CHAIN_INVENTORY` message is greater than 0), a new round of block synchronization process will be triggered.

After node B receives the `FETCH_INV_DATA` message from node A, it sends the block to node A through the `BLOCK` message. After node A receives the `BLOCK` message, it asynchronously processes the block.

#### Blockchain Summary and List of Missing Blocks
Below will take several different block synchronization scenarios as examples to illustrate the generation of the blockchain summary and the lost block ID list. 

* Blockchain summary: an ordered list of block IDs, including the highest solidified block, the highest non-solidified block, and the blocks corresponding to the dichotomy.
* List of missing blocks: The neighbor node compares its own chain with the received blockchain summary, determines the missing blocks list of peers, and returns a set of consecutive block IDs and the number of remaining blocks.

##### Normal Synchronization Scene

The height of the local header block is 1018, and the height of the solidified block is 1000. The two nodes have just established a connection, so the height of the common block is 0. The local blockchain summary of node A obtained by the dichotomy is 1000, 1010, 1015, 1017, and 1018.

After node B receives the blockchain summary of node A, combined with the local chain, it can produce the list of blocks that node A lacks: 1018, 1019, 1020, and 1021. Then, node A requests to synchronize blocks 1019, 1020, and 1021 according to the list of missing blocks.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_sync1.png)


##### Chain-Switching Scene

The head block height of the local main chain is 1018, and the height of the solidified block is 1000. The two nodes have just established a connection, so the height of the common block is 0. The local blockchain summary of node A obtained by the dichotomy is 1000, 1010, 1015, 1017, and 1018.

After node B receives the chain summary of node A, it finds that the local main chain is not the same as the main chain of node A, compares the chain summary of node A and finds that the common block height is 1015, then it computes the list of blocks that node A lacks are 1015, 1016', 1017', 1018', and 1019'. Then, node A requests to synchronize blocks 1018' and 1019' according to the list of missing blocks.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_sync2.png)

In another switching chain scenario, the height of the local main chain header block is 1018, the height of the solidified block is 1000, and the common block is 1017', which is located on the fork chain. The local blockchain summary of node A obtained by the dichotomy is 1000, 1009, 1014, 1016', and 1017'.

After node B receives the chain summary of node A, combined with the local chain, it can produce the list of blocks that node A lacks 1017', 1018', and 1019'. Then, node A requests to synchronize blocks 1018', and 1019' according to the list of missing blocks.

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_sync3.png)

### Block and Transaction Broadcast

When the super representative node produces a new block, or the fullnode receives a new transaction initiated by the user, the transaction & block broadcasting process will be initiated. When a node receives a new block or new transaction, it will forward the corresponding block or transaction, and the forwarding process is the same as that of broadcasting. The message interaction is shown in the following figure:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_broadcastflow.png)

The types of messages involved include:

* `INVENTORY` - broadcast list: list of block or transaction ids
* `FETCH_INV_DATA` - the list data that the node needs to get: block or transaction id list
* `BLOCK` - block data
* `TRXS` - transaction data

Node A sends the transaction or block to be broadcast to Node B via the `INVENTORY` list message. After node B receives the `INVENTORY` list message, it needs to check the status of the peer node, and if it can receive the message, it puts the blocks/transactions in the list into the "to be fetched queue" `invToFetch`. If it is a block list, it will also trigger the "get block & transaction task" immediately to send a `FETCH_INV_DATA` message to node A to get the block & transaction.

After node A receives the `FETCH_INV_DATA` message, it will check whether an "INVENTORY" message has been sent to the peer. If it has been sent, it will send a transaction or block message to node B according to the list data. After node B receives the transaction or block message, it processes the message and triggers the forwarding process.

### Summary
This article introduces the P2P network, the lowest level module of TRON. Node discovery and node connection have been extracted into the external libp2p dependency and are only briefly located here; block synchronization and the process of block and transaction broadcasting, which remain in java-tron's `core/net`, are introduced in detail. I hope that reading this article can help developers to further understand and develop java-tron network-related modules.






