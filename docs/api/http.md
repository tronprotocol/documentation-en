# HTTP API
This article introduces FullNode's HTTP APIs and their usage. 


!!! note
    Although TRON has avoided XSS by setting the Content-Type of HTTP APIs to application/json, there are a few APIs that don't have input validation. To better protect user data security, we recommend that you correctly encode any data from APIs before they use it in any UI, especially when the parameter `visible` equals true.
    
    Here is a typical XSS protection method: Encode all data from the APIs in HTML. Use methods such as `encodeURIComponent()` or `escape()` to encode the data, which can convert special characters into their HTML entities and prevent them from being interpreted as HTML code by the browser. 
    
    Please be sure to implement XSS protection for all data from the APIs to ensure the security of user data. We understand that you may need more information about XSS protection. It is recommended that you refer to the following resources: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

First, Let's explain the selection of the address format in the HTTP API: Account addresses of the TRON network have two formats: HexString format and Base58 format. The Fullnode HTTP API supports address format selection. Users can set the address format through the `visible` parameter. The default value is `false` and the address format in the parameter and return value is hex format. When `visible` is set to `true`, the address format in the parameter and return value are in Base58 format. If the parameter format does not match the `visible` setting, an error will be reported. Setting method:

- For HTTP GET API or the api needs no parameter: by adding `visible=true` parameter to the url 
```text
http://127.0.0.1:8090/wallet/listexchanges?visible=true
```
- For POST API: By adding `"visible": true` parameter to the most out layer of the json
```json
curl -X POST http://127.0.0.1:8090/wallet/createtransaction -d
'{
    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
    "amount": 1000000,
    "visible": true
}'
```



## Fullnode HTTP API
The FullNode HTTP API is categorized as follows:

- [Accounts](#accounts)
- [Transfer and Transactions](#transfers-and-transactions)
- [Account Resources](#account-resources)
- [Query The Network](#query-the-network)
- [Smart Contracts](#smart-contracts)
- [TRC-10 Token](#trc10-token)
- [Voting & SRs](#vote-and-sr)
- [Proposals](#proposals)
- [DEX Exchange](#dex-exchange)
- [Pending Pool](#pending-pool)


### Accounts
The following are the APIs related to on-chain accounts:

- [wallet/validateaddress](#walletvalidateaddress)
- [wallet/createaccount](#walletcreateaccount)
- [wallet/getaccount](#walletgetaccount)
- [wallet/updateaccount](#walletupdateaccount)
- [wallet/accountpermissionupdate](#walletaccountpermissionupdate)
- [wallet/getaccountbalance](#walletgetaccountbalance)
- [wallet/setaccountid](#walletsetaccountid)
- [wallet/getaccountbyid](#walletgetaccountbyid)

#### wallet/validateaddress
Description: Check the validity of the address
```
curl -X POST  http://127.0.0.1:8090/wallet/validateaddress -d '{"address": "4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
Parameters: address

Return: the address is correct or not

#### wallet/createaccount
Description: Create an account. Uses an already activated account to create a new account. If the owner_address has enough bandwidth obtained by freezing TRX, then creating an account will only consume bandwidth , otherwise, 0.1 TRX will be burned to pay for bandwidth, and at the same time, 1 TRX will be required to be created.
```
curl -X POST  http://127.0.0.1:8090/wallet/createaccount -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "account_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0"}'
```
Parameters: 

- `owner_address` Owner address, default hexString
- `account_address` New address, default hexString
- `Permission_id` Optional, for multi-signature use

Return: Unsigned transaction object

#### wallet/getaccount
Description: Query an account information
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccount -d '{"address": "41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
Parameters: `address` - account address

Return: Account object

#### wallet/updateaccount
Description: Update the name of an account
```
curl -X POST  http://127.0.0.1:8090/wallet/updateaccount -d '{"account_name": "0x7570646174654e616d6531353330383933343635353139" ,"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"}'
```
Parameters: 

- `account_name` Account name, default hexString
- `owner_address` Owner address, default hexString
- `Permission_id` Optional, for multi-signature use

Return:未签名的修改名称Transaction


#### wallet/accountpermissionupdate
Description: Update the account's permission.
```
curl -X POST  http://127.0.0.1:8090/wallet/accountpermissionupdate -d
'{
    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "owner": {
        "type": 0,
        "permission_name": "owner",
        "threshold": 1,
        "keys": [{
            "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "weight": 1
        }]
    },
    "witness": {
        "type": 1,
        "permission_name": "witness",
        "threshold": 1,
        "keys": [{
            "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "weight": 1
        }]
    },
    "actives": [{
        "type": 2,
        "permission_name": "active12323",
        "threshold": 2,
        "operations": "7fff1fc0033e0000000000000000000000000000000000000000000000000000",
        "keys": [{
            "address": "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR",
            "weight": 1
        }, {
            "address": "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
            "weight": 1
        }]
    }],
    "visible": true}'
```
Parameters: 

- owner_address: Owner address of the account, default hexString
- owner: Account owner permission
- witness: Account witness permission, only for witness
- actives: List of active permissions for the account

Return: Unsigned transaction

#### wallet/getaccountbalance
Description： Get the account balance in a specific block. 
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountbalance -d
'{
    "account_identifier": {
        "address": "TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm"
    },
    "block_identifier": {
        "hash": "0000000000010c4a732d1e215e87466271e425c86945783c3d3f122bfa5affd9",
        "number": 68682
    },
    "visible": true
}'
```

Parameters: 

- `account_identifier`: The account address. 
- `block_identifier`: The block number. 

Return: The balance object of the account in a specific block, the `block_identifier` is the block hash.
```
{
    "balance": 64086449348265042,
    "block_identifier": {
        "hash": "0000000000010c4a732d1e215e87466271e425c86945783c3d3f122bfa5affd9",
        "number": 68682
    }
}
```
**Notice**: Only node where `storage.balance.history.lookup= true` is set in the configuration file supports querying the account's historical balance. The supported official nodes can be queried [here](../using_javatron/backup_restore.md/#fullnode-data-snapshot).


#### wallet/setaccountid
Description: To set an account id for an account
```
curl -X POST  http://127.0.0.1:8090/wallet/setaccountid -d '{
"owner_address":"41a7d8a35b260395c14aa456297662092ba3b76fc0","account_id":"6161616162626262"}'
```
Parameters: 

- `owner_address`: Owner address, default hexString
- `account_id` :Account id, default hexString

Return: Unsigned transaction

#### wallet/getaccountbyid
Description: Query an account information by account id
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountbyid -d
'{"account_id":"6161616162626262"}'
```
Parameters: `account_id` Account id, default hexString

Return:Account object


### Transfers and transactions

The following are transfer and transaction related APIs:

- [wallet/createtransaction](#walletcreatetransaction)
- [wallet/broadcasttransaction](#walletbroadcasttransaction)
- [wallet/broadcasthex](#walletbroadcasthex)
- [wallet/getsignweight](#walletgetsignweight)
- [wallet/getapprovedlist](#walletgetapprovedlist)


#### wallet/createtransaction
Description: Create a transfer transaction, if to address is not existed, then create the account on the blockchain
```
curl -X POST  http://127.0.0.1:8090/wallet/createtransaction -d '{"to_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d", "owner_address": "41D1E7A6BC354106CB410E65FF8B181C600FF14292", "amount": 1000 }'
```
Parameters: 

- `to_address` To address, default hexString
- `owner_address` Owner address, default hexString
- `amount` Transfer amount
- `Permission_id` Optional, for multi-signature use

Return: Unsigned transaction


#### wallet/broadcasttransaction
Description: Broadcast transaction after sign
```
curl -X POST  http://127.0.0.1:8090/wallet/broadcasttransaction -d '{"signature":["97c825b41c77de2a8bd65b3df55cd4c0df59c307c0187e42321dcc1cc455ddba583dd9502e17cfec5945b34cad0511985a6165999092a6dec84c2bdd97e649fc01"],"txID":"454f156bf1256587ff6ccdbc56e64ad0c51e4f8efea5490dcbc720ee606bc7b8","raw_data":{"contract":[{"parameter":{"value":{"amount":1000,"owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0","to_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"267e","ref_block_hash":"9a447d222e8de9f2","expiration":1530893064000,"timestamp":1530893006233}}'
```
Parameters: Transaction after sign

Return:The result of the broadcast

#### wallet/broadcasthex
Description: Broadcast transaction hex string after sign
```
curl -X POST  http://127.0.0.1:8090/wallet/broadcasthex -d '{"transaction":"0A8A010A0202DB2208C89D4811359A28004098A4E0A6B52D5A730802126F0A32747970652E676F6F676C65617069732E636F6D2F70726F746F636F6C2E5472616E736665724173736574436F6E747261637412390A07313030303030311215415A523B449890854C8FC460AB602DF9F31FE4293F1A15416B0580DA195542DDABE288FEC436C7D5AF769D24206412418BF3F2E492ED443607910EA9EF0A7EF79728DAAAAC0EE2BA6CB87DA38366DF9AC4ADE54B2912C1DEB0EE6666B86A07A6C7DF68F1F9DA171EEE6A370B3CA9CBBB00"}'
```
Parameters: Transaction hex after sign

Return: The result of the broadcast


#### wallet/getsignweight
Description: Query the current signatures total weight of a transaction after sign
```
curl -X POST  http://127.0.0.1:8090/wallet/getsignweight -d '{
    "signature": [
        "e0bd4a60f1b3c89d4da3894d400e7e32385f6dd690aee17fdac4e016cdb294c5128b66f62f3947a7182c015547496eba95510c113bda2a361d811b829343c36501",
        "596ead6439d0f381e67f30b1ed6b3687f2bd53ce5140cdb126cfe4183235804741eeaf79b4e91f251fd7042380a9485d4d29d67f112d5387bc7457b355cd3c4200"
    ],
    "txID": "0ae84a8439f5aa8fd2c458879a4031a7452aebed8e6e99ffbccd26842d4323c4",
    "raw_data": {
        "contract": [{
            "parameter": {
                "value": {
                    "amount": 1000000,
                    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                },
                "type_url": "type.googleapis.com/protocol.TransferContract"
            },
            "type": "TransferContract"
        }],
        "ref_block_bytes": "163d",
        "ref_block_hash": "77ef4ace148b05ba",
        "expiration": 1555664823000,
        "timestamp": 1555664763418
    },
    "raw_data_hex": "0a02163d220877ef4ace148b05ba40d8c5e5a6a32d5a69080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18c0843d2802709af4e1a6a32d",
    "visible": true}'
```
Parameters: Transaction object after sign

Return: The current signatures total weight

#### wallet/getapprovedlist
Description: Query the signatures list of a transaction after sign
```
curl -X POST  http://127.0.0.1:8090/wallet/getapprovedlist -d '{
    "signature": [
        "e0bd4a60f1b3c89d4da3894d400e7e32385f6dd690aee17fdac4e016cdb294c5128b66f62f3947a7182c015547496eba95510c113bda2a361d811b829343c36501",
        "596ead6439d0f381e67f30b1ed6b3687f2bd53ce5140cdb126cfe4183235804741eeaf79b4e91f251fd7042380a9485d4d29d67f112d5387bc7457b355cd3c4200"
    ],
    "txID": "0ae84a8439f5aa8fd2c458879a4031a7452aebed8e6e99ffbccd26842d4323c4",
    "raw_data": {
        "contract": [{
            "parameter": {
                "value": {
                    "amount": 1000000,
                    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                },
                "type_url": "type.googleapis.com/protocol.TransferContract"
            },
            "type": "TransferContract"
        }],
        "ref_block_bytes": "163d",
        "ref_block_hash": "77ef4ace148b05ba",
        "expiration": 1555664823000,
        "timestamp": 1555664763418
    },
    "raw_data_hex": "0a02163d220877ef4ace148b05ba40d8c5e5a6a32d5a69080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18c0843d2802709af4e1a6a32d",
    "visible": true}'
```
Parameter: Transaction object after sign

Return: The list of the signatures


### Account Resources
The following are account resource related APIs:

- [wallet/getaccountresource](#walletgetaccountresource)
- [wallet/getaccountnet](#walletgetaccountnet)
- [wallet/unfreezebalance](#walletunfreezebalance)
- [wallet/getdelegatedresource](#walletgetdelegatedresource)
- [wallet/getdelegatedresourceaccountindex](#walletgetdelegatedresourceaccountindex)
- [wallet/freezebalancev2](#walletfreezebalancev2)
- [wallet/unfreezebalancev2](#walletunfreezebalancev2)
- [wallet/cancelallunfreezev2](#walletcancelallunfreezev2)
- [wallet/delegateresource](#walletdelegateresource)
- [wallet/undelegateresource](#walletundelegateresource)
- [wallet/withdrawexpireunfreeze](#walletwithdrawexpireunfreeze)
- [wallet/getavailableunfreezecount](#walletgetavailableunfreezecount)
- [wallet/getcanwithdrawunfreezeamount](#walletgetcanwithdrawunfreezeamount)
- [wallet/getcandelegatedmaxsize](#walletgetcandelegatedmaxsize)
- [wallet/getdelegatedresourcev2](#walletgetdelegatedresourcev2)
- [wallet/getdelegatedresourceaccountindexv2](#walletgetdelegatedresourceaccountindexv2)


#### wallet/getaccountresource
Description: Query the resource information of an account
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountresource -d {"address" : "419844f7600e018fd0d710e2145351d607b3316ce9"}
```
Parameters: 

- `address`: Address, default hexString

Return: The resource information



#### wallet/getaccountnet
Description: Query the bandwidth information of an account
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountnet -d '{"address": "4112E621D5577311998708F4D7B9F71F86DAE138B5"}'
```
Parameters: `address` - Address, default hexString

Return: Bandwidth information

#### wallet/freezebalance
Description: Stake TRX. This interface has been deprecated, please use FreezeBalanceV2 to stake TRX to obtain resources.


#### wallet/unfreezebalance
Description: Unstake the TRX that staked during stake1.0 phase.
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezebalance -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"resource": "BANDWIDTH",
"receiver_address":"414332f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```
Parameters: 

- `owner_address` Owner address, default hexString
- `resource` unstake type 'BANDWIDTH' or 'ENERGY'
- `receiverAddress` The address that will lose the resource, default hexString
- `Permission_id` Optional, for multi-signature use

Return: Unsigned transaction


#### wallet/getdelegatedresource
Description: Query the resource delegation information
```
curl -X POST  http://127.0.0.1:8090/wallet/getdelegatedresource -d '
{
"fromAddress": "419844f7600e018fd0d710e2145351d607b3316ce9",
"toAddress": "41c6600433381c731f22fc2b9f864b14fe518b322f"
}'
```
Parameters: 

- `fromAddress`: from address, default hexString
- `toAddress`: to address, default hexString

Return: Resource delegation information

#### wallet/getdelegatedresourceaccountindex
Description: Query the resource delegation by an account during stake1.0 phase. i.e. list all addresses that have delegated resources to an account.
```
curl -X POST  http://127.0.0.1:8090/wallet/getdelegatedresourceaccountindex -d '
{
"value": "419844f7600e018fd0d710e2145351d607b3316ce9",
}'
```
Parameters: 

- `value`: account address

Return:resource delegation index



#### wallet/freezebalancev2
Description: Stake TRX

```
curl -X POST http://127.0.0.1:8090/wallet/freezebalancev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "frozen_balance": 10000,
    "resource": "BANDWIDTH"
}'
```

Parameters:  

- `owner_address`: Owner address, default hexString
- `frozen_balance`: TRX stake amount, the unit is sun
- `resource`: TRX stake type, 'BANDWIDTH' or 'ENERGY'
- `permission_id`: Optional, for multi-signature use

Return: Unsigned transaction

#### wallet/unfreezebalancev2

Description: Unstake some TRX staked in Stake2.0, release the corresponding amount of bandwidth or energy, and voting rights (TP)

```
curl -X POST http://127.0.0.1:8090/wallet/unfreezebalancev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "unfreeze_balance": 1000000,
    "resource": "BANDWIDTH"
}'
```

Parameters: 

- `owner_address`: Owner address, default hexString
- `resource`: Resource type: 'BANDWIDTH' or 'ENERGY'
- `unfreeze_balance`: The amount of TRX to unstake, in sun
- `permission_id`: Optional, for multi-signature use

Return:Unsigned transaction

#### wallet/cancelallunfreezev2

Description: Cancel unstakings, all unstaked funds still in the waiting period will be re-staked, all unstaked funds that exceeded the 14-day waiting period will be automatically withdrawn to the owner’s account

```
curl -X POST http://127.0.0.1:8090/wallet/cancelallunfreezev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```

Parameters: 

- `owner_address`: Owner address, default hexString
- `permission_id`: Optional, for multi-signature use

Return:Unsigned transaction

#### wallet/delegateresource

Description: Delegate bandwidth or energy resources to other accounts in Stake2.0.

```
curl -X POST http://127.0.0.1:8090/wallet/delegateresource -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "receiver_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "balance": 1000000,
    "resource": "BANDWIDTH",
    "lock": false
}'
```

Parameters: 

- `owner_address`: Account address
- `receiver_address`: Resource receiver address
- `balance`: Amount of TRX staked for resources to be delegated, unit is sun
- `resource`: Resource type: 'BANDWIDTH' or 'ENERGY'
- `lock`: Whether it is locked, if it is set to true, the delegated resources cannot be undelegated within 3 days. When the lock time is not over, if the owner delegates the same type of resources using the lock to the same address, the lock time will be reset to 3 days
- `lock_period`: lock time,The unit is block interval(3 seconds), indicates the time of how many blocks will be produced from the moment the transaction is executed. Only when lock is true, this field is valid. If the delegate lock period is 1 day, the lock_period is: 28800
- `permission_id`: Optional, for multi-signature use

Return:Unsigned transaction

#### wallet/undelegateresource

Description: Cancel the delegation of bandwidth or energy resources to other account


```
curl -X POST http://127.0.0.1:8090/wallet/undelegateresource -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "receiver_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "balance": 1000000,
    "resource": "BANDWIDTH"
}'
```

Parameters: 

- `owner_address`: Account address
- `receiver_address`: Resource receiver address
- `balance`: Amount of TRX staked for resources to be delegated, unit is sun
- `resource`: Resource type: 'BANDWIDTH' or 'ENERGY'
- `permission_id`: Optional, for multi-signature use

Return:Unsigned transaction

#### wallet/withdrawexpireunfreeze

Description: Withdraw unfrozen balance in Stake2.0, the user can call this API to get back their funds after executing /wallet/unfreezebalancev2 transaction and waiting N days, N is a network parameter
```
curl -X POST http://127.0.0.1:8090/wallet/withdrawexpireunfreeze -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```

Parameters: 

- `owner_address`: Account address
- `permission_id`: Optional, for multi-signature use

Return: Unsigned transaction



#### wallet/getavailableunfreezecount

Description:Remaining times of executing unstake operation in Stake2.0
```
curl -X POST http://127.0.0.1:8090/wallet/getavailableunfreezecount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters: 

- `owner_address`: Account address

Return:Remaining times of available unstaking.

#### wallet/getcanwithdrawunfreezeamount

Description:Query the withdrawable balance at the specified timestamp In Stake2.0
```
curl -X POST http://127.0.0.1:8090/wallet/getcanwithdrawunfreezeamount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "timestamp": 1667977444000,
  "visible": true
}
'
```

Parameters: 

- `owner_address`: Account address
- `timestamp`: query cutoff timestamp, in milliseconds.

Return: withdrawable balance, unit is sun.


#### wallet/getcandelegatedmaxsize

Description: In Stake2.0, query the amount of delegatable resources share of the specified resource type for an address, unit is sun.
```
curl -X POST http://127.0.0.1:8090/wallet/getcandelegatedmaxsize -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "type": 0,
  "visible": true
}
'
```

Parameters: 

- `owner_address`: Account address
- `type`: resource type, 0 is bandwidth, 1 is energy

Return:the amount of delegatable resource share, unit is sun.


#### wallet/getdelegatedresourcev2

In Stake2.0, query the detail of resource share delegated from fromAddress to toAddress
```
curl -X POST http://127.0.0.1:8090/wallet/getdelegatedresourcev2 -d
'{
  "fromAddress": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "toAddress": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
  "visible": true
}
'
```

Parameters: 

- `fromAddress`: resource from address, default hexString
- `toAddress`: resource to address

Return:Resource delegation list

#### wallet/getdelegatedresourceaccountindexv2
In Stake2.0, query the resource delegation index by an account. Two lists will return, one is the list of addresses the account has delegated its resources(toAddress), and the other is the list of addresses that have delegated resources to the account(fromAddress).
```
curl -X POST http://127.0.0.1:8090/wallet/getdelegatedresourceaccountindexv2 -d
'{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters: 

- `value`: account address

Return:Two lists will return, one is the list of addresses the account has delegated its resources(toAddress), and the other is the list of addresses that have delegated resources to the account(fromAddress).


### Query The Network
The following is the API for querying data on the chain:

- [wallet/getnowblock](#walletgetnowblock)
- [wallet/getblock](#walletgetblock)
- [wallet/getblockbynum](#walletgetblockbynum)
- [wallet/getblockbyid](#walletgetblockbyid)
- [wallet/getblockbylatestnum](#walletgetblockbylatestnum)
- [wallet/getblockbylimitnext](#walletgetblockbylimitnext)
- [wallet/getblockbalance](#walletgetblockbalance)
- [wallet/gettransactionbyid](#walletgettransactionbyid)
- [wallet/gettransactioninfobyid](#walletgettransactioninfobyid)
- [wallet/gettransactioncountbyblocknum](#walletgettransactioncountbyblocknum)
- [wallet/gettransactioninfobyblocknum](#walletgettransactioninfobyblocknum)
- [wallet/listnodes](#walletlistnodes)
- [wallet/getnodeinfo](#walletgetnodeinfo)
- [wallet/getchainparameters](#walletgetchainparameters)
- [wallet/getenergyprices](#walletgetenergyprices)
- [wallet/getbandwidthprices](#walletgetbandwidthprices)
- [wallet/getburntrx](#walletgetburntrx)

#### wallet/getnowblock
Description: Query the latest block information
```
curl -X POST  http://127.0.0.1:8090/wallet/getnowblock
```
Parameters: N/A

Return: The latest block

#### wallet/getblock
Query block header information or entire block information according to block height or block hash
```
curl -X POST  http://127.0.0.1:8090/wallet/getblock -d '{"detail":false}'
```
Parameters: 

- `id_or_num`: id_or_num can be the block height or the block hash. No value entered means to query the latest block.
- `detail`: true means query the entire block information include the header and body. false means only query the block header information.

Return: block or block header

#### wallet/getblockbynum
Description: Query a block information by block height
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbynum -d '{"num": 1}'
```
Parameters: Block height

Return: block

#### wallet/getblockbyid
Description: Query a block information by block id
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbyid -d '{"value": "0000000000038809c59ee8409a3b6c051e369ef1096603c7ee723c16e2376c73"}'
```
Parameters: Block id

Return: block

#### wallet/getblockbylatestnum
Description: Query the several latest blocks
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbylatestnum -d '{"num": 5}'
```
Parameters: The number of the blocks expected to return

Return:The list of the blocks

#### wallet/getblockbylimitnext
Description: Query a list of blocks by range
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbylimitnext -d '{"startNum": 1, "endNum": 2}'
```
Parameters: 

- `startNum`: The start block height, itself included
- `endNum`: The end block height, itself not included

Return: The list of the blocks



#### wallet/getblockbalance
Description：Get all balance change operations in a block.
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbalance -d
'{
    "hash": "000000000000dc2a3731e28a75b49ac1379bcc425afc95f6ab3916689fbb0189",
    "number": 56362,
    "visible": true
}'
```
Parameters: The hash and block number must match.

Return:
```
{
    "block_identifier": {
        "hash": "000000000000dc2a3731e28a75b49ac1379bcc425afc95f6ab3916689fbb0189",
        "number": 56362
    },
    "timestamp": 1530060672000,
    "transaction_balance_trace": [
        {
            "transaction_identifier": "e6cabb1833cd1f795eed39d8dd7689eaa70e5bb217611766c74c7aa9feea80df",
            "operation": [
                {
                    "operation_identifier": 0,
                    "address": "TPttBLmFuykRi83y9HxDoEWxTQw6CCcQ4p",
                    "amount": -100000
                },
                {
                    "operation_identifier": 1,
                    "address": "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy",
                    "amount": 100000
                },
                {
                    "operation_identifier": 2,
                    "address": "TPttBLmFuykRi83y9HxDoEWxTQw6CCcQ4p",
                    "amount": -10000000
                },
                {
                    "operation_identifier": 3,
                    "address": "TMrysg7DbwR1M8xqhpaPdVCHCuWFhw7uk1",
                    "amount": 10000000
                }
            ],
            "type": "TransferContract",
            "status": "SUCCESS"
        }
    ]
}
```

#### wallet/gettransactionbyid
Description: Query a transaction information by transaction id
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactionbyid -d '{"value": "d5ec749ecc2a615399d8a6c864ea4c74ff9f523c2be0e341ac9be5d47d7c2d62"}'
```
Parameters: Transaction id

Return: Transaction information

#### wallet/gettransactioninfobyid
Description: Query the transaction fee, block height by transaction id
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioninfobyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
Parameters: value - Transaction id

Return: Transaction fee & block height

#### wallet/gettransactioncountbyblocknum
Description: Query th the number of transactions in a specific block
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioncountbyblocknum -d '{"num" : 100}'
```
Parameters: num - Block height

Return: The number of transactions

#### wallet/gettransactioninfobyblocknum
Description: Query the list of transaction information in a specific block
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioninfobyblocknum -d '{"num" : 100}'
```
Parameters: num is the Block height

Return:The list of transaction information


#### wallet/listnodes
Description: Query the list of nodes connected to the ip of the api
```
curl -X POST  http://127.0.0.1:8090/wallet/listnodes
```
Parameters: N/A

Return: The list of nodes


#### wallet/getnodeinfo
Description: Query the current node information
```
curl  http://127.0.0.1:8090/wallet/getnodeinfo
```
Return: The node information

#### wallet/getchainparameters
Description: Query the parameters of the blockchain used for SR(Super Representatives) to create a proposal
```
curl -X POST  http://127.0.0.1:8090/wallet/getchainparameters
```
Return: The list of parameters of the blockchain

#### wallet/getenergyprices
Description: Query historical energy unit price
```
curl -X POST  http://127.0.0.1:8090/wallet/getenergyprices
```
Return: All historical energy unit price information. Each unit price change is separated by a comma. Before the colon is the millisecond timestamp, and after the colon is the energy unit price in sun.

#### wallet/getbandwidthprices
Description: Query historical bandwidth unit price
```
curl -X POST  http://127.0.0.1:8090/wallet/getbandwidthprices
```
Return: All historical bandwidth unit price information. Each unit price change is separated by a comma. Before the colon is the millisecond timestamp, and after the colon is the bandwidth unit price in sun.

#### wallet/getburntrx
Description: Query the amount of TRX burned due to on-chain transaction fees since No. 54 Committee Proposal took effect
```
curl -X POST  http://127.0.0.1:8090/wallet/getburntrx
```
Return: Amount of TRX burned, in sun.


### Smart Contracts
The following are smart contract related APIs:

- [wallet/getcontract](#walletgetcontract)
- [wallet/getcontractinfo](#walletgetcontractinfo)
- [wallet/deploycontract](#walletdeploycontract)
- [wallet/triggersmartcontract](#wallettriggersmartcontract)
- [wallet/triggerconstantcontract](#wallettriggerconstantcontract)
- [wallet/updatesetting](#walletupdatesetting)
- [wallet/updateenergylimit](#walletupdateenergylimit)
- [wallet/clearabi](#walletclearabi)
- [wallet/estimateenergy](#walletestimateenergy)

#### wallet/getcontract
Queries a contract's information from the blockchain, including the bytecode of the contract, ABI, configuration parameters, etc.
```
curl -X POST  http://127.0.0.1:8090/wallet/getcontract -d '{"value":"4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
Parameters: value - Contract address

Return:SmartContract

#### wallet/getcontractinfo
Queries a contract's information from the blockchain. The difference from the wallet/getcontract interface is that this interface returns not only the bytecode but also the runtime bytecode of the contract. Compared with bytecode, runtime bytecode does not contain constructor and constructor parameter information.
```
curl -X POST  http://127.0.0.1:8090/wallet/getcontractinfo -d '{"value":"4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
Parameters: value - Contract address

Return: contract's information

#### wallet/deploycontract
Description: Deploy a smart contract
```
curl -X POST  http://127.0.0.1:8090/wallet/deploycontract -d '{"abi":"[{\"constant\":false,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"},{\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"set\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"}],\"name\":\"get\",\"outputs\":[{\"name\":\"value\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"}]","bytecode":"608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029","parameter":"","call_value":100,"name":"SomeContract","consume_user_resource_percent":30,"fee_limit":10,"origin_energy_limit": 10,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
Parameters: 

- `abi`:abi
- `bytecode`:bytecode，hexString
- `parameter`:The list of the parameters of the constructor, It should be converted hexString after encoded according to ABI encoder. If constructor has no parameter, this can be optional
- `consume_user_resource_percent`: Consume user's resource percentage. It should be an integer between [0, 100]. if 0, means it does not consume user's resource until the developer's resource has been used up
- `fee_limit`: The maximum TRX burns for resource consumption
- `call_value`: The TRX transfer to the contract for each call
- `owner_address`:Owner address of the contract, default hexString
- `name`:Contract name
- `origin_energy_limit`: The maximum resource consumption of the creator in one execution or creation
- `call_token_value`: The amount of trc10 token transfer to the contract for each call (Optional)
- `token_id`:The id of trc10 token transfer to the contract (Optional)
- `Permission_id`: Optional, for multi-signature use

Return:Unsigned transaction

#### wallet/triggersmartcontract
Description: Trigger smart contract
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/triggersmartcontract -d
'{
    "contract_address": "4189139CB1387AF85E3D24E212A008AC974967E561",
    "function_selector": "set(uint256,uint256)",
    "parameter": "00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002",
    "fee_limit": 10,
    "call_value": 100,
    "owner_address": "41D1E7A6BC354106CB410E65FF8B181C600FF14292"
}'
```
Parameters: 

- `contract_address`: Contract address, default hexString
- `function_selector`: Function call, must not leave a blank space
- `parameter`: The parameter passed to 'function_selector', the format must match with the VM's requirement. You can use a js tool provided by remix to convert a parameter like [1,2] to the format that VM requires
- `data`: The data for interacting with smart contracts, including the contract function and parameters. You can choose to use this field, or you can choose to use `function_selector` and `parameter` for contract interaction. When both of `data` and `function_selector` exist, `function_selector` is preferred
- `fee_limit`: The maximum TRX burns for resource consumption
- `call_value`: The TRX transfer to the contract for each call
- `call_token_value`: The amount of  trc10 token transfer to the contract for each call
- `token_id`: The id of trc10 token transfer to the contract
- `owner_address`: Owner address that triggers the contract, default hexString
- `permission_id`: Optional, for multi-signature use


Return:Unsigned transaction


#### wallet/triggerconstantcontract
Description: Trigger the constant of the smart contract, the transaction is off the blockchain
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/triggerconstantcontract -d
'{
    "contract_address": "4189139CB1387AF85E3D24E212A008AC974967E561",
    "function_selector": "set(uint256,uint256)",
    "parameter": "00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002",
    "call_value": 100,
    "owner_address": "41D1E7A6BC354106CB410E65FF8B181C600FF14292"
}'
```
Parameters: 

- `contract_address`: Smart contract address, default hexString
- `function_selector`:  Function call, must not leave a blank space
- `parameter`: The parameter passed to 'function_selector', the format must match with the VM's requirement. You can use a hs tool provided by remix to convert a parameter like [1,2] to the format that VM requires
- `data`: The data for interacting with smart contracts, including the contract function and parameters. You can choose to use this field, or you can choose to use `function_selector` and `parameter` for contract interaction. When both of `data` and `function_selector` exist, `function_selector` is preferred
- `call_value`: The TRX transfer to the contract for each call
- `owner_address`: Owner address that triggers the contract, default hexString
- `call_token_value`: The amount of  trc10 token transfer to the contract for each call
- `token_id`: The id of trc10 token transfer to the contract

Return: Transaction object

Note: The unit of TRX in the parameters is SUN



#### wallet/updatesetting
Description: Update the consume_user_resource_percent parameter of a smart contract
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/updatesetting -d
'{
    "owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9",
    "contract_address": "41c6600433381c731f22fc2b9f864b14fe518b322f",
    "consume_user_resource_percent": 7
}'
```

- `owner_address`:Owner address of the smart contract, default hexString
- `contract_address`:Smart contract address, default hexString
- `consume_user_resource_percent`:Consume user's resource percentage
- `Permission_id`: Optional, for multi-signature use

Return: Transaction object

#### wallet/updateenergylimit

Description: Update the origin_energy_limit parameter of a smart contract
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/updateenergylimit -d
'{
    "owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9",
    "contract_address": "41c6600433381c731f22fc2b9f864b14fe518b322f",
    "origin_energy_limit": 7
}'
```
Parameters: 

- `owner_address`: Owner address of the smart contract, default hexString
- `contract_address`: Smart contract address, default hexString
- `origin_energy_limit`: The maximum resource consumption of the creator in one execution or creation
- `permission_id`: Optional, for multi-signature use

Return: Transaction object




#### wallet/clearabi
Description: To clear the abi of a smart contract
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/clearabi -d
'{
    "owner_address": "41a7d8a35b260395c14aa456297662092ba3b76fc0",
    "contract_address": "417bcb781f4743afaacf9f9528f3ea903b3782339f"
}'
```

Parameters: 

- `owner_address`:Owner address of the smart contract
- `contract_address`: Smart contract address, default hexString

Return: Transaction object

#### wallet/estimateenergy
Estimate the energy required for the successful execution of smart contract transactions
```
curl -X POST  http://127.0.0.1:8090/wallet/estimateenergy -d '{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "contract_address": "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
  "function_selector": "transfer(address,uint256)",
  "parameter": "00000000000000000000004115208EF33A926919ED270E2FA61367B2DA3753DA0000000000000000000000000000000000000000000000000000000000000032",
  "visible": true
}'
```

Parameters: 

- `contract_address` : Smart contract address. If visible=true, use base58check format, otherwise use hex format.
- `function_selector`: Function call, must not be left blank.
- `parameter`: Parameter encoding needs to be in accordance with the ABI rules, the rules are more complicated, users can use the ethers library to encode
- `data`: The data for interacting with smart contracts, including the contract function and parameters. You can choose to use this field, or you can choose to use `function_selector` and `parameter` for contract interaction. When both of `data` and `function_selector` exist, `function_selector` is preferred
- `call_value`: The TRX transfer to the contract for each call
- `owner_address`:Owner address that triggers the contract. If visible=true, use base58check format, otherwise use hex 
- `call_token_value`: The amount of  trc10 token transfer to the contract for each call
- `token_id`: The id of trc10 token transfer to the contract

Return:Estimated the energy value


### TRC10 token
The following are TRC10 token-related APIs:

- [wallet/getassetissuebyaccount](#walletgetassetissuebyaccount)
- [wallet/getassetissuebyname](#walletgetassetissuebyname)
- [wallet/getassetissuelistbyname](#walletgetassetissuelistbyname)
- [wallet/getassetissuebyid](#walletgetassetissuebyid)
- [wallet/getassetissuelist](#walletgetassetissuelist)
- [wallet/getpaginatedassetissuelist](#walletgetpaginatedassetissuelist)
- [wallet/transferasset](#wallettransferasset)
- [wallet/participateassetissue](#walletparticipateassetissue)
- [wallet/createassetissue](#walletcreateassetissue)
- [wallet/unfreezeasset](#walletunfreezeasset)
- [wallet/updateasset](#walletupdateasset)


#### wallet/getassetissuebyaccount
Description: Query the token issue information of an account
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyaccount -d
'{
    "address": "41F9395ED64A6E1D4ED37CD17C75A1D247223CAF2D"
}'
```

Parameter address: Token issuer's address, default hexString

Return: Token object




#### wallet/getassetissuebyname
Description: Query a token by token name
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyname -d
'{
    "value": "44756354616E"
}'
```

Parameter value: Token name, default hexString

Return: Token object

#### wallet/getassetissuelistbyname
Description: Query the list of tokens by name
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getassetissuelistbyname -d
'{
    "value": "44756354616E"
}'
```

Parameter value: Token name, default hexString

Return: The list of tokens


#### wallet/getassetissuebyid
Description: Query a token by token id
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyid -d
'{
    "value": "1000001"
}'
```

Parameter value: Token id

Return: Token object



#### wallet/getassetissuelist
Description: Query the list of all the tokens
```console
$ curl -X GET  http://127.0.0.1:8090/wallet/getassetissuelist
```

Parameter: No parameter

Return: The list of all the tokens



#### wallet/getpaginatedassetissuelist
Description: Query the list of all the tokens by pagination
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedassetissuelist -d
'{
    "offset": 0,
    "limit": 10
}'
```

Parameters:

- `offset`: The index of the start token
- `limit`: The amount of tokens per page

Return: The list of tokens by pagination



#### wallet/transferasset
Description: Transfer token
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/transferasset -d
'{
    "owner_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
    "asset_name": "31303030303031",
    "amount": 100
}'
```
Parameters: 

- `owner_address`: Owner address, default hexString
- `to_address`: To address, default hexString
- `asset_name`: Token id, default hexString
- `amount`: Token transfer amount
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'amount' is the smallest unit of the token




#### wallet/participateassetissue
Description: Participate a token
```console
$ curl -X POST http://127.0.0.1:8090/wallet/participateassetissue -d
'{
    "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "amount": 100,
    "asset_name": "3230313271756265696a696e67"
}'
```
Parameters: 

- `to_address`: The issuer address of the token, default hexString
- `owner_address`: The participant address, default hexString
- `amount`: Participate token amount
- `asset_name`: Token id, default hexString
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'amount' is the smallest unit of the token




#### wallet/createassetissue
Description: Issue a token
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/createassetissue -d
'{
    "owner_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
    "name": "0x6173736574497373756531353330383934333132313538",
    "abbr": "0x6162627231353330383934333132313538",
    "total_supply": 4321,
    "trx_num": 1,
    "num": 1,
    "start_time": 1530894315158,
    "end_time": 1533894312158,
    "description": "007570646174654e616d6531353330363038383733343633",
    "url": "007570646174654e616d6531353330363038383733343633",
    "free_asset_net_limit": 10000,
    "public_free_asset_net_limit": 10000,
    "frozen_supply": {
        "frozen_amount": 1,
        "frozen_days": 2
    }
}'
```
Parameters: 

- `owner_address`: Owner address, default hexString
- `name`: Token name, default hexString
- `abbr`: Token name abbreviation, default hexString
- `total_supply`: Token total supply
- `trx_num`: Define the price by the ratio of trx_num/num
- `num`: Define the price by the ratio of trx_num/num
- `start_time`: ICO start time
- `end_time`: ICO end time
- `description`: Token description, default hexString
- `url`: Token official website url, default hexString
- `free_asset_net_limit`: Token free asset net limit
- `public_free_asset_net_limit`: Token public free asset net limit
- `frozen_supply`: Token staked supply
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'trx_num' is SUN


#### wallet/unfreezeasset
Description: Unstake the staked token that is due
```console
$ curl -X POST http://127.0.0.1:8090/wallet/unfreezeasset -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```

Parameters:
- `owner_address`: Owner address, default hexString
- `permission_id`: Optional, for multi-signature use

Return: Transaction object


#### wallet/updateasset
Description: Update token information
```console
$ curl -X POST http://127.0.0.1:8090/wallet/updateasset -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "description": "",
    "url": "",
    "new_limit": 1000000,
    "new_public_limit": 100
}'
```

Parameters:

- `owner_address`: The issuers address of the token, default hexString
- `description`: The description of token, default hexString
- `url`: The token's website url, default hexString
- `new_limit`: Each token holder's free bandwidth
- `new_public_limit`: The total free bandwidth of the token
- `permission_id`: Optional, for multi-signature use

Return: Transaction object


### Vote and SR
The following are voting and SR related APIs:


- [wallet/createwitness](#walletcreatewitness)
- [wallet/updatewitness](#walletupdatewitness)
- [wallet/listwitnesses](#walletlistwitnesses)
- [wallet/withdrawbalance](#walletwithdrawbalance)
- [wallet/votewitnessaccount](#walletvotewitnessaccount)
- [wallet/getBrokerage](#walletgetbrokerage)
- [wallet/updateBrokerage](#walletupdatebrokerage)
- [wallet/getReward](#walletgetreward)
- [wallet/getnextmaintenancetime](#walletgetnextmaintenancetime)

#### wallet/createwitness
Description: Apply to become a super representative
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/createwitness -d
'{
    "owner_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "url": "007570646174654e616d6531353330363038383733343633"
}'
```

Parameters:

- `owner_address`: Owner address, default hexString
- `url`: Website url, default hexString
- `permission_id`: Optional, for multi-signature use

Return: Transaction object


#### wallet/updatewitness
Description: Update the super representative' website url
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/updatewitness -d
'{
    "owner_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "update_url": "007570646174654e616d6531353330363038383733343633"
}'
```

Parameters:

- `owner_address`: Owner address, default hexString
- `update_url`: Website url, default hexString
- `permission_id`: Optional, for multi-signature use

Return: Transaction object


#### wallet/listwitnesses
Description: Qyery the list of the super representatives
```
curl -X POST  http://127.0.0.1:8090/wallet/listwitnesses
```
Parameters: N/A

Return:SR(Super Representatives) list

#### wallet/withdrawbalance
Description: Withdraw reward to account balance for super representatives
```console
$ curl -X POST http://127.0.0.1:8090/wallet/withdrawbalance -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```

Parameters:

- `owner_address`: Owner address, default hexString
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: It can only withdraw once for every 24 hours




#### wallet/votewitnessaccount
Description: Vote for super representatives
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/votewitnessaccount -d
'{
    "owner_address": "41d1e7a6bc354106cb410e65ff8b181c600ff14292",
    "votes": [
        {
            "vote_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
            "vote_count": 5
        }
    ]
}'
```

Parameters:

- `owner_address`: Owner address, default hexString
- `votes`: 'vote_address' stands for the address of the super representative you want to vote, default hexString, 'vote_count' stands for the number of votes you want to vote
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

#### wallet/getBrokerage
Description: Query the ratio of brokerage of the super representative
```console
$ curl -X GET  http://127.0.0.1:8090/wallet/getBrokerage -d '{
"address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```

Parameter `address`: The address of the SR's account, default hexString

Return: The ratio of brokerage of the SR

#### wallet/updateBrokerage
Description: Update the ratio of brokerage
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/updateBrokerage  -d '{
"owner_address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0",
"brokerage":30
}'
```

Parameters:

- `owner_address`: The address of the SR's account, default hexString
- `brokerage`: The ratio of brokerage you want to update to


Return: Transaction object


#### wallet/getReward
Description: Query unclaimed reward
```console
$ curl -X GET
http://127.0.0.1:8090/wallet/getReward -d '{
"address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```

Parameter `address`: The address of the voter's account, default hexString

Return: Unclaimed reward


#### wallet/getnextmaintenancetime
Description: Query the time interval till the next vote round
```
curl -X POST  http://127.0.0.1:8090/wallet/getnextmaintenancetime
```
Parameters: N/A


Return: The time interval till the next vote round(unit: ms)


### Proposals
The following are proposal-related APIs:


- [wallet/proposalcreate](#walletproposalcreate)
- [wallet/getproposalbyid](#walletgetproposalbyid)
- [wallet/listproposals](#walletlistproposals)
- [wallet/proposalapprove](#walletproposalapprove)
- [wallet/proposaldelete](#walletproposaldelete)
- [wallet/getpaginatedproposallist](#walletgetpaginatedproposallist)


#### wallet/proposalcreate
Description: Create a proposal
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/proposalcreate -d
'{
    "owner_address": "419844F7600E018FD0D710E2145351D607B3316CE9",
    "parameters": [
        {
            "key": 0,
            "value": 100000
        },
        {
            "key": 1,
            "value": 2
        }
    ]
}'
```

Parameters:

- `owner_address`: Creator address
- `parameters`: Proposal parameters
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

#### wallet/getproposalbyid
Description: Query a proposal by proposal id
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getproposalbyid -d
'{
    "id": 1
}'
```

Parameter `id`: Proposal id

Return: The proposal information


#### wallet/listproposals
Description: Query all the proposals
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/listproposals
```

Parameter: No parameter

Return: The list of all the proposals

#### wallet/proposalapprove
Description: To approve a proposal
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/proposalapprove -d
'{
    "owner_address": "419844F7600E018FD0D710E2145351D607B3316CE9",
    "proposal_id": 1,
    "is_add_approval": true
}'
```

Parameters:

- `owner_address`: The address that makes the approve action, default hexString
- `proposal_id`: Proposal id
- `is_add_approval`: Whether to approve
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

#### wallet/proposaldelete
Description: To delete a proposal
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/proposaldelete -d
'{
    "owner_address": "419844F7600E018FD0D710E2145351D607B3316CE9",
    "proposal_id": 1
}'
```

Parameters:

- `owner_address`: Owner address of the proposal, default hexString
- `proposal_id`: Proposal id
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

#### wallet/getpaginatedproposallist
Description: Query the list of all the proposals by pagination
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedproposallist -d
'{
    "offset": 0,
    "limit": 10
}'
```

Parameters:

- `offset`: The index of the start proposal
- `limit`: The amount of proposals per page

Return: The list of proposals by pagination



### DEX Exchange
The following are the APIs related to decentralized exchanges:

- [wallet/exchangecreate](#walletexchangecreate)
- [wallet/exchangeinject](#walletexchangeinject)
- [wallet/exchangewithdraw](#walletexchangewithdraw)
- [wallet/exchangetransaction](#walletexchangetransaction)
- [wallet/getexchangebyid](#walletgetexchangebyid)
- [wallet/listexchanges](#walletlistexchanges)
- [wallet/getpaginatedexchangelist](#walletgetpaginatedexchangelist)
- [wallet/marketsellasset](#walletmarketsellasset)
- [wallet/marketcancelorder](#walletmarketcancelorder)
- [wallet/getmarketorderbyaccount](#walletgetmarketorderbyaccount)
- [wallet/getmarketpairlist](#walletgetmarketpairlist)
- [wallet/getmarketorderlistbypair](#walletgetmarketorderlistbypair)
- [wallet/getmarketpricebypair](#walletgetmarketpricebypair)
- [wallet/getmarketorderbyid](#walletgetmarketorderbyid)


#### wallet/exchangecreate
Description: Create an exchange pair
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/exchangecreate -d
'{
    "owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9",
    "first_token_id": "token_a",
    "first_token_balance": 100,
    "second_token_id": "token_b",
    "second_token_balance": 200
}'
```

Parameters:

- `owner_address`: address
- `first_token_id`: The first token's id, default hexString
- `first_token_balance`: The first token's balance
- `second_token_id`: The second token's id, default hexString
- `second_token_balance`: The second token's balance
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'first_token_balance' and 'second_token_balance' is the smallest unit of the token


#### wallet/exchangeinject
Description: Inject funds for exchange pair
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/exchangeinject -d
'{
    "owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9",
    "exchange_id": 1,
    "token_id": "74726f6e6e616d65",
    "quant": 100
}'
```

Parameters:

- `owner_address`: Owner address of the exchange pair, default hexString
- `exchange_id`: Exchange pair id
- `token_id`: Token id, default hexString
- `quant`: Token inject amount
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'quant' is the smallest unit of the token

#### wallet/exchangewithdraw
Description: Withdraw from exchange pair
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/exchangewithdraw -d
'{
    "owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9",
    "exchange_id": 1,
    "token_id": "74726f6e6e616d65",
    "quant": 100
}'
```

Parameters:

- `owner_address`: Owner address of the exchange pair, default hexString
- `exchange_id`: Exchange pair id
- `token_id`: Token id, default hexString
- `quant`: Token withdraw amount
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'quant' is the smallest unit of the token

#### wallet/exchangetransaction
Description: Participate the transaction of exchange pair
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/exchangetransaction -d
'{
    "owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9",
    "exchange_id": 1,
    "token_id": "74726f6e6e616d65",
    "quant": 100,
    "expected": 10
}'
```

Parameters:

- `owner_address`: Owner address of the exchange pair, default hexString
- `exchange_id`: Exchange pair id
- `token_id`: Token id, default hexString
- `quant`: Sell token amount
- `expected`: Expected token amount to get
- `permission_id`: Optional, for multi-signature use

Return: Transaction object

Note: The unit of 'quant' and 'expected' is the smallest unit of the token

#### wallet/getexchangebyid
Description: Query an exchange pair by exchange pair id
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getexchangebyid -d
'{
    "id": 1
}'
```

Parameter id: Exchange pair id

Return: Exchange pair information

#### wallet/listexchanges
Description: Query the list of all the exchange pairs
```console
$ curl -X GET  http://127.0.0.1:8090/wallet/listexchanges
```

Parameter: No parameter

Return: The list of all the exchange pairs

#### wallet/getpaginatedexchangelist
Description: Query the list of all the exchange pairs by pagination
```console
$ curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedexchangelist -d
'{
    "offset": 0,
    "limit": 10
}'
```

Parameters:

- `offset`:  The index of the start exchange pair
- `limit`: The amount of exchange pairs per page

Return: The list of exchange pairs by pagination

#### wallet/marketsellasset
Description：Create an market order 

```
curl -X POST  http://127.0.0.1:8090/wallet/marketsellasset -d 
'{
    "owner_address": "4184894b42f66dce8cb84aec2ed11604c991351ac8",
    "sell_token_id": "5f",
    "sell_token_quantity": 100,
    "buy_token_id": "31303030303031",
    "buy_token_quantity": 200 
}'  
```
Parameters：

- `owner_address`：owner address, default hexString 
- `sell_token_id`：sell token id, default hexString     
- `sell_token_quantity`：sell token quantity           
- `buy_token_id`：buy token id, default hexString         
- `buy_token_quantity`：buy token quantity (min to receive)     


Return：Transaction object   


#### wallet/marketcancelorder
Description：Cancel the order

```
curl -X POST  http://127.0.0.1:8090/wallet/marketcancelorder -d 
'{
    "owner_address": "4184894b42f66dce8cb84aec2ed11604c991351ac8",
    "order_id": "0a7af584a53b612bcff1d0fc86feab05f69bc4528f26a4433bb344d453bd6eeb"
}' 
```  
Parameters：

- `owner_address`：owner address, default hexString 
- `order_id`：order id        

Return：Transaction object   

#### wallet/getmarketorderbyaccount
Description：Get all orders for the account

```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderbyaccount -d 
'{
    "value": "4184894b42f66dce8cb84aec2ed11604c991351ac8" 
}' 
```  
Parameters：`value` - owner address, default hexString     

Return：order list   

#### wallet/getmarketpairlist
Description：Get all trading pairs
```
curl -X get  http://127.0.0.1:8090/wallet/getmarketpairlist
```
Parameters: 
N/A

Return: makket pair list

#### wallet/getmarketorderlistbypair
Description：Get all orders for the trading pair
demo: 
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderlistbypair -d 
'{
    "sell_token_id": "5f" ,
    "buy_token_id": "31303030303031"
}' 
```  
Parameters：

- `sell_token_id`：sell token id, default hexString          
- `buy_token_id`：buy token id, default hexString         

Return：order list

#### wallet/getmarketpricebypair
Description：Get all prices for the trading pair

```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketpricebypair -d 
'{
    "sell_token_id": "5f" 
    "buy_token_id": "31303030303031" 
}' 
```  
Parameters：

- `sell_token_id`：sell token id, default hexString        
- `buy_token_id`：buy token id, default hexString      
Return：price list


#### wallet/getmarketorderbyid
Description：Get all orders for the account

```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderbyid -d 
'{
    "value": "orderid" 
}' 
```  
Parameters：`value` - order id, default hexString     

Return：order  


### Pending Pool
The following are Pending Pool related APIs:

- [wallet/gettransactionfrompending](#walletgettransactionfrompending)
- [wallet/gettransactionlistfrompending](#walletgettransactionlistfrompending)
- [wallet/getpendingsize](#walletgetpendingsize)

#### wallet/gettransactionfrompending
Get transaction details from the pending pool
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactionfrompending -d
'{
  "value": "txId"
}'
```
Parameters: value: transaction id

Return: Transaction details

#### wallet/gettransactionlistfrompending
Get transaction list information from pending pool
```
curl -X get  http://127.0.0.1:8090/wallet/gettransactionlistfrompending
```
Parameters: N/A

Return: Pending transaction IDs in the pool

#### wallet/getpendingsize
Get the size of the pending pool queue
```
curl -X get  http://127.0.0.1:8090/wallet/getpendingsize
```
Parameters: N/A

Return:pending pool size




## FullNode Solidity HTTP API


### Account Resources

#### walletsolidity/getaccount
Description: Query an account information
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getaccount -d '{"address": "41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
Parameters: `address` - Account to query, default hexString

Return: Account object

#### walletsolidity/getdelegatedresource
Description: Query the energy delegation information
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getdelegatedresource -d '
{
"fromAddress": "419844f7600e018fd0d710e2145351d607b3316ce9",
"toAddress": "41c6600433381c731f22fc2b9f864b14fe518b322f"
}'
```
Parameters: 

- `fromAddress`:  Energy from address, default hexString
- `toAddress`: Energy to address, default hexString

Return: Energy delegation information list, the elements of the list is DelegatedResource

#### walletsolidity/getdelegatedresourceaccountindex
Description: Query the energy delegation index by an account
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getdelegatedresourceaccountindex -d '
{
"value": "419844f7600e018fd0d710e2145351d607b3316ce9",
}'
```
Parameters: 

- `value`: Address, default hexString

Return: DelegatedResourceAccountIndex of the address

#### walletsolidity/getaccountbyid
Description: Query an account information by account id
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getaccountbyid -d '{"account_id":"6161616162626262"}'
```
Parameters: `account_id` - Account id, default hexString

Return: Account object

#### walletsolidity/getavailableunfreezecount

Description:Remaining times of executing unstake operation in Stake2.0
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getavailableunfreezecount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters: 

- `owner_address`: Account address

Return:Remaining times of available unstaking.

#### walletsolidity/getcanwithdrawunfreezeamount

Description: Query the withdrawable balance at the specified timestamp In Stake2.0
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getcanwithdrawunfreezeamount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "timestamp": 1667977444000,
  "visible": true
}
'
```

Parameters: 

- `owner_address`: Account address
- `timestamp`: query cutoff timestamp, in milliseconds.

Return: Withdrawable balance, unit is sun.

#### walletsolidity/getcandelegatedmaxsize
Description: In Stake2.0, query the amount of delegatable resources share of the specified resource type for an address, unit is sun.
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getcandelegatedmaxsize -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "type": 0,
  "visible": true
}
'
```

Parameters: 

- `owner_address`: Account address
- `type`: Resource type, 0 is bandwidth, 1 is energy

Return: The amount of delegatable resource share, unit is sun.

#### walletsolidity/getdelegatedresourcev2
In Stake2.0, query the detail of resource share delegated from `fromAddress` to `toAddress`
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getdelegatedresourcev2 -d
'{
  "fromAddress": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "toAddress": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
  "visible": true
}
'
```

Parameters: 

- `fromAddress`: resource from address, default hexString
- `toAddress`: resource to address

Return: Resource delegation list


#### walletsolidity/getdelegatedresourceaccountindexv2
In Stake2.0, query the resource delegation index by an account. Two lists will return, one is the list of addresses the account has delegated its resources(`toAddress`), and the other is the list of addresses that have delegated resources to the account(`fromAddress`).
```
curl -X POST http://127.0.0.1:8090/walletsolidity/getdelegatedresourceaccountindexv2 -d
'{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters: 

- `value`: account address

Return: Two lists will return, one is the list of addresses the account has delegated its resources(`toAddress`), and the other is the list of addresses that have delegated resources to the account(`fromAddress`).


### Voting & SRs

#### walletsolidity/listwitnesses
Description: Query the list of super representatives
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/listwitnesses
```
Parameters: N/A

Return: List of all super representatives

### TRC10 Token

#### walletsolidity/getassetissuelist
Description: Query the list of all tokens
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuelist
```
Parameters: N/A

Return: The list of all tokens

#### walletsolidity/getpaginatedassetissuelist
Description: Query the list of all the tokens by pagination
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getpaginatedassetissuelist -d '{"offset": 0, "limit":10}'
```
Parameters: 
- `offset`: The index of the start token
- `limit`: The amount of tokens per page

Return: List of tokens

#### walletsolidity/getassetissuebyname
Description: Query a token by token name
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuebyname -d '{"value": "44756354616E"}'
```
Parameters: `value` - Token name, default hexString

Return: Token object
Note: Since Odyssey-v3.2, `getassetissuebyid` or `getassetissuelistbyname` is recommended, as since v3.2, token name can be repeatable. If the token name you query is not unique, this api will throw out an error.

#### walletsolidity/getassetissuelistbyname
Description: Query the token list by name
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuelistbyname -d '{"value": "44756354616E"}'
```
Parameters: `value` - Token name, default hexString

Return: Token list

#### walletsolidity/getassetissuebyid
Description: Query a token by token id
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuebyid -d '{"value": "1000001"}'
```
Parameters: `value` - Token id

Return: Token object


### Blocks

#### walletsolidity/getnowblock
Description: Query the latest block information
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getnowblock
```
Parameters: N/A

Return: The latest block from solidityNode

#### walletsolidity/getblockbynum
Description: Query a block information by block height
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbynum -d '{"num" : 100}'
```
Parameters: `num` - Block height

Return: Block information

#### walletsolidity/getblockbyid
Description: Query a block information by block id
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbyid-d '{"value":
"0000000000038809c59ee8409a3b6c051e369ef1096603c7ee723c16e2376c73"}'
```
Parameters: `value` -  Block id

Return: The block object

#### walletsolidity/getblockbylimitnext
Description: Query a list of blocks by range
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbylimitnext -d '{"startNum": 1, "endNum": 2}'
```
Parameters: 

- `startNum`: The start block height, inclusive
- `endNum`: The end block height, exclusive

Return: List of blocks

#### walletsolidity/getblockbylatestnum
Description: Query the latest few blocks
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbylatestnum -d '{"num": 5}'
```
Parameters: `num` - The number of blocks expected to return

Return: List of blocks

#### wallet/getnodeinfo
Description: Query the current node information
```
curl -X GET http://127.0.0.1:8091/wallet/getnodeinfo
```
Parameters: N/A

Return: NodeInfo of the current node



### Transactions

#### walletsolidity/gettransactionbyid
Description: Query an transaction information by transaction id
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactionbyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
Parameters: `value` - Transaction id

Return: Transaction information

#### walletsolidity/gettransactioncountbyblocknum
Description: Query th the number of transactions in a specific block
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioncountbyblocknum -d '{"num" : 100}'
```
Parameters: `num` - Block height

Return: The number of transactions

#### walletsolidity/gettransactioninfobyid
Description: Query the transaction fee, block height by transaction id
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioninfobyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
Parameters: `value` - Transaction id

Return: Transaction fee, block height and the time of creation

#### walletsolidity/gettransactioninfobyblocknum
Description: Query the list of transaction information in a specific block
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioninfobyblocknum -d '{"num" : 100}'
```
Parameters: `num` - Block height

Return: The list of transaction information inside the queried block


### DEX Exchanges

#### walletsolidity/getexchangebyid
Description: Query an exchange pair by exchange pair id
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getexchangebyid -d {"id":1}
```
Parameters: 

- id: Exchange pair id

Return: Exchange pair information

#### walletsolidity/listexchanges
Description: Query the list of all the exchange pairs
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/listexchanges
```
Parameters: N/A

Return: The list of all the exchange pairs

