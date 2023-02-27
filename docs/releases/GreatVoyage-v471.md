# GreatVoyage-v4.7.1(Sartre)

GreatVoyage-v4.7.1(Sartre) introduces several important optimizations and updates. The optimized block synchronization logic improves the stability of block synchronization; the optimized node IP setting improves the availability of nodes; the optimized node log improves the maintainability of nodes.

Please see the details below.

## Cores
### 1. Optimize the node IP setting
When the node starts, it will obtain the local IP of the node, and then use this IP to communicate with other nodes in the network. If the node cannot access the external network, it will not be able to obtain the local IP. At this time, the node will set its local IP to the default value of 0.0.0.0, and this IP will make the node even unable to communicate with other nodes successfully in the LAN. So the GreatVoyage- v4.7.1 (Sartre) version changes the default IP of the node. If the node cannot obtain the local IP, it will set its local IP to 127.0.0.1, so that even if the node cannot access the external network, it can still communicate with other nodes in the LAN normally. 

Source code: [https://github.com/tronprotocol/java-tron/pull/4990](https://github.com/tronprotocol/java-tron/pull/4990)   

### 2. Optimize block synchronization logic
During the block synchronization process, the node will maintain a block request list, which contains the IDs of all blocks that have sent requests to other nodes. When the connection between the node and node A is abnormally disconnected with a very small probability, the block ID that is being requested to node A will be deleted from the request list. After that, the node will think that it has not requested the block, and then send the block request to node B and add the block ID to the request list again. Before this node disconnects with node A, the requested block may have already been sent by node A，and it is received by the node after disconnecting. Since the node found that the block is from node A that has already been disconnected, it will discard the block, and delete the block ID from the request list again, this will lead to the node to send a request for the same block to node B again. When Node B receives the repeated block request, it will consider it an illegal message and disconnect from the node.

In order to improve the efficiency of block synchronization in concurrent scenarios, the GreatVoyage-v4.7.1 (Sartre) version optimized the update mechanism of the block request list, and saved the block ID and node information in the request list at the same time. In the above scenario, after receiving a block from node A that has been disconnected, the same block ID requested from node B will not be deleted from the request list to ensure that it will not be disconnected from node B, thereby improving the stability of block synchronization.

Source code: [https://github.com/tronprotocol/java-tron/pull/4995](https://github.com/tronprotocol/java-tron/pull/4995) 

When a node synchronizes blocks from other nodes, it needs to obtain the local block chain summary of the node. The summary includes the IDs of several blocks including the local header block. In versions prior to GreatVoyage-v4.7.1 (Sartre), when obtaining the summary, the node will first query the Dynamic database to obtain the block height, and then query the Block database to obtain the ID of the block according to the block height. However, when the node is processing a block, the writing to each database is not carried out at the same time. The node will first update the Dynamic database, and then update other databases such as Block. As a result, in versions prior to GreatVoyage-v4.7.1 (Sartre), the following scenario will occur with a very small probability: when the latest block information is only written into the Dynamic database, but have not yet been written into the block database, the node starts to obtain the summary. In this situation the corresponding block ID will not be found in the block database according to the head block height obtained from the Dynamic database, leading to the summary reading fail. The GreatVoyage-v4.7.1 (Sartre) version optimizes the block chain summary acquisition logic. The ID of the head block is directly obtained from the Dynamic database instead of the Block database, which improves the stability of summary reading.


Source code: [https://github.com/tronprotocol/java-tron/pull/5009](https://github.com/tronprotocol/java-tron/pull/5009) 

The GreatVoyage-v4.7.1 (Sartre) version optimizes the lock mechanism during block synchronization and improves the stability of the node connection under concurrency.

Source code: [https://github.com/tronprotocol/java-tron/pull/4996](https://github.com/tronprotocol/java-tron/pull/4996) 

## API
### 1. Optimize the list of solidified block APIs
GreatVoyage-v4.7.1(Sartre) version deletes the useless solidified block query API to make the code more clearer.


Source code: [https://github.com/tronprotocol/java-tron/pull/4997](https://github.com/tronprotocol/java-tron/pull/4997)  
### 2. Optimize resource delegation relationship API
GreatVoyage-v4.7.1 (Sartre) version optimizes the resource delegation relationship query API, addes the check to the interface parameters, and makes the interface more stable.



## Other Changes


### 1. Optimize LiteFullNode detection logic
In versions prior to GreatVoyage-v4.7.1 (Sartre), different modules of the node have different logics for detecting whether the current node is a LiteFullNode. GreatVoyage-v4.7.1 (Sartre) version unifies the logic of light node judgment, making the code more concise.


Source code: [https://github.com/tronprotocol/java-tron/pull/4986](https://github.com/tronprotocol/java-tron/pull/4986)  


### 2. Optimize node log output

**The Database Log**

Starting from GreatVoyage-v4.7.0.1 (Aristotle), the logs of LevelDB or RocksDB databases are redirected to the node log file, which simplifies the difficulty of database troubleshooting. GreatVoyage-v4.7.1 (Sartre) further optimizes the log module, Output database logs to a separate db.log file to make node logs clearer.

Source code: [https://github.com/tronprotocol/java-tron/pull/4985](https://github.com/tronprotocol/java-tron/pull/4985) [https://github.com/tronprotocol/java-tron/pull/5001](https://github.com/tronprotocol/java-tron/pull/5001) [https://github.com/tronprotocol/java-tron/pull/5010](https://github.com/tronprotocol/java-tron/pull/5010)
 

**The Event Service Module Log**

Remove invalid logging output for event service module.

Source code: [https://github.com/tronprotocol/java-tron/pull/4974](https://github.com/tronprotocol/java-tron/pull/4974)  

**The network module log** 

Optimized the log output of the network module, outputting Error-level logs for received abnormal blocks, and outputting Warn-level logs for network requests that have already timed out, improving the efficiency of troubleshooting network-related problems.


Source code: [https://github.com/tronprotocol/java-tron/pull/4977](https://github.com/tronprotocol/java-tron/pull/4977)
 
--- 

*The more sand that has escaped from the hourglass of our life, the clearer we should see through it.* 
<p align="right"> ---Sartre</p>
