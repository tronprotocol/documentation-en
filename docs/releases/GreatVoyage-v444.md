# GreatVoyage-4.4.4(Plotinus)
The GreatVoyage-v4.4.4 (Plotinus) version introduces several important optimization updates, which reduces the node memory usage; speeds up node startup; Optimized network module, block production threads, improve the stability of nodes; Improved java-tron upgrade mechanism achieves more efficient decentralized governance; TVM supports multi-version program executors, which helps make it more compatible with EVM, brings users a more convenient development experience, and helps further flourish the TRON ecosystem.

# Core
## 1. Optimize node startup time

Before the GreatVoyage-v4.4.4 (Plotinus), the node will execute about a minute from startup to block synchronization. The block synchronization thread will first delay 30s to wait for the P2P thread to discover remote nodes, then establish TCP connection with the discovered nodes, and finally perform the block synchronization. This delay time occupies most of the startup time. In fact, every newly discovered node will be persisted to the local database, so there is no need to spend extra time waiting for the node to be discovered when node is started for the second time. So in the GreatVoyage-v4.4.4(Plotinus) version, the waiting time for node discovery has been reduced from 30s to 100ms to improve the speed of node startup.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-366.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4254  


## 2. Optimize memory usage
In order to avoid repeatedly broadcasting a transaction, the node will cache the transaction data into the broadcast data buffer. However,due to the limitation of the JVM's recycling policy, old cached data cannot be deleted in time until the buffer is full. Therefore, a buffer with a larger capacity will occupy a large amount of memory space. Before the GreatVoyage-v4.4.4 (Plotinus) version, the buffer pool size was 100000 transactions. In order to release the memory occupied by expired transactions in time , the GreatVoyage-v4.4.4 (Plotinus) version changed the buffer size to 20000 to reduce memory usage.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-362.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4250 


## 3. Optimize the block-producing thread

The GreatVoyage-v4.4.4 (Plotinus) version adds the interrupt exceptions handling in block-producing thread, so that when the block-producing node catches the interrupt instruction, it can exit safely.


Source Code：https://github.com/tronprotocol/java-tron/pull/4219 



# TVM
## 1. TVM support multi-version program-executors

In order to enable the TRON network to support various types of smart contract transactions in the future, starting from GreatVoyage-v4.4.4 (Plotinus), TVM code is refactored to support multi-version program  executors, it will select different instruction set to interpret and execute the bytecode of smart contract according to the contract version information.

Source Code：https://github.com/tronprotocol/java-tron/pull/4257 
                             https://github.com/tronprotocol/java-tron/pull/4259 

# Other Changes

## 1. Optimize log storage

The GreatVoyage-v4.4.4 (Plotinus) version modifies the node log retention time from 3 days to 7 days to facilitate users to troubleshoot issues.

Source Code：https://github.com/tronprotocol/java-tron/pull/4245 


## 2. Optimize network service shutdown logic

The GreatVoyage-v4.4.4(Plotinus) version optimizes the network service shutdown logic, closing the synchronization service first, and then closing the TCP connection service to ensure that all P2P connection related services exit safely.


Source Code：https://github.com/tronprotocol/java-tron/pull/4220 


## 3. improve the Java-tron upgrade mechenism
For upgrade mechanism of java-tron,Before the GreatVoyage-v4.4.4 (Plotinus) version,all 27 super representative nodes need to complete the code upgrade, TRON network can be upgraded to the new version,TRON is a completely decentralized governance network,Sometimes the 27 super representative nodes cannot complete the code upgrade within a certain period of time, making the version upgrade process slow.In order to achieve more efficient decentralized governance, in GreatVoyage-v4.4.4 (Plotinus), the upgrade mechanism of Java-tron has been improved, only 22 super representative nodes are needed to complete the code upgrade, and the TRON network can complete the upgrade.

Source Code：https://github.com/tronprotocol/java-tron/pull/4218

---
*The world is knowable, harmonious, and good.* 
<p align="right"> --- Plotinus </p>