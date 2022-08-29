# GreatVoyage-4.4.0(Rousseau)
The GreatVoyage-v4.4.0 (Rousseau) version introduces several important updates: the optimization of block broadcasting will let the block be broadcast to the entire network faster; the query performance optimization of `dynamic store` and the optimization of database parameters will be greatly improved Block processing speed, thereby improving the performance of java-tron; API customization in FullNode makes node configuration more flexible for different application scenarios; TVM will also be better compatible with EVM and adapt to the Ethereum London upgrade, the new JSON-RPC API will bring developers a better development experience, help developers to join the TRON ecosystem more easily, and promote the prosperity of the TRON ecosystem.

# Core
## 1. Optimize the block broadcasting
In the version before GreatVoyage-v4.4.0 (Rousseau), the logic of block processing is: verify block -> process block -> broadcast block. However, due to the long block processing time, there is a delay in block broadcasting. In order to speed up block broadcasting, In GreatVoyage-v4.4.0 (Rousseau) version, the block processing logic is changed to: verify block -> broadcast block -> process block, so that the block can be quickly broadcast to the entire network.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-289.md 
Source Code:https://github.com/tronprotocol/java-tron/pull/3986  

## 2. Optimize the query performance of `dynamic store`
During the block processing, The frequency of visits to `dynamic store` is very high. The GreatVoyage-v4.4.0(Rousseau) version optimizes the query performance of the  `dynamic store` by loading all the data of  `dynamic store`  into the first-level cache, the cache hit rate of the `dynamic store`  is improved and the block processing speed is also improved.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-290.md
Source Code：https://github.com/tronprotocol/java-tron/pull/3993  

## 3. Optimize the transaction broadcasting interface
The GreatVoyage-v4.4.0 (Rousseau) version optimizes the processing flow of the transaction broadcast interface. The transaction broadcast is changed from asynchronous to synchronous, and the result will be returned after the broadcast is successful, making the return result of the broadcast more accurate.

Source code：https://github.com/tronprotocol/java-tron/pull/4000 

## 4. Optimize the parameters of the database
The GreatVoyage-v4.4.0 (Rousseau) version optimizes the parameters of the database, which improves the read and write performance of the database, thereby improving the efficiency of block processing.

Source Code：https://github.com/tronprotocol/java-tron/pull/4018 
https://github.com/tronprotocol/java-tron/pull/3992 

# TVM
## 1. Provide compatibility with EVM
The GreatVoyage-v4.4.0 (Rousseau) version provides compatibility solution for those instructions that are different from EVM, so that the newly deployed contract supports the following features:
- The `GASPRICE` instruction returns the unit price of energy.
- The `try/catch-statement` supports catching all types of TVM exceptions.
- Forbid the system contract “TransferContract” to transfer TRX to the smart contract account.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-272.md 
Source Code：https://github.com/tronprotocol/java-tron/pull/4032 

**NOTICE**：
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

## 2. Adapt to Ethereum London Release

In the GreatVoyage-v4.4.0 (Rousseau) version, TVM is also adapted to the Ethereum London upgrade: introduce the `BASEFEE` opcode; the deployment of new contracts starting with 0xEF is prohibited.

TIP: https://github.com/tronprotocol/tips/blob/master/tip-318.md 
Source Code：https://github.com/tronprotocol/java-tron/pull/4032 

**NOTICE**：
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

## 3. In constant mode, `Energy limit` supports customization and the default value is increased

Before the GreatVoyage-v4.4.0 (Rousseau) version, the energy limit in constant mode was a fixed value(`3,000,000`). The GreatVoyage-v4.4.0 (Rousseau) version changed it to configurable, and increase the default value to `100,000,000`. after upgraded to the latest version, `Energy limit` can be configured in startup parameters(`--max-energy-limit-for-constant`) or in the configuration file(`vm.maxEnergyLimitForConstant`). 

Source Code：https://github.com/tronprotocol/java-tron/pull/4032 

# API
## 1. Support Ethereum compatible JSON-RPC API
Starting from the GreatVoyage-v4.4.0 (Rousseau) version, the FullNode supports JSON-RPC APIs. For details, please refer to: https://developers.tron.network/reference#json-rpc-api 

Source Code：https://github.com/tronprotocol/java-tron/pull/4046 

## 2. FullNode supports disabling APIs
In order to make the FullNode customizable, starting from GreatVoyage-v4.4.0 (Rousseau) version, FullNode supports disabling specific APIs through the configuration file.

Source code：https://github.com/tronprotocol/java-tron/pull/4045 

## 3. Optimize the `TriggerConstantContract` API
In GreatVoyage-v4.4.0 (Rousseau), the following optimizations have been introduced to the `TriggerConstantContract` interface:
-  Execute contract creation when `ContractAddress` is empty
-  Remove the check of the incoming parameters `callvalue` and `tokenvalue`
-  The log list and internal transaction list are added to `TransactionExtention`

Source Code： https://github.com/tronprotocol/java-tron/pull/4032 


# Changes
## 1. Upgrade event plugin to support `BTTC` data 
The event plugin has been upgraded in GreatVoyage-v4.4.0 (Rousseau) to support `BTTC`.

Source code: https://github.com/tronprotocol/java-tron/pull/4067  

## 2. Increase the upper limit of the `MaxFeeLimit` network parameter.
In the version before GreatVoyage-v4.4.0 (Rousseau), the value range of `MaxFeeLimit` is [0,1e10] sun, in GreatVoyage-v4.4.0 (Rousseau)  the value range of `MaxFeeLimit` is expanded to [0, 1e17] sun.

Source Code： https://github.com/tronprotocol/java-tron/pull/4032 

**NOTICE**：
By default, this feature is disabled, it will be enabled after the London upgrade proposal takes effect.

## 3. Optimize the quick start script `start.sh`
The quick start script tool is also upgraded in the GreatVoyage-v4.4.0 (Rousseau) version, please refer to the latest user guide from: https://github.com/tronprotocol/java-tron/blob/release_v4.4.0/shell.md


--- 

*The world of reality has its limits; the world of imagination is boundless.* 
<p align="right"> ---  Rousseau</p>