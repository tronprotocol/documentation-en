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

> For a detailed walkthrough of the ChainBase module — transaction processing, state rollback, block solidity, and data persistence — see [ChainBase Deep Dive](chainbase.md).


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

> The networking layer above lives in `core/net`. For a detailed walkthrough of the P2P network subsystem — block synchronization, and block & transaction broadcast — see [P2P Network Deep Dive](network.md).

### Summary
This article mainly introduces the code structure of java-tron, as well as the function, location and directory structure of each functional module. Through this article, you will have a general understanding of the overall structure and key interfaces of java-tron, which is helpful for subsequent code analysis and development.
