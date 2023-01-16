# GreatVoyage-v4.7.0(Aristotle)

GreatVoyage-v4.7.0 (Aristotle) introduces several important optimizations and updates. The new stake mechanism, Stake 2.0, improves the flexibility of the resource model and the stability of the stake system; the dynamic energy model helps to promote ecologically balanced development; the secondary cache mechanism optimizes the database reading performance, improves transaction execution performance, and expands the network throughput; uses the libp2p library as the Java-tron P2P network module to make the code structure clearer and reduce code coupling; optimizes the log output, redirect the logs of LevelDB and RocksDB to Java-tron log files; integrate more tools and functions into the ‘Toolkit.jar’ toolbox to bring users a more convenient development experience.

Please see the details below.

## Cores
### 1. A new stake model - Stake 2.0 
GreatVoyage-v4.7.0 (Aristotle) version introduces a new stake model, Stake 2.0, aiming to establish a more flexible, efficient and stable stake system. Compared with the current Stake 1.0 model, Stake 2.0 has been improved in the following aspects,

* Staking and delegating are separated

    In Stake 1.0, staking and resource delegating are combined in one operation. The resource recipient must be specified in the operation. After the staking is completed, the resource will be delegated to the designated resource recipient. The unstaking and undelegating are also combined in one operation. If you want to cancel the delegating, you must unstake the corresponding TRX as well. Stake 2.0 separates staking and resource delegating into two independent operations. The user executes the staking first, the resource selected is allocated to the owner now. And then executes the delegate operation to assign the resource to the designated address. Unstaking and undelegating are also separated into two operations. If the user wants to cancel the delegating, he or she can directly perform the undelegate operation without unstaking and then can delegate the resource to others again as needed. Separation of staking/unstaking and delegating/undelegating simplifies user operations and reduces operational complexity.

* Resource Fragmentation Management

    In Stake 1.0, one unstake operation will unstake all the staked TRX, and the specified amount of TRX cannot be unstaked. This is optimized in Stake 2.0 now. We can specify an amount of TRX to unstake, as long as the specified amount is less than or equal to the total staked amount. In Stake 1.0, to cancel a certain resource delegate, you can only cancel all delegated resources at once, and you cannot cancel by specifying an amount. Stake 2.0 has also brought partially undelegate, we can now undelegate part of the delegated resources as needed, which improves the flexibility of resource management.

* Unstake Lock Period and Delayed Arrival of Unstaked TRX

    In Stake 1.0, after staking TRX, we need to wait 3 days before releasing the TRX. After the release, the TRX staked will immediately arrive in the owner’s account. In Stake 2.0, after the staking is completed, the TRX staked can be released at any time, but it needs to wait for ’N’ days. After the ’N’ days delay, the TRX released could be withdrawn to the owner’s account. ’N’ is the TRON network parameter. When the TRX market fluctuates violently, due to the delayed arrival of funds, it will no longer trigger a large number of stake or unstake operations, which improves the stability of the stake model, and at the same time will not cause a large number of funds to flood into the market and aggravate market volatility. It helps to build a more anticipated future of the entire network circulation for the network participants.
 
* TVM Supports Staking and Resource Management

    In Stake 2.0, the TRON virtual machine integrates instructions related to stake and resource management. Users can perform TRX stake/unstake operations in smart contracts, as well as perform resource delegate/undelegate operations.


For more details on Stake 2.0, please refer to  [What is Stake 2.0?](https://coredevs.medium.com/what-is-stake-2-0-e04f59b948a6)

The new stake mechanism is a dynamic parameter in the TRON network. After GreatVoyage-v4.7.0 (Aristotle) is deployed, it is disabled by default and can be enabled by initiating a proposal vote.

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4838](https://github.com/tronprotocol/java-tron/pull/4838) 

### 2.Enhance database query performance
Java-tron uses memory and disk databases for data storage. The solidified block data will be stored in multiple disk databases, and the unsolidified data will be stored in memory. When a block is solidified, the corresponding in-memory data is written to the disk databases. When querying data, first query the data in memory, if not found, then query the disk database. The disk database query is time-consuming. Therefore, the GreatVoyage-v4.7.0 (Aristotle) version optimizes the database query performance and adds a secondary cache before performing the underlying disk database operation. When data is written to the disk, the data is also written to the second-level cache. When the disk database needs to be queried, if the data to be queried exists in the second-level cache, it will be returned directly without querying the disk database. The second-level cache reduces the number of queries to the disk database, improves transaction execution speed, and improves network throughput.



* Source code: [https://github.com/tronprotocol/java-tron/pull/4740](https://github.com/tronprotocol/java-tron/pull/4740) 

### 3. Optimize block production process
When a node produces a block, it will sequentially verify and execute all transactions that can be packaged into the block, and each transaction verification and execution will involve the acquisition of block data, such as block number, block size, block transaction information, etc. In versions prior to GreatVoyage-v4.7.0 (Aristotle), when nodes package transactions, block data is recalculated during the process of verifying and executing each transaction, which includes many repeated calculations.

In order to improve the efficiency of packaging transactions, the GreatVoyage-v4.7.0 (Aristotle) optimizes the block production process, only calculates the block data once and updates the data only when necessary, thus greatly reducing the number of block data calculations and improving the block packaging efficiency.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4756](https://github.com/tronprotocol/java-tron/pull/4756) 

### 4. Add transaction hash cache
When a node processes a block, it will use the transaction hash value multiple times. In versions before GreatVoyage-v4.7.0 (Aristotle), the transaction hash value is calculated as it is used, and the calculation of the transaction hash value is time-consuming, which leads to slower block processing. Therefore, GreatVoyage-v4.7.0 (Aristotle) adds a transaction hash cache, the transaction hash will be directly obtained from the cache when used. Only when the transaction data changes, the transaction hash is recalculated. The newly added cache reduces unnecessary transaction hash calculations and improves block processing speed.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4792](https://github.com/tronprotocol/java-tron/pull/4792)  

### 5. Add `libp2p` module as Java-tron p2p network protocol implementation
Starting from GreatVoyage-v4.7.0 (Aristotle), the libp2p library will be directly used as the P2P network module of Java-tron, instead of using the original p2p network stack, so that the code structure is clearer, the code coupling is lower, and is easy to maintain.


* Source code: [https://github.com/tronprotocol/java-tron/pull/4791](https://github.com/tronprotocol/java-tron/pull/4791) 


## TVM
### 1. Add new instructions to support Stake 2.0
GreatVoyage-v4.7.0 (Aristotle) introduces Stake 2.0, TVM will support Stake 2.0 related stake and resource delegate instructions simultaneously. Users can perform stake and resource delegate operations through smart contracts, which further enriches the application scenarios of smart contracts on the TRON network. A total of 6 instructions from 0xda to 0xdf have been added to TVM:

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



Stake 2.0 is a dynamic parameter in the TRON network. After GreatVoyage-v4.7.0 (Aristotle) is deployed, it is disabled by default and can be enabled by initiating a proposal vote.

* TIP: [https://github.com/tronprotocol/tips/issues/467](https://github.com/tronprotocol/tips/issues/467) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4872](https://github.com/tronprotocol/java-tron/pull/4872) 

### 2. Dynamic energy model
The dynamic energy model is a scheme to dynamically adjust the future energy consumption of the contract based on the known energy usage of the contract. If a contract uses too many resources in one cycle, then the next cycle in this contract, a certain percentage of punitive consumption will be added, and users who send the same transaction to this contract will cost more energy than before. When the contract uses resources reasonably, the energy consumption generated by the user calling the contract will gradually return to normal. Through this mechanism, the allocation of energy resources on the chain will be more reasonable, and excessive concentration of network resources on a few contracts will be prevented. 

For more information about the dynamic energy model: [Introduction to Dynamic Energy Model](https://coredevs.medium.com/introduction-to-dynamic-energy-model-31917419b61a)

The dynamic energy model is a dynamic parameter in the TRON network. After GreatVoyage-v4.7.0 (Aristotle) is deployed, it is disabled by default and can be enabled by initiating a proposal vote.

* TIP: [https://github.com/tronprotocol/tips/issues/491](https://github.com/tronprotocol/tips/issues/491) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 

### 3. Optimize the return value of the `chainId` opcode

Starting from the GreatVoyage-v4.7.0 (Aristotle) version, the return value of the `chainid` opcode is changed from the block hash of the genesis block to the last four bytes of the block hash of the genesis block, keeping the return value of the chainid opcode consistent with the return value of the Java-tron JSON-RPC `eth_chainId` API.

The return value optimization of the chainId opcode is a dynamic parameter of the TRON network. It is disabled by default after GreatVoyage-v4.7.0 (Aristotle) is deployed, and can be enabled by initiating a proposal.

* TIP: [https://github.com/tronprotocol/tips/issues/474](https://github.com/tronprotocol/tips/issues/474) 
* Source code: [https://github.com/tronprotocol/java-tron/pull/4863](https://github.com/tronprotocol/java-tron/pull/4863) 


## API

### 1. Add APIs to support Stake 2.0
GreatVoyage-v4.7.0 (Aristotle) adds 10 APIs to support Stake 2.0:

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

### 2. Add energy estimation API
In versions prior to GreatVoyage-v4.7.0 (Aristotle), users can estimate the energy consumption for executing smart contract transactions through the `/wallet/triggerconstantcontract` interface, and then set the `feelimit` parameter of the transaction according to the estimated consumption. However, since some smart contract transactions may call other smart contracts, it is possible that the estimated `feelimit` parameter is inaccurate.

Therefore, the GreatVoyage-v4.7.0(Aristotle) version adds an energy estimation interface `/wallet/estimateenergy`, and the `feelimit` estimated by this interface is reliable in any case. The `energy_required` field in the return value of this interface indicates the estimated amount of energy required for the successful execution of this smart contract transaction. So user can calculate the `feelimit` parameter based on this field: `feelimit` = `energy_required` * energy unit price, currently the unit price of energy is 420 sun.

If the execution of the estimated interface call fails for some reason, the value of the `energy_required` field will be 0, and this field will not be displayed in the return value. At this time, you can check the reason for the execution failure for the estimated interface call through the `result` field.

After the GreatVoyage-v4.7.0 (Aristotle) version is successfully deployed, this API is closed by default. To open this interface, the two configuration items `vm.estimateEnergy` and `vm.supportConstant` must be enabled in the node configuration file at the same time. The default values of `vm.estimateEnergy` and `vm.supportConstant` are both false,

* Source code: [https://github.com/tronprotocol/java-tron/pull/4873](https://github.com/tronprotocol/java-tron/pull/4873) 



## Other Changes
### 1. Optimize Gradle compilation parameters
GreatVoyage-v4.7.0(Aristotle) optimizes the compiling parameters of Gradle, configuring JVM minimum heap size to 1GB, which improves the compilation speed of Java-tron.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4837](https://github.com/tronprotocol/java-tron/pull/4837) 

### 2. Optimize node conditional stop function

In order to facilitate data backup or data statistics for node deployers, starting from GreatVoyage-v4.5.1 (Tertullian), nodes support stopping under specific conditions. Users can set the conditions for node stopping through the node configuration file, and the node will stop running when the conditions are met. It supports three stop conditions to be set at the same time, and the node is stopped when any condition is met. These three conditions include block time, block height, and the number of blocks that need to be synchronized from the start to the stop of the node. However, since multiple stop conditions are allowed to be set at the same time, when the user only needs one condition,  the other 2 conditional configuration items in the configuration file need to be deleted, so if the user forgets to delete, the node may stop on an unexpected block. However, there are actually no application scenarios that require multiple conditions to be set at the same time. Therefore, the GreatVoyage-v4.7.0 (Aristotle) version optimizes the node conditional stop function. The optional configuration parameters remain unchanged, but only one valid parameter is allowed to be set at the same time. If the node deployer sets multiple parameters, the node will report an error and exit run. This optimization simplifies the complexity of users’ settings.

* Source code:  [https://github.com/tronprotocol/java-tron/pull/4853](https://github.com/tronprotocol/java-tron/pull/4853)
[https://github.com/tronprotocol/java-tron/pull/4858](https://github.com/tronprotocol/java-tron/pull/4858) 

### 3. Delete code related to database v1
In versions prior to GreatVoyage-v4.7.0 (Aristotle), there are two versions of the database, v1 and v2. Users can choose from them through the configuration item `db.version`. Since the v2 version adopts the memory + disk database mode, it supports the expansion of the underlying database, the correct data recovery function under abnormal conditions, etc., and has obvious advantages compared with v1. Therefore, in order to make the code structure clearer, starting from GreatVoyage-v4.7.0 (Aristotle), the code related to the database v1 version and the database version configuration item `db.version` has been deleted. Users no longer need to configure the database version, only v2 is available from now on, which reduces the complexity of configuring nodes.

* Source code:  [https://github.com/tronprotocol/java-tron/pull/4836](https://github.com/tronprotocol/java-tron/pull/4836)

### 4. Optimize database log output
In versions prior to GreatVoyage-v4.7.0 (Aristotle), the node logs do not include the underlying logs output by LevelDB or RocksDB itself, making it difficult to troubleshoot database read and write problems. Therefore, the GreatVoyage-v4.7.0 (Aristotle) optimizes the database log and redirects the output of the underlying log of the LevelDB or RocksDB data module to the node log file, which simplifies the difficulty of database troubleshooting and improves the reliability of node operation and maintenance efficiency.

* Source code:  [https://github.com/tronprotocol/java-tron/pull/4833](https://github.com/tronprotocol/java-tron/pull/4833) 

### 5. Make snapshot flush speed configurable   
Nodes newly added to the network need to synchronize block data from other nodes, and the nodes will first save the synchronized block data in memory, and then store it on disk. In versions prior to GreatVoyage-v4.7.0 (Aristotle), when a node synchronizes the blocks, a flush operation will write the data of 500 blocks from the memory to the disk, so more than 500 blocks data will be kept in the memory, and each block data is associated through a linked list. When querying data, it will first search in these more than 500 blocks in sequence, and then query the disk database when the data to be queried is not found, but traversing more than 500 block data reduces the efficiency of data query.

Therefore, starting from the GreatVoyage-v4.7.0 (Aristotle) version, the number of snapshot flush can be configured, and the maximum number of snapshot flush at one time can be set through the configuration item: `storage.snapshot.maxFlushCount` to maximize the efficiency of database query and improve block processing speed. If the configuration item is not set, the maximum number of snapshots flush into the dish is the default value of 1.

* Source code: [https://github.com/tronprotocol/java-tron/pull/4834](https://github.com/tronprotocol/java-tron/pull/4834) 

### 6. Toolkit.jar Integration
`DBConvert.jar` is a database conversion tool, which can convert LevelDB into RocksDB; `LiteFullNodeTool.jar` is a light FullNode tool, which can convert FullNode data into LiteFullNode data. Starting from GreatVoyage-v4.7.0 (Aristotle), `DBConvert.jar` and `LiteFullNodeTool.jar` have been integrated into the `Toolkit.jar` toolbox, and a database copy function is added which can realize fast Node database copy. In the future, the tools around Java-tron will be gradually integrated into the `Toolkit.jar` toolbox in order to facilitate tool maintenance and developer use. The commands for using the new functions of the `Toolkit.jar` toolbox are as follows:



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




