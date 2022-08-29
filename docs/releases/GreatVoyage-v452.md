
# GreatVoyage-v4.5.2(Aurelius)
The GreatVoyage-v4.5.2 (Aurelius) version introduces several important optimizations. The optimized transaction cache mechanism greatly reduces memory usage and improves node performance; the optimized P2P node connection strategy improves the efficiency of establishing connections between nodes and speeds up the node synchronization process;  the optimized block production and processing logic improve node stability; the newly added database storage partition tool reduces the pressure on data storage; the newly added block header query API and historical bandwidth unit price Query API are to bring users a more convenient development experience.


# Core
## 1. Optimize block processing 
In versions prior to GreatVoyage-v4.5.2 (Aurelius), threads such as block production, block processing, and transaction processing compete for synchronization lock at the same time. In the case of high concurrency and transactions executing much time, the block production thread or the block processing thread will take a long time to get to the synchronization lock, which leads to the occurrence of a small probability of a block loss event. In order to improve node stability, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the synchronization lock in the block processing logic, allowing only one transaction processing thread to compete for the synchronization lock with the block production or processing thread, and when the transaction processing thread finds that block-related threads waiting for the synchronization lock, it will voluntarily give in, which greatly increases the probability of block production and block processing threads acquiring synchronization lock, and ensures high throughput and stable operation of the node.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-428.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4551 

## 2. Optimize transaction cache
The node uses the transaction cache to determine whether the newly received transaction is a duplicate transaction. In versions prior to GreatVoyage-v4.5.2 (Aurelius), the transaction cache is a hashmap data structure, which saves transactions in the latest 65536 blocks. The hashmap allocates memory for each transaction separately. Therefore, the transaction cache will occupy nearly 2GB of memory during program runtime, meanwhile, frequent memory requests will trigger frequent JVM garbage collection which indirectly affects the performance of the node. To solve this issue, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the implementation of the transaction cache, using the bloom filter instead of the hashmap, the bloom filter uses a fixed and extremely small memory space to record recent historical transactions, which greatly reduces the memory usage of the transaction cache and improve the node performance.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-440.md
Source Code：https://github.com/tronprotocol/java-tron/pull/4538  




## 3. Optimize nodes connection strategy
In versions prior to GreatVoyage-v4.5.2 (Aurelius), when the number of remote nodes connected by a node has reached the maximum value, the node will reject connection requests from new remote nodes. With the increase of such fully connected nodes in the network, it will become more and more difficult for the newly added nodes to establish connections with other nodes in the network.

In order to speed up the connection process between nodes in the network, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the P2P node connection strategy. It will periodically check the number of TCP connections of the node. When the number of  connections is full, a certain disconnection strategy is adopted to disconnect one or two nodes to increase the possibility of a newly added node in the network successfully connecting to it, thereby improving the efficiency of establishing connections between P2P nodes in the network and improving network stability. Please note that the nodes configured in the `node.active` and `node.passive` lists in the configuration file are trusted nodes and will not be disconnected.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-425.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4549   



## 4. Optimize block generating logic
In versions prior to GreatVoyage-v4.5.2 (Aurelius), for pre-executed normal transactions, they may encounter JVM GC pauses during packaging which can result in transaction execution timeout and being discarded. Therefore, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the block generating logic. For a pre-executed normal transaction, if it executes time out during packaging, a retry operation is taken to avoid transaction discard caused by JVM GC pause during the packaging.

Source Code：https://github.com/tronprotocol/java-tron/pull/4387 

## 5. Optimize fork switching logic
Micro-forks occur in the TRON network occasionally. The chain switching behavior will occur when a micro-fork happens.  The chain switching will roll back blocks, and the transactions in the rolled back block will be put back into the transaction pending queue. When these transactions are repackaged and executed, the execution results may be inconsistent due to chain switching. In versions prior to GreatVoyage-v4.5.2 (Aurelius), the entire process refers to the same transaction object, so chain switching may lead to the transaction result in the rolled back block being changed. When the chain switching occurs again and the original chain is switched back, the transaction on the original chain will be executed again, at this time, it will report a `Different resultCode` error, which will cause the node to stop synchronizing. 

Therefore, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the chain-switching logic. When a block is rolled back, a new transaction object is created for the transaction in the rolled-back block, so as to avoid the modification of the transaction result and improve the node's stability for fork handling.


Source Code：https://github.com/tronprotocol/java-tron/pull/4583 

## 6. Add database storage partition tool
As the data on the chain grows, the disk space of the FullNode may be insufficient, and a larger capacity disk needs to be replaced. So starting from the GreatVoyage-v4.5.2 (Aurelius) version, a database storage partition tool is provided, which can migrate some databases to other disk partitions according to the user's configuration, so users only need to add disks according to capacity requirements, no need to replace the original disk, that is convenient for users to expand the disk capacity, and at the same time reduces the cost of running a node.


Source Code：https://github.com/tronprotocol/java-tron/pull/4545 
https://github.com/tronprotocol/java-tron/pull/4559 
https://github.com/tronprotocol/java-tron/pull/4563 


 
# API
## 1. New block header query API

From the GreatVoyage-v4.5.2 (Aurelius) version, a new block header query API is added, which only returns the block header information, not the transaction information in the block. Users can obtain the block header information without querying the entire block. This not only reduces the network I/O load of the node, and since the block does not carry transaction information, the serialization time is reduced, the interface delay is reduced, and the query efficiency is improved.
 
Source Code：https://github.com/tronprotocol/java-tron/pull/4492 
https://github.com/tronprotocol/java-tron/pull/4552 

## 2. New historical bandwidth unit price query API
According to the bandwidth consumption rules, if the transaction initiator’s  bandwidth obtained by staking TRX or free bandwidth is insufficient, TRX will be burned to pay for the bandwidth fee. At this time, only the bandwidth fee is recorded in the transaction record, but not the bandwidth consumption number. In order to understand bandwidth consumption of historical transactions, starting from GreatVoyage-v4.5.2 (Aurelius), a new historical bandwidth unit price query API `/wallet/getbandwidthprices` is added. Users can obtain historical records of bandwidth unit price through this API so that they can calculate bandwidth consumption of historical transactions.

Source Code：https://github.com/tronprotocol/java-tron/pull/4556 

# Other Changes
## 1. Optimize block synchronization logic
The GreatVoyage-v4.5.2 (Aurelius) version optimizes the block synchronization logic, avoids unnecessary node disconnection in the process of synchronizing blocks, and improves node stability.

Source Code：https://github.com/tronprotocol/java-tron/pull/4542 
https://github.com/tronprotocol/java-tron/pull/4540 
## 2. Optimize `eth_estimateGas` and `eth_call` API
The GreatVoyage-v4.5.2 (Aurelius) version optimizes the `eth_estimateGas` and `eth_cal` JSON-RPC interfaces; they can return error information when smart contract transaction execution is interrupted.

Source Code：https://github.com/tronprotocol/java-tron/pull/4570 

## 3. Enhance the fault tolerance of the interface
The GreatVoyage-v4.5.2 (Aurelius) version optimizes multiple API interfaces, enhances its fault tolerance for parameters, and improves the stability of API interfaces.

Source Code：https://github.com/tronprotocol/java-tron/pull/4560 
https://github.com/tronprotocol/java-tron/pull/4556 
 
--- 

*The universe is change; our life is what our thoughts make it.* 
<p align="right"> ---  Aurelius</p>