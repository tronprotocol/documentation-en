# Contract

## Smart Contract Introduction

Smart contract is a computerized transaction protocol that automatically implements its terms. Smart contract is the same as common contract, they all define the terms and rules related to the participants. Once the contract is started, it can runs in the way it is designed.

TRON smart contract support Solidity language in (Ethereum). Currently recommend Solidity language version is 0.4.24 ~ 0.4.25. Write a smart contract, then build the smart contract and deploy it to TRON network. When the smart contract is triggered, the corresponding function will be executed automatically.

## Smart Contract Features
TRON virtual machine is based on Ethereum solidity language, it also has TRON's own features.

<h3> 1. Smart Contract </h3>
TRON VM is compatible with Ethereum's smart contract, using protobuf to define the content of the contract:

    message SmartContract {
      message ABI {
        message Entry {
          enum EntryType {
            UnknownEntryType = 0;
            Constructor = 1;
            Function = 2;
            Event = 3;
            Fallback = 4;
          }
          message Param {
            bool indexed = 1;
            string name = 2;
            string type = 3;
            // SolidityType type = 3;
          }
          enum StateMutabilityType {
            UnknownMutabilityType = 0;
            Pure = 1;
            View = 2;
            Nonpayable = 3;
            Payable = 4;
          }

          bool anonymous = 1;
          bool constant = 2;
          string name = 3;
          repeated Param inputs = 4;
          repeated Param outputs = 5;
          EntryType type = 6;
          bool payable = 7;
          StateMutabilityType stateMutability = 8;
        }
        repeated Entry entrys = 1;
      }
      bytes origin_address = 1;
      bytes contract_address = 2;
      ABI abi = 3;
      bytes bytecode = 4;
      int64 call_value = 5;
      int64 consume_user_resource_percent = 6;
      string name = 7；
      int64 origin_energy_limit = 8;
    }

origin_address: smart contract creator address
contract_address: smart contract address
abi: the api information of the all the function of the smart contract
bytecode: smart contract byte code
call_value: TRX transferred into smart contract while call the contract
consume_user_resource_percent: resource consumption percentage set by the developer
name: smart contract name
origin_energy_limit: energy consumption of the developer limit in one call, must greater than 0. For the old contracts, if this parameter is not set, it will be set 0, developer can use updateEnergyLimit api to update this parameter (must greater than 0)

Through other two grpc message types CreateSmartContract and TriggerSmartContract to create and use smart contract.

<h3> 2. The Usage of the Function of Smart Contract </h3>

1.&nbsp;constant function and inconstant function

There are two types of function according to whether any change will be made to the properties on the chain: constant function and inconstant function
Constant function uses view/pure/constant to decorate, will return the result on the node it is called and not be broadcasted in the form of a transaction
Inconstant function will be broadcasted in the form of a transaction while be called, the function will change the data on the chain, such as transfer, changing the value of the internal variables of contracts, etc.

Note: If you use create command inside a contract (CREATE instruction), even use view/pure/constant to decorate the dynamically created contract function, this function will still be treated as inconstant function, be dealt in the form of transaction.

2.&nbsp;message calls

Message calls can call the functions of other contracts, also can transfer TRX to the accounts of contract and none-contract. Like the common TRON triggercontract, Message calls have initiator, recipient, data, transfer amount, fees and return attributes. Every message call can generate a new one recursively. Contract can define the distribution of the remaining energy in the internal message call. If it comes with OutOfEnergyException in the internal message call, it will return false, but not error. In the meanwhile, only the gas sent with the internal message call will be consumed, if energy is not specified in call.value(energy), all the remaining energy will be used.

3.&nbsp;delegate call/call code/libary

There is a special type of message call, delegate call. The difference with common message call is the code of the target address will be run in the context of the contract that initiates the call, msg.sender and msg.value remain unchanged. This means a contract can dynamically loadcode from another address while running. Storage, current address and balance all point to the contract that initiates the call, only the code is get from the address being called. This gives Solidity the ability to achieve the 'lib' function: the reusable code lib can be put in the storage of a contract to implement complex data structure library.

4.&nbsp;CREATE command

This command will create a new contract with a new address. The only difference with Ethereum is the newly generated TRON address used the smart contract creation transaction id and the hash of nonce called combined. Different from Ethereum, the defination of nonce is the comtract sequence number of the creation of the root call. Even there are many CREATE commands calls, contract number in sequence from 1. Refer to the source code for more detail.
Note: Different from creating a contract by grpc's deploycontract, contract created by CREATE command does not store contract abi.

5.&nbsp;built-in function and built-in function attribute (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)

1)TVM is compatible with solidity language's transfer format, including:
- accompany with constructor to call transfer
- accompany with internal function to call transfer
- use transfer/send/call/callcode/delegatecall to call transfer

Note: TRON's smart contract is different from TRON's system contract, if the transfer to address does not exist it can not create an account by smart contract transfer.

2)Different accouts vote for SuperNode (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
3)SuperNode gets all the reward (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
4)SuperNode approves or disappoves the proposal (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
5)SuperNode proposes a proposal (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
6)SuperNode deletes  a proposal (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
7)TRON byte address converts to solidity address (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
8)TRON string address converts to solidity address (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
9)Send token to target address (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
10)Query token amount of target address (Since Odyssey-v3.1.1, TVM built-in function is not supported temporarily)
11)Compatible with all the built-in functions of Ethereum

Note: Ethereum's RIPEMD160 function is not recommended, because the return of TRON is a hash result based on TRON's sha256, not an accurate Ethereum RIPEMD160.

<h3> 3. Contract Address Using in Solidity Language </h3>

Ethereum VM address is 20 bytes, but TRON's VM address is 21 bytes.

1.&nbsp;address conversion

Need to convert TRON's address while using in solidity (recommended):
```text
/**
     *  @dev    convert uint256 (HexString add 0x at beginning) tron address to solidity address type
     *  @param  tronAddress uint256 tronAddress, begin with 0x, followed by HexString
     *  @return Solidity address type
*/

function convertFromTronInt(uint256 tronAddress) public view returns(address){
        return address(tronAddress);
}
```
This is similar with the grammar of the conversion from other types converted to address type in Ethereum.

2.&nbsp;address judgement

Solidity has address constant judgement, if using 21 bytes address the compiler will throw out an error, so you should use 20 bytes address, like:
```text
function compareAddress(address tronAddress) public view returns (uint256){
        // if (tronAddress == 0x41ca35b7d915458ef540ade6068dfe2f44e8fa733c) { // compile error
        if (tronAddress == 0xca35b7d915458ef540ade6068dfe2f44e8fa733c) { // right
            return 1;
        } else {
            return 0;
        }
}
```
But if you are using wallet-cli, you can use 21 bytes address, like 0000000000000000000041ca35b7d915458ef540ade6068dfe2f44e8fa733c

3.&nbsp;variable assignment

Solidity has address constant assignment, if using 21 bytes address the compiler will throw out an error, so you should use 20 bytes address, like:
```text
function assignAddress() public view {
        // address newAddress = 0x41ca35b7d915458ef540ade6068dfe2f44e8fa733c; // compile error
        address newAddress = 0xca35b7d915458ef540ade6068dfe2f44e8fa733c;
        // do something
}
```
If you want to use TRON address of string type (TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm) please refer to (2-4-7,2-4-8).

<h3> 4. The Special Constants Differ from Ethereum </h3>

**Currency**

Like solidity supports ETH, TRON VM supports trx and sun, 1 trx = 1000000 sun, case sensitive, only support lower case. tron-studio supports trx and sun, remix does not support trx and sun.
We recommend to use tron-studio instead of remix to build TRON smart contract.

**Block**

- block.blockhash (uint blockNumber) returns (bytes32): specified block hash, can only apply to the latest 256 blocks and current block excluded
- block.coinbase (address): SuperNode address that produced the current block
- block.difficulty (uint): current block difficulty, not recommended, set 0
- block.gaslimit (uint): current block gas limit, not supported, set 0
- block.number (uint): current block number
- block.timestamp (uint): current block timestamp
- gasleft() returns (uint256): remaining gas
- msg.data (bytes): complete call data
- msg.gas (uint): remaining gas - since 0.4.21, not recommended, replaced by gesleft()
- msg.sender (address): message sender (current call)
- msg.sig (bytes4): first 4 bytes of call data (function identifier)
- msg.value (uint): the amount of SUN send with message
- now (uint): current block timestamp (block.timestamp)
- tx.gasprice (uint): the gas price of transaction, not recommended, set 0
- tx.origin (address): transaction initiator


Each command of smart contract consume system resource while running, we use 'Energy' as the unit of the consumption of the resource.


## Built-in Contracts

<h3 id="1">1.创建账户 AccountCreateContract</h3>

   `AccountCreatContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `account_address`： 将要创建的账户地址。
   `type`：账户类型——比如：_0_ 代表的账户类型是`Normal`。

     message AccountCreateContract {
       bytes owner_address = 1;
       bytes account_address = 2;
       AccountType type = 3;
     }

 <h3 id="2">2.转账 TransferContract</h3>

   `TransferContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `to_address`： 目标账户地址。
   `amount`：转账金额，单位为 sun。

     message TransferContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       int64 amount = 3;
     }


 <h3 id="3">3.转账发布的Token TransferAssetContract</h3>

   `TransferAssetContract`包含4种参数：
   `asset_name`：发布Token的名称。
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `to_address`： 目标账户地址。
   `amount`：转账Token的数量。

     message TransferAssetContract {
       bytes asset_name = 1;
       bytes owner_address = 2;
       bytes to_address = 3;
       int64 amount = 4;
     }


 <h3 id="4">4.投票超级节点  VoteWitnessContract</h3>

   `VoteWitnessContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `vote_address`： 超级节点候选人的地址。
   `vote_count`：投给超级节点候选人的票数。
   `votes`：超级节点候选人列表。
   `support`：是否支持，这里应该是恒为true,暂未使用该参数。

     message VoteWitnessContract {
       message Vote {
         bytes vote_address = 1;
         int64 vote_count = 2;
       }
       bytes owner_address = 1;
       repeated Vote votes = 2;
       bool support = 3;
     }


 <h3 id="5">5.创建超级节点候选人 WitnessCreateContract</h3>

   `WitnessCreateContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `url`： 超级节点后续人网址。

     message WitnessCreateContract {
       bytes owner_address = 1;
       bytes url = 2;
     }


 <h3 id="6">6.发布Token AssetIssueContract</h3>

   `AssetIssueContract`包含17种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `name`：发布Token的名称——比如：_“SiCongcontract”_。
   `abbr`： 。
   `total_supply`：发行总的token数量——比如：_100000000_。
   `frozen_supply`：冻结Token的数量和冻结时间列表。
   `trx_num`：对应TRX数量——比如：_232241_。
   `num`： 对应的自定义资产数目。
   `start_time`：开始时间——比如：_20170312_。
   `end_time`：结束时间——比如：_20170512_。
   `order`：相同asset_name时，order递增，默认初始值为0。
   `vote_score`：合约的评分——比如：_12343_。
   `description`：Token的描述——比如：_”trondada”_。
   `url`：Token的url地址链接。
   `free_asset_net_limit`：每个账户可以使用的免费带宽(转移该资产时使用)。
   `public_free_asset_net_limit`：所有账户可以使用的免费带宽(转移该资产时使用)。
   `public_free_asset_net_usage`：所有账户使用免费带宽(转移该资产时使用)。
   `public_latest_free_net_time`：最近一次转移该Token使用免费带宽的时间。

     message AssetIssueContract {
       message FrozenSupply {
         int64 frozen_amount = 1;
         int64 frozen_days = 2;
       }
       bytes owner_address = 1;
       bytes name = 2;
       bytes abbr = 3;
       int64 total_supply = 4;
       repeated FrozenSupply frozen_supply = 5;
       int32 trx_num = 6;
       int32 num = 8;
       int64 start_time = 9;
       int64 end_time = 10;
       int64 order = 11; // the order of tokens of the same name
       int32 vote_score = 16;
       bytes description = 20;
       bytes url = 21;
       int64 free_asset_net_limit = 22;
       int64 public_free_asset_net_limit = 23;
       int64 public_free_asset_net_usage = 24;
       int64 public_latest_free_net_time = 25;
     }


 <h3 id="7">7.更新超级节点候选人URL WitnessUpdateContract</h3>

   `WitnessUpdateContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `update_url`： 超级节点更新后的url。

     message WitnessUpdateContract {
       bytes owner_address = 1;
       bytes update_url = 12;
     }

<h3 id="8">8.购买发行的Token ParticipateAssetIssueContract</h3>

   `ParticipateAssetIssueContract`包含4种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `to_address`：发行Token所有者地址。
   `account_name`： 发行Token的名称，包括Token名称和order
   `amount`：购买发行Token使用TRX的数量，单位是 sun。

     message ParticipateAssetIssueContract {
       bytes owner_address = 1;
       bytes to_address = 2;
       bytes asset_name = 3;
       int64 amount = 4;
     }

 <h3 id="9">9.更新账户 AccountUpdateContract</h3>

   `AccountUpdateContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `account_name`： 账户名称——比如： _"SiCongsaccount”_。

     // Update account name. Account name is not unique now.
     message AccountUpdateContract {
       bytes account_name = 1;
       bytes owner_address = 2;
     }

 <h3 id="10">10.冻结资产 FreezeBalanceContract</h3>

   `FreezeBalanceContract`包含4种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `frozen_balance`：冻结资产的数量。
   `frozen_duration`：冻结资产的时间段。
   `resource`： 冻结TRX获取资源的类型。
   `receiver_address` ：接收资源的账户。

     message FreezeBalanceContract {
       bytes owner_address = 1;
       int64 frozen_balance = 2;
       int64 frozen_duration = 3;
       ResourceCode resource = 10;
       bytes receiver_address = 15;
     }

 <h3 id="11">11.解冻资产 UnfreezeBalanceContract</h3>

   `UnfreezeBalanceContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `resource`： 解冻资源的类型。
   `receiver_address` ：接收资源的账户。

     message UnfreezeBalanceContract {
       bytes owner_address = 1;
       ResourceCode resource = 10;
       bytes receiver_address = 13;
     }

 <h3 id="12">12.提取奖励 WithdrawBalanceContract</h3>

   `WithdrawBalanceContract`包含1种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。

     message WithdrawBalanceContract {
       bytes owner_address = 1;
     }

 <h3 id="13">13.解冻发布的Token UnfreezeAssetContract</h3>

   `UnfreezeAssetContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。

     message UnfreezeAssetContract {
       bytes owner_address = 1;
     }

 <h3 id="14">14.更新通证参数 UpdateAssetContract</h3>

   `UpdateAssetContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `description`： 通证的描述。
   `url`：通证的Url。
   `new_limit`：每个调用者可以消耗Bandwidth point的限制。
   `new_public_limit`： 所有调用者可以消耗Bandwidth points的限制。

     message UpdateAssetContract {
       bytes owner_address = 1;
       bytes description = 2;
       bytes url = 3;
       int64 new_limit = 4;
       int64 new_public_limit = 5;
     }

 <h3 id="15">15.创建提议  ProposalCreateContract</h3>

   `ProposalCreateContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `parameters`： 提议。

     message ProposalCreateContract {
       bytes owner_address = 1;
       map<int64, int64> parameters = 2;
     }

 <h3 id="16">16.赞成提议 ProposalApproveContract</h3>

   `ProposalApproveContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `proposal_id`： 提议的Id。
   `is_add_approval`：是否赞成提议。

     message ProposalApproveContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
       bool is_add_approval = 3; // add or remove approval
     }

 <h3 id="17">17.删除提议 ProposalDeleteContract</h3>

   `ProposalDeleteContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `proposal_id`： 提议ID。

     message ProposalDeleteContract {
       bytes owner_address = 1;
       int64 proposal_id = 2;
     }

 <h3 id="18">18.设置账户ID SetAccountIdContract</h3>

   `SetAccountIdContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `account_id`： 账户Id。

     // Set account id if the account has no id. Account id is unique and case insensitive.
     message SetAccountIdContract {
       bytes account_id = 1;
       bytes owner_address = 2;
     }


 <h3 id="19">19.创建智能合约 CreateSmartContract</h3>

   `CreateSmartContract`包含2种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `new_contract`： 智能合约。

     message CreateSmartContract {
       bytes owner_address = 1;
       SmartContract new_contract = 2;
     }

 <h3 id="20">20.触发智能合约 TriggerSmartContract</h3>

   `TriggerSmartContract`包含4种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `contract_address`： 合约地址。
   `call_value`：TRX的值。
   `data`：操作参数。

     message TriggerSmartContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 call_value = 3;
       bytes data = 4;
     }

 <h3 id="21">21.更新合约 UpdateSettingContract</h3>

   `UpdateSettingContract`包含3种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `contract_address`： 合约地址。
   `consume_user_resource_percent`：将要更新的账户消耗资源的百分比。

     message UpdateSettingContract {
       bytes owner_address = 1;
       bytes contract_address = 2;
       int64 consume_user_resource_percent = 3;
     }

 <h3 id="22">22.创建交易所 ExchangeCreateContract</h3>

   `ExchangeCreateContract`包含5种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `first_token_id`： 第1种token的id 。
   `first_token_balance`：第1种token的balance。
   `second_token_id`：第2种token的id。
   `second_token_balance`：第2种token的balance。

     message ExchangeCreateContract {
       bytes owner_address = 1;
       bytes first_token_id = 2;
       int64 first_token_balance = 3;
       bytes second_token_id = 4;
       int64 second_token_balance = 5;
     }

 <h3 id="23">23.给交易所注资 ExchangeInjectContract</h3>

   `ExchangeInjectContract`包含4种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `exchange_id`： 交易对的id。
   `token_id`：要注资的token的id。
   `quant`：要注资的token的金额。

     message ExchangeInjectContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }

 <h3 id="24">24.从交易所撤资 ExchangeWithdrawContract</h3>

   `ExchangeWithdrawContract`包含4种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `exchange_id`： 交易对的id。
   `token_id`：要撤资的token的id。
   `quant`：要撤资的token的金额。

     message ExchangeWithdrawContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }

 <h3 id="25">25.在交易所交易 ExchangeTransactionContract</h3>

   `ExchangeTransactionContract`包含4种参数：
   `owner_address`：合约持有人地址——比如： _“0xu82h…7237”_。
   `exchange_id`： 交易对的id。
   `token_id`：要卖出的token的id。
   `quant`：要卖出的token的金额。

     message ExchangeTransactionContract {
       bytes owner_address = 1;
       int64 exchange_id = 2;
       bytes token_id = 3;
       int64 quant = 4;
     }
