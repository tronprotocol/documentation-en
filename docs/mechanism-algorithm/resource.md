# Resource Model

## Introduction

Voting Right, bandwidth and energy are important system resources of the TRON network. Among them, voting rights are used to vote for super representatives; Bandwidth is the unit that measures the size of the transaction bytes stored in the blockchain database. The larger the transaction, the more bandwidth resources will be consumed. Energy is the unit that measures the amount of computation required by the TRON virtual machine to perform specific operations on the TRON network. Since smart contract transactions require computing resources to execute, each smart contract transaction requires to pay for the energy fee.

!!! note
    - Ordinary transaction only consumes Bandwidth points
    - Smart contract related transaction not only consumes Bandwidth points, but also Energy

## Voting Right
Before any account can vote for super representatives, it needs to obtain voting rights, that is, TRON Power (TP). Voting rights can be obtained by staking TRX. In addition to obtaining bandwidth or energy, staking TRX will also obtain voting rights at the same time. Voters who stake 1TRX will receive 1TP. For how to stake, please refer to the [Staking on TRON Network](#staking-on-tron-network) chapter.

Voters can stake multiple times, and the voting rights obtained by multiple stake will be added to the voter's account. Voters can query the total number of voting rights owned by the account and the number of used voting rights through the `wallet/getaccountresource` interface.

## Bandwidth Points

The transaction information is stored and transmitted in the form of byte array, Bandwidth Points consumed = the number of bytes of the transaction * Bandwidth Points rate. Currently Bandwidth Points rate = 1.

Such as if the number of bytes of a transaction is 200, so this transaction consumes 200 Bandwidth Points.

!!! note
    Due to the change of the total amount of the staked TRX in the network and the self-staked TRX amount, the Bandwidth Points an account possesses is not fixed.

### 1. How to Get Bandwidth Points

1. By staking TRX to get Bandwidth Points, Bandwidth Points = the amount of TRX self-staked / the total amount of TRX staked for Bandwidth Points in the network * 43_200_000_000
2. Every account has a fixed amount of free Bandwidth Points(600) every day

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

After the account's free bandwidth and the bandwidth obtained by staking TRX are consumed, they will gradually recover within 24 hours.

## Energy

Each command of smart contract consume system resource while running, we use 'Energy' as the unit of the consumption of the resource.

### 1. How to Get Energy

Stake TRX to get energy.

Example (Using wallet-cli):

```text
freezeBalanceV2 frozen_balance [ResourceCode:0 BANDWIDTH,1 ENERGY]
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

After the energy resource of the account is consumed, it will gradually recover within 24 hours.

### 2. How to Set Fee Limit (Caller Must Read)

***
*Within the scope of this section, the smart contract developer will be called "developer", the users or other contracts which call the smart contract will be called "caller"*

*The amount of energy consumed while call the contract can be converted to TRX or SUN, so within the scope of this section, when refer to the consumption of the resource, there's no strict difference between Energy, TRX and SUN, unless they are used as a number unit.*

***

Set a rational fee limit can guarantee the smart contract execution. And if the execution of the contract cost great energy, it will not consume too much energy from the caller. Before you set fee limit, you need to know several conception:

1. The legal fee limit is a integer between 0 - 10^9, unit is SUN.
2. Different smart contracts consume different amount of energy due to their complexity. The same trigger in the same contract almost consumes the same amount of energy[^1]. When the contract is triggered, the commands will be executed one by one and consume energy. If it reaches the fee limit, commands will fail to be executed, and energy is not refundable.
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

2. Developer can set the proportion of the energy consumption it undertakes during the execution, this proportion can be changed later. If the developer's energy is not enough, it will consume the caller's energy.

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
- The energy converted from the amount of TRX burning according to a fixed rate -- Y;

    If fee limit is greater than the energy obtained from staking TRX, then it will burn TRX to get energy. The fixed rate is: 1 Energy = 100 SUN, fee limit still has (200 - 10) TRX = 190 TRX available, but A only has 90 TRX left, so the energy it can keep consuming is 90 TRX / 100 SUN = 900000 energy;

- D's energy by staking TRX -- Z;

There are two situation:
if (X + Y) / 40% >= Z / 60%, the energy A can use is X + Y + Z
if (X + Y) / 40% < Z / 60%, the energy A can use is (X + Y) / 40%

If contract executes successfully without any exception, the energy needed for the execution will be deducted. Generally, it is far more less than the amount of energy this trigger can use.

If Assert-style error comes out, it will consume the whole number of energy set for fee limit. Assert-style error introduction, refer to [Exception Handling(zh-cn)](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md).

Note: when developer create a contract, do not set consume_user_resource_percent to 0, which means developer will undertake all the energy consumption. If Assert-style error comes out, it will consume all energy from the developer itself.

Assert-style error introduction, refer to [Exception Handling(zh-cn)](https://github.com/tronprotocol/Documentation/blob/master/%E4%B8%AD%E6%96%87%E6%96%87%E6%A1%A3/%E8%99%9A%E6%8B%9F%E6%9C%BA/%E5%BC%82%E5%B8%B8%E5%A4%84%E7%90%86.md).

To avoid unnecessary lost, 10 - 100 is recommended for consume_user_resource_percent.

## Staking on TRON network


### How to stake to obtain system resources

Energy and bandwidth resources are obtained by the account owner through staking, please use `wallet/freezebalancev2` to complete the stake operation through HTTP API, use [Stake2.0 Solidity API](https://developers.tron.network/docs/stake-20-solidity-api) to complete the stake operation through the contract.

TRON allocates resources through the staking mechanism. In addition to obtaining bandwidth or energy resources, staking TRX will also obtain voting rights (TRON Power, TP for short) equal to the amount staked. Staking 1 TRX, you will get 1TP. The energy or bandwidth resources obtained by staking are used to pay transaction fees, and the obtained voting rights are used to vote for super representatives to obtain voting rewards.

The unstaking operation will release the corresponding resources.

### How to delegate resources

After the account obtains energy or bandwidth resources through staking, it can delegate resources to other addresses through `delegateresource`, and can also take back allocated resources through `undelegateresource`. Please pay attention to the following situations when delegating resource:

- Only energy and bandwidth can be delegated to other addresses, voting rights cannot be delegated
- Only unused resources obtained by staking through Stake2.0 can be delegated to other addresses
- Energy/Bandwidth can only be delegated to an activated external account address, not to a contract address

You can use the `wallet/getcandelegatedmaxsize` interface to query the available delegation share of a certain resource type in the account. `Time lock` can be used when delegating resources. If time lock is used, after the resource delegating is completed, the resource delegation for the address only can be canceled after 3 days. During the locking period, if the user performs resource delegating for the same address again, it will Reset the 3-days waiting period. If the time lock is not used, the delegation can be canceled immediately after the resource is delegated.

### How to unstake TRX

After completing the TRX staking, you can unstake at any time. After unstaking, you need to wait for 14 days before you can withdraw the unstaked TRX into your account. 14 days is [the No.70 parameter](https://tronscan.org/#/sr/committee) of TRON network which can be voted on by network governance proposals. Please use `unfreezebalancev2` to complete unfreeze balance through HTTP API.

The staked TRX can be partially unstaked multiple times, but only a maximum of 32 unstaking operations are allowed at the same time. That is to say, when a user initiates the first unstake operation, before the TRX of the first unstaking arrives and is ready to be withdrawn to his or her account, he or she can only initiate another 31 unstake operations. The remaining counts of unfreeze can be queried through the `getavailableunfreezecount` interface.

The TRX that have been delegated cannot be unstaked. In addition to losing the same amount of resource shares, the unstaking will also lose the same amount of TP resources.

When unstaking, if there are unclaimed voting rewards, the voting rewards will be automatically withdrawn to the account. If there is a previously unstaked principal that has passed the lock-up period, then this unstake operation will also withdraw the unstaked principal that has passed the lock-up period to the account at the same time. You can use the `gettransactioninfobyid`API to query the voting reward extracted in this transaction in `withdraw_amount` field and the withdrawn amount of unstaked TRX that has expired the lock-up period in `withdraw_expire_amount` field.

#### TRON Power Reclaim

After unstaking the TRX staked in the Stake2.0 stage, the same amount of voting rights will be lost. The system will first reclaim the idle voting rights in the account. If the idle TP is insufficient, it will continue to reclaim the used TP. If the user has voted for multiple super representatives, a certain number of votes will be withdrawn in proportion from each super representative, and the corresponding voting rights will be recovered. The calculation formula for withdrawing votes for each SR is,

```
The number of votes withdrawn from the current super representative = total number of votes to be withdrawn  * (number of votes for the current super representative / total number of votes of this account)
```



For example, Suppose A staked 2,000TRX and obtained 2,000 TRON Power, of which 1,000 TRON Power voted for 2 super representatives, 600 votes and 400 votes respectively, and 1,000 TRON Power remained in the account. At this time, A unstakes 1,500TRX, which means that 1,500 TRON Power needs to be reclaimed from A’ account. In this case, the idle 1,000 TP in A’s account will be withdrawn first, and the spared 500 TP will be withdrawn from the voted TP,  
which is 300 TP and 200 TP respectively from the two super representatives. Here's how the votes are calculated:

- Number of votes withdrawn by Super Representative 1 = 500 \* (600 / 1,000) = 300
- Number of votes withdrawn by Super Representative 2 = 500 \* (400 / 1,000) = 200

At present, the TRON network uses the Stake2.0 stake mechanism, but the resources and votes obtained by Stake1.0 are still valid. The TRX staked at Stake1.0 can still be withdrawal through Stake1.0 API `unfreezebalance`, but it should be noted that if the TRX staked in Stake 1.0 is unstaked, all votes in the account will be revoked.

### API

The following table shows the relevant interfaces of the stake model and their descriptions:

| API                                                                                   | Description                                                                          |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| freezebalancev2                                     | Stake TRX                                                                            |
| unfreezebalancev2                               | Unstake TRX                                                                          |
| delegateresource                                    | Delegate resources                                                                   |
| undelegateresource                              | Undelegate resources                                                                 |
| withdrawexpireunfreeze                          | Withdraw unfrozen balance                                                            |
| getavailableunfreezecount                  | Query the remaining times of executing unstake operation                             |
| getcanwithdrawunfreezeamount             | Query the withdrawable balance                                                       |
| getcandelegatedmaxsize                    | Query the amount of delegatable resources share of the specified resource Type       |
| getdelegatedresourcev2                        | Query the amount of resource delegated by fromAddress to toAddress                   |
| getdelegatedresourceaccountindexv2 | Query the resource delegation index by an account                                    |
| getaccount                                        | Query the account stake status, resource share, unstake status, and voting status    |
| getaccountresource                                | Query the total amount of resources, the amount of used, and the amount of available |

## Other Fees

|Type|Fee|
| :------|:------:|
|Create a witness|9999 TRX|
|Issue a token|1024 TRX|
|Create an account|1 TRX|
|Create an exchange|1024 TRX|
|Update the account permission|100 TRX|
|Transaction note|1 TRX|
|Multi-sig transaction|1 TRX|

