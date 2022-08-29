# Great Voyage - v4.1.2
GreatVoyage-version 4.1.2 is released with the following new features and modifications:
 
## I. Core Protocol
### 1、Reward SRs with the transaction fees charged for bandwidth and energy. 

After this feature is turned on, the transaction fee from burning TRX which charged for bandwidth/energy (except OUT_OF_TIME) will be transferred to TRANSACTION_FEE_POOL. At the end of each block, the fee of all transactions in this block is rewarded to the block SR and its voters. At the same time, in "transactioninfo", the "packingFee" field is added to indicate the available fees to the current SR and SR voters. 

- TIP: [TIP-196](https://github.com/tronprotocol/tips/issues/196)
- Source Code:  [#3532](https://github.com/tronprotocol/java-tron/pull/3532)


### 2、Support account history balance query.

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

## II. TVM
### 1、Adopt to solidity0.6.0.

After this upgrade, TRON will be fully compatible with the new features introduced by solidity 0.6.0, including the new virtual and override keywords, and supporting try/catch. For details, please refer to the TRON Solidity release note: https://github.com/tronprotocol/solidity/releases/tag/tv_0.6.0 

- TIP:  [TIP-209](https://github.com/tronprotocol/tips/issues/209)
- Source Code： [#3351](https://github.com/tronprotocol/java-tron/pull/3535)

###2、Make MAX_FEE_LIMIT configurable as a chain property.

After the new version, SR and SRP can initiate a voting request to modify MAX_FEE_LIMIT. The range of MAX_FEE_LIMIT is [0,10000_000_000].

- TIP： [TIP-204](https://github.com/tronprotocol/tips/issues/204) 
- Source code：  [#3534](https://github.com/tronprotocol/java-tron/pull/3534)
 
## III. Others Changes
###1、Use the jitpack repository to provide dependency support and make it easy for developers to use java-tron as a dependency for their projects. 

- Source code: [#3554](https://github.com/tronprotocol/java-tron/pull/3554)