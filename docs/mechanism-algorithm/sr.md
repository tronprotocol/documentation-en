# Super Representative

## How to Become a Super Representative

In TRON network, any account can apply to become a witness. Every account can vote for witnesses.

The top 27 witnesses are called SR, the witnesses from 28th to 127th are called Partner, the witnesses after 128th are called Candidates. Only SR can produce blocks.

The votes will be counted every 6 hours, so super representatives may also change every 6 hours.

To prevent vicious attack, TRON network burns 9999 TRX from the account that applies to become a super representative candidate.

## Super Representative Election

To vote, you need to have TRON Power(TP). To get TRON Power, you need to stake TRX. Every 1 staked TRX accounts for one TRON Power(TP). Every account in TRON network has the right to vote for a super representative candidate. After you unstake your staked TRX, you will lose the responding TRON Power(TP), so your previous vote will be invalid.

Note: Only your latest vote will be counted in TRON network which means your previous vote will be over written by your latest vote.

Example (Using wallet-cli):

```console
> freezebalance 10,000,000 3 // Stake 10 TRX to get 10 TRON Power(TP)
> votewitness witness1 4 witness2 6 // Vote 4 votes for witness1, 6 votes for witness2
> votewitness witness1 3 witness2 7 // Vote 3 votes for witness1, 7 votes for witness2
```

The final output above is: Vote 3 votes for witness1, 7 votes for witness2

### Witnesses Brokerage

The default ratio is 20%, which can be modified by the witnesses.

If a witness get 20% of the reward, and the other 80% will be awarded to the voters. If the brokerage ratio is set to 100%, the rewards are all obtained by the witness; if set to 0, the rewards are all sent to the voters.

## Reward for Witnesses

### Votes Reward

Vote rewards are 160 TRX every block, with a block generated every 3 seconds, the total vote rewards per day is  4,608,000 TRX.

For each SR and Partner, the daily Vote Rewards = 4,608,000 * ( votes /  total votes) x 20%  TRX

### Block Producing Reward

Every time after a super representative produces a block, it will be reward 16 TRX. The 27 super representatives take turns to produce blocks every 3 seconds. The annual block producing reward is 168,192,000 TRX in total.

Every time after a super representative produces a block, the 16 TRX block producing reward will be sent to it's sub-account. The sub-account is a read-only account, it allows a withdraw action from sub-account to super representative account every 24 hours.

$16 (\mathsf{TRX}/block) \times 28,800 (blocks/day) = 460,800 (\mathsf{TRX}/day)$

For each super representative, the daily block $Rewards_{sr} = (460,800 / 27) \times 20 \% \mathsf{TRX}$.

Reward may be less than the theoretical number due to missed blocks and maintenance period.

## Reward for Voters

If you vote for a Super Representative:

the daily Voter Rewards = (((the number of votes you vote to a witness) * 4,608,000 / total votes) * 80%) + ((460,800 / 27) * 80%) * (the number of votes you vote to a witness) / (the total number of votes a witness receives) TRX

If you vote for a Partner:

the daily Voter Rewards = (((the number of votes you vote to a witness) * 4,608,000 / total votes) * 80%) TRX

## Committee

### 1. What is Committee

Committee can modify the TRON network parameters, like transacton fees, block producing reward amount, etc. Committee is composed of the current 27 super representatives. Every super representative has the right to start a proposal. The proposal will be passed after it gets more than 18 approves from the super representatives and will become valid in the next maintenance period.

### 2. Create a Proposal

Only SRs, Partners and Candidates can create a proposal.

The network parameters can be modified([min,max]).

{0,1}: 1 means 'allowed' or 'actived', 0 means 'disallow', 'disable' or 'no'.

|  #    | Command  |  Value  |
|  ----  | ----    | ---- |
|  0     | MaintenanceTimeInterval <br> (To modify the maintenance interval of SR)  | 6  Hours <br> [3 * 27, 24 * 3600] s |
|  1     | AccountUpgradeCost <br> (To modify the cost of applying for SR account) | 9999  TRX <br> [0, 100000000000] TRX |
|  2     | CreateAccountFee <br> (To modify the account creation fee) | 0.1  TRX <br> [0, 100000000000] TRX |
|  3     | TransactionFee <br> (To modify the amount of TRX used to gain extra bandwidth) | 1000  Sun/Byte <br> [0, 100000000000] TRX |
|  4     | AssetIssueFee <br> (To modify asset issuance fee) | 1024  TRX <br> [0, 100000000000] TRX|
|  5     | WitnessPayPerBlock <br> (To modify SR block generation reward) | 16 TRX <br> [0, 100000000000] TRX |
|  6     | WitnessStandbyAllowance <br> (To modify the rewards given to the top 27 SRs and <br> the following 100 partners) | 115200  TRX <br> [0, 100000000000] TRX |
|  7     | CreateNewAccountFeeInSystemContract <br> (To modify the cost of account creation) | 1 TRX  |
|  8     | CreateNewAccountBandwidthRate <br> (To modify the consumption of bandwidth of account creation) | 1&nbsp;Bandwidth/Byte |
|  9     | AllowCreationOfContracts <br> (To activate the Virtual Machine (VM)) | 1 <br> {0, 1} |
|  10   | RemoveThePowerOfTheGr <br> (To remove the GR Genesis votes) |  1 <br> {0, 1}|
|  11   | EnergyFee <br> (To modify the fee of 1 energy) | 140 Sun <br> [0, 100000000000] TRX |
|  12   | ExchangeCreateFee <br> (To modify the cost of trading pair creation) | 1024 TRX <br> [0, 100000000000] TRX |
|  13   | MaxCpuTimeOfOneTx <br> (To modify the maximum execution time of one transaction) | 50 ms <br> [0, 1000] ms |
|  14   | AllowUpdateAccountName <br> (To allow to change the account name) | 0 <br> {0, 1} |
|  15   | AllowSameTokenName <br> (To allow the same token name) | 1 <br> {0, 1} |
|  16   | AllowDelegateResource <br> (To allow resource delegation) | 1 <br> {0, 1} |
|  18   | AllowTvmTransferTrc10 <br> (To allow the TRC-10 token transfer in smart contracts) | 1 <br> {0, 1} |
|  19   | TotalEnergyCurrentLimit <br> (To modify current total energy limit) | 50000000000 |
|  20   | AllowMultiSign <br> (To allow the initiation of multi-signature) | 1 <br> {0, 1} |
|  21   | AllowAdaptiveEnergy <br> (To allow adaptive adjustment for total Energy) | 0 <br> {0, 1} |
|  22   | UpdateAccountPermissionFee <br> (To modify the fee for updating account permission) | 100 TRX |
|  23   | MultiSignFee <br> (To modify the fee for multi-signature) | 1 TRX |
|  24   | AllowProtoFilterNum <br> (To enable protocol optimization) | 0 <br> {0, 1} |
|  26   | AllowTvmConstantinople <br> (To support the new commands of Constantinople) | 1 <br> {0, 1} |
|  27   | AllowShieldedTransaction <br> (To enable shielded transaction) | 0 <br> {0, 1} |
|  28   | ShieldedTransactionFee <br> (To modify shielded transaction fee) | 10 TRX <br> [0, 10000] TRX |
|  29   | AdaptiveResourceLimitMultiplier <br> (To modify the adaptive energy limit multiplier) | 1000 <br> [1, 10000] |
|  30    | ChangeDelegation <br> (Propose to support the decentralized vote dividend) | 1 <br> {0, 1} |
|  31    | Witness127PayPerBlock <br> (Propose to modify the block voting rewards given to <br> the top 27 SRs and the following 100 partners) | 160  TRX <br> [0, 100000000000] TRX |
|  32    | AllowTvmSolidity059 <br> (To allow TVM to support solidity compiler 0.5.9) | 0 <br> {0, 1} |
|  33    | AdaptiveResourceLimitTargetRatio <br> (To modify the target energy limit) | 10 <br> [1, 1000] |

Example (Using wallet-cli):

```console
> createproposal id value
# id: the serial number (0 ~ 33)
# value: the parameter value
```

Note: In TRON network, 1 TRX = 1_000_000 SUN

### 3. Vote for a Proposal

Proposal only support YES vote. Since the creation time of the proposal, the proposal is valid within 3 days. If the proposal does not receive enough YES votes within the period of validity, the proposal will be invalid beyond the period of validity. Yes vote can be cancelled.

Example (Using wallet-cli):

```console
> approveProposal id is_or_not_add_approval
# id: proposal id
# is_or_not_add_approval: YES vote or cancel YES vote
```

### 4. Cancel Proposal

Proposal creator can cancel the proposal before it is passed.

Example (Using wallet-cli):

```console
> deleteProposal id
# id: proposal id
```

### 5. Query Proposal

- Query all the proposals list (ListProposals)
- Query all the proposals list by pagination (GetPaginatedProposalList)
- Query a proposal by proposal id (GetProposalById)

For more API detail, please refer to [HTTP API](../api/http.md).
