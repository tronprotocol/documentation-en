# GreatVoyage-4.2.0(Plato)
The GreatVoyage-4.2.0 (Plato) version introduces two important updates. The optimization of the resource model will increase the utilization rate of TRON network resources and make the resource acquisition method more reasonable. The new TVM instructions make the use scenarios of smart contracts more abundant and will further enrich the TRON ecosystem.

# Core Protocol
## 1. Optimize the resource model 

Before the GreatVoyage-4.2.0 (Plato) version, while users obtained a large amount of TRON power by staking TRX, they also obtained a large amount of energy and bandwidth. The utilization rate of these energies and bandwidth is extremely low, and most of them are not used at all, which increases the cost of obtaining resources. In order to improve the utilization rate of these resources, the GreatVoyage-4.2.0(Plato) version proposes an optimization of the resource model, where staking TRX can only obtain one of the three resources, namely bandwidth, energy, and TRON power. After optimization, users can obtain the corresponding resources based on their own needs, thereby improving the utilization rate of resources.

- TIP： [TIP-207](https://github.com/tronprotocol/tips/blob/master/tip-207.md)
- Source Code:  [#3726](https://github.com/tronprotocol/java-tron/pull/3726)

**Notes:**
  * This feature is disabled by default and can be enabled through the proposal system.
  * After the feature is enabled, the user's previously obtained resources remain unchanged. The TRON power obtained before the proposal passage will be cleared when the user triggers an unstake  transaction (unstake bandwidth, energy, or TRON power).

# TVM
## 1、Add Freeze/Unfreeze instructions in TVM


In the TRON network, one non-contract account can stake TRX to obtain resources such as bandwidth, energy, TRON power, and reasonable use of these resources can bring certain benefits to users. At the same time, although smart contract accounts do have TRX, there is no way to stake these TRX to obtain resources.  In order to solve this inconsistency, the GreatVoyage-4.2.0(Plato) version introduces Freeze/Unfreeze instructions in TVM, so that smart contracts can also support staking TRX to obtain resources.

- TIP: [TIP-157](https://github.com/tronprotocol/tips/blob/master/tip-157.md)
- Source Code： [#3728](https://github.com/tronprotocol/java-tron/pull/3728)

**Notes:**
  * This feature is disabled by default and can be enabled through the proposal system.
  * The TVM `freeze` instruction can obtain bandwidth and energy. For TRON POWER, it can be obtained and used after the TVM supports the voting instruction.
  * The `receiving` address/`target` address used in the Freeze/Unfreeze instructions must be `address payable` type, and the `receiving` address/`target` address cannot be a contract address other than itself.
  * The inactive account will be automatically activated if the account is the receiver of TVM `Freeze` instruction, and 25,000 energy will be deducted as the account activation cost.

# Other Changes
## 1、Optimize the block synchronization.

- Source code：[#3732](https://github.com/tronprotocol/java-tron/pull/3732)




--- 
*The beginning is the most important part of the work.* 
<p align="right"> --- Plato</p>