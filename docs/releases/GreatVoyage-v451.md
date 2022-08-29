# GreatVoyage-v4.5.1(Tertullian)
The GreatVoyage-v4.5.1(Tertullian) version introduces several important optimization updates. The optimized transaction cache loading process shortens the node startup time; the optimized block acquisition logic and light node synchronization logic promote the stability of the node; the optimized account asset structure and TVM cache structure improves the processing speed of transactions, thereby further improving the performance of node; supporting prometheus protocol interface brings users a more convenient development experience and helps to further prosper the TRON ecosystem.



# Core
## 1. Optimize transaction cache loading
In versions prior to GreatVoyage-v4.5.1 (Tertullian), it took a long time from node startup to block synchronization, and the loading of the transaction cache took up most of the node startup time. The transaction cache is used by the node to determine whether a transaction is a duplicate transaction, so during the node startup process, the transaction cache needs to be loaded from the database to the memory, and in versions prior to GreatVoyage-v4.5.1 (Tertullian), it adopts transaction as the storage unit to read the database when loading the transaction cache, so the amount of data to be read is large, and the entire reading process is time-consuming.

In order to speed up the startup of the node, the GreatVoyage-v4.5.1 (Tertullian) version optimizes the loading of the transaction cache. By adopting the block as the storage unit to read the database reduces the times of database reading,  improves the efficiency of transaction cache loading, and improves the speed of node startup.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-383.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4319 

## 2. Optimize account TRC-10 asset storage structure
In versions prior to GreatVoyage-v4.5.1 (Tertullian), when there were too many TRC10 assets in the account, the content of the account stored in the database was large, resulting in the deserialization of the account during the transaction execution process is very time-consuming , therefore, the GreatVoyage-v4.5.1 (Tertullian) version adds a new proposal to optimize the asset structure of the account, allowing TRC-10 assets to be separated from the account and stored separately in a key-value data structure. That will reduce the content of the account structure, speed up the deserialization operation of the account and reduce the execution time of the transaction, thereby increasing the network throughput and improving the network performance.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-382.md  
Source Code: https://github.com/tronprotocol/java-tron/pull/4392 

## 3. Optimize light node synchronization
Since light nodes do not store complete block data, there is a possibility that a node connects to a light node which does not have the block the node wants to synchronize with, in this situation, the light node will actively disconnect the connection. In versions prior to GreatVoyage-v4.5.1 (Tertullian), nodes may repeatedly establish connections with such light nodes, and then be disconnected by the other part, which greatly affects the efficiency of synchronizing blocks between nodes. Therefore, in the GreatVoyage-v4.5.1 (Tertullian) version, the logic of establishing a connection with light nodes has been optimized, and the two fields of "node type" and "node's lowest block" are added to the handshake message between nodes, and the nodes will save the handshake messages with each node. If the highest block of the current node is lower than the lowest block of the light node, it will actively disconnect from the light node, and the next time it establishes a connection with the node, it will filter out such nodes to avoid more invalidations connection, which improves the efficiency of synchronization between nodes.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-388.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4323  



## 4. Optimize block broadcasting
The GreatVoyage-v4.5.1 (Tertullian) version optimizes the block broadcast logic, so that the fast forward node only broadcasts the block to the three super representative nodes that will produce blocks next (the number of broadcasted super representative nodes can be changed through the configuration file) to ensure that the super representative node can obtain the latest block in time, which improves the efficiency of block production.


Source Code: https://github.com/tronprotocol/java-tron/pull/4336 

## 5. Optimize fetch block process
Due to network reasons, the node may not receive the new broadcasted block. In versions before GreatVoyage-v4.5.1 (Tertullian), when the block acquisition times out, the node will acquire the block through the P2P synchronization process, but the process is complicated and time-consuming. Therefore, the GreatVoyage-v4.5.1 (Tertullian) version optimizes the process of obtaining the latest block. The node will first select a node according to the status of each node, and then directly send the block obtaining message `FetchInvDataMessage` to this node to obtain the latest block, which saves most of the time in the block synchronization process, speeds up the acquisition of the latest block, and improves the stability of the node.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-391.md
Source Code: https://github.com/tronprotocol/java-tron/pull/4326 

## 6. Support prometheus metric protocol interface
Starting from the GreatVoyage-v4.5.1 (Tertullian) version, the node provides an open source system monitoring tool - prometheus’s protocol interface, and users can monitor the health status of the node more conveniently.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-369.md  
Source Code: https://github.com/tronprotocol/java-tron/pull/4337 

## 7. Support node stop at specified condition
In order to facilitate node deployers to do data backup or data statistics, starting from the GreatVoyage-v4.5.1 (Tertullian) version, the node could stop running under specific conditions. Users can set the conditions for node stop through the node configuration file, such as the node stop’s block time, block height, and the number of blocks the node needs to synchronize from start to stop. The node will stop running automatically when the set conditions are met.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-370.md  
Source Code: https://github.com/tronprotocol/java-tron/pull/4325 


# TVM
## 1. Adjust the upper limit that can be set for the maximum execution time of TVM
"TVM maximum execution time" is a dynamic parameter of the TRON network, indicating the maximum time allowed for a smart contract to be executed. Super representatives can change this parameter through proposal voting. In versions prior to GreatVoyage-v4.5.1 (Tertullian), the maximum value that this parameter can be modified is 100ms. With the stability of the TRON network infrastructure and the vigorous development of the ecology, the 100ms upper limit confines the complexity of smart contracts. Therefore, GreatVoyage-v4.5.1 (Tertullian) version adds a new proposal that allows to raise the configurable upper limit of "TVM maximum execution time" to 400ms.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-397.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4375 


## 2. Optimize the cache structure of TVM
In versions prior to GreatVoyage-v4.5.1 (Tertullian), the cached data in TVM is stored in the form of a byte array. When the data in the cache needs to be changed, the data must first be converted from the form of a byte array to a protobuf object by performing a serialization operation, then change a field of the object (such as account balance, etc.) to generate a new object, then serialize the newly generated protobuf object to byte array, and at last write the result byte array to TVM cache. Since the serialization and deserialization of protobuf is time-consuming, the GreatVoyage-v4.5.1 (Tertullian) version optimizes the data structure in the cache when TVM is executed, and directly saves the protobuf object data to reduce the serialize/deserialize operations when accessing the data in the cache, speeding up TVM execution of bytecode.


Source Code: https://github.com/tronprotocol/java-tron/pull/4375   


--- 

*Hope is patience with the lamp lit.* 
<p align="right"> --- Tertullian </p>