# Odyssey-v3.7
Odyssey-v3.7 is a non-mandatory upgrade, includes the following new features and improvements.

## Modularization
Odyssey-v3.7 has modularized the code organization structure, making it much easier for developers to develop customized module，several mainly modules are listed as follows：

### Framework
As the core module, Framework performs as both a gateway to the blockchain and an adhesive that effectively connects all other modules. In other words, the framework module initializes each module and facilitates communication between modules.

### Protocol
The decentralized Tron protocol can be implemented by any teams without limitation of programming languages. Any clients in accordance with the Tron protocol can communicate with each other.
A concise and efficient data transfer protocol is essential to a distributed network, even more for the blockchain. So, the implementation of the protocol is based on the Protocol Buffers, an open-source and excellent software protocol maintained by Google. 
The specific business logic of the blockchain defined by the protocol includes:
- the data format of message，including block, transaction, proposal, witness, vote, account, exchange and so on.
- the communication protocols between blockchain nodes, including the node discovery protocol, the node data synchronization protocol, the node scoring protocol and so on.
- the interface protocols that the blockchain provides to the external system or clients

### Consensus 
The consensus mechanism is an essential part of the blockchain. The Tron blockchain chooses the DPoS as the core consensus mechanism and it has been running steadily for a long time. But replaceable consensus module is essential if we want to redefine the java-tron as the powerful infrastructure for building application-specific blockchains. The developers of blockchain should determine to choose the consensus mechanism that considered to be most suitable to the specific application scenario. The ultimate goal of the replaceable consensus module is that the consensus mechanism can be determined by configuring some necessary parameters. In addition, the developers can implement a customized consensus module as long as several essential interfaces implemented.

### Crypto
Encryption is also one of the core modules of the blockchain. It is the foundation of the
blockchain data security. such as public and private key deduction, transaction verification, zero-knowledge proof, etc. The java-tron abstracts the encryption module and supports the replacement of encryption algorithms. A suitable encryption algorithm can be chosen according to different business needs.

### Actuator
Actuator is the core module used for handling various kinds of transactions. As you know, every transaction in the Tron blockchain contains a contract. On a high level, there are two types of contracts in the Tron blockchain, the system contract and the smart contract. A large number of applications are implemented by the smart contracts and ran in an internal virtual machine of the blockchain. Unfortunately, smart contracts are constrained in terms of their functions and not flexible enough to accommodate the needs of complex applications. Customized actuators offer application developers a brand new way of development. They can choose to implant their application codes into the chain instead of running them on virtual machines.

### Chainbase
Chainbase is specially designed for data storage in the blockchain. Nodes always consider the longest chain to be the correct one and will keep working on extending it. So switching to the longest chain is a common scenario for the blockchain unless it uses a deterministic consensus algorithm like PBFT. For this reason, supporting data rollback is the most distinctive feature of the chainbase module. Several well-designed abstract interfaces are defined in this module. So, the developers can choose the storage engine freely and then implement corresponding interfaces. The LevelDB and RocksDB are two existing implementation.

## New event subscription trigger for solidified block
Added a subscription trigger for the updating a solidified block, which triggers the solidified block update event to the message queue, so that users can get the latest solidified block information on time. A solidified block is a block that regarded as can not be revocable. So, when the block becomes a solidified block, it means that the transactions packed in this block are accepted by the blockchain.

## Two new HTTP APIs added
**gettransactioninfobyblocknum**

This api is both added in the context: /wallet & /walletsolidity.
* Description: Query the list of information of transactions in a specific block.
* Parameter num: the height of the block.
* Return: The list of transaction information.

**broadcasthex**

/wallet/broadcasthex
* Description: broadcast signed transaction with the format of the hex string
* Parameter: signed transaction with the format of the hex string
* Return: the result of the broadcast

## A new RPC API added
Adding the `GetTransactionInfoByBlockNum` method both in `Wallet` `WalletSolidity` services：
```proto
rpc GetTransactionInfoByBlockNum (NumberMessage) returns (TransactionInfoList) {
}
```
a code snippet：
```
NumberMessage.Builder builder = NumberMessage.newBuilder();
builder.setNum(blockNum);
TransactionInfoList transactionInfoList = blockingStubFull.getTransactionInfoByBlockNum(builder.build());
```