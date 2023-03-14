# History
## GreatVoyage-v4.7.1(Sartre)

GreatVoyage-v4.7.1(Sartre) introduces several important optimizations and updates. The optimized block synchronization logic improves the stability of block synchronization; the optimized node IP setting improves the availability of nodes; the optimized node log improves the maintainability of nodes.

Please see the details below.

### Cores
#### 1. Optimize the node IP setting
When the node starts, it will obtain the local IP of the node, and then use this IP to communicate with other nodes in the network. If the node cannot access the external network, it will not be able to obtain the local IP. At this time, the node will set its local IP to the default value of 0.0.0.0, and this IP will make the node even unable to communicate with other nodes successfully in the LAN. So the GreatVoyage- v4.7.1 (Sartre) version changes the default IP of the node. If the node cannot obtain the local IP, it will set its local IP to 127.0.0.1, so that even if the node cannot access the external network, it can still communicate with other nodes in the LAN normally. 

Source code: [https://github.com/tronprotocol/java-tron/pull/4990](https://github.com/tronprotocol/java-tron/pull/4990)   

#### 2. Optimize block synchronization logic
During the block synchronization process, the node will maintain a block request list, which contains the IDs of all blocks that have sent requests to other nodes. When the connection between the node and node A is abnormally disconnected with a very small probability, the block ID that is being requested to node A will be deleted from the request list. After that, the node will think that it has not requested the block, and then send the block request to node B and add the block ID to the request list again. Before this node disconnects with node A, the requested block may have already been sent by node A，and it is received by the node after disconnecting. Since the node found that the block is from node A that has already been disconnected, it will discard the block, and delete the block ID from the request list again, this will lead to the node to send a request for the same block to node B again. When Node B receives the repeated block request, it will consider it an illegal message and disconnect from the node.

In order to improve the efficiency of block synchronization in concurrent scenarios, the GreatVoyage-v4.7.1 (Sartre) version optimized the update mechanism of the block request list, and saved the block ID and node information in the request list at the same time. In the above scenario, after receiving a block from node A that has been disconnected, the same block ID requested from node B will not be deleted from the request list to ensure that it will not be disconnected from node B, thereby improving the stability of block synchronization.

Source code: [https://github.com/tronprotocol/java-tron/pull/4995](https://github.com/tronprotocol/java-tron/pull/4995) 

When a node synchronizes blocks from other nodes, it needs to obtain the local block chain summary of the node. The summary includes the IDs of several blocks including the local header block. In versions prior to GreatVoyage-v4.7.1 (Sartre), when obtaining the summary, the node will first query the Dynamic database to obtain the block height, and then query the Block database to obtain the ID of the block according to the block height. However, when the node is processing a block, the writing to each database is not carried out at the same time. The node will first update the Dynamic database, and then update other databases such as Block. As a result, in versions prior to GreatVoyage-v4.7.1 (Sartre), the following scenario will occur with a very small probability: when the latest block information is only written into the Dynamic database, but have not yet been written into the block database, the node starts to obtain the summary. In this situation the corresponding block ID will not be found in the block database according to the head block height obtained from the Dynamic database, leading to the summary reading fail. The GreatVoyage-v4.7.1 (Sartre) version optimizes the block chain summary acquisition logic. The ID of the head block is directly obtained from the Dynamic database instead of the Block database, which improves the stability of summary reading.


Source code: [https://github.com/tronprotocol/java-tron/pull/5009](https://github.com/tronprotocol/java-tron/pull/5009) 

The GreatVoyage-v4.7.1 (Sartre) version optimizes the lock mechanism during block synchronization and improves the stability of the node connection under concurrency.

Source code: [https://github.com/tronprotocol/java-tron/pull/4996](https://github.com/tronprotocol/java-tron/pull/4996) 

### API
#### 1. Optimize the list of solidified block APIs
GreatVoyage-v4.7.1(Sartre) version deletes the useless solidified block query API to make the code more clearer.


Source code: [https://github.com/tronprotocol/java-tron/pull/4997](https://github.com/tronprotocol/java-tron/pull/4997)  
#### 2. Optimize resource delegation relationship API
GreatVoyage-v4.7.1 (Sartre) version optimizes the resource delegation relationship query API, adds the check to the interface parameters, and makes the interface more stable.



### Other Changes


#### 1. Optimize LiteFullNode detection logic
In versions prior to GreatVoyage-v4.7.1 (Sartre), different modules of the node have different logics for detecting whether the current node is a LiteFullNode. GreatVoyage-v4.7.1 (Sartre) version unifies the logic of light node judgment, making the code more concise.


Source code: [https://github.com/tronprotocol/java-tron/pull/4986](https://github.com/tronprotocol/java-tron/pull/4986)  


#### 2. Optimize node log output

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



## GreatVoyage-v4.7.0.1(Aristotle)

GreatVoyage-v4.7.0.1 (Aristotle) introduces several important optimizations and updates. The new stake mechanism, Stake 2.0, improves the flexibility of the resource model and the stability of the stake system; the dynamic energy model helps to promote ecologically balanced development; the secondary cache mechanism optimizes the database reading performance, improves transaction execution performance, and expands the network throughput; uses the libp2p library as the Java-tron P2P network module to make the code structure clearer and reduce code coupling; optimizes the log output, redirect the logs of LevelDB and RocksDB to Java-tron log files; integrate more tools and functions into the ‘Toolkit.jar’ toolbox to bring users a more convenient development experience.

Please see the details below.

### Cores
#### 1. A new stake model - Stake 2.0 
GreatVoyage-v4.7.0.1 (Aristotle) version introduces a new stake model, Stake 2.0, aiming to establish a more flexible, efficient and stable stake system. Compared with the current Stake 1.0 model, Stake 2.0 has been improved in the following aspects,

* Staking and delegating are separated

    In Stake 1.0, staking and resource delegating are combined in one operation. The resource recipient must be specified in the operation. After the staking is completed, the resource will be delegated to the designated resource recipient. The unstaking and undelegating are also combined in one operation. If you want to cancel the delegating, you must unstake the corresponding TRX as well. Stake 2.0 separates staking and resource delegating into two independent operations. The user executes the staking first, the resource selected is allocated to the owner now. And then executes the delegate operation to assign the resource to the designated address. Unstaking and undelegating are also separated into two operations. If the user wants to cancel the delegating, he or she can directly perform the undelegate operation without unstaking and then can delegate the resource to others again as needed. Separation of staking/unstaking and delegating/undelegating simplifies user operations and reduces operational complexity.

* Resource Fragmentation Management

    In Stake 1.0, one unstake operation will unstake all the staked TRX, and the specified amount of TRX cannot be unstaked. This is optimized in Stake 2.0 now. We can specify an amount of TRX to unstake, as long as the specified amount is less than or equal to the total staked amount. In Stake 1.0, to cancel a certain resource delegate, you can only cancel all delegated resources at once, and you cannot cancel by specifying an amount. Stake 2.0 has also brought partially undelegate, we can now undelegate part of the delegated resources as needed, which improves the flexibility of resource management.

* Unstake Lock Period and Delayed Arrival of Unstaked TRX

    In Stake 1.0, after staking TRX, we need to wait 3 days before releasing the TRX. After the release, the TRX staked will immediately arrive in the owner’s account. In Stake 2.0, after the staking is completed, the TRX staked can be released at any time, but it needs to wait for ’N’ days. After the ’N’ days delay, the TRX released could be withdrawn to the owner’s account. ’N’ is the TRON network parameter. When the TRX market fluctuates violently, due to the delayed arrival of funds, it will no longer trigger a large number of stake or unstake operations, which improves the stability of the stake model, and at the same time will not cause a large number of funds to flood into the market and aggravate market volatility. It helps to build a more anticipated future of the entire network circulation for the network participants.
 
* TVM Supports Staking and Resource Management

    In Stake 2.0, the TRON virtual machine integrates instructions related to stake and resource management. Users can perform TRX stake/unstake operations in smart contracts, as well as perform resource delegate/undelegate operations.


For more details on Stake 2.0, please refer to  [What is Stake 2.0?](https://coredevs.medium.com/what-is-stake-2-0-e04f59b948a6)

The new stake mechanism is a dynamic parameter in the TRON network. After GreatVoyage-v4.7.0.1 (Aristotle) is deployed, it is disabled by default and can be enabled by initiating a proposal vote.

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4838](https://github.com/tronprotocol/java-tron/pull/4838) 

#### 2.Enhance database query performance
Java-tron uses memory and disk databases for data storage. The solidified block data will be stored in multiple disk databases, and the unsolidified data will be stored in memory. When a block is solidified, the corresponding in-memory data is written to the disk databases. When querying data, first query the data in memory, if not found, then query the disk database. The disk database query is time-consuming. Therefore, the GreatVoyage-v4.7.0.1 (Aristotle) version optimizes the database query performance and adds a secondary cache before performing the underlying disk database operation. When data is written to the disk, the data is also written to the second-level cache. When the disk database needs to be queried, if the data to be queried exists in the second-level cache, it will be returned directly without querying the disk database. The second-level cache reduces the number of queries to the disk database, improves transaction execution speed, and improves network throughput.



* Source code: [https://github.com/tronprotocol/java-tron/pull/4740](https://github.com/tronprotocol/java-tron/pull/4740) 

#### 3. Optimize block production process
When a node produces a block, it will sequentially verify and execute all transactions that can be packaged into the block, and each transaction verification and execution will involve the acquisition of block data, such as block number, block size, block transaction information, etc. In versions prior to GreatVoyage-v4.7.0.1 (Aristotle), when nodes package transactions, block data is recalculated during the process of verifying and executing each transaction, which includes many repeated calculations.

In order to improve the efficiency of packaging transactions, the GreatVoyage-v4.7.0.1 (Aristotle) optimizes the block production process, only calculates the block data once and updates the data only when necessary, thus greatly reducing the number of block data calculations and improving the block packaging efficiency.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4756](https://github.com/tronprotocol/java-tron/pull/4756) 

#### 4. Add transaction hash cache
When a node processes a block, it will use the transaction hash value multiple times. In versions before GreatVoyage-v4.7.0.1 (Aristotle), the transaction hash value is calculated as it is used, and the calculation of the transaction hash value is time-consuming, which leads to slower block processing. Therefore, GreatVoyage-v4.7.0.1 (Aristotle) adds a transaction hash cache, the transaction hash will be directly obtained from the cache when used. Only when the transaction data changes, the transaction hash is recalculated. The newly added cache reduces unnecessary transaction hash calculations and improves block processing speed.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4792](https://github.com/tronprotocol/java-tron/pull/4792)  

#### 5. Add `libp2p` module as Java-tron p2p network protocol implementation
Starting from GreatVoyage-v4.7.0.1 (Aristotle), the libp2p library will be directly used as the P2P network module of Java-tron, instead of using the original p2p network stack, so that the code structure is clearer, the code coupling is lower, and is easy to maintain.


* Source code: [https://github.com/tronprotocol/java-tron/pull/4791](https://github.com/tronprotocol/java-tron/pull/4791) 


### TVM
#### 1. Add new instructions to support Stake 2.0
GreatVoyage-v4.7.0.1 (Aristotle) introduces Stake 2.0, TVM will support Stake 2.0 related stake and resource delegate instructions simultaneously. Users can perform stake and resource delegate operations through smart contracts, which further enriches the application scenarios of smart contracts on the TRON network. A total of 6 instructions from 0xda to 0xdf have been added to TVM:

|  ID |  TVM instruction |  Description |
| -------- | -------- | -------- |
| 0xda     | FREEZEBALANCEV2     | Performs the same operation as the system contract FreezeBalanceV2 for contract account     |
| 0xdb     | UNFREEZEBALANCEV2     | Performs the same operation as the system contract UnfreezeBalanceV2 for contract account     |
| 0xdc     | CANCELALLUNFREEZEV2     | Cancel all pending unfreeze balances for contract account     |
| 0xdd     | WITHDRAWEXPIREUNFREEZE     | Performs the same operation as the system contract WithdrawExpireUnfreeze for contract account     |
| 0xde     | DELEGATERESOURCE     | Performs the same operation as the system contract DelegateResource for contract account     |
| 0xdf     | UNDELEGATERESOURCE     | Performs the same operation as the system contract UnDelegateResource for contract account     |

A total of 11 precompiled contracts from 0x100000b to 0x1000015 have been added to TVM:

|  ID |  Precompiled Contract |  Description |
| -------- | -------- | -------- |
| 0x100000b     | GetChainParameter     | Query the specific chain parameters     |
| 0x100000c     | AvailableUnfreezeV2Size     | Query the size of the available unfreeze queue for target address     |
| 0x100000d     | UnfreezableBalanceV2     | Query the unfreezable balance of a specified resourceType for target address     |
| 0x100000e     | ExpireUnfreezeBalanceV2     | Query the withdrawal balance at the specified timestamp for target address     |
| 0x100000f     | DelegatableResource     | Query the amount of delegatable resources(unit: SUN) of the specified resourceType for the target address     |
| 0x1000010     | ResourceV2     | Query the amount of resources(unit: SUN) of a specific resourceType delegated by from address to target address     |
| 0x1000011     | CheckUnDelegateResource     | Check whether the contract can recycle the specified amount of resources of a specific resourceType that have been delegated to target address, and return the amount of clean resource(unit: SUN), the amount of dirty resource(unit: SUN) and the restore time     |
| 0x1000012     | ResourceUsage     | Query the usage of a specific resourceType of resources for target address, and return the amount of usage(unit: SUN) and the restore time     |
| 0x1000013     | TotalResource     | Query the total amount of resources(unit: SUN) of a specific resourceType for target address    |
| 0x1000014     | TotalDelegatedResource     |  Query the amount of delegated resources of a specific resourceType for target address     |
| 0x1000015     | TotalAcquiredResource     | Query the amount of acquired resources(unit: SUN) of a specific resourceType for target address     |



Stake 2.0 is a dynamic parameter in the TRON network. After GreatVoyage-v4.7.0.1 (Aristotle) is deployed, it is disabled by default and can be enabled by initiating a proposal vote.

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4872](https://github.com/tronprotocol/java-tron/pull/4872) 

#### 2. Dynamic energy model
The dynamic energy model is a scheme to dynamically adjust the future energy consumption of the contract based on the known energy usage of the contract. If a contract uses too many resources in one cycle, then the next cycle in this contract, a certain percentage of punitive consumption will be added, and users who send the same transaction to this contract will cost more energy than before. When the contract uses resources reasonably, the energy consumption generated by the user calling the contract will gradually return to normal. Through this mechanism, the allocation of energy resources on the chain will be more reasonable, and excessive concentration of network resources on a few contracts will be prevented. 

For more information about the dynamic energy model: [Introduction to Dynamic Energy Model](https://coredevs.medium.com/introduction-to-dynamic-energy-model-31917419b61a)

The dynamic energy model is a dynamic parameter in the TRON network. After GreatVoyage-v4.7.0.1 (Aristotle) is deployed, it is disabled by default and can be enabled by initiating a proposal vote.

* TIP: [https://github.com/tronprotocol/tips/issues/491](https://github.com/tronprotocol/tips/issues/491) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 

#### 3. Optimize the return value of the `chainId` opcode

Starting from the GreatVoyage-v4.7.0.1 (Aristotle) version, the return value of the `chainid` opcode is changed from the block hash of the genesis block to the last four bytes of the block hash of the genesis block, keeping the return value of the chainid opcode consistent with the return value of the Java-tron JSON-RPC `eth_chainId` API.

The return value optimization of the chainId opcode is a dynamic parameter of the TRON network. It is disabled by default after GreatVoyage-v4.7.0.1 (Aristotle) is deployed, and can be enabled by initiating a proposal.

* TIP: [https://github.com/tronprotocol/tips/issues/474](https://github.com/tronprotocol/tips/issues/474) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4863](https://github.com/tronprotocol/java-tron/pull/4863) 


### API

#### 1. Add APIs to support Stake 2.0
GreatVoyage-v4.7.0.1 (Aristotle) adds 10 APIs to support Stake 2.0:

|  API |  Description |
| -------- | -------- |
| /wallet/freezebalancev2     | Stake TRX to obtain resources     | 
| /wallet/unfreezebalancev2     | Unstake TRX     |
| /wallet/delegateresource     | Delegate resources to other account     |
| /wallet/undelegateresource     | Undelegate resource     |
| /wallet/withdrawexpireunfreeze     | Withdraw the funds that has expired the `N` lock-up period     |
| /wallet/getavailableunfreezecount     | Query the remaining times of available unstaking operation     |
| /wallet/getcanwithdrawunfreezeamount     | Query the withdrawable balance at the specified timestamp     |
| /wallet/getcandelegatedmaxsize     |  Query the amount of delegatable resources of the specified resource type for target address|
| /wallet/getdelegatedresourcev2     | Query the resource delegate amount from an address to the target address (unit: sun)     |
| /wallet/getdelegatedresourceaccountindexv2     | Query the resource delegate amount from an address to the target address (unit: sun)     |


For detailed information of new APIs, please refer to: [What is Stake 2.0?](https://coredevs.medium.com/what-is-stake-2-0-e04f59b948a6)

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4838](https://github.com/tronprotocol/java-tron/pull/4838) 

#### 2. Add energy estimation API
In versions prior to GreatVoyage-v4.7.0.1 (Aristotle), users can estimate the energy consumption for executing smart contract transactions through the `/wallet/triggerconstantcontract` interface, and then set the `feelimit` parameter of the transaction according to the estimated consumption. However, since some smart contract transactions may call other smart contracts, it is possible that the estimated `feelimit` parameter is inaccurate.

Therefore, the GreatVoyage-v4.7.0.1(Aristotle) version adds an energy estimation interface `/wallet/estimateenergy`, and the `feelimit` estimated by this interface is reliable in any case. The `energy_required` field in the return value of this interface indicates the estimated amount of energy required for the successful execution of this smart contract transaction. So user can calculate the `feelimit` parameter based on this field: `feelimit` = `energy_required` * energy unit price, currently the unit price of energy is 420 sun.

If the execution of the estimated interface call fails for some reason, the value of the `energy_required` field will be 0, and this field will not be displayed in the return value. At this time, you can check the reason for the execution failure for the estimated interface call through the `result` field.

After the GreatVoyage-v4.7.0.1 (Aristotle) version is successfully deployed, this API is closed by default. To open this interface, the two configuration items `vm.estimateEnergy` and `vm.supportConstant` must be enabled in the node configuration file at the same time. The default values of `vm.estimateEnergy` and `vm.supportConstant` are both false.

An example of `/wallet/estimateenergy` call is as follows:

```
curl --location --request POST 'https://api.nileex.io/wallet/estimateenergy' \
--header 'Content-Type: application/json' \
--data-raw '{
     "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
     "contract_address": "TXLAQ63Xg1NAzckPwKHvzw7CSEmLMEqcdj",
     "function_selector": "transfer(address,uint256)",
     "parameter": "0000000000000000000000002EEF13ADA48F286066F9066CE84A9AD686A3EA480000000000000000000000000000000000000000000000000000000000000004",
     "visible": true
}'
```


* Source code: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 



### Other Changes
#### 1. Optimize Gradle compilation parameters
GreatVoyage-v4.7.0.1(Aristotle) optimizes the compiling parameters of Gradle, configuring JVM minimum heap size to 1GB, which improves the compilation speed of Java-tron.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4837](https://github.com/tronprotocol/java-tron/pull/4837) 

#### 2. Optimize node conditional stop function

In order to facilitate data backup or data statistics for node deployers, starting from GreatVoyage-v4.5.1 (Tertullian), nodes support stopping under specific conditions. Users can set the conditions for node stopping through the node configuration file, and the node will stop running when the conditions are met. It supports three stop conditions to be set at the same time, and the node is stopped when any condition is met. These three conditions include block time, block height, and the number of blocks that need to be synchronized from the start to the stop of the node. However, since multiple stop conditions are allowed to be set at the same time, when the user only needs one condition,  the other 2 conditional configuration items in the configuration file need to be deleted, so if the user forgets to delete, the node may stop on an unexpected block. However, there are actually no application scenarios that require multiple conditions to be set at the same time. Therefore, the GreatVoyage-v4.7.0.1 (Aristotle) version optimizes the node conditional stop function. The optional configuration parameters remain unchanged, but only one valid parameter is allowed to be set at the same time. If the node deployer sets multiple parameters, the node will report an error and exit run. This optimization simplifies the complexity of users’ settings.

* Source code:  [https://github.com/tronprotocol/java-tron/pull/4853](https://github.com/tronprotocol/java-tron/pull/4853)
[https://github.com/tronprotocol/java-tron/pull/4858](https://github.com/tronprotocol/java-tron/pull/4858) 

#### 3. Delete code related to database v1
In versions prior to GreatVoyage-v4.7.0.1 (Aristotle), there are two versions of the database, v1 and v2. Users can choose from them through the configuration item `db.version`. Since the v2 version adopts the memory + disk database mode, it supports the expansion of the underlying database, the correct data recovery function under abnormal conditions, etc., and has obvious advantages compared with v1. Therefore, in order to make the code structure clearer, starting from GreatVoyage-v4.7.0.1 (Aristotle), the code related to the database v1 version and the database version configuration item `db.version` has been deleted. Users no longer need to configure the database version, only v2 is available from now on, which reduces the complexity of configuring nodes.

* Source code:  [https://github.com/tronprotocol/java-tron/pull/4836](https://github.com/tronprotocol/java-tron/pull/4836)

#### 4. Optimize database log output
In versions prior to GreatVoyage-v4.7.0.1 (Aristotle), the node logs do not include the underlying logs output by LevelDB or RocksDB itself, making it difficult to troubleshoot database read and write problems. Therefore, the GreatVoyage-v4.7.0.1 (Aristotle) optimizes the database log and redirects the output of the underlying log of the LevelDB or RocksDB data module to the node log file, which simplifies the difficulty of database troubleshooting and improves the reliability of node operation and maintenance efficiency.

* Source code:  [https://github.com/tronprotocol/java-tron/pull/4833](https://github.com/tronprotocol/java-tron/pull/4833) 

#### 5. Make snapshot flush speed configurable   
Nodes newly added to the network need to synchronize block data from other nodes, and the nodes will first save the synchronized block data in memory, and then store it on disk. In versions prior to GreatVoyage-v4.7.0.1 (Aristotle), when a node synchronizes the blocks, a flush operation will write the data of 500 blocks from the memory to the disk, so more than 500 blocks data will be kept in the memory, and each block data is associated through a linked list. When querying data, it will first search in these more than 500 blocks in sequence, and then query the disk database when the data to be queried is not found, but traversing more than 500 block data reduces the efficiency of data query.

Therefore, starting from the GreatVoyage-v4.7.0.1 (Aristotle) version, the number of snapshot flush can be configured, and the maximum number of snapshot flush at one time can be set through the configuration item: `storage.snapshot.maxFlushCount` to maximize the efficiency of database query and improve block processing speed. If the configuration item is not set, the maximum number of snapshots flush into the dish is the default value of 1.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4834](https://github.com/tronprotocol/java-tron/pull/4834) 

#### 6. Toolkit.jar Integration
`DBConvert.jar` is a database conversion tool, which can convert LevelDB into RocksDB; `LiteFullNodeTool.jar` is a light FullNode tool, which can convert FullNode data into LiteFullNode data. Starting from GreatVoyage-v4.7.0.1 (Aristotle), `DBConvert.jar` and `LiteFullNodeTool.jar` have been integrated into the `Toolkit.jar` toolbox, and a database copy function is added which can realize fast Node database copy. In the future, the tools around Java-tron will be gradually integrated into the `Toolkit.jar` toolbox in order to facilitate tool maintenance and developer use. The commands for using the new functions of the `Toolkit.jar` toolbox are as follows:



```
// Convert LevelDB data to RocksDB data
java -jar Toolkit.jar db convert -h
// convert FullNode data into LiteFullNode data
java -jar Toolkit.jar db lite -h
// Database copy
java -jar Toolkit.jar db copy -h
```

* Source code: [https://github.com/tronprotocol/java-tron/pull/4813](https://github.com/tronprotocol/java-tron/pull/4813) 



--- 

*Courage is the first of human qualities because it is the quality that guarantees others.* 
<p align="right"> --- Aristotle</p>




## GreatVoyage-v4.6.0 (Socrates)

The GreatVoyage-v4.6.0 (Socrates) introduces several important optimizations and updates, such as an optimized database checkpoint mechanism, which improves the stability of node operation; optimized resource delegate relationship index structure, and an updated voting reward algorithm, which speed up the execution speed of transactions and increase network throughput; a new proposal to add transaction memo fees, increasing the cost of transactions with memo to reduce the number of low-value transactions, so that improves the security and reliability of the TRON network. The integrated toolkit, new network-related Prometheus metrics, and new help command line together bring users a more convenient development experience.

Please check below for details.


### Core
#### 1. Optimize delegate relationship index structure

In the TRON network, accounts can delegate resources to other accounts through staking, and can also accept resources that other accounts stake for themselves. Therefore, each account needs to maintain a record of the delegate relationship, including all the recipient addresses that the account delegated resources to and all the addresses that delegated resources for the account.

In versions prior to GreatVoyage-v4.6.0 (Socrates), the delegate relationship is stored in the form of a list. When performing resource delegating, it needs first to check whether the recipient account already exists in the list and then adds the account to the list only if it is not present. If a particular account has delegated resources to multiple accounts or many accounts have delegated the resources to the particular account, then the length of the delegate relationship list for the particular account will be substantial. The lookup operation would be considerably time-consuming, resulting in long transaction execution times. 

Therefore,  GreatVoyage-v4.6.0 (Socrates) optimizes the index storage structure of the resource delegate relationship and changes it from a list to a key-value pair, so as to complete the querying and modification of its data in a constant time, which greatly speeds up the execution speed of the delegation related transactions and improves network throughput.

The delegate relationship storage optimization is a dynamic parameter of the TRON network. It is disabled by default and can be enabled by initiating a proposal.

* TIP: [https://github.com/tronprotocol/tips/issues/476](https://github.com/tronprotocol/tips/issues/476) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4788](https://github.com/tronprotocol/java-tron/pull/4788)  

#### 2. Add transaction memo fee proposal
Starting from GreatVoyage-v4.6.0 (Socrates), a memo fee will be charged for transactions with a memo. By increasing the cost, the fee will reduce the number of low-value transactions, so as to improve the security and reliability of the TRON network.

The memo fee is a dynamic parameter of the TRON network. After GreatVoyage-v4.6.0 (Socrates) is deployed, the default value is ‘0’, and the unit is ‘sun’. It can be enabled by specifying a non-zero value by initiating a proposal, for example, ‘1000000’, indicating that the transaction with memo will require an additional 1 TRX fee.

* TIP: [https://github.com/tronprotocol/tips/issues/387](https://github.com/tronprotocol/tips/issues/387) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4758](https://github.com/tronprotocol/java-tron/pull/4758)  



#### 3. Add optimized reward algorithm proposal
Many voters in the TRON network will accumulate rewards for a long time before withdrawing them. The interval between two withdrawals of rewards is often very long. In versions prior to GreatVoyage-v4.6.0 (Socrates), for the transaction to withdraw rewards, it will calculate and accumulate rewards for each maintenance period since the last withdrawal of rewards, so the longer the time since the last withdrawal of rewards, the more time-consuming it will be to calculate the reward. Therefore, GreatVoyage-v4.6.0 (Socrates) optimizes the calculation algorithm of voting rewards. Instead of accumulating the rewards of each maintenance period, the sum of unwithdrawn rewards can be obtained by subtracting the total number of rewards recorded in the maintenance period of the last reward withdrawal from the total rewards recorded in the previous maintenance period. This algorithm realizes the calculation of the total number of unclaimed rewards in a constant time, which greatly improves the calculation efficiency and speeds up the execution of reward calculation, thereby improving the throughput of the network.

The optimized reward algorithm is a TRON network parameter and is disabled by default once GreatVoyage-v4.6.0 (Socrates) is deployed, and can be enabled by voting through a proposal.

* TIP: [https://github.com/tronprotocol/tips/issues/465](https://github.com/tronprotocol/tips/issues/465) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4694](https://github.com/tronprotocol/java-tron/pull/4694) 



#### 4. Upgrade checkpoint mechanism to v2 in database module

The Checkpoint is a recovery mechanism established to prevent database damage caused by the exceptional shutdown. Java-tron uses memory and multi-disk databases for data storage. The data of the solidified block will be stored in multiple business databases. Unsolidified data is stored in the memory. When a block is solidified, the corresponding memory data will be written to relevant databases. However, since the writing to multiple business databases is not an atomic operation, if there is an unexpected downtime due to some reason, then all the data in the block may not be able to be written to the disk, and the node will not be able to restart due to database corruption.

Therefore, before the memory data is written to the disk, a checkpoint would be created. The checkpoint contains all the data that needs to be written to each business database this time. After the checkpoint is created, first writes the checkpoint data to an independent Checkpoint database, and then performs the operation of writing the business database, and the Checkpoint database always retains the latest solidified block data. If the business database is damaged due to system shutdown, after the node restarts, the business database will be recovered through the data previously saved in the checkpoint database.

At present, the Checkpoint mechanism can deal with the vast majority of downtime situations, but there is still a small probability that the business database will be damaged due to downtime. At present, the data writing of LevelDB is asynchronous. The program calls LevelDB to request to write the data to the disk. In fact, the data is only written into the cache of the operating system, and then the operating system will decide when to actually write to the disk according to its own strategy. If an unexpected downtime occurs at the time when the node just finished writing to the Checkpoint database and continues to write to the business database, it is possible that the data written to the Checkpoint database is not actually written to the disk by the operating system. In this case, the node would fail to restart properly because the Checkpoint database has no recovery data.

In order to solve this problem, GreatVoyage-v4.6.0 (Socrates) upgrades the V2 version of Checkpoint implementation. The Checkpoint mechanism V2 will store multiple solidified blocks data. So that even if the latest solidified block data is not written successfully to the Checkpoint database due to abnormal shutdown, the historical solidified block data can be used to restore the business database when the node restarts.

The  Checkpoint mechanism V2 is disabled by default in the configuration file. This function can be enabled by modifying the configuration. It should be noted that if a node has enabled the checkpoint V2 and has been running for a certain period of time, it would not be able to roll back to V1 anymore.

* TIP: [https://github.com/tronprotocol/tips/issues/461](https://github.com/tronprotocol/tips/issues/461) 
* Source code:  [https://github.com/tronprotocol/java-tron/pull/4614](https://github.com/tronprotocol/java-tron/pull/4614)  
#### 5. Optimize block production priority between active and backup nodes 

If the super representative deploys the active and backup nodes, the connection between the nodes will be maintained. When the active and backup nodes are temporarily disconnected due to network problems, the backup node will consider that the active node is invalid and take over the block production. This will cause a duplicate block production process as both the active and backup nodes will produce blocks at the same time. In versions prior to GreatVoyage-v4.6.0 (Socrates), when the active and backup nodes receive blocks of the same height block generated by each other, both of them will suspend for 1-9 block production cycles. That is, the super representative will miss 1-9 blocks.

The GreatVoyage-v4.6.0 (Socrates) optimizes the priority of block production logic. When the situation above happens, both nodes will compare the hash value of the block produced by the other node. The node with a larger block hash will continue to produce blocks, and the node with smaller block hash will suspend a block production cycle, then continue to produce blocks, and compare the block hash again. A total of 27 super representatives will generate blocks sequentially, so it takes 81 seconds to skip a block production cycle. During this period, if the connection problem between them is a short-term network failure, there will be enough time to recover it. In addition, after receiving these two blocks, other nodes will also choose the block with a larger hash and discard the one with a smaller hash. This implementation will significantly improve the block production efficiency during obstructed network connections between active and backup nodes and network stability.


* Source code：[https://github.com/tronprotocol/java-tron/pull/4630](https://github.com/tronprotocol/java-tron/pull/4630) 


#### 6.Optimize the Kademlia algorithm for the network module
The Java-tron node ID is a random number, which will be regenerated every time the node is started. In the implementation of the Kademlia algorithm of Java-tron, the distance of the node will be calculated according to the node ID, and then the node information will be put into the corresponding K bucket according to the distance. If the node in the K bucket is restarted for some reason, the node ID will change. When it is detected that the node is offline again, the distance calculated according to the latest node ID has been unable to locate the original K bucket, therefore it is not able to delete the node from the bucket. Too many such nodes restarted will cause too much invalid data to be stored in the K bucket of the node.

Therefore, the GreatVoyage-v4.6.0 (Socrates) optimizes the Kademlia algorithm, and uses a hash table to record the discovered nodes. The distance of a node is only calculated once when it is written into the K bucket for the first time and is assigned to the ‘distance’ field of the node, and then the node is added to the hash table. In the future, the node distance will be obtained directly through this field. Even if the node ID changes after the node is restarted, the distance of the node in the Hash table will not be updated. When the node is detected to be offline, the corresponding node can be found from the hash table according to the node IP, and then the distance to the node can be obtained through the node distance field, at last the node information can be deleted from the K bucket.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4620](https://github.com/tronprotocol/java-tron/pull/4620) [https://github.com/tronprotocol/java-tron/pull/4622](https://github.com/tronprotocol/java-tron/pull/4622) 


### Other Changes
#### 1.  Merge ArchiveManifest.jar into Toolkit.jar
ArchiveManifest.jar is an independent LevelDB startup optimization tool, which can optimize the file size of LevelDB manifest, thereby reducing memory usage and greatly improving node startup speed. Starting from the GreatVoyage-v4.6.0 (Socrates), the ArchiveManifest.jar tool has been integrated into the Toolkit.jar. In the future, all the tools around Java-tron will be gradually integrated into the Toolkit.jar toolbox to facilitate tool maintenance and developer use.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4603](https://github.com/tronprotocol/java-tron/pull/4603)      

#### 2. Add prometheus metrics for network module
GreatVoyage-v4.6.0 (Socrates) adds three new Prometheus metrics related to the network module: block fetching delay, block receiving delay, and message processing delay. New metrics help with network health monitoring of the node.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4626](https://github.com/tronprotocol/java-tron/pull/4626) 


#### 3. Add the --help command option

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


#### 4. Optimize LiteFullNodeTool.jar
LiteFullNodeTool.jar is a light node tool of java-tron. Its main function is to convert the fullnode database into a light node database. GreatVoyage-v4.6.0 (Socrates) optimizes the tool and improves the convenience and stability of the tool.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4607](https://github.com/tronprotocol/java-tron/pull/4607)

#### 5. Optimize the return value of  eth_getBlockByHash and eth_getBlockByNumber APIs

In order to be better compatible with Ethereum's JsonRPC 2.0 protocol interface, GreatVoyage-v4.6.0(Socrates) changes the unit of the `timestamp` field in the return value of the eth_getBlockByHash and eth_getBlockByNumber APIs from milliseconds to seconds, making the return values of these two APIs fully compatible with Ethereum Geth.


* Source code: [https://github.com/tronprotocol/java-tron/pull/4642](https://github.com/tronprotocol/java-tron/pull/4642) 

--- 

*To move the world we must move ourselves.* 
<p align="right"> --- Socrates</p>



## GreatVoyage-v4.5.2(Aurelius)
The GreatVoyage-v4.5.2 (Aurelius) version introduces several important optimizations. The optimized transaction cache mechanism greatly reduces memory usage and improves node performance; the optimized P2P node connection strategy improves the efficiency of establishing connections between nodes and speeds up the node synchronization process;  the optimized block production and processing logic improve node stability; the newly added database storage partition tool reduces the pressure on data storage; the newly added block header query API and historical bandwidth unit price Query API are to bring users a more convenient development experience.


### Core
#### 1. Optimize block processing 
In versions prior to GreatVoyage-v4.5.2 (Aurelius), threads such as block production, block processing, and transaction processing compete for synchronization lock at the same time. In the case of high concurrency and transactions executing much time, the block production thread or the block processing thread will take a long time to get to the synchronization lock, which leads to the occurrence of a small probability of a block loss event. In order to improve node stability, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the synchronization lock in the block processing logic, allowing only one transaction processing thread to compete for the synchronization lock with the block production or processing thread, and when the transaction processing thread finds that block-related threads waiting for the synchronization lock, it will voluntarily give in, which greatly increases the probability of block production and block processing threads acquiring synchronization lock, and ensures high throughput and stable operation of the node.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-428.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4551 

#### 2. Optimize transaction cache
The node uses the transaction cache to determine whether the newly received transaction is a duplicate transaction. In versions prior to GreatVoyage-v4.5.2 (Aurelius), the transaction cache is a hashmap data structure, which saves transactions in the latest 65536 blocks. The hashmap allocates memory for each transaction separately. Therefore, the transaction cache will occupy nearly 2GB of memory during program runtime, meanwhile, frequent memory requests will trigger frequent JVM garbage collection which indirectly affects the performance of the node. To solve this issue, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the implementation of the transaction cache, using the bloom filter instead of the hashmap, the bloom filter uses a fixed and extremely small memory space to record recent historical transactions, which greatly reduces the memory usage of the transaction cache and improve the node performance.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-440.md
Source Code：https://github.com/tronprotocol/java-tron/pull/4538  




#### 3. Optimize nodes connection strategy
In versions prior to GreatVoyage-v4.5.2 (Aurelius), when the number of remote nodes connected by a node has reached the maximum value, the node will reject connection requests from new remote nodes. With the increase of such fully connected nodes in the network, it will become more and more difficult for the newly added nodes to establish connections with other nodes in the network.

In order to speed up the connection process between nodes in the network, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the P2P node connection strategy. It will periodically check the number of TCP connections of the node. When the number of  connections is full, a certain disconnection strategy is adopted to disconnect one or two nodes to increase the possibility of a newly added node in the network successfully connecting to it, thereby improving the efficiency of establishing connections between P2P nodes in the network and improving network stability. Please note that the nodes configured in the `node.active` and `node.passive` lists in the configuration file are trusted nodes and will not be disconnected.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-425.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4549   



#### 4. Optimize block generating logic
In versions prior to GreatVoyage-v4.5.2 (Aurelius), for pre-executed normal transactions, they may encounter JVM GC pauses during packaging which can result in transaction execution timeout and being discarded. Therefore, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the block generating logic. For a pre-executed normal transaction, if it executes time out during packaging, a retry operation is taken to avoid transaction discard caused by JVM GC pause during the packaging.

Source Code：https://github.com/tronprotocol/java-tron/pull/4387 

#### 5. Optimize fork switching logic
Micro-forks occur in the TRON network occasionally. The chain switching behavior will occur when a micro-fork happens.  The chain switching will roll back blocks, and the transactions in the rolled back block will be put back into the transaction pending queue. When these transactions are repackaged and executed, the execution results may be inconsistent due to chain switching. In versions prior to GreatVoyage-v4.5.2 (Aurelius), the entire process refers to the same transaction object, so chain switching may lead to the transaction result in the rolled back block being changed. When the chain switching occurs again and the original chain is switched back, the transaction on the original chain will be executed again, at this time, it will report a `Different resultCode` error, which will cause the node to stop synchronizing. 

Therefore, the GreatVoyage-v4.5.2 (Aurelius) version optimizes the chain-switching logic. When a block is rolled back, a new transaction object is created for the transaction in the rolled-back block, so as to avoid the modification of the transaction result and improve the node's stability for fork handling.


Source Code：https://github.com/tronprotocol/java-tron/pull/4583 

#### 6. Add database storage partition tool
As the data on the chain grows, the disk space of the FullNode may be insufficient, and a larger capacity disk needs to be replaced. So starting from the GreatVoyage-v4.5.2 (Aurelius) version, a database storage partition tool is provided, which can migrate some databases to other disk partitions according to the user's configuration, so users only need to add disks according to capacity requirements, no need to replace the original disk, that is convenient for users to expand the disk capacity, and at the same time reduces the cost of running a node.


Source Code：https://github.com/tronprotocol/java-tron/pull/4545 
https://github.com/tronprotocol/java-tron/pull/4559 
https://github.com/tronprotocol/java-tron/pull/4563 


 
### API
#### 1. New block header query API

From the GreatVoyage-v4.5.2 (Aurelius) version, a new block header query API is added, which only returns the block header information, not the transaction information in the block. Users can obtain the block header information without querying the entire block. This not only reduces the network I/O load of the node, and since the block does not carry transaction information, the serialization time is reduced, the interface delay is reduced, and the query efficiency is improved.
 
Source Code：https://github.com/tronprotocol/java-tron/pull/4492 
https://github.com/tronprotocol/java-tron/pull/4552 

#### 2. New historical bandwidth unit price query API
According to the bandwidth consumption rules, if the transaction initiator’s  bandwidth obtained by staking TRX or free bandwidth is insufficient, TRX will be burned to pay for the bandwidth fee. At this time, only the bandwidth fee is recorded in the transaction record, but not the bandwidth consumption number. In order to understand bandwidth consumption of historical transactions, starting from GreatVoyage-v4.5.2 (Aurelius), a new historical bandwidth unit price query API `/wallet/getbandwidthprices` is added. Users can obtain historical records of bandwidth unit price through this API so that they can calculate bandwidth consumption of historical transactions.

Source Code：https://github.com/tronprotocol/java-tron/pull/4556 

### Other Changes
#### 1. Optimize block synchronization logic
The GreatVoyage-v4.5.2 (Aurelius) version optimizes the block synchronization logic, avoids unnecessary node disconnection in the process of synchronizing blocks, and improves node stability.

Source Code：https://github.com/tronprotocol/java-tron/pull/4542 
https://github.com/tronprotocol/java-tron/pull/4540 
#### 2. Optimize `eth_estimateGas` and `eth_call` API
The GreatVoyage-v4.5.2 (Aurelius) version optimizes the `eth_estimateGas` and `eth_cal` JSON-RPC interfaces; they can return error information when smart contract transaction execution is interrupted.

Source Code：https://github.com/tronprotocol/java-tron/pull/4570 

#### 3. Enhance the fault tolerance of the interface
The GreatVoyage-v4.5.2 (Aurelius) version optimizes multiple API interfaces, enhances its fault tolerance for parameters, and improves the stability of API interfaces.

Source Code：https://github.com/tronprotocol/java-tron/pull/4560 
https://github.com/tronprotocol/java-tron/pull/4556 
 
--- 

*The universe is change; our life is what our thoughts make it.* 
<p align="right"> ---  Aurelius</p>


## GreatVoyage-v4.5.1(Tertullian)
The GreatVoyage-v4.5.1(Tertullian) version introduces several important optimization updates. The optimized transaction cache loading process shortens the node startup time; the optimized block acquisition logic and light node synchronization logic promote the stability of the node; the optimized account asset structure and TVM cache structure improves the processing speed of transactions, thereby further improving the performance of node; supporting prometheus protocol interface brings users a more convenient development experience and helps to further prosper the TRON ecosystem.



### Core
#### 1. Optimize transaction cache loading
In versions prior to GreatVoyage-v4.5.1 (Tertullian), it took a long time from node startup to block synchronization, and the loading of the transaction cache took up most of the node startup time. The transaction cache is used by the node to determine whether a transaction is a duplicate transaction, so during the node startup process, the transaction cache needs to be loaded from the database to the memory, and in versions prior to GreatVoyage-v4.5.1 (Tertullian), it adopts transaction as the storage unit to read the database when loading the transaction cache, so the amount of data to be read is large, and the entire reading process is time-consuming.

In order to speed up the startup of the node, the GreatVoyage-v4.5.1 (Tertullian) version optimizes the loading of the transaction cache. By adopting the block as the storage unit to read the database reduces the times of database reading,  improves the efficiency of transaction cache loading, and improves the speed of node startup.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-383.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4319 

#### 2. Optimize account TRC-10 asset storage structure
In versions prior to GreatVoyage-v4.5.1 (Tertullian), when there were too many TRC10 assets in the account, the content of the account stored in the database was large, resulting in the deserialization of the account during the transaction execution process is very time-consuming , therefore, the GreatVoyage-v4.5.1 (Tertullian) version adds a new proposal to optimize the asset structure of the account, allowing TRC-10 assets to be separated from the account and stored separately in a key-value data structure. That will reduce the content of the account structure, speed up the deserialization operation of the account and reduce the execution time of the transaction, thereby increasing the network throughput and improving the network performance.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-382.md  
Source Code: https://github.com/tronprotocol/java-tron/pull/4392 

#### 3. Optimize light node synchronization
Since light nodes do not store complete block data, there is a possibility that a node connects to a light node which does not have the block the node wants to synchronize with, in this situation, the light node will actively disconnect the connection. In versions prior to GreatVoyage-v4.5.1 (Tertullian), nodes may repeatedly establish connections with such light nodes, and then be disconnected by the other part, which greatly affects the efficiency of synchronizing blocks between nodes. Therefore, in the GreatVoyage-v4.5.1 (Tertullian) version, the logic of establishing a connection with light nodes has been optimized, and the two fields of "node type" and "node's lowest block" are added to the handshake message between nodes, and the nodes will save the handshake messages with each node. If the highest block of the current node is lower than the lowest block of the light node, it will actively disconnect from the light node, and the next time it establishes a connection with the node, it will filter out such nodes to avoid more invalidations connection, which improves the efficiency of synchronization between nodes.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-388.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4323  



#### 4. Optimize block broadcasting
The GreatVoyage-v4.5.1 (Tertullian) version optimizes the block broadcast logic, so that the fast forward node only broadcasts the block to the three super representative nodes that will produce blocks next (the number of broadcasted super representative nodes can be changed through the configuration file) to ensure that the super representative node can obtain the latest block in time, which improves the efficiency of block production.


Source Code: https://github.com/tronprotocol/java-tron/pull/4336 

#### 5. Optimize fetch block process
Due to network reasons, the node may not receive the new broadcasted block. In versions before GreatVoyage-v4.5.1 (Tertullian), when the block acquisition times out, the node will acquire the block through the P2P synchronization process, but the process is complicated and time-consuming. Therefore, the GreatVoyage-v4.5.1 (Tertullian) version optimizes the process of obtaining the latest block. The node will first select a node according to the status of each node, and then directly send the block obtaining message `FetchInvDataMessage` to this node to obtain the latest block, which saves most of the time in the block synchronization process, speeds up the acquisition of the latest block, and improves the stability of the node.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-391.md
Source Code: https://github.com/tronprotocol/java-tron/pull/4326 

#### 6. Support prometheus metric protocol interface
Starting from the GreatVoyage-v4.5.1 (Tertullian) version, the node provides an open source system monitoring tool - prometheus’s protocol interface, and users can monitor the health status of the node more conveniently.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-369.md  
Source Code: https://github.com/tronprotocol/java-tron/pull/4337 

#### 7. Support node stop at specified condition
In order to facilitate node deployers to do data backup or data statistics, starting from the GreatVoyage-v4.5.1 (Tertullian) version, the node could stop running under specific conditions. Users can set the conditions for node stop through the node configuration file, such as the node stop’s block time, block height, and the number of blocks the node needs to synchronize from start to stop. The node will stop running automatically when the set conditions are met.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-370.md  
Source Code: https://github.com/tronprotocol/java-tron/pull/4325 


### TVM
#### 1. Adjust the upper limit that can be set for the maximum execution time of TVM
"TVM maximum execution time" is a dynamic parameter of the TRON network, indicating the maximum time allowed for a smart contract to be executed. Super representatives can change this parameter through proposal voting. In versions prior to GreatVoyage-v4.5.1 (Tertullian), the maximum value that this parameter can be modified is 100ms. With the stability of the TRON network infrastructure and the vigorous development of the ecology, the 100ms upper limit confines the complexity of smart contracts. Therefore, GreatVoyage-v4.5.1 (Tertullian) version adds a new proposal that allows to raise the configurable upper limit of "TVM maximum execution time" to 400ms.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-397.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4375 


#### 2. Optimize the cache structure of TVM
In versions prior to GreatVoyage-v4.5.1 (Tertullian), the cached data in TVM is stored in the form of a byte array. When the data in the cache needs to be changed, the data must first be converted from the form of a byte array to a protobuf object by performing a serialization operation, then change a field of the object (such as account balance, etc.) to generate a new object, then serialize the newly generated protobuf object to byte array, and at last write the result byte array to TVM cache. Since the serialization and deserialization of protobuf is time-consuming, the GreatVoyage-v4.5.1 (Tertullian) version optimizes the data structure in the cache when TVM is executed, and directly saves the protobuf object data to reduce the serialize/deserialize operations when accessing the data in the cache, speeding up TVM execution of bytecode.


Source Code: https://github.com/tronprotocol/java-tron/pull/4375   


--- 

*Hope is patience with the lamp lit.* 
<p align="right"> --- Tertullian </p>



## GreatVoyage-v4.4.6(David)
GreatVoyage-v4.4.6 (David) updated the version of the dependency library fastjson to ensure the security of using fastjson.

### Other Changes
#### 1. Update the fastjson dependency library to the latest version
Due to security vulnerabilities in fastjson 1.2.80 and earlier versions, GreatVoyage-v4.4.6 (David) updated the version of the fastjson dependency library to 1.2.83, and enabled the `safemode` mode of fastjson to ensure the safety of using fastjson.

Source Code：https://github.com/tronprotocol/java-tron/pull/4393 



---
*Beauty in things exists in the mind which contemplates them. * 
<p align="right"> ---David Hume</p>


## GreatVoyage-4.4.5(Cicero)
The GreatVoyage-v4.4.5 (Cicero) version optimizes the query interface of the node to filter out invalid fields, which ensures the stability of the interface for parsing data.

### Other Changes
#### 1. Optimize the query interface of the node
The GreatVoyage-v4.5.0 (Cicero) version optimizes the query interface of the node. When parsing the obtained data, the node will filter out invalid fields to ensure to return the correct interface data 

Source Code：https://github.com/tronprotocol/java-tron/pull/4349 



---
*No one can give you better advice than yourself.* 
<p align="right"> ---Cicero </p>



## GreatVoyage-4.4.4(Plotinus)
The GreatVoyage-v4.4.4 (Plotinus) version introduces several important optimization updates, which reduces the node memory usage; speeds up node startup; Optimized network module, block production threads, improve the stability of nodes; Improved java-tron upgrade mechanism achieves more efficient decentralized governance; TVM supports multi-version program executors, which helps make it more compatible with EVM, brings users a more convenient development experience, and helps further flourish the TRON ecosystem.

### Core
#### 1. Optimize node startup time

Before the GreatVoyage-v4.4.4 (Plotinus), the node will execute about a minute from startup to block synchronization. The block synchronization thread will first delay 30s to wait for the P2P thread to discover remote nodes, then establish TCP connection with the discovered nodes, and finally perform the block synchronization. This delay time occupies most of the startup time. In fact, every newly discovered node will be persisted to the local database, so there is no need to spend extra time waiting for the node to be discovered when node is started for the second time. So in the GreatVoyage-v4.4.4(Plotinus) version, the waiting time for node discovery has been reduced from 30s to 100ms to improve the speed of node startup.


TIP: https://github.com/tronprotocol/tips/blob/master/tip-366.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4254  


#### 2. Optimize memory usage
In order to avoid repeatedly broadcasting a transaction, the node will cache the transaction data into the broadcast data buffer. However,due to the limitation of the JVM's recycling policy, old cached data cannot be deleted in time until the buffer is full. Therefore, a buffer with a larger capacity will occupy a large amount of memory space. Before the GreatVoyage-v4.4.4 (Plotinus) version, the buffer pool size was 100000 transactions. In order to release the memory occupied by expired transactions in time , the GreatVoyage-v4.4.4 (Plotinus) version changed the buffer size to 20000 to reduce memory usage.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-362.md 
Source Code: https://github.com/tronprotocol/java-tron/pull/4250 


#### 3. Optimize the block-producing thread

The GreatVoyage-v4.4.4 (Plotinus) version adds the interrupt exceptions handling in block-producing thread, so that when the block-producing node catches the interrupt instruction, it can exit safely.


Source Code：https://github.com/tronprotocol/java-tron/pull/4219 



### TVM
#### 1. TVM support multi-version program-executors

In order to enable the TRON network to support various types of smart contract transactions in the future, starting from GreatVoyage-v4.4.4 (Plotinus), TVM code is refactored to support multi-version program  executors, it will select different instruction set to interpret and execute the bytecode of smart contract according to the contract version information.

Source Code：https://github.com/tronprotocol/java-tron/pull/4257 
                             https://github.com/tronprotocol/java-tron/pull/4259 

### Other Changes

#### 1. Optimize log storage

The GreatVoyage-v4.4.4 (Plotinus) version modifies the node log retention time from 3 days to 7 days to facilitate users to troubleshoot issues.

Source Code：https://github.com/tronprotocol/java-tron/pull/4245 


#### 2. Optimize network service shutdown logic

The GreatVoyage-v4.4.4(Plotinus) version optimizes the network service shutdown logic, closing the synchronization service first, and then closing the TCP connection service to ensure that all P2P connection related services exit safely.


Source Code：https://github.com/tronprotocol/java-tron/pull/4220 


#### 3. improve the Java-tron upgrade mechenism
For upgrade mechanism of java-tron,Before the GreatVoyage-v4.4.4 (Plotinus) version,all 27 super representative nodes need to complete the code upgrade, TRON network can be upgraded to the new version,TRON is a completely decentralized governance network,Sometimes the 27 super representative nodes cannot complete the code upgrade within a certain period of time, making the version upgrade process slow.In order to achieve more efficient decentralized governance, in GreatVoyage-v4.4.4 (Plotinus), the upgrade mechanism of Java-tron has been improved, only 22 super representative nodes are needed to complete the code upgrade, and the TRON network can complete the upgrade.

Source Code：https://github.com/tronprotocol/java-tron/pull/4218

---
*The world is knowable, harmonious, and good.* 
<p align="right"> --- Plotinus </p>



## GreatVoyage-4.4.2(Augustinus)
The GreatVoyage-v4.4.2(Augustinus) has three essential updates: The new execution model of opcode boosts the TVM performance; individualized LevelDB parameters improve the database performance; and the newly added log filter APIs make the JSON-RPC API more comprehensive.

### TVM
#### 1. TVM Opcode Execution Model Optimization
The opcode execution model of the interpreter in TVM is optimized in GreatVoyage-v4.4.2(Augustinus). The performance of TVM is proven to have a great boost through testing.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-344.md
Source Code：https://github.com/tronprotocol/java-tron/pull/4157

### API
#### 1. Newly Adding ETH compatible log filter for JSON-RPC APIs.
Log filter related APIs are available from GreatVoyage-v4.4.2 for compatibility with Ethereum JSON-RPC API.

TIP: https://github.com/tronprotocol/tips/issues/343 
Source Code：https://github.com/tronprotocol/java-tron/pull/4153 

### Other Changes
#### 1. LevelDB Databases Performance Optimization

Parameters of each LevelDB database have been individualized by the I/O frequencies from GreatVoyage-v4.4.2(Augustinus). This will significantly boost the database performance.

Source Code：https://github.com/tronprotocol/java-tron/pull/4154 

--- 

*Patience is the companion of wisdom.* 
<p align="right"> ---  Augustinus </p>



## GreatVoyage-4.4.0(Rousseau)
The GreatVoyage-v4.4.0 (Rousseau) version introduces several important updates: the optimization of block broadcasting will let the block be broadcast to the entire network faster; the query performance optimization of `dynamic store` and the optimization of database parameters will be greatly improved Block processing speed, thereby improving the performance of java-tron; API customization in FullNode makes node configuration more flexible for different application scenarios; TVM will also be better compatible with EVM and adapt to the Ethereum London upgrade, the new JSON-RPC API will bring developers a better development experience, help developers to join the TRON ecosystem more easily, and promote the prosperity of the TRON ecosystem.

### Core
#### 1. Optimize the block broadcasting
In the version before GreatVoyage-v4.4.0 (Rousseau), the logic of block processing is: verify block -> process block -> broadcast block. However, due to the long block processing time, there is a delay in block broadcasting. In order to speed up block broadcasting, In GreatVoyage-v4.4.0 (Rousseau) version, the block processing logic is changed to: verify block -> broadcast block -> process block, so that the block can be quickly broadcast to the entire network.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-289.md 
Source Code:https://github.com/tronprotocol/java-tron/pull/3986  

#### 2. Optimize the query performance of `dynamic store`
During the block processing, The frequency of visits to `dynamic store` is very high. The GreatVoyage-v4.4.0(Rousseau) version optimizes the query performance of the  `dynamic store` by loading all the data of  `dynamic store`  into the first-level cache, the cache hit rate of the `dynamic store`  is improved and the block processing speed is also improved.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-290.md
Source Code：https://github.com/tronprotocol/java-tron/pull/3993  

#### 3. Optimize the transaction broadcasting interface
The GreatVoyage-v4.4.0 (Rousseau) version optimizes the processing flow of the transaction broadcast interface. The transaction broadcast is changed from asynchronous to synchronous, and the result will be returned after the broadcast is successful, making the return result of the broadcast more accurate.

Source code：https://github.com/tronprotocol/java-tron/pull/4000 

#### 4. Optimize the parameters of the database
The GreatVoyage-v4.4.0 (Rousseau) version optimizes the parameters of the database, which improves the read and write performance of the database, thereby improving the efficiency of block processing.

Source Code：https://github.com/tronprotocol/java-tron/pull/4018 
https://github.com/tronprotocol/java-tron/pull/3992 

### TVM
#### 1. Provide compatibility with EVM
The GreatVoyage-v4.4.0 (Rousseau) version provides compatibility solution for those instructions that are different from EVM, so that the newly deployed contract supports the following features:
- The `GASPRICE` instruction returns the unit price of energy.
- The `try/catch-statement` supports catching all types of TVM exceptions.
- Forbid the system contract “TransferContract” to transfer TRX to the smart contract account.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-272.md 
Source Code：https://github.com/tronprotocol/java-tron/pull/4032 

**NOTICE**：
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

#### 2. Adapt to Ethereum London Release

In the GreatVoyage-v4.4.0 (Rousseau) version, TVM is also adapted to the Ethereum London upgrade: introduce the `BASEFEE` opcode; the deployment of new contracts starting with 0xEF is prohibited.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-318.md 
Source Code：https://github.com/tronprotocol/java-tron/pull/4032 

**NOTICE**：
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

#### 3. In constant mode, `Energy limit` supports customization and the default value is increased

Before the GreatVoyage-v4.4.0 (Rousseau) version, the energy limit in constant mode was a fixed value(`3,000,000`). The GreatVoyage-v4.4.0 (Rousseau) version changed it to configurable, and increase the default value to `100,000,000`. after upgraded to the latest version, `Energy limit` can be configured in startup parameters(`--max-energy-limit-for-constant`) or in the configuration file(`vm.maxEnergyLimitForConstant`). 

Source Code：https://github.com/tronprotocol/java-tron/pull/4032 

### API
#### 1. Support Ethereum compatible JSON-RPC API
Starting from the GreatVoyage-v4.4.0 (Rousseau) version, the FullNode supports JSON-RPC APIs. For details, please refer to: https://developers.tron.network/reference#json-rpc-api 

Source Code：https://github.com/tronprotocol/java-tron/pull/4046 

#### 2. FullNode supports disabling APIs
In order to make the FullNode customizable, starting from GreatVoyage-v4.4.0 (Rousseau) version, FullNode supports disabling specific APIs through the configuration file.

Source code：https://github.com/tronprotocol/java-tron/pull/4045 

#### 3. Optimize the `TriggerConstantContract` API
In GreatVoyage-v4.4.0 (Rousseau), the following optimizations have been introduced to the `TriggerConstantContract` interface:
-  Execute contract creation when `ContractAddress` is empty
-  Remove the check of the incoming parameters `callvalue` and `tokenvalue`
-  The log list and internal transaction list are added to `TransactionExtention`

Source Code： https://github.com/tronprotocol/java-tron/pull/4032 


### Changes
#### 1. Upgrade event plugin to support `BTTC` data 
The event plugin has been upgraded in GreatVoyage-v4.4.0 (Rousseau) to support `BTTC`.

Source code: https://github.com/tronprotocol/java-tron/pull/4067  

#### 2. Increase the upper limit of the `MaxFeeLimit` network parameter.
In the version before GreatVoyage-v4.4.0 (Rousseau), the value range of `MaxFeeLimit` is [0,1e10] sun, in GreatVoyage-v4.4.0 (Rousseau)  the value range of `MaxFeeLimit` is expanded to [0, 1e17] sun.

Source Code： https://github.com/tronprotocol/java-tron/pull/4032 

**NOTICE**：
By default, this feature is disabled, it will be enabled after the London upgrade proposal takes effect.

#### 3. Optimize the quick start script `start.sh`
The quick start script tool is also upgraded in the GreatVoyage-v4.4.0 (Rousseau) version, please refer to the latest user guide from: https://github.com/tronprotocol/java-tron/blob/release_v4.4.0/shell.md


--- 

*The world of reality has its limits; the world of imagination is boundless.* 
<p align="right"> ---  Rousseau</p>


## GreatVoyage-4.3.0(Bacon)
The release of GreatVoyage-v4.3.0 (Bacon) includes several significant optimization enhancements. The configurability of the parameters `FREE_NET_LIMIT` and `TOTAL_NET_LIMIT` will aid the TRON community in achieving improved on-chain governance; The addition of new TVM instructions and ABI types facilitates the use of smart contracts; the new cryptography library strengthens the TRON network's security; the optimization of the account data storage and transaction verification procedures increases transaction processing speed and block verification speed, greatly improving the TRON network's performance; node startup speed improvement will benefit customers and help the TRON ecosystem grow even further.

### Core

#### 1. Add a proposal to adjust the free net limit in an account.
Prior to GreatVoyage-v4.3.0 (Bacon), the account's daily free bandwidth quota was fixed at 5000. The GreatVoyage-v4.3.0 (Bacon) version includes the #61 proposal `FREE_NET_LIMIT`, which allows for the customization of the free bandwidth quota. Super representatives and super partners may initiate a vote request for Proposal 61, which modifies the `FREE_NET_LIMIT` variable, which has the value [0, 100000].

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-292.md
* Source Code: https://github.com/tronprotocol/java-tron/pull/3917 

**NOTICE**
The account's daily free bandwidth quota  is not changed now. The super representative or super partner will initiate a vote request to change the value in the future.

#### 2. Add a proposal to adjust the total net limit.
Prior to GreatVoyage-v4.3.0 (Bacon), the total bandwidth obtained by staking TRX throughout the entire network was fixed at 43,200,000,000.
The GreatVoyage-v4.3.0 (Bacon) version incorporates proposal #62 `TOTAL_NET_LIMIT`, which allows for configuring the total bandwidth available by staking TRX over the entire network. Super representatives and super partners may initiate a voting request for Proposal 62, which amends `TOTAL_NET_LIMIT`. `TOTAL_NET_LIMIT` has a range of [0, 1000000000000].

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-293.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3917  

**NOTICE**
The total net limit is not changed now. The super representative or super partner will initiate a vote request to change the value in the future.

#### 3. Optimize the Account Data Structure
Account is a database that receives numerous accesses during the node's operation, necessitating frequent deserialization operations on the account data structure. Prior to GreatVoyage-v4.3.0 (Bacon), Account contained not only the account's basic data, but also user TRC-10 asset data. However, for TRX transfers and smart contract-related transactions, only the Account's basic data is used. An excessively large TRC-10 asset list will have a significant impact on the Account data structure's deserialization performance.
GreatVoyage-v4.3.0 (Bacon) improves the Account database's storage structure by separating TRC-10 asset data from the Account and storing it independently in the `AccountAssetIssue`. Reduce the amount of data that is deserialized during Account deserialization and increase the deserialization speed.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-295.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3906 

**NOTICE**
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

### TVM

#### 1. Add Vote Instructions and Precompile Contracts in TVM
Ordinary accounts can earn block rewards and voting rewards in versions prior to GreatVoyage-v4.3.0 (Bacon) by voting for super representatives or super representative candidates. However, because TVM does not accept voting instructions, TRX assets in smart contract accounts are unable to generate revenue via voting.
The GreatVoyage-v4.3.0 (Bacon) version adds voting instructions to TVM: `VOTE` / `WITHDRAWBALANCE`, allowing smart contract accounts to vote for super representatives or super representative candidates.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-271.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3921 

**NOTICE**
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

#### 2. Add a New Type: `Error` in Smart Contract ABI
GreatVoyage-v4.3.0 (Bacon) provides a new ABI type Error, which is a custom error type that is compatible with Ethereum solidity 0.8.4's new features.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-306.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3921 

### API

#### 1. Add a New Field: `energy_used` in `TransactionExtention`
Users cannot forecast the energy usage of smart contract transactions in versions earlier to GreatVoyage-v4.3.0 (Bacon).
The version of GreatVoyage-v4.3.0 (Bacon) adds the `energy_used` field to the `TransactionExtension`. When the user invokes the contract method via `TriggerConstantContract`, a sandbox environment based on the most recently synchronized block at the current node is created to supply TVM with this method call. Following the execution, the actual energy consumption figure is written to the `energy_used` field(this operation will not generate an on-chain transaction, nor will it change the status of the current node).

 * Source Code: https://github.com/tronprotocol/java-tron/pull/3940 

### Changes

#### 1. Change the Cryptography Library to Bouncy Castle
Since `SpongyCastle` is no longer maintained, `BouncyCastle` is utilized as the encryption library starting with GreatVoyage-v4.3.0 (Bacon).

* Source Code: https://github.com/tronprotocol/java-tron/pull/3919 

#### 2. Modify the Calculation of `net_usage` Value in the `Transactioninfo` when Creating New Accounts
When a new account is created in GreatVoyage-v4.3.0 (Bacon), the method for calculating `net_usage` is altered.

* Source Code: https://github.com/tronprotocol/java-tron/pull/3917 

#### 3. Optimize the Block Verification
When a node checks a block prior to GreatVoyage-v4.3.0 (Bacon), it verifies each transaction included inside it, regardless of whether it has been verified previously. The transaction verification procedure consumes roughly one-third of the total time required to process a block.
The GreatVoyage-v4.3.0 (Bacon) release optimizes the block verification logic. If non-`AccountUpdateContract` transactions in the block have been validated previously (`AccountUpdateContract` transactions entail account permission changes), they will no longer be verified to expedite block verification.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-276.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3910 

#### 4. Optimize the Node Startup
Prior to GreatVoyage-v4.3.0 (Bacon), during node startup, transaction cache and block data from the database are read to complete the RAM transaction cache initialization. The RAM transaction cache initialization process has been streamlined in GreatVoyage-v4.3.0 (Bacon), and some superfluous parsing processes have been deleted. The speed of node startup will be increased following optimization.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-285.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3907 

#### 5. Optimize Transaction Processing Flow to Reduce Memory Usage

The transaction processing flow is streamlined in GreatVoyage-v4.3.0 (Bacon), unneeded objects are released in advance, and memory utilization is optimized.

* Source Code: https://github.com/tronprotocol/java-tron/pull/3911 

#### 6. Add New Plugins to Optimize the Performance of `levedb` Startup

In the version before GreatVoyage-v4.3.0 (Bacon), with the running of `levedb`, the manifest file will continue to grow. Excessive manifest file will not only affect the startup speed of the node but also may cause the memory to continue to grow and lead to insufficient memory and the service was terminated abnormally.
GreatVoyage-v4.3.0 (Bacon) introduces the `leveldb` startup optimization plug-in. The plug-in optimizes the file size of the manifest and the startup process of LevelDB, reduces memory usage, and improves node startup speed.

* TIP:  https://github.com/tronprotocol/tips/blob/master/tip-298.md 
* Source Code:  https://github.com/tronprotocol/java-tron/pull/3925
* Plug-in Usage Guide: https://github.com/tronprotocol/documentation-en/blob/master/docs/developers/archive-manifest.md

*Knowledge is power.* 
<p align="right"> --- Francis Bacon </p>




## GreatVoyage-4.2.2.1(Epictetus)
We have just released the version of GreatVoyage-v4.2.2.1(Epictetus). The main new features and modifications are as follows:

### Core Protocol
#### 1. Optimize the processing logic of `pending transactions`.
In the versions before GreatVoyage-v4.2.2.1(Epictetus), if the node has enabled the event subscription service, there will be a small probability of abnormal node synchronization.


The GreatVoyage-v4.2.2.1(Epictetus) version optimizes the processing logic of `pending transaction`, fixes the synchronization exception, and improves the stability of the event subscription service.

- Source code: [#3874](https://github.com/tronprotocol/java-tron/pull/3874 )

The update introduced by the GreatVoyage-v4.2.2.1(Epictetus) version optimizes the processing logic of `pending transaction`, which will greatly improve the stability of the event subscription service, bring a better experience for TRON users, and further prosper the TRON ecosystem.

 --- 
*No great thing is created suddenly.* 
<p align="right"> --- Epictetus</p>



## GreatVoyage-4.2.2(Lucretius)
The version of GreatVoyage-v4.2.2 (Lucretius) introduces three important optimizations. The optimization of block processing effectively improves the execution speed of the block, thereby significantly improving the performance of the TRON network. Efficient HTTP/RPC query and excellent TVM performance will bring a better experience to TRON DAPP users and further prosper the TRON ecosystem.

### Core Protocol

#### 1. Block Processing optimization

In the versions before GreatVoyage-v4.2.2 (Lucretius), to obtain the witness list during block processing, multiple database queries and deserialization operations were performed, which took up nearly 1/3 of the block processing time.

The GreatVoyage-v4.2.2 (Lucretius) version simplifies the query of witnesses. In the block processing process, the witness list can be obtained by only one query. After testing, this optimization has dramatically improved the block processing performance.


- TIP: [TIP-269](https://github.com/tronprotocol/tips/blob/master/tip-269.md)
- Source code: [#3827](https://github.com/tronprotocol/java-tron/pull/3827)

#### 2. Data Query optimization

In the versions before GreatVoyage-v4.2.2 (Lucretius), multiple HTTP or RPC queries for data on the chain are mutually exclusive. If a query request is being processed, a new query request will keep waiting until the previous request is completed. 

However, data query methods never use shared data, and no lock operation is required. This optimization removes unnecessary synchronization locks in the query process and improves the performance of internal queries, HTTP and RPC query requests of nodes.

#### 3. Smart Contract ABI Storage optimization

In the version before GreatVoyage-v4.2.2 (Lucretius), the ABI other data of the smart contract are stored together in the contract database, and some high-frequency instructions (SLOAD, SSTORE, Etc.) will read all the data of a smart contract from the contract database. However, the execution of the contract does not use these ABI data, and these frequent readings will impact the execution efficiency of these instructions.

In the version of GreatVoyage-v4.2.2 (Lucretius), smart contract ABIs are transferred to a particular ABI database. The ABI data will no longer be read during the execution of the contract, thus significantly improving the performance of TVM.

- TIP: [TIP-268](https://github.com/tronprotocol/tips/blob/master/tip-268.md)
- Source code: [#3836](https://github.com/tronprotocol/java-tron/pull/3836)

### Other Changes

#### 1. System Contract `BatchValidateSign` Initialization Process optimization

- Source code: [#3836](https://github.com/tronprotocol/java-tron/pull/3836)




 --- *Truths kindle light for truths.* 
<p align="right"> --- Lucretius</p>




## GreatVoyage-4.2.0(Plato)
The GreatVoyage-4.2.0 (Plato) version introduces two important updates. The optimization of the resource model will increase the utilization rate of TRON network resources and make the resource acquisition method more reasonable. The new TVM instructions make the use scenarios of smart contracts more abundant and will further enrich the TRON ecosystem.

### Core Protocol
#### 1. Optimize the resource model 

Before the GreatVoyage-4.2.0 (Plato) version, while users obtained a large amount of TRON power by staking TRX, they also obtained a large amount of energy and bandwidth. The utilization rate of these energies and bandwidth is extremely low, and most of them are not used at all, which increases the cost of obtaining resources. In order to improve the utilization rate of these resources, the GreatVoyage-4.2.0(Plato) version proposes an optimization of the resource model, where staking TRX can only obtain one of the three resources, namely bandwidth, energy, and TRON power. After optimization, users can obtain the corresponding resources based on their own needs, thereby improving the utilization rate of resources.

- TIP： [TIP-207](https://github.com/tronprotocol/tips/blob/master/tip-207.md)
- Source Code:  [#3726](https://github.com/tronprotocol/java-tron/pull/3726)

**Notes:**
  * This feature is disabled by default and can be enabled through the proposal system.
  * After the feature is enabled, the user's previously obtained resources remain unchanged. The TRON power obtained before the proposal passage will be cleared when the user triggers an unstake  transaction (unstake bandwidth, energy, or TRON power).

### TVM
#### 1、Add Freeze/Unfreeze instructions in TVM


In the TRON network, one non-contract account can stake TRX to obtain resources such as bandwidth, energy, TRON power, and reasonable use of these resources can bring certain benefits to users. At the same time, although smart contract accounts do have TRX, there is no way to stake these TRX to obtain resources.  In order to solve this inconsistency, the GreatVoyage-4.2.0(Plato) version introduces Freeze/Unfreeze instructions in TVM, so that smart contracts can also support staking TRX to obtain resources.

- TIP: [TIP-157](https://github.com/tronprotocol/tips/blob/master/tip-157.md)
- Source Code： [#3728](https://github.com/tronprotocol/java-tron/pull/3728)

**Notes:**
  * This feature is disabled by default and can be enabled through the proposal system.
  * The TVM `freeze` instruction can obtain bandwidth and energy. For TRON POWER, it can be obtained and used after the TVM supports the voting instruction.
  * The `receiving` address/`target` address used in the Freeze/Unfreeze instructions must be `address payable` type, and the `receiving` address/`target` address cannot be a contract address other than itself.
  * The inactive account will be automatically activated if the account is the receiver of TVM `Freeze` instruction, and 25,000 energy will be deducted as the account activation cost.

### Other Changes
#### 1、Optimize the block synchronization.

- Source code：[#3732](https://github.com/tronprotocol/java-tron/pull/3732)




--- 
*The beginning is the most important part of the work.* 
<p align="right"> --- Plato</p>




## GreatVoyage-4.1.3(Thales)
GreatVoyage-4.1.3(Thales)  is released with the following new features and modifications:
### Core Protocol
#### 1.Sorting the transactions in pending pool,  SR will prioritize the transactions with high packing fee
In GreatVoyage-4.1.2 and earlier versions, SR packaging transactions are carried out in accordance with the time sequence of the arrival of the transaction.This will easily be attacked by low transaction fees.

After this optimization, block producers sort the transactions to be packaged according to the cost, and then prioritize the transaction with high cost to prevent low-cost transaction attacks.

### API
#### 1.Add new API to support transaction query in pending pool.
It is currently impossible to query the intermediate state information of a certain transaction from after it is issued to before it is on the chain.After a transaction is sent, if it is not on the chain, we cannot know whether it is waiting for packaging or has been discarded.

In this upgrade, the Fullnode node provides 3 API to obtain detailed information about the pending pool:
- /wallet/gettransactionfrompending: Obtain the transaction information from pending pool through the - transaction ID
- /wallet/gettransactionlistfrompending: Get all transactions from the pending pool
- /wallet/getpendingsize: Get the number of transactions in pending pool


The optimization of transaction packaging logic of GreatVoyage-4.1.3(Thales)  will effectively reduce low-cost attacks and greatly improve the security of the TRON public chain.


---




## Great Voyage - v4.1.2
GreatVoyage-version 4.1.2 is released with the following new features and modifications:
 
### I. Core Protocol
#### 1、Reward SRs with the transaction fees charged for bandwidth and energy. 

After this feature is turned on, the transaction fee from burning TRX which charged for bandwidth/energy (except OUT_OF_TIME) will be transferred to TRANSACTION_FEE_POOL. At the end of each block, the fee of all transactions in this block is rewarded to the block SR and its voters. At the same time, in "transactioninfo", the "packingFee" field is added to indicate the available fees to the current SR and SR voters. 

- TIP: [TIP-196](https://github.com/tronprotocol/tips/issues/196)
- Source Code:  [#3532](https://github.com/tronprotocol/java-tron/pull/3532)


#### 2、Support account history balance query.

The account historical balance query function can facilitate developers to query the account balance information at a specific block height. Developers can obtain the account historical balance information through the following two APIs.

- /wallet/getaccountbalance ：query account balance at a specific block.
- /wallet/getblockbalance ： Query the balance-changing operations in a specific block.

**Note:**
1. This function is disabled by default and can be enabled through the node configuration file.
2. After the function is enabled, users can only query the historical balance after the enabled time. If users need to query the complete historical balance information, they can use the data snapshot which contains the historical balance information to resynchronize the node.

- Source Code：[#3538](https://github.com/tronprotocol/java-tron/pull/3538)
- Guide ： https://github.com/tronprotocol/documentation-en/blob/master/docs/api/http.md

###3、Optimzed the blackhole account to improve transaction execution speed

After the feature is turned on, the transaction fee from burning TRX which charged f for bandwidth and energy will no longer be transferred to the black hole address but will be directly accumulated and recorded in the database.

- Source code： [#3617](https://github.com/tronprotocol/java-tron/pull/3617)

### II. TVM
#### 1、Adopt to solidity0.6.0.

After this upgrade, TRON will be fully compatible with the new features introduced by solidity 0.6.0, including the new virtual and override keywords, and supporting try/catch. For details, please refer to the TRON Solidity release note: https://github.com/tronprotocol/solidity/releases/tag/tv_0.6.0 

- TIP:  [TIP-209](https://github.com/tronprotocol/tips/issues/209)
- Source Code： [#3351](https://github.com/tronprotocol/java-tron/pull/3535)

###2、Make MAX_FEE_LIMIT configurable as a chain property.

After the new version, SR and SRP can initiate a voting request to modify MAX_FEE_LIMIT. The range of MAX_FEE_LIMIT is [0,10000_000_000].

- TIP： [TIP-204](https://github.com/tronprotocol/tips/issues/204) 
- Source code：  [#3534](https://github.com/tronprotocol/java-tron/pull/3534)
 
### III. Others Changes
###1、Use the jitpack repository to provide dependency support and make it easy for developers to use java-tron as a dependency for their projects. 

- Source code: [#3554](https://github.com/tronprotocol/java-tron/pull/3554)




## GreatVoyage-v4.1.1
GreatVoyage-version 4.1.1 is released with the following new features and modifications:
 
### I. Core Protocol
#### 1. New Consensus Protocol
The new consensus mechanism combines TRON's existing DPoS consensus with the PBFT consensus mechanism. PBFT's three-phase voting mechanism is adopted to confirm whether a block should be solidified. It will take an average of 1-2 slots (a slot equals 3s) from creation to confirmation of a TRON block, much shorter than the previous 19 slots. This signifies a remarkable increase in the block confirmation speed.
TIP: [TICP-Optimized-PBFT](https://github.com/tronprotocol/tips/blob/master/tp/ticp/ticp-optimized-pbft/ticp-Optimized-PBFT.md)
Source code: [#3082](https://github.com/tronprotocol/java-tron/pull/3082)
 
#### 2. New Node Type
We added another type of node to the existing FullNode: Lite FullNode. Lite FullNode executes the same code with the FullNode. What sets it apart is that its launch is based on the status data snapshot, which contains all the status data and data history of the latest 256 blocks.
The status data snapshot can be acquired by executing LiteFullNodeTool.jar (please see: [Use the LiteFullNode Tool](https://tronprotocol.github.io/documentation-en/developers/litefullnode/)).
- TIP: [TIP-128](https://github.com/tronprotocol/tips/blob/master/tip-128.md)
- Source code: [#3031](https://github.com/tronprotocol/java-tron/pull/3031)
 
### II. TVM
#### Achieved compatibility with Ethereum Istanbul upgrade
a. Added new instruction `CHAINID` to fetch the genesis block ID of the current chain, which avoids possible replay attacks of one transaction being repeated on different chains.
- TIP: [TIP-174](https://github.com/tronprotocol/tips/blob/master/tip-174.md)
- Source code: [#3351](https://github.com/tronprotocol/java-tron/pull/3351)

b. Added new instruction `SELFBALANCE` to fetch the balance of the current contract address in the smart contract. For obtaining the balance of any address, please stick with instruction BALANCE.SELFBALANCE is safer to use. Energy consumption of using `BALANCE` might rise in the future.
- TIP: [TIP-175](https://github.com/tronprotocol/tips/blob/master/tip-175.md)
- Source code: [#3351](https://github.com/tronprotocol/java-tron/pull/3351)
 
c. Reduced Energy consumption of three precompiled contract instructions, namely BN128Addition, BN128Multiplication, and BN128Pairing.
BN128Addition: from 500 Energy to 150 Energy
BN128Multiplication: from 40000 Energy to 6000 Energy
BN128Pairing: from (80000 \* pairs + 100000) Energy to (34000 \* pairs + 45000) Energy
- TIP: [TIP-176](https://github.com/tronprotocol/tips/blob/master/tip-176.md)
- Source code: [#3351](https://github.com/tronprotocol/java-tron/pull/3351)
 
### III. Mechanism
1. Added two new system contracts, namely MarketSellAssetContract and MarketCancelOrderContract, for on-chain TRX/TRC10 transactions in decentralized exchanges.
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md)
- Source code: [#3302](https://github.com/tronprotocol/java-tron/pull/3302)
 
### IV. Other Modifications
1. Added a few node performance indicators.
- Source code: [#3350](https://github.com/tronprotocol/java-tron/pull/3350)
 
2. Added market order detail in the original transactionInfo interface.
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md)
- Source code: [#3302](https://github.com/tronprotocol/java-tron/pull/3302)
 
3. Improved the script for docker deployment.
- Source code: [#3330](https://github.com/tronprotocol/java-tron/pull/3330)





## GreatVoyage-v4.0.0
Release 4.0.0 has implemented the shielded TRC-20 contract, which can hide the source address, destination address, and the token amount for TRC-20 transactions and provide users with better privacy.  The shielded TRC-20 contract has three core functions: `mint`, `transfer` and `burn`. `mint` is used to transform the public TRC-20 token to shielded token; `transfer` is used for shielded token transactions; `burn` is used to transform the shielded token back to the public TRC-20 token. To support the shielded TRC-20 contract,  four new zero-knowledge instructions (`verifyMintProof`, `verifyTransferProof`, `verifyBurnProof` and `pedersenHash`) are add in TVM, which make it convenient to provide privacy for arbitrary TRC-20 contract.

### Notices 
Forced upgrade

### New features
 - Add 4 new instructions (`verifyMintProof`, `verifyTransferProof`, `verifyBurnProof` and `pedersenHash`) in TVM to support TRC20 shielded transactions based on zk-SNARKs (#3172).
   - `verifyMintProof`: used to validate the zero-knowledge proof for `mint` function.
   - `verifyTransferProof`: used to validate the zero-knowledge proof for `transfer` function.
   - `verifyBurnProof`: used to validate  the zero-knowledge proof for `burn` function.
   - `pedersenHash`: used to compute the Pedersen hash.
- Update the initial parameters of zk-SNARKs scheme generated by the MPC Torch (#3210).
- Add the APIs to support shielded TRC-20 contract transaction (#3172).
  
   1.&nbsp;Create shielded contract parameters
  ```protobuf
  rpc CreateShieldedContractParameters (PrivateShieldedTRC20Parameters) returns (ShieldedTRC20Parameters) {}
  ```
  2.&nbsp;Create shielded contract parameters without ask
  ```protobuf
  rpc CreateShieldedContractParametersWithoutAsk (PrivateShieldedTRC20ParametersWithoutAsk) returns (ShieldedTRC20Parameters) {}
  ```
  3.&nbsp;Scan shielded TRC20 notes by ivk
  ```protobuf
  rpc ScanShieldedTRC20NotesByIvk (IvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
  ```
  4.&nbsp;Scan shielded TRC20 notes by ovk
  ```protobuf
  rpc ScanShieldedTRC20NotesByOvk (OvkDecryptTRC20Parameters) returns (DecryptNotesTRC20) {}
  ```
  5.&nbsp;Check if the shielded TRC20 note is spent
  ```protobuf
  rpc IsShieldedTRC20ContractNoteSpent (NfTRC20Parameters) returns (NullifierResult) {}
  ```
  6.&nbsp;Get the trigger input for the shielded TRC20 contract
  ```protobuf
    rpc GetTriggerInputForShieldedTRC20Contract (ShieldedTRC20TriggerContractParameters) returns (BytesMessage) {}
  ```
- Support the `ovk` to scan the transparent output of  `burn` transaction (#3203).
- Support the `burn` transaction with zero or one shielded output (#3224).
- Add data field in transaction log trigger class for future memo note (#3200).

The following TIPs are implemented in this release:
- [TIP-135](https://github.com/tronprotocol/tips/blob/master/tip-135.md): Shielded TRC-20 contract standards, guarantee the privacy of the shielded transfer of TRC-20 tokens.
- [TIP-137](https://github.com/tronprotocol/tips/blob/master/tip-137.md): Implements three zero-knowledge proof instructions in TVM to support the shielded TRC-20 contract (#3172).
- [TIP-138](https://github.com/tronprotocol/tips/blob/master/tip-138.md): Implements the Pedersen hash computation instruction in TVM to support the shielded TRC-20 contract (#3172).
 
### Changes
- Check if null before getInstance when get transaction info from DB to fix exception of `getTransactioninfoByBlkNum` (#3165).


## Odyssey-v3.7
Odyssey-v3.7 is a non-mandatory upgrade, includes the following new features and improvements.

### Modularization
Odyssey-v3.7 has modularized the code organization structure, making it much easier for developers to develop customized module，several mainly modules are listed as follows：

#### Framework
As the core module, Framework performs as both a gateway to the blockchain and an adhesive that effectively connects all other modules. In other words, the framework module initializes each module and facilitates communication between modules.

#### Protocol
The decentralized Tron protocol can be implemented by any teams without limitation of programming languages. Any clients in accordance with the Tron protocol can communicate with each other.
A concise and efficient data transfer protocol is essential to a distributed network, even more for the blockchain. So, the implementation of the protocol is based on the Protocol Buffers, an open-source and excellent software protocol maintained by Google. 
The specific business logic of the blockchain defined by the protocol includes:
- the data format of message，including block, transaction, proposal, witness, vote, account, exchange and so on.
- the communication protocols between blockchain nodes, including the node discovery protocol, the node data synchronization protocol, the node scoring protocol and so on.
- the interface protocols that the blockchain provides to the external system or clients

#### Consensus 
The consensus mechanism is an essential part of the blockchain. The Tron blockchain chooses the DPoS as the core consensus mechanism and it has been running steadily for a long time. But replaceable consensus module is essential if we want to redefine the java-tron as the powerful infrastructure for building application-specific blockchains. The developers of blockchain should determine to choose the consensus mechanism that considered to be most suitable to the specific application scenario. The ultimate goal of the replaceable consensus module is that the consensus mechanism can be determined by configuring some necessary parameters. In addition, the developers can implement a customized consensus module as long as several essential interfaces implemented.

#### Crypto
Encryption is also one of the core modules of the blockchain. It is the foundation of the
blockchain data security. such as public and private key deduction, transaction verification, zero-knowledge proof, etc. The java-tron abstracts the encryption module and supports the replacement of encryption algorithms. A suitable encryption algorithm can be chosen according to different business needs.

#### Actuator
Actuator is the core module used for handling various kinds of transactions. As you know, every transaction in the Tron blockchain contains a contract. On a high level, there are two types of contracts in the Tron blockchain, the system contract and the smart contract. A large number of applications are implemented by the smart contracts and ran in an internal virtual machine of the blockchain. Unfortunately, smart contracts are constrained in terms of their functions and not flexible enough to accommodate the needs of complex applications. Customized actuators offer application developers a brand new way of development. They can choose to implant their application codes into the chain instead of running them on virtual machines.

#### Chainbase
Chainbase is specially designed for data storage in the blockchain. Nodes always consider the longest chain to be the correct one and will keep working on extending it. So switching to the longest chain is a common scenario for the blockchain unless it uses a deterministic consensus algorithm like PBFT. For this reason, supporting data rollback is the most distinctive feature of the chainbase module. Several well-designed abstract interfaces are defined in this module. So, the developers can choose the storage engine freely and then implement corresponding interfaces. The LevelDB and RocksDB are two existing implementation.

### New event subscription trigger for solidified block
Added a subscription trigger for the updating a solidified block, which triggers the solidified block update event to the message queue, so that users can get the latest solidified block information on time. A solidified block is a block that regarded as can not be revocable. So, when the block becomes a solidified block, it means that the transactions packed in this block are accepted by the blockchain.

### Two new HTTP APIs added
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

### A new RPC API added
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



## Odyssey-v3.6.5
Odyssey v3.6.5 Update includes the following new features and improvements   

### 1. New delegation mechanism  

The new delegation mechanism enables SRs to set commission rates by themselves, which will serve as a reference for users when they vote for SRs. Meanwhile, traceability of the SR’s commission rate on the chain makes the amount of rewards that users receive through voting more transparent. Moreover, the new delegation mechanism lays a foundation for more complex consensus mechanisms and incentive schemes in the near future. 

### 2. Fairer and more efficient staking rewards mechanism
    
Staking rewards are now distributed in a fully-decentralized way, a step forward from the old partially-decentralized mechanism. With this change, staking rewards are now distributed entirely through the blockchain, ensuring complete supervision from the chain and thus true decentralization. Moreover, the new mechanism cuts unnecessary reward distribution transactions, signaling lower bandwidth consumption and higher efficiency on the TRON network.

### 3. Fairer incentive mechanism

Block rewards decreased from 32 TRX to 16 TRX, while voting rewards increased from 16 TRX to 160 TRX. The adjustment will boost voter turnout in the community, with more TRX locked up by users in the TRON ecosystem. This move is accompanied by the new staking rewards mechanism to guarantee real staking revenues to users.

### 4. Improvement and optimization of TVM

(1) Added a new VM instruction ISCONTRACT(0xd4), which has made smart contract development more flexible by allowing developers to identify the type of the target address in VMs when writing contracts. 
batchvalidatesign(bytes32 hash, bytes[] memory signatures, address[] memory addresses) 

(2) Adopted a multi-thread method for VMs to verify signatures, which is faster than ecrecover of Ethereum while cutting Energy consumption by half.
Contract address: 0x09. To use it in solidity: batchvalidatesign(bytes32 hash, bytes[] memory signatures, address[] memory addresses) 
validatemultisign(address accountAddress, uint256 permissionId, bytes32 content, bytes[] signatures)

(3) Added a new pre-compiled contract to boost multi-signature verification in TVM, speeding up the verification process and reducing Energy consumption.

(4) Banned transfer TRX to smart contract address by two system contract TransferContract and TransferAssetContract. The transfer would fail if the target address is a smart 	 address when using TransferContract and TransferAssetContract. This can prevent general users from transferring assets to smart contract address by mistake, avoiding users’ asset loss.

(5) Allowed automatic activation of inactive accounts when transferring TRX/ TRC10 tokens to accounts in smart contracts. 

(6) Added triggerConstantContract feature for SolidityNode and FullNode so as to improve the functionality of node APIs.

### 5. Improvement of the dynamic adjustment scheme of Energy upper limit

The method of calculating Energy consumed per unit of time shifted from only calculating the staked Energy consumed to all Energy consumed. With this change, statistics of Energy consumption will be more accurate and effective, providing reference for adjusting Energy upper limit, saving users’ costs of using TRON blockchain network and improving network efficiency.





