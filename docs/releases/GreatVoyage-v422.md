# GreatVoyage-4.2.2(Lucretius)
The version of GreatVoyage-v4.2.2 (Lucretius) introduces three important optimizations. The optimization of block processing effectively improves the execution speed of the block, thereby significantly improving the performance of the TRON network. Efficient HTTP/RPC query and excellent TVM performance will bring a better experience to TRON DAPP users and further prosper the TRON ecosystem.

# Core Protocol

## 1. Block Processing optimization

In the versions before GreatVoyage-v4.2.2 (Lucretius), to obtain the witness list during block processing, multiple database queries and deserialization operations were performed, which took up nearly 1/3 of the block processing time.

The GreatVoyage-v4.2.2 (Lucretius) version simplifies the query of witnesses. In the block processing process, the witness list can be obtained by only one query. After testing, this optimization has dramatically improved the block processing performance.


- TIP: [TIP-269](https://github.com/tronprotocol/tips/blob/master/tip-269.md)
- Source code: [#3827](https://github.com/tronprotocol/java-tron/pull/3827)

## 2. Data Query optimization

In the versions before GreatVoyage-v4.2.2 (Lucretius), multiple HTTP or RPC queries for data on the chain are mutually exclusive. If a query request is being processed, a new query request will keep waiting until the previous request is completed. 

However, data query methods never use shared data, and no lock operation is required. This optimization removes unnecessary synchronization locks in the query process and improves the performance of internal queries, HTTP and RPC query requests of nodes.

## 3. Smart Contract ABI Storage optimization

In the version before GreatVoyage-v4.2.2 (Lucretius), the ABI other data of the smart contract are stored together in the contract database, and some high-frequency instructions (SLOAD, SSTORE, Etc.) will read all the data of a smart contract from the contract database. However, the execution of the contract does not use these ABI data, and these frequent readings will impact the execution efficiency of these instructions.

In the version of GreatVoyage-v4.2.2 (Lucretius), smart contract ABIs are transferred to a particular ABI database. The ABI data will no longer be read during the execution of the contract, thus significantly improving the performance of TVM.

- TIP: [TIP-268](https://github.com/tronprotocol/tips/blob/master/tip-268.md)
- Source code: [#3836](https://github.com/tronprotocol/java-tron/pull/3836)

# Other Changes

## 1. System Contract `BatchValidateSign` Initialization Process optimization

- Source code: [#3836](https://github.com/tronprotocol/java-tron/pull/3836)




 --- *Truths kindle light for truths.* 
<p align="right"> --- Lucretius</p>

