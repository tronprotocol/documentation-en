# Java-tron Code Structure
Java-tron is a TRON network client developed based on the Java language. It implements all the functions mentioned in the TRON white paper, including consensus mechanism, cryptography, database, TVM virtual machine, network management, etc. We can run a TRON node by starting Java-tron. In this article, we will describe the code structure of Java-tron in detail, and introduce the functions of its various modules, to facilitate the subsequent code analysis and development of developers.

Java-tron adopts a modular code structure; the code structure is clear and easy to maintain and expand. Currently Java-tron is divided into 7 modules: [protocol](#protocol), [common](#common), [chainbase](#chainbase), [consensus](#consensus), [actuator](#actuator), [crypto](#crypto), [framework](#framework), the following introduces the functions of each module and its code organization.



## protocol

For a distributed network such as blockchain, a concise and efficient data interaction protocol is very important. The protocol module defines:

* Inter-node communication protocol
* Communication protocol between modules within the node
* Agreement for Services Provided Externally

The above protocols adopt the [`Google Protobuf`](https://developers.google.com/protocol-buffers) data exchange format. Compared with JSON and XML, the `Google Protobuf` format is more efficient and flexible and can be compiled by the ProtoBuf compiler to generate language-specific serialization and deserialization source code for the defined protocol files. Protobuf is the basis for java-tron to achieve cross-language and cross-platform.

[protocol](https://github.com/tronprotocol/java-tron/tree/develop/protocol) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/protocol` , its directory structure is as follows:

```
|-- protos
    |-- api
    |   |-- api.proto
    |   |-- zksnark.proto
    |-- core
        |-- Discover.proto
        |-- Tron.proto
        |-- TronInventoryItems.proto
        |-- contract
```

* `protos/api/` - The gRPC interface and data structure provided by the Java-tron node externally
* `protos/core/` - Data structure for communication between nodes and between modules within nodes
    * `Discover.proto` - Node discovers related data structures
    * `TronInventoryItems.proto` - Data structure related to block transferring between nodes
    * `contract/` - Contract related data structures
    * `Tron.proto` - Other important data structures, including accounts, blocks, transactions, resources, super representatives, voting, and proposals...



## common

The common module encapsulates common components and tools, such as exception handling, metrics monitoring tools, etc which make it easy to use by other modules.

[common](https://github.com/tronprotocol/java-tron/tree/develop/common) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/common`, its directory structure is as follows:

```
|-- /common/src/main/java/org/tron
    |-- common
    |   |-- args
    |   |-- config
    |   |-- entity
    |   |-- logsfilter
    |   |-- overlay
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
```


* `common/prometheus` - Prometheus metrics monitoring
* `common/utils` - The wrapper class of basic data type
* `core/config` - Node configuration related classes
* `core/exception` - All exception handling related classes




## chainbase

Chainbase is a database module. For probabilistic consensus algorithms such as PoW, PoS and DPoS, situations of switching to a new chain, however unlikely, are inevitable. Because of this, chainbase defines an interface standard supporting databases that can roll back. This interface requires databases to have a state rollback mechanism, a checkpoint-based disaster tolerant mechanism and so on. 

In addition, the chainbase module features a well-designed abstract interface. Any database that implements the interface can be used for underlying storage on the blockchain, granting more flexibility to developers. LevelDB and RocksDB are two default implementations.

[chainbase](https://github.com/tronprotocol/java-tron/tree/develop/chainbase) module's source code is located at: `https://github.com/tronprotocol/java-tron/tree/develop/chainbase`, its directory structure is as follows:
```
|-- chainbase.src.main.java.org.tron
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
    
        Implemented rollbackable databases, including two rollbackable databases: `AbstractRevokingStore` located in the `db/` directory and `SnapshotManager` located in the `db2/` directory. Compared with `AbstractRevokingStore`, `SnapshotManager` has a more stable data rollback function and supports the extension of the underlying database. Therefore, Java-tron uses `SnapshotManager` to roll back the database. Several important interfaces and implementation classes are as follows:

        * `RevokingDatabase.java` - It is the interface of the database container, used to manage all rollbackable databases, `SnapshotManager` is an implementation of this interface
        * `TronStoreWithRevoking.java` - It is the base class that supports rollbackable databases. All rollbackable databases are their implementations, such as `BlockStore`, `TransactionStore`, etc
    

## consensus

The consensus mechanism is a crucial module in blockchains. Common ones are PoW, PoS, DPoS and PBFT, etc. While Paxos, Raft, etc, are applied to consortium blockchains and other trusted networks. The consensus mechanism should match the business scenario. For instance, PoW is not suitable for real-time games that are sensitive to consensus efficiency, while PBFT can make an optimized choice for exchanges demanding high real-time capability. In this sense, a replaceable consensus is a creative innovation and an essential link in building application-specific blockchains. Even star blockchain programs like Cosmos SDK are still at a stage where the application layer provides developers with limited autonomy and the consensus at the base level is subject to Tendermint. Therefore, the ultimate goal of the consensus module is to make consensus switch as easy as configuring parameters for application developers.

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
consensus module divides the consensus process into several important parts that are defined in `ConsensusInterface`:

1. `start` - start the consensus service with customizable startup parameters
2. `stop` - stop the consensus service
3. `receiveBlock` - define the consensus logic of receiving blocks
4. `validBlock` - define the consensus logic of validating blocks
5. `applyBlock` - define the consensus logic of processing blocks

Currently, Java-tron implements DPOS consensus and PBFT consensus based on the `ConsensusInterface` interface, which is located in the `dpos/` and `pbft/` directories respectively. Developers can also implement the `ConsensusInterface` interface according to their own business needs to customize the consensus mechanism.


## actuator

Ethereum was the first to introduce the virtual machine and define the smart contract. However, smart contracts are constrained in terms of their functions and not flexible enough to accommodate the needs of complex applications. This is one of the reasons why java-tron supports the creation of a chain of applications. For the reasons mentioned, java-tron includes a separate module, Actuator, offering application developers a brand new way of development. They can choose to implant their application codes into a chain instead of running them on virtual machines. 

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

* `actuator/` - The executors of various types of transactions in the TRON network which define the processing logic of different types of transactions. For example, `TransferActuator` is the processing class for transferring TRX, and `FreezeBalanceActuator` is the processing class for staking TRX to obtain resource
* `utils/` - tools needed to execute transaction
* `vm/` - TRON virtual machine related code

Actuator module defines the `Actuator` interface, which includes 4 different methods:

* `execute` - execute specific actions of transactions, such as state modification, communication between modules, logic execution, etc.
* `validate` - validate authenticity of transactions
* `getOwnerAddress` - acquire the address of transaction initiators
* `calcFee` - define the logic of calculating transaction fees

Depending on their businesses, developers may set up Actuator accordingly and customize the processing of different types of transactions.
 
## crypto
Crypto is a relatively independent module, but it is also a very important module. Data security in Java-tron is almost entirely guaranteed by this module. Currently, SM2 and ECKey encryption algorithms are supported.

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

## framework

The framework is the core module of java-tron and the entrance of the node. The framework module is responsible for the initialization of each module and business logic. The framework module includes the services provided externally, the node discovery and node management process related to the P2P network, and the block broadcasting and processing procedures.

[framework](https://github.com/tronprotocol/java-tron/tree/develop/framework) module's source code is located at:  `https://github.com/tronprotocol/java-tron/tree/develop/framework`, its directory structure is as follows:

```
|-- framework/src/main/java/org/tron
    |-- common
    |   |-- application
    |   |-- backup
    |   |-- logsfilter
    |   |-- net
    |   |-- overlay
    |   |   |-- client
    |   |   |-- discover
    |   |   |-- message
    |   |   |-- server
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
    |-- tool
```

* `program/FullNode.java` - It is the entry point of the program and initializes external HTTP, gRPC and json-rpc interface services
* `core/services` - Defines the externally provided services, its subdirectory `http/` contains all http interface processing classes, `json-rpc/` contains all json-rpc interface processing classes
* `common/overlay/discover` - Node discovery logic
* `common/overlay/server` - Node management and block synchronization logic among nodes
* `core/net` - Message processing, its subdirectory `/service` is  transaction and block broadcasting, block fetching and synchronization logic
* `core/db/Manager.java` - Transaction and block verification and processing logic

## Summary
This article mainly introduces the code structure of Java-tron, as well as the function, location and directory structure of each functional module. Through this article, you will have a general understanding of the overall structure and key interfaces of Java-tron, which is helpful for subsequent code analysis and development.

