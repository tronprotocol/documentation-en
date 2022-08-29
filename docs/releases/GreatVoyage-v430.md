# GreatVoyage-4.3.0(Bacon)
The release of GreatVoyage-v4.3.0 (Bacon) includes several significant optimization enhancements. The configurability of the parameters `FREE_NET_LIMIT` and `TOTAL_NET_LIMIT` will aid the TRON community in achieving improved on-chain governance; The addition of new TVM instructions and ABI types facilitates the use of smart contracts; the new cryptography library strengthens the TRON network's security; the optimization of the account data storage and transaction verification procedures increases transaction processing speed and block verification speed, greatly improving the TRON network's performance; node startup speed improvement will benefit customers and help the TRON ecosystem grow even further.

# Core

## 1. Add a proposal to adjust the free net limit in an account.
Prior to GreatVoyage-v4.3.0 (Bacon), the account's daily free bandwidth quota was fixed at 5000. The GreatVoyage-v4.3.0 (Bacon) version includes the #61 proposal `FREE_NET_LIMIT`, which allows for the customization of the free bandwidth quota. Super representatives and super partners may initiate a vote request for Proposal 61, which modifies the `FREE_NET_LIMIT` variable, which has the value [0, 100000].

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-292.md
* Source Code: https://github.com/tronprotocol/java-tron/pull/3917 

**NOTICE**
The account's daily free bandwidth quota  is not changed now. The super representative or super partner will initiate a vote request to change the value in the future.

## 2. Add a proposal to adjust the total net limit.
Prior to GreatVoyage-v4.3.0 (Bacon), the total bandwidth obtained by staking TRX throughout the entire network was fixed at 43,200,000,000.
The GreatVoyage-v4.3.0 (Bacon) version incorporates proposal #62 `TOTAL_NET_LIMIT`, which allows for configuring the total bandwidth available by staking TRX over the entire network. Super representatives and super partners may initiate a voting request for Proposal 62, which amends `TOTAL_NET_LIMIT`. `TOTAL_NET_LIMIT` has a range of [0, 1000000000000].

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-293.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3917  

**NOTICE**
The total net limit is not changed now. The super representative or super partner will initiate a vote request to change the value in the future.

## 3. Optimize the Account Data Structure
Account is a database that receives numerous accesses during the node's operation, necessitating frequent deserialization operations on the account data structure. Prior to GreatVoyage-v4.3.0 (Bacon), Account contained not only the account's basic data, but also user TRC-10 asset data. However, for TRX transfers and smart contract-related transactions, only the Account's basic data is used. An excessively large TRC-10 asset list will have a significant impact on the Account data structure's deserialization performance.
GreatVoyage-v4.3.0 (Bacon) improves the Account database's storage structure by separating TRC-10 asset data from the Account and storing it independently in the `AccountAssetIssue`. Reduce the amount of data that is deserialized during Account deserialization and increase the deserialization speed.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-295.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3906 

**NOTICE**
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

# TVM

## 1. Add Vote Instructions and Precompile Contracts in TVM
Ordinary accounts can earn block rewards and voting rewards in versions prior to GreatVoyage-v4.3.0 (Bacon) by voting for super representatives or super representative candidates. However, because TVM does not accept voting instructions, TRX assets in smart contract accounts are unable to generate revenue via voting.
The GreatVoyage-v4.3.0 (Bacon) version adds voting instructions to TVM: `VOTE` / `WITHDRAWBALANCE`, allowing smart contract accounts to vote for super representatives or super representative candidates.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-271.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3921 

**NOTICE**
By default, this feature is disabled, and the super representative or super partner will initiate a vote request to enable it in the future.

## 2. Add a New Type: `Error` in Smart Contract ABI
GreatVoyage-v4.3.0 (Bacon) provides a new ABI type Error, which is a custom error type that is compatible with Ethereum solidity 0.8.4's new features.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-306.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3921 

# API

## 1. Add a New Field: `energy_used` in `TransactionExtention`
Users cannot forecast the energy usage of smart contract transactions in versions earlier to GreatVoyage-v4.3.0 (Bacon).
The version of GreatVoyage-v4.3.0 (Bacon) adds the `energy_used` field to the `TransactionExtension`. When the user invokes the contract method via `TriggerConstantContract`, a sandbox environment based on the most recently synchronized block at the current node is created to supply TVM with this method call. Following the execution, the actual energy consumption figure is written to the `energy_used` field(this operation will not generate an on-chain transaction, nor will it change the status of the current node).

 * Source Code: https://github.com/tronprotocol/java-tron/pull/3940 

# Changes

## 1. Change the Cryptography Library to Bouncy Castle
Since `SpongyCastle` is no longer maintained, `BouncyCastle` is utilized as the encryption library starting with GreatVoyage-v4.3.0 (Bacon).

* Source Code: https://github.com/tronprotocol/java-tron/pull/3919 

## 2. Modify the Calculation of `net_usage` Value in the `Transactioninfo` when Creating New Accounts
When a new account is created in GreatVoyage-v4.3.0 (Bacon), the method for calculating `net_usage` is altered.

* Source Code: https://github.com/tronprotocol/java-tron/pull/3917 

## 3. Optimize the Block Verification
When a node checks a block prior to GreatVoyage-v4.3.0 (Bacon), it verifies each transaction included inside it, regardless of whether it has been verified previously. The transaction verification procedure consumes roughly one-third of the total time required to process a block.
The GreatVoyage-v4.3.0 (Bacon) release optimizes the block verification logic. If non-`AccountUpdateContract` transactions in the block have been validated previously (`AccountUpdateContract` transactions entail account permission changes), they will no longer be verified to expedite block verification.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-276.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3910 

## 4. Optimize the Node Startup
Prior to GreatVoyage-v4.3.0 (Bacon), during node startup, transaction cache and block data from the database are read to complete the RAM transaction cache initialization. The RAM transaction cache initialization process has been streamlined in GreatVoyage-v4.3.0 (Bacon), and some superfluous parsing processes have been deleted. The speed of node startup will be increased following optimization.

* TIP: https://github.com/tronprotocol/tips/blob/master/tip-285.md 
* Source Code: https://github.com/tronprotocol/java-tron/pull/3907 

## 5. Optimize Transaction Processing Flow to Reduce Memory Usage

The transaction processing flow is streamlined in GreatVoyage-v4.3.0 (Bacon), unneeded objects are released in advance, and memory utilization is optimized.

* Source Code: https://github.com/tronprotocol/java-tron/pull/3911 

## 6. Add New Plugins to Optimize the Performance of `levedb` Startup

In the version before GreatVoyage-v4.3.0 (Bacon), with the running of `levedb`, the manifest file will continue to grow. Excessive manifest file will not only affect the startup speed of the node but also may cause the memory to continue to grow and lead to insufficient memory and the service was terminated abnormally.
GreatVoyage-v4.3.0 (Bacon) introduces the `leveldb` startup optimization plug-in. The plug-in optimizes the file size of the manifest and the startup process of LevelDB, reduces memory usage, and improves node startup speed.

* TIP:  https://github.com/tronprotocol/tips/blob/master/tip-298.md 
* Source Code:  https://github.com/tronprotocol/java-tron/pull/3925
* Plug-in Usage Guide: https://github.com/tronprotocol/documentation-en/blob/master/docs/developers/archive-manifest.md

*Knowledge is power.* 
<p align="right"> --- Francis Bacon </p>