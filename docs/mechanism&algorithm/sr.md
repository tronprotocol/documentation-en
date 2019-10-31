
## How to Become a Super Representative

 In TRON network, any account can apply to become a super representative candidate. Every account can vote for super representative candidates. The top 27 candidates with the most votes are the super representatives. Super representatives can produce blocks. The votes will be counted every 6 hours, so super representatives may also change every 6 hours.  

 To prevent vicious attack, TRON network burns 9999 TRX from the account that applies to become a super representative candidate.

## Super Representatives Election

 To vote, you need to have TRON Power(TP). To get TRON Power, you need to freeze TRX. Every 1 frozen TRX accounts for one TRON Power(TP). Every account in TRON network has the right to vote for a super representative candidate. After you unfreeze your frozen TRX, you will lose the responding TRON Power(TP), so your previous vote will be invalid.  

 Note: Only your latest vote will be counted in TRON network which means your previous vote will be over written by your latest vote.  

Example (Using wallet-cli):  

```text
freezebalance 10,000,000 3 // Freeze 10 TRX to get 10 TRON Power(TP)  
votewitness witness1 4 witness2 6 // Vote 4 votes for witness1, 6 votes for witness2  
votewitness witness1 3 witness2 7 // Vote 3 votes for witness1, 7 votes for witness2  
```

The final output above is: Vote 3 votes for witness1, 7 votes for witness2

## Reward for Super Representatives

**Votes Reward:**  
Every 6 hours, the top 127 super representative candidates with the most votes will share a total amount of 115,200 TRX according to their votes percentage. The annual votes reward is 168,192,000 TRX in total.

**Block Producing Reward:**   
Every time after a super representative produces a block, it will be reward 32 TRX. The 27 super representatives take turns to produce blocks every 3 seconds. The annual block producing reward is 336,384,000 TRX in total.  

Every time after a super representative produces a block, the 32 TRX block producing reward will be sent to it's sub-account. The sub-account is a read-only account, it allows a withdraw action from sub-account to super representative account every 24 hours.

## Committee

<h3> 1. What is Committee </h3>

Committee can modify the TRON network parameters, like transacton fees, block producing reward amount, etc. Committee is composed of the current 27 super representatives. Every super representative has the right to start a proposal. The proposal will be passed after it gets more than 19 approves from the super representatives and will become valid in the next maintenance period.

<h3> 2. Create a Proposal </h3>

Only the account of a super representative can create a proposal.   
The network parameters can be modified([min,max]):  

- 0: MAINTENANCE_TIME_INTERVAL, [3 * 27* 1000, 24 * 3600 * 1000] //super representative votes count time interval, currently 6 * 3600 * 1000 ms  
- 1: ACCOUNT_UPGRADE_COST, [0, 100 000 000 000 000 000]  //the fee to apply to become a super representative candidate, currently 9999_000_000 SUN   
- 2: CREATE_ACCOUNT_FEE, [0, 100 000 000 000  000 000] //the fee to create an account, currently 100_000 SUN  
- 3: TRANSACTION_FEE, [0, 100 000 000 000 000 000] //the fee for bandwidth, currently 10 SUN/byte  
- 4: ASSET_ISSUE_FEE, [0, 100 000 000 000 000 000] //the fee to issue an asset, currently 1024_000_000 SUN  
- 5: WITNESS_PAY_PER_BLOCK, [0, 100 000 000 000 000 000] //the block producing reward, currently 32_000_000 SUN  
- 6: WITNESS_STANDBY_ALLOWANCE, [0, 100 000 000 000 000 000] //the votes reward for top 127 super representative candidates, currently 115_200_000_000 SUN   
- 7: CREATE_NEW_ACCOUNT_FEE_IN_SYSTEM_CONTRACT, //the fee to create an account in system, currently 0 SUN  
- 8: CREATE_NEW_ACCOUNT_BANDWIDTH_RATE, //the consumption of bandwith or TRX while creating an account, using together with #7  
- 9: ALLOW_CREATION_OF_CONTRACTS, //to enable the VM  
- 10: REMOVE_THE_POWER_OF_THE_GR, //to clear the votes of GR  
- 11: ENERGY_FEE, [0,100 000 000 000 000 000] //SUN  
- 12: EXCHANGE_CREATE_FEE, [0, 100 000 000 000 000 000] //SUN  
- 13: MAX_CPU_TIME_OF_ONE_TX, [0, 1000] //ms  
- 14: ALLOW_UPDATE_ACCOUNT_NAME, //to allow users to change account name and allow account duplicate name, currently 0, means false  
- 15: ALLOW_SAME_TOKEN_NAME, //to allow create a token with duplicate name, currently 1, means true  
- 16: ALLOW_DELEGATE_RESOURCE, //to enable the resource delegation  
- 17: TOTAL_ENERGY_LIMIT, //to modify the energy limit  
- 18: ALLOW_TVM_TRANSFER_TRC10, //to allow smart contract to transfer TRC-10 token, currently 0, means false
- 19: TOTAL_CURRENT_ENERGY_LIMIT, //to modify the total energy, currently 50000000000
- 20: ALLOW_MULTI_SIGN, //to multi-signature, currently 1
- 21: ALLOW_ADAPTIVE_ENERGY, //to allow the total energy adaptive, currently 0, means false
- 22: UPDATE_ACCOUNT_PERMISSION_FEE, //the fee to update the account permission, currently 100000000 SUN
- 23: MULTI_SIGN_FEE, //the fee to modify multi-signature fee, currently 1000000 SUN
- 24: ALLOW_PROTO_FILTER_NUM, //update allow protobuf number
- 25: ALLOW_ACCOUNT_STATE_ROOT, //to enable the account state root
- 26: ALLOW_TVM_CONSTANTINOPLE, //to allow the TVM support the upgrade of Constantinople
- 27: ALLOW_SHIELDED_TRANSACTION, //to allow shielded transactions, currently 0, means false
- 28: SHIELDED_TRANSACTION_FEE, [0,10 000 000 000] //the fee to modify shielded transactons, currently 10
- 29: ADAPTIVE_RESOURCE_LIMIT_MULTIPLIER, [1,10 000] //the limit of dynamic energy maximum multiplier, currently 1000, means the value is 1000 times of total energy
- 30: ALLOW_CHANGE_DELEGATION, //to change the replacement of delegation mechanism switch, currently 0, means false
- 31: WITNESS_127_PAY_PER_BLOCK, [0,100 000 000 000 000 000] //the modification of votes rank reward, currently 16000000 SUN
- 32: ALLOW_TVM_SOLIDITY_059, //to allow TVM supports Solidity Compiler Version 0.5.9, currently 0, means false
- 33: ADAPTIVE_RESOURCE_LIMIT_TARGET_RATIO, [1,1 000] //the target value of energy, currently 10, means The target energy is 1/10 of the total energy


Example (Using wallet-cli):  
```text
createproposal id value  
id: the serial number (0 ~ 18)  
value: the parameter value  
```

Note: In TRON network, 1 TRX = 1000_000 SUN

<h3> 3. Vote for a Proposal </h3>

Proposal only support YES vote. Since the creation time of the proposal, the proposal is valid within 3 days. If the proposal does not receive enough YES votes within the period of validity, the proposal will be invalid beyond the period of validity. Yes vote can be cancelled.  

Example (Using wallet-cli):  
```text
approveProposal id is_or_not_add_approval
id: proposal id  
is_or_not_add_approval: YES vote or cancel YES vote  
```

<h3> 4. Cancel Proposal </h3>

Proposal creator can cancel the proposal before it is passed.  

Example (Using wallet-cli):  
```text
deleteProposal id
id: proposal id
```

<h3> 5. Query Proposal </h3>

- Query all the proposals list (ListProposals)  
- Query all the proposals list by pagination (GetPaginatedProposalList)  
- Query a proposal by proposal id (GetProposalById)  

For more api detail, please refer to [Tron-http](Tron-http.md)  
