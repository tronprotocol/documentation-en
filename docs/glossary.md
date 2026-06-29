# Glossary

**energyUsage**

The Energy consumption of the contract caller in one contract trigger.  (EnergyFee not included)

**energyFee**

The amount of TRX (measured in sun, 1 TRX = 1,000,000 sun) burned from the contract caller for Energy consumption in one contract trigger.

**originEnergyUsage**

The total Energy consumption of the contract developer in one contract trigger.

**energyUsageTotal**

The total Energy consumption of the contract developer and the contract caller combined.

**FeeLimit**

When the user triggers or creates the contract, this is used to set the usage limit of the Energy obtained from burning or staking TRX, Energy obtained from staking TRX will be used first.

**CallValue**

When the user triggers or creates the contract, this can be used to send TRX to the contract.

**consume_user_resource_percent**

For a contract, Resource consumption is composed of two parts: one part is afforded by the contract developer and the other by the contract caller. This is the percentage afforded by the contract caller; the remaining part (100 minus this value) is afforded by the contract developer.

**origin_energy_limit**

The usage limit of the Energy consumption of the developer in one contract trigger, should be greater than 0.

**net_usage**

The Bandwidth consumption in one contract trigger.  (NetFee not included)

**net_fee**

The amount of TRX (measured in sun, 1 TRX = 1,000,000 sun) burned for Bandwidth consumption in one contract trigger.

**Bandwidth**

The Bandwidth Points consumed by a transaction is the size of the byte array in this transaction. If the byte array length of a transaction is 100, then the transaction needs to consume 100 Bandwidth Points.

**Energy**

Energy is the resource consumed by the creation and execution of smart contracts. Every operation executed in the TRON Virtual Machine (TVM) costs a fixed, deterministic amount of Energy defined by the VM's Energy cost schedule (for example, an `SLOAD` costs 50 Energy and creating a new storage slot via `SSTORE` costs 20000 Energy). The more computation a contract performs, the more Energy it consumes. Energy can be obtained by staking TRX, or paid for by burning TRX.

**TRON Power(TP)**

1 staked TRX = 1 TP, TP can be used to vote, 1 TP = 1 vote.

**Super Representative(SR)**

The top 27 witnesses by votes, responsible for producing blocks.
