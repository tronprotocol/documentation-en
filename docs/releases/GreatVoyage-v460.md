# The GreatVoyage-v4.6.0 (Socrates)

The GreatVoyage-v4.6.0 (Socrates) introduces several important optimizations and updates, such as an optimized database checkpoint mechanism, which improves the stability of node operation; optimized resource delegate relationship index structure, and an updated voting reward algorithm, which speed up the execution speed of transactions and increase network throughput; a new proposal to add transaction memo fees, increasing the cost of transactions with memo to reduce the number of low-value transactions, so that improves the security and reliability of the TRON network. The integrated toolkit, new network-related Prometheus metrics, and new help command line together bring users a more convenient development experience.

Please check below for details.


## Core
### 1. Optimize delegate relationship index structure

In the TRON network, accounts can delegate resources to other accounts through staking, and can also accept resources that other accounts stake for themselves. Therefore, each account needs to maintain a record of the delegate relationship, including all the recipient addresses that the account delegated resources to and all the addresses that delegated resources for the account.

In versions prior to GreatVoyage-v4.6.0 (Socrates), the delegate relationship is stored in the form of a list. When performing resource delegating, it needs first to check whether the recipient account already exists in the list and then adds the account to the list only if it is not present. If a particular account has delegated resources to multiple accounts or many accounts have delegated the resources to the particular account, then the length of the delegate relationship list for the particular account will be substantial. The lookup operation would be considerably time-consuming, resulting in long transaction execution times. 

Therefore,  GreatVoyage-v4.6.0 (Socrates) optimizes the index storage structure of the resource delegate relationship and changes it from a list to a key-value pair, so as to complete the querying and modification of its data in a constant time, which greatly speeds up the execution speed of the delegation related transactions and improves network throughput.

The delegate relationship storage optimization is a dynamic parameter of the TRON network. It is disabled by default and can be enabled by initiating a proposal.

* TIP: [https://github.com/tronprotocol/tips/issues/476](https://github.com/tronprotocol/tips/issues/476) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4788](https://github.com/tronprotocol/java-tron/pull/4788)  

### 2. Add transaction memo fee proposal
Starting from GreatVoyage-v4.6.0 (Socrates), a memo fee will be charged for transactions with a memo. By increasing the cost, the fee will reduce the number of low-value transactions, so as to improve the security and reliability of the TRON network.

The memo fee is a dynamic parameter of the TRON network. After GreatVoyage-v4.6.0 (Socrates) is deployed, the default value is ‘0’, and the unit is ‘sun’. It can be enabled by specifying a non-zero value by initiating a proposal, for example, ‘1000000’, indicating that the transaction with memo will require an additional 1 TRX fee.

* TIP: [https://github.com/tronprotocol/tips/issues/387](https://github.com/tronprotocol/tips/issues/387) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4758](https://github.com/tronprotocol/java-tron/pull/4758)  



### 3. Add optimized reward algorithm proposal
Many voters in the TRON network will accumulate rewards for a long time before withdrawing them. The interval between two withdrawals of rewards is often very long. In versions prior to GreatVoyage-v4.6.0 (Socrates), for the transaction to withdraw rewards, it will calculate and accumulate rewards for each maintenance period since the last withdrawal of rewards, so the longer the time since the last withdrawal of rewards, the more time-consuming it will be to calculate the reward. Therefore, GreatVoyage-v4.6.0 (Socrates) optimizes the calculation algorithm of voting rewards. Instead of accumulating the rewards of each maintenance period, the sum of unwithdrawn rewards can be obtained by subtracting the total number of rewards recorded in the maintenance period of the last reward withdrawal from the total rewards recorded in the previous maintenance period. This algorithm realizes the calculation of the total number of unclaimed rewards in a constant time, which greatly improves the calculation efficiency and speeds up the execution of reward calculation, thereby improving the throughput of the network.

The optimized reward algorithm is a TRON network parameter and is disabled by default once GreatVoyage-v4.6.0 (Socrates) is deployed, and can be enabled by voting through a proposal.

* TIP: [https://github.com/tronprotocol/tips/issues/465](https://github.com/tronprotocol/tips/issues/465) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4694](https://github.com/tronprotocol/java-tron/pull/4694) 



### 4. Upgrade checkpoint mechanism to v2 in database module

The Checkpoint is a recovery mechanism established to prevent database damage caused by the exceptional shutdown. Java-tron uses memory and multi-disk databases for data storage. The data of the solidified block will be stored in multiple business databases. Unsolidified data is stored in the memory. When a block is solidified, the corresponding memory data will be written to relevant databases. However, since the writing to multiple business databases is not an atomic operation, if there is an unexpected downtime due to some reason, then all the data in the block may not be able to be written to the disk, and the node will not be able to restart due to database corruption.

Therefore, before the memory data is written to the disk, a checkpoint would be created. The checkpoint contains all the data that needs to be written to each business database this time. After the checkpoint is created, first writes the checkpoint data to an independent Checkpoint database, and then performs the operation of writing the business database, and the Checkpoint database always retains the latest solidified block data. If the business database is damaged due to system shutdown, after the node restarts, the business database will be recovered through the data previously saved in the checkpoint database.

At present, the Checkpoint mechanism can deal with the vast majority of downtime situations, but there is still a small probability that the business database will be damaged due to downtime. At present, the data writing of LevelDB is asynchronous. The program calls LevelDB to request to write the data to the disk. In fact, the data is only written into the cache of the operating system, and then the operating system will decide when to actually write to the disk according to its own strategy. If an unexpected downtime occurs at the time when the node just finished writing to the Checkpoint database and continues to write to the business database, it is possible that the data written to the Checkpoint database is not actually written to the disk by the operating system. In this case, the node would fail to restart properly because the Checkpoint database has no recovery data.

In order to solve this problem, GreatVoyage-v4.6.0 (Socrates) upgrades the V2 version of Checkpoint implementation. The Checkpoint mechanism V2 will store multiple solidified blocks data. So that even if the latest solidified block data is not written successfully to the Checkpoint database due to abnormal shutdown, the historical solidified block data can be used to restore the business database when the node restarts.

The  Checkpoint mechanism V2 is disabled by default in the configuration file. This function can be enabled by modifying the configuration. It should be noted that if a node has enabled the checkpoint V2 and has been running for a certain period of time, it would not be able to roll back to V1 anymore.

* TIP: [https://github.com/tronprotocol/tips/issues/461](https://github.com/tronprotocol/tips/issues/461) 
* Source code:  [https://github.com/tronprotocol/java-tron/pull/4614](https://github.com/tronprotocol/java-tron/pull/4614)  
### 5. Optimize block production priority between active and backup nodes 

If the super representative deploys the active and backup nodes, the connection between the nodes will be maintained. When the active and backup nodes are temporarily disconnected due to network problems, the backup node will consider that the active node is invalid and take over the block production. This will cause a duplicate block production process as both the active and backup nodes will produce blocks at the same time. In versions prior to GreatVoyage-v4.6.0 (Socrates), when the active and backup nodes receive blocks of the same height block generated by each other, both of them will suspend for 1-9 block production cycles. That is, the super representative will miss 1-9 blocks.

The GreatVoyage-v4.6.0 (Socrates) optimizes the priority of block production logic. When the situation above happens, both nodes will compare the hash value of the block produced by the other node. The node with a larger block hash will continue to produce blocks, and the node with smaller block hash will suspend a block production cycle, then continue to produce blocks, and compare the block hash again. A total of 27 super representatives will generate blocks sequentially, so it takes 81 seconds to skip a block production cycle. During this period, if the connection problem between them is a short-term network failure, there will be enough time to recover it. In addition, after receiving these two blocks, other nodes will also choose the block with a larger hash and discard the one with a smaller hash. This implementation will significantly improve the block production efficiency during obstructed network connections between active and backup nodes and network stability.


* Source code：[https://github.com/tronprotocol/java-tron/pull/4630](https://github.com/tronprotocol/java-tron/pull/4630) 


### 6.Optimize the Kademlia algorithm for the network module
The Java-tron node ID is a random number, which will be regenerated every time the node is started. In the implementation of the Kademlia algorithm of Java-tron, the distance of the node will be calculated according to the node ID, and then the node information will be put into the corresponding K bucket according to the distance. If the node in the K bucket is restarted for some reason, the node ID will change. When it is detected that the node is offline again, the distance calculated according to the latest node ID has been unable to locate the original K bucket, therefore it is not able to delete the node from the bucket. Too many such nodes restarted will cause too much invalid data to be stored in the K bucket of the node.

Therefore, the GreatVoyage-v4.6.0 (Socrates) optimizes the Kademlia algorithm, and uses a hash table to record the discovered nodes. The distance of a node is only calculated once when it is written into the K bucket for the first time and is assigned to the ‘distance’ field of the node, and then the node is added to the hash table. In the future, the node distance will be obtained directly through this field. Even if the node ID changes after the node is restarted, the distance of the node in the Hash table will not be updated. When the node is detected to be offline, the corresponding node can be found from the hash table according to the node IP, and then the distance to the node can be obtained through the node distance field, at last the node information can be deleted from the K bucket.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4620](https://github.com/tronprotocol/java-tron/pull/4620) [https://github.com/tronprotocol/java-tron/pull/4622](https://github.com/tronprotocol/java-tron/pull/4622) 


## Other Changes
### 1.  Merge ArchiveManifest.jar into Toolkit.jar
ArchiveManifest.jar is an independent LevelDB startup optimization tool, which can optimize the file size of LevelDB manifest, thereby reducing memory usage and greatly improving node startup speed. Starting from the GreatVoyage-v4.6.0 (Socrates), the ArchiveManifest.jar tool has been integrated into the Toolkit.jar. In the future, all the tools around Java-tron will be gradually integrated into the Toolkit.jar toolbox to facilitate tool maintenance and developer use.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4603](https://github.com/tronprotocol/java-tron/pull/4603)      

### 2. Add prometheus metrics for network module
GreatVoyage-v4.6.0 (Socrates) adds three new Prometheus metrics related to the network module: block fetching delay, block receiving delay, and message processing delay. New metrics help with network health monitoring of the node.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4626](https://github.com/tronprotocol/java-tron/pull/4626) 


### 3. Add the --help command option

GreatVoyage-v4.6.0(Socrates) adds ‘help’ command line options to check all parameters and instructions. Please check the example below,
```
$ java -jar FullNode.jar --help

Name:
	FullNode - the java-tron command line interface

Usage: java -jar FullNode.jar [options] [seedNode <seedNode> ...]

VERSION:
4.5.2-d05f766

TRON OPTIONS:
-v, --version			Output code version
-h, --help   			Show help message
-c, --config 			Config file (default:config.conf)
--log-config 			Logback config file
--es         			Start event subscribe server

DB OPTIONS:
-d, --output-directory			Data directory for the databases (default:output-directory)

WITNESS OPTIONS:
-w, --witness    			Is witness node
-p, --private-key			Witness private key

VIRTUAL MACHINE OPTIONS:
--debug			Switch for TVM debug mode. In debug model, TVM will not check for timeout. (default: false)
```



* Source code: [https://github.com/tronprotocol/java-tron/pull/4606](https://github.com/tronprotocol/java-tron/pull/4606) 


### 4. Optimize LiteFullNodeTool.jar
LiteFullNodeTool.jar is a light node tool of java-tron. Its main function is to convert the fullnode database into a light node database. GreatVoyage-v4.6.0 (Socrates) optimizes the tool and improves the convenience and stability of the tool.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4607](https://github.com/tronprotocol/java-tron/pull/4607)

--- 

*To move the world we must move ourselves.* 
<p align="right"> --- Socrates</p>