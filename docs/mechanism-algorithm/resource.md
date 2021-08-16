# Resource Model

## Introduction

TRON network has 4 types of resources: Bandwidth, CPU, Storage and RAM. Benefit by TRON's exclusive RAM model, TRON's RAM resource is almost infinite.

TRON network imports two resource conceptions: Bandwidth points and Energy. Bandwidth Point represents Bandwidth, Energy represents CPU and Storage.

!!! note
    - Ordinary transaction only consumes Bandwidth points
    - Smart contract related transaction not only consumes Bandwidth points, but also Energy

## Bandwidth Points

The transaction information is stored and transmitted in the form of byte array, Bandwidth Points consumed = the number of bytes of the transaction * Bandwidth Points rate. Currently Bandwidth Points rate = 1.

Such as if the number of bytes of a transaction is 200, so this transaction consumes 200 Bandwidth Points.

!!! note
    Due to the change of the total amount of the staked TRX in the network and the self-staked TRX amount, the Bandwidth Points an account possesses is not fixed.

### 1. How to Get Bandwidth Points

1. By staking TRX to get Bandwidth Points, Bandwidth Points = the amount of TRX self-staked / the total amount of TRX staked for Bandwidth Points in the network * 43_200_000_000
2. Every account has a fixed amount of free Bandwidth Points(5000) every day

### 2. Bandwidth Points Consumption

Except for query operation, any transaction consumes Bandwidth points.

There's another situation: When you transfer(TRX or token) to an account that does not exist in the network, this operation will first create that account in the network and then do the transfer. It only consumes Bandwidth points for account creation, no extra Bandwidth points consumption for transfer.

To create an account, a flat charge of 1 TRX is required. If there are insufficient Bandwidth points obtained by TRX staking, an additional 0.1 TRX will be spent.

Bandwidth points consumption sequence for TRC-10 transfer:

1. Free Bandwidth points.

2. TRC-10 issuer's Bandwidth points(if possible.)

3. Bandwidth points TRX staking.

4. Bandwidth points obtained by TRX burning, the rate = the number of bytes of the transaction * 1_000 SUN;

Bandwidth points consumption sequence for other transactions:

1. Free Bandwidth points.

2. Bandwidth points TRX staking.

3. Bandwidth points obtained by TRX burning, the rate = the number of bytes of the transaction * 1_000 SUN;

### 3. Bandwidth Points Recovery

Every 24 hours, the amount of the usage of Bandwidth points of an account will be reset to 0. For the specific formula:

$$
U^\prime = ( 1 - \frac{T_2 - T_1}{24h} ) * U + u
$$

Every 24 hours, the amount of the usage of Bandwidth points of an account will be reset to 0.

## Energy

Each command of smart contract consume system resource while running, we use 'Energy' as the unit of the consumption of the resource.

### 1. How to Get Energy

Stake TRX to get energy.

Example (Using wallet-cli):

```text
freezeBalance frozen_balance frozen_duration [ResourceCode:0 BANDWIDTH,1 ENERGY]
```

stake TRX to get energy, energy obtained = user's TRX staked amount / total amount of staked TRX in TRON * 50_000_000_000.

Example:

```text
If there are only two users, A stakes 2 TRX, B stakes 2 TRX
the energy they can get is:
A: 25_000_000_000 and energy_limit is 25_000_000_000
B: 25_000_000_000 and energy_limit is 25_000_000_000

when C stakes 1 TRX:
the energy they can get is:
A: 20_000_000_000 and energy_limit is 20_000_000_000
B: 20_000_000_000 and energy_limit is 20_000_000_000
B: 10_000_000_000 and energy_limit is 10_000_000_000
```

#### Energy Recovery

The energy consumed will reduce to 0 smoothly within 24 hours.

Example:

```text
at one moment, A has used 72_000_000 Energy
if there is no continuous consumption or TRX stake
one hour later, the energy consumption amount will be 72_000_000 - (72_000_000 * (60*60/60*60*24)) Energy = 69_000_000 Energy
24 hours later, the energy consumption amount will be 0 Energy
```

### 2. How to Set Fee Limit (Caller Must Read)

***
*Within the scope of this section, the smart contract developer will be called "developer", the users or other contracts which call the smart contract will be called "caller"*

*The amount of energy consumed while call the contract can be converted to TRX or SUN, so within the scope of this section, when refer to the consumption of the resource, there's no strict difference between Energy, TRX and SUN, unless they are used as a number unit.*

***

Set a rational fee limit can guarantee the smart contract execution. And if the execution of the contract cost great energy, it will not consume too much energy from the caller. Before you set fee limit, you need to know several conception:

1. The legal fee limit is a integer between 0 - 10^9, unit is SUN.
2. Different smart contracts consume different amount of energy due to their complexity. The same trigger in the same contract almost consumes the same amount fo energy[^1]. When the contract is triggered, the commands will be executed one by one and consume energy. If it reaches the fee limit, commands will fail to be executed, and energy is not refundable.
3. Currently fee limit only refers to the energy converted to SUN that will be consumed from the caller[^2]. The energy consumed by triggering contract also includes developer's share.
4. For a vicious contract, if it encounters execution timeout or bug crash, all it's energy will be consumed.
5. Developer may undertake a proportion of energy consumption(like 90%). But if the developer's energy is not enough for consumption, the rest of the energy consumption will be undertaken by caller completely. Within the fee limit range, if the caller does not have enough energy, then it will burn equivalent amount of TRX [^2].

To encourage caller to trigger the contract, usually developer has enough energy.

#### Example

How to estimate the fee limit:

Assume contract C's last execution consumes 18000 Energy, so estimate the energy consumption limit to be 20000 Energy[^3]

According to the staked TRX amount and energy conversion, assume 1 TRX = 400 energy.

When to burn TRX, 4 TRX = 100000 energy[^4]

Assume developer undertake 90% energy consumption, and developer has enough energy.

Then the way to estimate the fee limit is:

1. A = 20000 energy * (1 TRX / 400 energy) = 50 TRX = 50_000_000 SUN,
2. B = 20000 energy * (4 TRX / 100000 energy) = 0.8 TRX = 800_000 SUN,
3. Take the greater number of A and B, which is 50_000_000 SUN,
4. Developer undertakes 90% energy consumption, caller undertakes 10% energy consumption,

So, the caller is suggested to set fee limit to 50_000_000 SUN * 10% = 5_000_000 SUN

### 3. Energy Calculation (Developer Must Read)

1. In order to punish the vicious developer, for the abnormal contract, if the execution times out (more than 50ms) or quits due to bug (revert not included), the maximum available energy will be deducted. If the contract runs normally or revert, only the energy needed for the execution of the commands will be deducted.

2. Developer can set the proportion of the energy consumption it undertakes during the execution, this proportion cna be changed later. If the developer's energy is not enough, it will consume the caller's energy.

3. Currently, the total energy available when trigger a contract is composed of caller fee limit and developer's share

!!! note
    - If the developer is not sure about whether the contract is normal, do not set caller's energy consumption proportion to 0%, in case all developer's energy will be deducted due to vicious execution[^1].
    - We recommend to set caller's energy consumption proportion to 10% ~ 100%[^2].

** Example 1 **

A has an account with a balance of 90 TRX(90000000 SUN) and 10 TRX staked for 100000 energy.

Smart contract C set the caller energy consumption proportion to 100% which means the caller will pay for the energy consumption completely.

A triggers C, the fee limit set is 30000000 (unit SUN, 30 TRX)

So during this trigger the energy A can use is from two parts:

- A's energy by staking TRX;
- The energy converted from the amount of TRX burning according to a fixed rate;

If fee limit is greater than the energy obtained from staking TRX, then it will burn TRX to get energy. The fixed rate is: 1 Energy = 100 SUN, fee limit still has (30 - 10) TRX = 20 TRX available, so the energy it can keep consuming is 20 TRX / 100 SUN = 200000 energy.

Finally, in this call, the energy A can use is (100000 + 200000) = 300000 energy.

If contract executes successfully without any exception, the energy needed for the execution will be deducted. Generally, it is far more less than the amount of energy this trigger can use.

If Assert-style error come out, it will consume the whole number of energy set for fee limit.

Assert-style error introduction, refer to [Exception Handling(zh-cn)](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md)

** Example 2 **

A has an account with a balance of 90 TRX(90000000 SUN) and 10 TRX staked for 100000 energy.

Smart contract C set the caller energy consumption proportion to 40% which means the developer will pay for the rest 60% energy consumption.

Developer D stakes 50 TRX to get 500000 energy.

A triggers C, the fee limit set is 200000000 (unit SUN, 200 TRX).

So during this trigger the energy A can use is from three parts:

- A's energy by staking TRX -- X;
- The energy converted from the amount of TRX bruning according to a fixed rate -- Y;

    If fee limit is greater than the energy obtained from staking TRX, then it will burn TRX to get energy. The fixed rate is: 1 Energy = 100 SUN, fee limit still has (200 - 10) TRX = 190 TRX available, but A only has 90 TRX left, so the energy it can keep consuming is 90 TRX / 100 SUN = 900000 energy;

- D's energy by staking TRX -- Z;

There are two situation:
if (X + Y) / 40% >= Z / 60%, the energy A can use is X + Y + Z
if (X + Y) / 40% < Z / 60%, the energy A can use is (X + Y) / 40%

If contract executes successfully without any exception, the energy needed for the execution will be deducted. Generally, it is far more less than the amount of energy this trigger can use.

If Assert-style error comes out, it will consume the whole number of energy set for fee limit. Assert-style error introduction, refer to [Exception Handling(zh-cn)](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md).

Note: when developer create a contract, do not set consume_user_resource_percent to 0, which means developer will undertake all the energy consumption. If Assert-style error comes out, it will consume all energy from the developer itsef.

Assert-style error introduction, refer to [Exception Handling(zh-cn)](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md).

To avoid unnecessary lost, 10 - 100 is recommended for consume_user_resource_percent.

## Resource Delegation
In TRON network, an account can stake TRX for Bandwidth or Energy for other accounts. The primary account owns the staked TRX and TRON power, the recipient account owns the Bandwidth or Energy. Like ordinary staking, resource delegation staking is also at least 3 days.

+ Example(Using wallet-cli)
```text
freezeBalance frozen_balance frozen_duration [ResourceCode:0 BANDWIDTH,1 ENERGY] [receiverAddress]

frozen_balance: the amount of TRX to stake (unit SUN)
frozen_duration: the staking period (currently a fixed 3 days)
ResourceCode: 0 for Bandwidth, 1 for Energy
receiverAddress: recipient account address
```

## Other Fees

|Type|Fee|
| :------|:------:|
|Create a witness|9999 TRX|
|Issue a token|1024 TRX|
|Create an account|1 TRX|
|Create an exchange|1024 TRX|

[^1]: The energy consumption of each execution may fluctuate slightly due to the situation of all the nodes.
[^2]: TRON may change this policy.
[^3]: The estimated energy consumption limit for the next execution should be greater than the last one.
[^4]: 4 TRX = 10^5 energy is a fixed number for burning TRX to get energy, TRON may change it in future.
