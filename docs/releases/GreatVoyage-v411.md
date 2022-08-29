# GreatVoyage-v4.1.1
GreatVoyage-version 4.1.1 is released with the following new features and modifications:
 
## I. Core Protocol
### 1. New Consensus Protocol
The new consensus mechanism combines TRON's existing DPoS consensus with the PBFT consensus mechanism. PBFT's three-phase voting mechanism is adopted to confirm whether a block should be solidified. It will take an average of 1-2 slots (a slot equals 3s) from creation to confirmation of a TRON block, much shorter than the previous 19 slots. This signifies a remarkable increase in the block confirmation speed.
TIP: [TICP-Optimized-PBFT](https://github.com/tronprotocol/tips/blob/master/tp/ticp/ticp-optimized-pbft/ticp-Optimized-PBFT.md)
Source code: [#3082](https://github.com/tronprotocol/java-tron/pull/3082)
 
### 2. New Node Type
We added another type of node to the existing FullNode: Lite FullNode. Lite FullNode executes the same code with the FullNode. What sets it apart is that its launch is based on the status data snapshot, which contains all the status data and data history of the latest 256 blocks.
The status data snapshot can be acquired by executing LiteFullNodeTool.jar (please see: [Use the LiteFullNode Tool](https://tronprotocol.github.io/documentation-en/developers/litefullnode/)).
- TIP: [TIP-128](https://github.com/tronprotocol/tips/blob/master/tip-128.md)
- Source code: [#3031](https://github.com/tronprotocol/java-tron/pull/3031)
 
## II. TVM
### Achieved compatibility with Ethereum Istanbul upgrade
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
 
## III. Mechanism
1. Added two new system contracts, namely MarketSellAssetContract and MarketCancelOrderContract, for on-chain TRX/TRC10 transactions in decentralized exchanges.
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md)
- Source code: [#3302](https://github.com/tronprotocol/java-tron/pull/3302)
 
## IV. Other Modifications
1. Added a few node performance indicators.
- Source code: [#3350](https://github.com/tronprotocol/java-tron/pull/3350)
 
2. Added market order detail in the original transactionInfo interface.
- TIP: [TIP-127](https://github.com/tronprotocol/tips/blob/master/tip-127.md)
- Source code: [#3302](https://github.com/tronprotocol/java-tron/pull/3302)
 
3. Improved the script for docker deployment.
- Source code: [#3330](https://github.com/tronprotocol/java-tron/pull/3330)