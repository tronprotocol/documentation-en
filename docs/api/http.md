# HTTP API
This article introduces FullNode's HTTP APIs and their usage.

!!! Note
    Although TRON has avoided XSS by setting the Content-Type of HTTP APIs to application/json, there are a few APIs that don't have input validation. To better protect user data security, we recommend that you correctly encode any data from APIs before using it in any UI, especially when the parameter visible equals true.
    
    Here is a typical XSS protection method: Encode all data from the APIs in HTML. Use methods such as `encodeURIComponent()` or `escape()` to encode the data, which can convert special characters into their HTML entities and prevent them from being interpreted as HTML code by the browser.
    
    Please ensure that XSS protection is implemented for all data from the APIs to maintain the security of user data. We understand that you may need more information about XSS protection. It is recommended that you refer to the following resources: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

The TRON node's HTTP API supports two address formats. Developers can use the visible parameter to control the address format in both requests and responses.

The rules for the visible parameter are as follows:

* `"visible": false (default)`： Addresses in parameters and return values must be in HexString format. If this parameter is omitted, the default value is used.
* `"visible": true`：Addresses in parameters and return values must be in Base58Check format.

**How to Set:**：

1. For GET requests or queries without parameters
Append `visible=true` as a URL query parameter.
```
http://127.0.0.1:8090/wallet/listexchanges?visible=true
```

2. For POST requests
Add `"visible": true` to the JSON request body.
```
curl -X POST http://127.0.0.1:8090/wallet/createtransaction -d
'{
    "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
    "amount": 1000000,
    "visible": true
}'
```

## Fullnode HTTP API

The Fullnode HTTP API is categorized as follows:

- [Accounts](#account)
- [Transfers and Transactions](#txn)
- [Account Resources](#resources)
- [Query the Network](#network)
- [Smart Contracts](#contract)
- [TRC-10 Token](#trc10)
- [Voting & SRs](#sr)
- [Proposals](#tip)
- [DEX Exchange](#dex)
- [Pending Pool](#pending-pool)



<a id="account"></a>
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
Description: Validates if a TRON address is effective. This is useful for pre-checking user-inputted addresses in applications before sending a transaction.

```
curl -X POST  http://127.0.0.1:8090/wallet/validateaddress -d '{"address": "4189139CB1387AF85E3D24E212A008AC974967E561"}'
```

Parameters: 
* `address`:can be in Base58Checksum, hexString, or base64 format.

Return Value: Indicates whether the address is valid or invalid. Example:
```
# Success Example
{
    "result": true,
    "message": "Hex string format"
}

# Error Example
{
    "result": false,
    "message": "Invalid address"
}
```


#### wallet/createaccount
Description: Activates an account. If the creator's account has enough Bandwidth from staking TRX, this only consumes Bandwidth. Otherwise, it burns 0.1 TRX for Bandwidth and an additional 1 TRX as an account creation fee.
```
curl -X POST  http://127.0.0.1:8090/wallet/createaccount -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "account_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0"}'
```
Parameters:

* `owner_address`: The creator's address, which must be an activated account.
* `account_address`: The new account address to be activated, which must be generated offline beforehand.
* `Permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* * `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.


Return Value: An unsigned transaction for activating the account.



#### wallet/getaccount
Description: Queries and returns the complete on-chain information for a specified TRON account, including balance, resources, permissions, and assets.
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccount -d '{"address": "41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
参数：
* `address`: The account address to query.
* * `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: An Account object.

#### wallet/updateaccount
Description: Updates or sets the on-chain name (`account_name`) for a specified TRON account.
```
curl -X POST  http://127.0.0.1:8090/wallet/updateaccount -d '{"account_name": "0x7570646174654e616d6531353330383933343635353139" ,"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"}'
```
参数：

* `account_name`: The account name, in hexString format by default.
* `owner_address`: The address of the account to be updated, in hexString format by default.
* `Permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* * `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: An unsigned transaction for updating the account name.

#### wallet/accountpermissionupdate
Description: Modifies the permission structure of an account.
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

* `owner_address`: The address of the account creating the contract, in hexString format by default.
* `owner`: The permission details for the account's owner.
* `witness`: The permission details for block production. Not required if the account is not a witness.
* `actives`: The permission details for other functionalities.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: An unsigned transaction.

#### wallet/getaccountbalance
Description: Queries the TRX balance of a TRON account at a specific historical block height.
The following official nodes currently support this query:

* 13.228.119.63
* 18.139.193.235
* 18.141.79.38
* 18.139.248.26

A local node must have `storage.balance.history.lookup=true` enabled in its configuration file.
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

* `account_identifier.address`: The account address to query.
* `block_identifier.hash`: The hash of the target block.
* `block_identifier.number`: The height (block number) of the target block.
* `visible `(optional): Sets the address format. true for Base58Check, false (or omitted) for HexString.


Return Value Example:
```
{
    "balance": 64086449348265042,
    "block_identifier": {
        "hash": "0000000000010c4a732d1e215e87466271e425c86945783c3d3f122bfa5affd9",
        "number": 68682
    }
}
```

#### wallet/setaccountid
Description: Sets or updates a custom Account ID (`account_id`) for a specified TRON account.
```
curl -X POST  http://127.0.0.1:8090/wallet/setaccountid -d '{
"owner_address":"41a7d8a35b260395c14aa456297662092ba3b76fc0","account_id":"6161616162626262"}'
```
Parameters:

* `owner_address`: The address of the transaction creator, in hexString format by default.
* `account_id`: The account ID, in hexString format by default.
* * `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.


Return Value: An unsigned transaction for set the Account ID.

#### wallet/getaccountbyid
Description: Queries account information by its `account_id`.
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountbyid -d
'{"account_id":"6161616162626262"}'
```
Parameter: `account_id` in hexString format by default.

Return Value: An Account object.


<a id="txn"></a>
### Transfers and transactions

The following are transfer and transaction related APIs:

- [wallet/createtransaction](#walletcreatetransaction)
- [wallet/broadcasttransaction](#walletbroadcasttransaction)
- [wallet/broadcasthex](#walletbroadcasthex)
- [wallet/getsignweight](#walletgetsignweight)
- [wallet/getapprovedlist](#walletgetapprovedlist)

#### wallet/createtransaction
Description: Creates a TRX transfer transaction. If the to_address does not exist, this transaction will also create the account on the blockchain
```
curl -X POST  http://127.0.0.1:8090/wallet/createtransaction -d '{"to_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d", "owner_address": "41D1E7A6BC354106CB410E65FF8B181C600FF14292", "amount": 1000 }'
```

Parameters:

* `to_address`: The recipient's address.
* `owner_address`: The sender's address.
* `amount`: The transfer amount, in sun (1 TRX = 1,000,000 sun).
* `Permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: An unsigned TRX transfer transaction.

#### wallet/broadcasttransaction
Description: Broadcasts a signed transaction to the TRON network.
```
curl -X POST  http://127.0.0.1:8090/wallet/broadcasttransaction -d '{"signature":["97c825b41c77de2a8bd65b3df55cd4c0df59c307c0187e42321dcc1cc455ddba583dd9502e17cfec5945b34cad0511985a6165999092a6dec84c2bdd97e649fc01"],"txID":"454f156bf1256587ff6ccdbc56e64ad0c51e4f8efea5490dcbc720ee606bc7b8","raw_data":{"contract":[{"parameter":{"value":{"amount":1000,"owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0","to_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"267e","ref_block_hash":"9a447d222e8de9f2","expiration":1530893064000,"timestamp":1530893006233}}'
```
Parameter:

* A complete signed transaction object. This is created by adding a signature field to the unsigned transaction returned by a creation API (e.g., wallet/createtransaction).

Return Value:
* A JSON object with the broadcast result.
* A successful response typically includes `"result": true`, indicating the node has received the transaction and started broadcasting it.

**Important Note**: `"result": true` does not mean the transaction has been confirmed on the blockchain. It only means `"successfully broadcast."` You must use the txID with the `wallet/gettransactioninfobyid` or `wallet/gettransactionbyid` endpoints to check the final on-chain status.

#### wallet/broadcasthex
Description: Broadcasts a transaction that has been signed and serialized into a hexadecimal string.
```
curl -X POST  http://127.0.0.1:8090/wallet/broadcasthex -d '{"transaction":"0A8A010A0202DB2208C89D4811359A28004098A4E0A6B52D5A730802126F0A32747970652E676F6F676C65617069732E636F6D2F70726F746F636F6C2E5472616E736665724173736574436F6E747261637412390A07313030303030311215415A523B449890854C8FC460AB602DF9F31FE4293F1A15416B0580DA195542DDABE288FEC436C7D5AF769D24206412418BF3F2E492ED443607910EA9EF0A7EF79728DAAAAC0EE2BA6CB87DA38366DF9AC4ADE54B2912C1DEB0EE6666B86A07A6C7DF68F1F9DA171EEE6A370B3CA9CBBB00"}'
```
Parameters:

* `transaction`: A complete transaction, including all data and signatures, serialized into a single hex string.

Return Value:

* A JSON object with the broadcast result.
* A successful response typically includes `"result": true`, indicating the node has received the transaction and started broadcasting it.

**Important Note**: `"result": true` does not mean the transaction has been confirmed on the blockchain. It only means `"successfully broadcast."` You must use the txID with the `wallet/gettransactioninfobyid` or `wallet/gettransactionbyid` endpoints to check the final on-chain status.


#### wallet/getsignweight
Description: Checks the current signature status of a transaction requiring Account Management Permission. This is a key pre-broadcast check in the workflow for an Account Management Permission to see if the collected signature weight has met the required threshold.

In a scenario involving an Account Management Permission, a transaction may require multiple private key signatures. This API is used to check whether the currently collected signature weight has reached the set threshold before all signatures are collected. It is a key pre-broadcast check tool in the signing process for an Account Management Permission.

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
Parameter:

* A complete transaction object that includes o`ne or more signatures`.

Return Value: 

* A JSON object detailing the signature status, including whether the weight threshold has been met, a list of signing addresses, permission details, the current signed weight, and the transaction itself.


#### wallet/getapprovedlist
Description: In the workflow of an Account Management Permission, this queries and returns the list of addresses that have already signed a transaction. It is similar to wallet/getsignweight but focuses on tracking progress.

This interface is similar to wallet/getsignweight, but its main Description is to quickly obtain a list of parties that have provided valid signatures to track the progress for an Account Management Permission.

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
Parameters:
* A complete transaction object with one or more signatures.

Return Value: 
* A JSON object containing the list of approved addresses and the overall signature status of the transaction.

<a id="resources"></a>
### Resources
The following are the APIs related to on-chain resources:

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
Description: Queries the resource overview for a specified TRON account, including Bandwidth, Energy, TRON Power, and related staking information.
```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountresource -d {"address" : "419844f7600e018fd0d710e2145351d607b3316ce9"}
```
Parameters:

* address: The account address to query.
* visible (optional): Sets the address format.

Return Value: 
* A JSON object containing all resource-related information for the account.

#### wallet/getaccountnet
Description: Queries the Bandwidth resource details for a specified TRON account.

```
curl -X POST  http://127.0.0.1:8090/wallet/getaccountnet -d '{"address": "4112E621D5577311998708F4D7B9F71F86DAE138B5"}'
```
Parameters:

* `address`: The account address to query.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value:

* A JSON object containing all Bandwidth-related information for the account.

#### wallet/freezebalance
Description: [Deprecated] This API is from the TRON Stake 1.0 era and has been officially deprecated. Please use `freezebalancev2` for all new staking operations.


#### wallet/unfreezebalance
Description: Unstakes TRX that was staked during the Stake 1.0 phase and has completed its freezing period. This will also cause the loss of the Bandwidth and TRON Power associated with this stake.
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezebalance -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"resource": "BANDWIDTH",
"receiver_address":"414332f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```
Parameters:

* `owner_address`: The address of the account unstaking TRX.
* `resource`: Can be Bandwidth or Energy.
* `receiverAddress`: The address of the delegated account.
* `Permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.


Return Value:
* An unsigned unstaking transaction object.


#### wallet/getdelegatedresource
Description: In Stake 1.0, queries the resources (Energy or Bandwidth) delegated from one account to another.
```
curl -X POST  http://127.0.0.1:8090/wallet/getdelegatedresource -d '
{
"fromAddress": "419844f7600e018fd0d710e2145351d607b3316ce9",
"toAddress": "41c6600433381c731f22fc2b9f864b14fe518b322f"
}'
```
Parameters:
* `fromAddress`: The address of the delegating account.
* `toAddress`: The address of the recipient account.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: 
* A list of `DelegatedResource` objects.

#### wallet/getdelegatedresourceaccountindex
Description: In Stake 1.0, queries the list of accounts that have delegated resources to or received resources from a specified account.
```
curl -X POST  http://127.0.0.1:8090/wallet/getdelegatedresourceaccountindex -d '
{
"value": "419844f7600e018fd0d710e2145351d607b3316ce9",
}'
```
Parameters:

- `value`: The account address to query.
- `visible` (optional): Sets the address format. true for Base58Check, false (or omitted) for HexString.

Return Value: 
* A `DelegatedResourceAccountIndex` object showing the account's delegation overview.

#### wallet/freezebalancev2
Description: Stakes TRX under the **Stake 2.0** mechanism. This operation allows the staker to obtain a specified network resource (Energy or Bandwidth) and will **simultaneously** grant an equivalent amount of **TRON Power (TP)** at a 1:1 ratio with the staked TRX.
```
curl -X POST http://127.0.0.1:8090/wallet/freezebalancev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "frozen_balance": 10000,
    "resource": "BANDWIDTH"
}'
```

Parameters:

- `owner_address`: The address of the account staking TRX.
- `frozen_balance`: The amount of TRX to stake, in sun.
- `resource`: The type of resource to obtain, can be `BANDWIDTH` or `ENERGY`.
- `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
- `visible` (optional): Sets the address format. true for Base58Check, false (or omitted) for HexString.


Return Value: 
* An unsigned staking transaction object.

#### wallet/unfreezebalancev2

Description: Unstakes TRX staked via the Stake 2.0 mechanism. This releases the corresponding amount of Bandwidth or Energy and reclaims the equivalent amount of TRON Power (TP).
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezebalancev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
    "unfreeze_balance": 1000000,
    "resource": "BANDWIDTH"
}'
```

Parameters:

* `owner_address`: The address of the account unstaking TRX.
* `resource`: The type of resource being unstaked, BANDWIDTH or ENERGY.
* `unfreeze_balance`: The amount of TRX to unstake, in sun.
* `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: 

* An unsigned unstaking transaction object.


#### wallet/cancelallunfreezev2

Description: Immediately cancels all pending (not yet unlocked) unfreeze requests for an account. This has a dual effect:

* Restakes: All TRX from the canceled unfreezing requests are immediately restaked for the same resource type.
* Withdraws: Any TRX from unfreeze requests that have already completed their 14-day pending period is automatically withdrawn to the account's balance.

```
curl -X POST http://127.0.0.1:8090/wallet/cancelallunfreezev2 -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1"
}'
```

Parameters:

- `owner_address`: The account address.
- `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
- `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: 

* An unsigned cancel unfreeze transaction object.

#### wallet/delegateresource

Description: Delegates `Energy` or `Bandwidth` obtained from staking TRX to another TRON account. TRON Power (TP) cannot be delegated.

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

* `owner_address`: The address of the transaction initiator.
* `receiver_address`: The recipient account address.
* `balance`: The amount of TRX whose corresponding resource share will be delegated, in sun.
* `resource`: The type of resource to delegate, `BANDWIDTH` or `ENERGY`.
* `lock`: true sets a 3-day lock on the delegation, during which it cannot be canceled. If resources are delegated again to the same address during the lock period, the 3-day timer resets. false means no lock period.
* `lock_period`: A custom lock period in units of blocks (1 block ≈ 3s). Only effective when lock is true. For a 1-day lock, lock_period would be 28800.
* `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value:
* An unsigned delegate resource transaction object.

#### wallet/undelegateresource

Description: Cancels (reclaims) previously delegated Energy or Bandwidth from another account.

Important Note: If a resource delegation was made with a time lock (lock: true) that has not yet expired, this call will fail. You must wait for the lock period to end.

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

* `owner_address`: The address of the transaction initiator.
* `receiver_address`: The recipient account from which resources are being reclaimed.
* `balance`: The amount of TRX whose corresponding resource share will be undelegated, in sun.
* `resource`: The type of resource to undelegate, `BANDWIDTH` or `ENERGY`.
* `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: 
* An unsigned undelegate resource transaction object.

#### wallet/withdrawexpireunfreeze

Description: Withdraws all unstaked TRX that have completed their lock period.
```
curl -X POST http://127.0.0.1:8090/wallet/withdrawexpireunfreeze -d
'{
    "owner_address": "41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```

Parameters:
* `owner_address`: The address of the transaction initiator.
* `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: An unsigned withdraw expired unfreeze transaction object.

#### wallet/getavailableunfreezecount

Description: Queries the remaining number of unstake operations an account can initiate. The TRON network limits each account to a maximum of 32 concurrent unstaking operations within the 14-day lock period. This API can be used to pre-check whether there is an available "unstaking quota" before calling `unfreezebalancev2`.

```
curl -X POST http://127.0.0.1:8090/wallet/getavailableunfreezecount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters:

* `owner_address`: The account address to query.
* `visible` (optional): Sets the address format.

Return Value: A JSON object containing the remaining count.

#### wallet/getcanwithdrawunfreezeamount

Description: Queries the total amount of unstaked principal that can be withdrawn at a specific point in time.
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

* `owner_address`: The address of the transaction initiator.
* `timestamp`: The timestamp (in milliseconds) at which to query the withdrawable amount.
* `visible `(optional): Sets the address format.

Return Value: A JSON object containing the withdrawable amount.


#### wallet/getcandelegatedmaxsize

Description: Queries the maximum amount of a specified resource type that a target address can delegate, in sun.
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

- `owner_address`: The account address to query.
- `type`: The resource type, `0` for Bandwidth, `1` for Energy.
- `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: A JSON object containing the maximum delegatable share.

#### wallet/getdelegatedresourcev2

Description: Queries the resource details delegated from one address to a target address under the Stake 2.0 mechanism.
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

* `fromAddress`: The delegating account address.
* `toAddress`: The recipient account address.
* `visible` (optional): Sets the address format.

Return Value: An array of delegatedResource objects, containing all delegation records between the two addresses under Stake 2.0.



#### wallet/getdelegatedresourceaccountindexv2
Description: Queries the resource delegation index for an address under the Stake 2.0 mechanism. It returns two lists: one of addresses to which the account has delegated resources (toAccounts), and one of addresses that have delegated resources to this account (fromAccounts).
```
curl -X POST http://127.0.0.1:8090/wallet/getdelegatedresourceaccountindexv2 -d
'{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters:

* `value`: The account address.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: This interface returns a JSON object containing a list of bidirectional proxy relationships. It contains two lists: one for the addresses to which the account delegates resources (toAddress), and one for the addresses that delegate resources to the account (fromAddress).


<a id="network"></a>
### Query the Network
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
- [wallet/getmemofee](#walletgetmemofee)
- [wallet/getburntrx](#walletgetburntrx)

#### wallet/getnowblock
Description: Query the latest block.
```
curl -X POST  http://127.0.0.1:8090/wallet/getnowblock
```
Parameter: None

Return Value: The latest Block object.

#### wallet/getblock
Description: Query block information based on block height or block hash.
```
curl -X POST  http://127.0.0.1:8090/wallet/getblock -d '{"detail":false}'
```
Parameters:

* `id_or_num`: Block height or block hash. If not set, queries the latest block.
* `detail`: Defaults to false, meaning only the block header information is queried. If `true`, the entire block is queried.

Return Value: A Block object or an object containing only block header information.

#### wallet/getblockbynum
Description: Query complete block information by a specified block height.
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbynum -d '{"num": 1}'
```
Parameter: `num`: Block height (integer).

Return Value: The Block object at the specified height.

#### wallet/getblockbyid
Description: Query complete block information by a specified Block ID (hash).
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbyid -d '{"value": "0000000000038809c59ee8409a3b6c051e369ef1096603c7ee723c16e2376c73"}'
```
Parameter: `value`: The Block ID (hash).

Return Value: The Block object with the specified ID.

#### wallet/getblockbylatestnum
Description: Query the latest N blocks in descending order.
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbylatestnum -d '{"num": 5}'
```
Parameter: `num`: The number of blocks to query.

Return Value: An array containing multiple Block objects (Block[]).

#### wallet/getblockbylimitnext
Description: Paginate and query a list of blocks within a specified height range.
code

```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbylimitnext -d '{"startNum": 1, "endNum": 2}'
```
Parameters:

* `startNum`: Starting block height (inclusive).
* `endNum`: Ending block height (exclusive).

Return Value: An array containing multiple Block objects (Block[]).


#### wallet/getblockbalance
Description: Get the details of TRX balance changes caused by all transactions in a specified block.
```
curl -X POST  http://127.0.0.1:8090/wallet/getblockbalance -d
'{
    "hash": "000000000000dc2a3731e28a75b49ac1379bcc425afc95f6ab3916689fbb0189",
    "number": 56362,
    "visible": true
}'
```
Parameters:

* `hash`: The hash value of the block.
* `number`: The height of the block. Must exactly match the block hash.
* `visible`: Whether to display addresses in Base58Check format (`true`) or HexString format (`false` or omitted).

Return Value: An object containing all balance change tracing information for the block, for example:
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
Description: Query the complete information of an on-chain transaction by its Transaction ID (hash).
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactionbyid -d '{"value": "d5ec749ecc2a615399d8a6c864ea4c74ff9f523c2be0e341ac9be5d47d7c2d62"}'
```
Parameter: `value`: Transaction ID (hash).

Return Value: The complete Transaction object. Returns an empty object if the transaction does not exist.

#### wallet/gettransactioninfobyid
Description: Query the summary information of a transaction, such as fees and block location, based on its Transaction ID (hash).
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioninfobyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
Parameter: `value`: Transaction ID (hash).

Return Value: A TransactionInfo object containing transaction fees, block height, block timestamp, contract execution results, etc.

#### wallet/gettransactioncountbyblocknum
Description: Query the total number of transactions contained in a specified block height.
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioncountbyblocknum -d '{"num" : 100}'
```
Parameter: `num`: Block height.

Return Value: An object containing the transaction count, such as {"count": 50}.

#### wallet/gettransactioninfobyblocknum
Description: Get a list of summary information for all transactions at a specified block height.
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactioninfobyblocknum -d '{"num" : 100}'
```
Parameter: `num`: Block height.

Return Value: A list containing multiple `TransactionInfo` objects.

#### wallet/listnodes
Description: Query other nodes discovered by the current node's node discovery feature.
```
curl -X POST  http://127.0.0.1:8090/wallet/listnodes
```
Parameter: None

Return Value: An array containing information for multiple nodes, each including an IP address and port.

#### wallet/getnodeinfo
Description: View the current node's own operating status and information.
```
curl  http://127.0.0.1:8090/wallet/getnodeinfo
```
Return Value: An object containing information such as node version, network status, block synchronization status, etc.

#### wallet/getchainparameters
Description: Query all dynamic parameters of the current TRON network.
```
curl -X POST  http://127.0.0.1:8090/wallet/getchainparameters
```
Return Value: A list containing all on-chain parameters and their current values.

#### wallet/getenergyprices
Description: Query the historical record of Energy unit price changes.
```
curl -X POST  http://127.0.0.1:8090/wallet/getenergyprices
```
Return Value: All historical Energy unit price information. Each price change is separated by a comma, with the millisecond timestamp before the colon and the Energy unit price in sun after the colon.

#### wallet/getbandwidthprices
Description: Query the historical record of Bandwidth unit price changes.
```
curl -X POST  http://127.0.0.1:8090/wallet/getbandwidthprices
```
Return Value: All historical Bandwidth unit price information. Each price change is separated by a comma, with the millisecond timestamp before the colon and the Bandwidth unit price in sun after the colon.

#### wallet/getmemofee
Description: Query the historical record of memo price changes.
```
curl -X POST  http://127.0.0.1:8090/wallet/getmemofee
```
Return Value: All historical memo price information. Each price change is separated by a comma, with the millisecond timestamp before the colon and the memo price in sun after the colon.

#### wallet/getburntrx
Description: Query the total amount of TRX burned since the TRON network's genesis.
```
curl -X POST  http://127.0.0.1:8090/wallet/getburntrx
```
Return Value: The amount of TRX burned, in sun.



<a id="contract"></a>
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
Description: Get a contract's static information, such as ABI and bytecode, via its contract address.
```
curl -X POST  http://127.0.0.1:8090/wallet/getcontract -d '{"value":"4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
Parameters:

* `value`: Contract address, defaults to HexString format.
* `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: A SmartContract object, containing ABI, deployment bytecode, name, etc.

#### wallet/getcontractinfo
Description: Get a contract's runtime information via its contract address.
```
curl -X POST  http://127.0.0.1:8090/wallet/getcontractinfo -d '{"value":"4189139CB1387AF85E3D24E212A008AC974967E561"}'
```
Parameters:

* `value`: Contract address, defaults to HexString format.
* `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.
 
Return Value: Queries on-chain contract information. Unlike the `wallet/getcontract` interface, this interface returns not only bytecode but also the contract's runtime bytecode. Runtime bytecode, compared to bytecode, does not include constructor functions and constructor parameter information.


#### wallet/deploycontract
Description: Create a transaction to deploy a smart contract.
```
curl -X POST  http://127.0.0.1:8090/wallet/deploycontract -d '{"abi":"[{\"constant\":false,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"},{\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"set\",\"outputs\":[],\"payable\":false,\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"constant\":true,\"inputs\":[{\"name\":\"key\",\"type\":\"uint256\"}],\"name\":\"get\",\"outputs\":[{\"name\":\"value\",\"type\":\"uint256\"}],\"payable\":false,\"stateMutability\":\"view\",\"type\":\"function\"}]","bytecode":"608060405234801561001057600080fd5b5060de8061001f6000396000f30060806040526004361060485763ffffffff7c01000000000000000000000000000000000000000000000000000000006000350416631ab06ee58114604d5780639507d39a146067575b600080fd5b348015605857600080fd5b506065600435602435608e565b005b348015607257600080fd5b50607c60043560a0565b60408051918252519081900360200190f35b60009182526020829052604090912055565b600090815260208190526040902054905600a165627a7a72305820fdfe832221d60dd582b4526afa20518b98c2e1cb0054653053a844cf265b25040029","parameter":"","call_value":100,"name":"SomeContract","consume_user_resource_percent":30,"fee_limit":10,"origin_energy_limit": 10,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
Parameters:

- `abi`：abi.
- `bytecode`: The bytecode of the contract, must be in HexString format.
- `parameter`: The parameter list for the constructor needs to be ABI encoded and then converted to HexString format. If the constructor has no parameters, this parameter can be omitted.
- `consume_user_resource_percent`: The percentage of resources used by users calling this contract, an integer between. If 0, users will not consume resources. If the developer's resources are exhausted, then user resources will be fully consumed.
- `fee_limit`：Maximum sun to be consumed (1 TRX = 1,000,000 sun).
- `call_value`: The amount of sun (1 TRX = 1,000,000 sun) to transfer to the contract during this call.
- `owner_address`: The account address initiating the `deploycontract`, defaults to HexString format.
name: The contract name.
- `name`: The contract name.
- `origin_energy_limit`: The maximum energy that the creator is willing to consume for themselves during a single contract execution or creation, an integer greater than 0.
- `call_token_value`: The amount of TRC-10 tokens to transfer to the contract during this call. If `token_id` is not set, this should be `0` or not set.
- `token_id`: The ID of the TRC-10 token to transfer to the contract during this call. If none, do not set.
- `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
- `visible`: sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an object containing an unsigned deployment transaction.

#### wallet/triggersmartcontract
Description: Create a transaction to call a smart contract function.
```
curl -X POST  http://127.0.0.1:8090/wallet/triggersmartcontract -d '{"contract_address":"4189139CB1387AF85E3D24E212A008AC974967E561","function_selector":"set(uint256,uint256)","parameter":"00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002","fee_limit":10,"call_value":100,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
Parameters：

- `contract_address`：The address of the callee contract, defaults to HexString format.
- `function_selector`：The function signature, no spaces allowed.
- `parameter`：The virtual machine format of the call parameters. Use the JS tool provided by Remix to convert the contract caller's parameter array into the format required by the virtual machine.
- `data`：Data for interacting with the smart contract, including the called contract function and parameters. You can choose to interact through this field, or through `function_selector` and `parameter`. If `data` and `function_selector` exist simultaneously, `function_selector` will be used for contract interaction.
- `fee_limit`：Maximum sun to be consumed (1 TRX = 1,000,000 sun).
- `call_value`：The amount of sun (1 TRX = 1,000,000 sun) to transfer to the contract during this call.
- `owner_address`：The account address initiating the `triggercontract`, defaults to HexString format.
- `call_token_value`:The amount of TRC-10 tokens to transfer to the contract during this call. If `token_id` is not set, this should be `0` or not set.
- `token_id`:The ID of the TRC-10 token to transfer to the contract during this call. If none, do not set.
- `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
- `visible` :Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an object containing an unsigned deployment transaction.


#### wallet/triggerconstantcontract
Description: Simulate contract execution on the local node for data querying, transaction pre-execution, or energy consumption estimation. This operation is off-chain and does not consume resources.
```
curl -X POST  http://127.0.0.1:8090/wallet/triggerconstantcontract -d '{"contract_address":"4189139CB1387AF85E3D24E212A008AC974967E561","function_selector":"set(uint256,uint256)","parameter":"00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002","call_value":100,"owner_address":"41D1E7A6BC354106CB410E65FF8B181C600FF14292"}'
```
Parameters：

- `contract_address`：The address of the callee contract, defaults to HexString format.
- `function_selector`: The function signature, no spaces allowed.
- `parameter`：The virtual machine format of the call parameters. Use the JS tool provided by Remix to convert the contract caller's parameter array into the format required by the virtual machine.
- `data`：Contract bytecode or data for interacting with the smart contract, including the called contract function and parameters. You can choose to interact through this field or through `function_selector` and parameter. If `data` and `function_selector` exist simultaneously, function_selector will be prioritized.
- `owner_address`：The account address initiating the `triggercontract`, defaults to HexString format.
- `call_value`：The amount of sun (1 TRX = 1,000,000 sun) to transfer to the contract during this call.
- `call_token_value`:The amount of TRC-10 tokens to transfer to the contract during this call. If `token_id` is not set, this should be `0` or not set.
- `token_id`:The ID of the TRC-10 token to transfer to the contract during this call. If none, do not set.
- `visible` Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: The return value of the contract function, encoded in ABI format.



#### wallet/updatesetting
Description: Update the consume_user_resource_percent (user energy consumption ratio) of a deployed contract.
```
curl -X POST  http://127.0.0.1:8090/wallet/updatesetting -d '{"owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9", "contract_address": "41c6600433381c731f22fc2b9f864b14fe518b322f", "consume_user_resource_percent": 7}'
```
Parameters：

- `owner_address`：The owner address of the contract, defaults to HexString format.
- `contract_address`：The address of the contract to be modified, defaults to HexString format.
- `consume_user_resource_percent`：The specified percentage of resources consumed by users calling this contract.
- `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
- `visible`:Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an object containing an unsigned update transaction.

#### wallet/updateenergylimit
Description: Update the origin_energy_limit (developer's maximum energy provided for a single call) of a deployed contract.
```
curl -X POST  http://127.0.0.1:8090/wallet/updateenergylimit -d '{"owner_address": "419844f7600e018fd0d710e2145351d607b3316ce9", "contract_address": "41c6600433381c731f22fc2b9f864b14fe518b322f", "origin_energy_limit": 7}'
```
Parameters：

* `owner_address`: The owner address of the contract, defaults to HexString format.
* `contract_address`: The address of the contract to be modified, defaults to HexString format.
* `origin_energy_limit`: The maximum energy that the creator is willing to consume for themselves during a single contract execution or creation.
* `permission_id` (optional): Used to specify the permission ID when signing with a permission other than the default owner permission.
* `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an object containing an unsigned update transaction.

#### wallet/clearabi
Description: Create a transaction to clear the ABI of a smart contract.
```
curl -X POST  http://127.0.0.1:8090/wallet/clearabi -d '{
"owner_address":"41a7d8a35b260395c14aa456297662092ba3b76fc0",
"contract_address":"417bcb781f4743afaacf9f9528f3ea903b3782339f"}'
```
Parameters：

* `owner_address`: The account address that created the contract, defaults to HexString format.
* `contract_address`: The contract address, defaults to HexString format.
* `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an unsigned transaction object.

#### wallet/estimateenergy
Description: Estimate the energy required for a smart contract call.
```
curl -X POST  http://127.0.0.1:8090/wallet/estimateenergy -d '{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "contract_address": "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
  "function_selector": "transfer(address,uint256)",
  "parameter": "00000000000000000000004115208EF33A926919ED270E2FA61367B2DA3753DA0000000000000000000000000000000000000000000000000000000000000032",
  "visible": true
}'
```

Parameters：

- `contract_address`: The address of the callee contract, defaults to HexString format.
- `function_selector`: The function signature, no spaces allowed.
- `parameter`: The virtual machine format of the call parameters. Use the JS tool provided by Remix to convert the contract caller's parameter array into the format required by the virtual machine.
- `data`: Contract bytecode or data for interacting with the smart contract, including the called contract function and parameters. You can choose to interact through this field, or through `function_selector` and parameter. If `data` and `function_selector` exist simultaneously, `function_selector` will be prioritized.
- `owner_address`: The account address initiating the `triggercontract`, defaults to HexString format.
- `call_value`: The amount of sun (1 TRX = 1,000,000 sun) to transfer to the contract during this call.
- `call_token_value`: The amount of TRC-10 tokens to transfer to the contract during this call. If `token_id` is not set, this should be `0` or not set.
- `token_id`: The ID of the TRC-10 token to transfer to the contract during this call. If none, do not set.
- `visible` Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an object containing the estimated energy value.

<a id="trc10"></a>
### TRC-10 token
The following are TRC-10 token-related APIs:

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
Description: Query all TRC-10 tokens issued by a specified account.
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyaccount -d '{"address": "41F9395ED64A6E1D4ED37CD17C75A1D247223CAF2D"}'
```

Parameters:

* `address`: The issuer account address, defaults to HexString format.
* `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: This interface returns an object containing a list of TRC-10 tokens issued by the address.

#### wallet/getassetissuebyname
Description: Query TRC-10 tokens by name.
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyname -d '{"value": "44756354616E"}'
```
Parameter: `value`：Token name, defaults to HexString format.
 
Return Value: A TRC-10 token object.


Note: Starting from Odyssey-v3.2, it is recommended to use getassetissuebyid or getassetissuelistbyname to replace this interface, because starting from 3.2, tokens are allowed to have the same name. If identical token names exist, this interface will report an error.

#### wallet/getassetissuelistbyname
Description: Query all matching TRC-10 token lists by name.
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuelistbyname -d '{"value": "44756354616E"}'
```
Parameters:
 - `value`：Token name, defaults to HexString format.

Return Value: An array containing all TRC-10 token objects with the same name.

#### wallet/getassetissuebyid
Description: Query TRC-10 token by ID.
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuebyid -d '{"value": "1000001"}'
```
Parameters：
* `value`: The ID of the TRC-10 token.

Return Value: The specified TRC-10 token object.


#### wallet/getassetissuelist
Description: Query a list of all TRC-10 tokens on the entire network.
```
curl -X POST  http://127.0.0.1:8090/wallet/getassetissuelist
```
Parameters: None

Return Value: An array containing objects for all TRC-10 tokens on the network.

#### wallet/getpaginatedassetissuelist
Description:Paginate and query a list of TRC-10 tokens on the entire network.
```
curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedassetissuelist -d '{"offset": 0, "limit": 10}'
```
Parameters:

*  `offset`: The starting index for pagination.
*  `limit`: The desired number of tokens to return in this query.

Return Value: An array containing TRC-10 token objects for the paginated results.


#### wallet/transferasset
Description: Create a TRC-10 token transfer transaction.
```
curl -X POST  http://127.0.0.1:8090/wallet/transferasset -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0", "asset_name": "0x6173736574497373756531353330383934333132313538", "amount": 100}'
```
Parameters:

*   `owner_address`: The sender's address, defaults to HexString format.
*   `to_address`: The recipient's address, defaults to HexString format.
*   `asset_name`: The TRC-10 token ID, defaults to HexString format.
*   `amount`: The amount of tokens to transfer.
*   `permission_id` (optional): Used to specify the permission ID when signing with a permission other than the default owner permission.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned TRC-10 transfer transaction object.


#### wallet/participateassetissue
Description: Create a transaction to participate in a TRC-10 token crowdsale.

```
curl -X POST http://127.0.0.1:8090/wallet/participateassetissue -d '{
"to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"amount":100,
"asset_name":"3230313271756265696a696e67"
}'
```
Parameters:

*   `to_address`: The token issuer's address, defaults to HexString format.
*   `owner_address`: The participant's address (buyer), defaults to HexString format.
*   `amount`: The amount of tokens to participate with.
*   `asset_name`: The ID of the token to participate in, defaults to HexString format.
*   `permission_id` (optional): Used to specify the permission ID when signing with a permission other than the default owner permission.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned participate in crowdsale transaction object.

**Note:** The current `asset_name` is the token name. After the committee passes the `AllowSameTokenName` proposal, `asset_name` will be changed to the String type of the token ID.


#### wallet/createassetissue
Description: Create a transaction to issue TRC-10 tokens (costing 1024 TRX).
```
curl -X POST  http://127.0.0.1:8090/wallet/createassetissue -d '{
"owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
"name":"0x6173736574497373756531353330383934333132313538",
"abbr": "0x6162627231353330383934333132313538",
"total_supply" :4321,
"trx_num":1,
"num":1,
"start_time" : 1530894315158,
"end_time":1533894312158,
"description":"007570646174654e616d6531353330363038383733343633",
"url":"007570646174654e616d6531353330363038383733343633",
"free_asset_net_limit":10000,
"public_free_asset_net_limit":10000,
"frozen_supply":{"frozen_amount":1, "frozen_days":2}
}'
```
Parameters:

*   `owner_address`: The issuer's address, defaults to HexString format.
*   `name`: The token name, defaults to HexString format.
*   `abbr`: The token abbreviation, defaults to HexString format.
*   `total_supply`: The total supply to be issued.
*   `trx_num` and `num`: The minimum exchange ratio between token and TRX.
*   `start_time` and `end_time`: The start and end times for token issuance.
*   `description`: The token description, defaults to HexString format.
*   `url`: The official website of the token issuer, defaults to HexString format.
*   `free_asset_net_limit`: The total free bandwidth for the Token.
*   `public_free_asset_net_limit`: The free bandwidth that each token holder can use for this token.
*   `frozen_supply`: Tokens that the issuer can pledge at the time of issuance.
*   `permission_id` (optional): Used to specify the permission ID when signing with a permission other than the default owner permission.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned TRC-10 token issuance transaction object.

#### wallet/unfreezeasset
Description: Unfreeze tokens whose freezing period has ended.
```
curl -X POST http://127.0.0.1:8090/wallet/unfreezeasset -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```
Parameters:

*   `owner_address`: The address of the account unfreezing tokens, defaults to HexString format.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned unfreeze token transaction object.

#### wallet/updateasset
Description: Update the information of an issued TRC-10 token.
```
curl -X POST http://127.0.0.1:8090/wallet/updateasset -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
"description": ""，
"url": "",
"new_limit" : 1000000,
"new_public_limit" : 100
}'
```
Parameters:

*   `owner_address`: The token issuer's address, defaults to HexString format.
*   `description`: The token's description, defaults to HexString format.
*   `url`: The token issuer's official website address, defaults to HexString format.
*   `new_limit`: The free bandwidth each token holder can use.
*   `new_public_limit`: The total free bandwidth for this token.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned update token information transaction object.


<a id="sr"></a>
### Vote and Super Representative
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
Description: Create a transaction to apply to become a Super Representative.
```
curl -X POST  http://127.0.0.1:8090/wallet/createwitness -d '{"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292", "url": "007570646174654e616d6531353330363038383733343633"}'
```
Parameters:

*   `owner_address`: The account address applying to become a Super Representative, defaults to HexString format.
*   `url`: The official website address, defaults to HexString format.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned apply for SR transaction object.


#### wallet/updatewitness
Description: Update a Super Representative's website URL.
```
curl -X POST  http://127.0.0.1:8090/wallet/updatewitness -d '{
"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292",
"update_url": "007570646174654e616d6531353330363038383733343633"
}'
```
Parameters:

*   `owner_address`: The creator's address, defaults to HexString format.
*   `update_url`: The updated official website URL, defaults to HexString format.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned update URL transaction object.


#### wallet/listwitnesses
Description: Query the current list of all Super Representatives.
```
curl -X POST  http://127.0.0.1:8090/wallet/listwitnesses
```
Parameter: None

Return Value: A list of all Super Representative information.

#### wallet/withdrawbalance
Description:** SR or users withdraw rewards to their balance. This can be done once every 24 hours.

```
curl -X POST http://127.0.0.1:8090/wallet/withdrawbalance -d '{
"owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
}'
```
Parameters:

*   `owner_address`: The address of the account to withdraw from, defaults to HexString format.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned withdraw reward transaction object.



#### wallet/votewitnessaccount
Description: Vote for a Super Representative.
```
curl -X POST  http://127.0.0.1:8090/wallet/votewitnessaccount -d '{
"owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292",
"votes": [{"vote_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0", "vote_count": 5}]
}'
```
Parameters:

*   `owner_address`: The voter's address, defaults to HexString format.
*   `votes.vote_address`: The address of the Super Representative being voted for, defaults to HexString format.
*   `vote_count`: The number of votes.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned vote transaction object.

#### wallet/getBrokerage
Description: Query the brokerage ratio set by a specified SR.
```
curl -X GET  http://127.0.0.1:8090/wallet/getBrokerage -d '{
"address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
Parameters:

*   `address`: The address of the Super Representative being voted for, defaults to HexString format.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: The current brokerage ratio of the Super Representative.

#### wallet/updateBrokerage
Description: Update a Super Representative's current brokerage ratio.
```
curl -X POST  http://47.252.81.126:8090/wallet/updateBrokerage  -d '{
"owner_address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0",
"brokerage":30}'
```
Parameters:

*   `owner_address`: The address of the SR being voted for, defaults to HexString format.
*   `brokerage`: The brokerage ratio the SR wants to update to.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned update brokerage transaction object.

#### wallet/getReward
Description: Query the total unclaimed voting rewards for a voter account.
```
curl -X GET
http://127.0.0.1:8090/wallet/getReward -d '{
"address":"41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
Parameters:

*   `address`: The voter's address, defaults to HexString format.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An object containing the unclaimed reward amount (in sun).

#### wallet/getnextmaintenancetime
Description: Get the time of the next vote count.
```
curl -X POST  http://127.0.0.1:8090/wallet/getnextmaintenancetime
```
Parameter: None

Return Value: The millisecond timestamp of the next vote count.


<a id="tip"></a>
### Proposals
The following are proposal-related APIs:

- [wallet/proposalcreate](#walletproposalcreate)
- [wallet/getproposalbyid](#walletgetproposalbyid)
- [wallet/listproposals](#walletlistproposals)
- [wallet/proposalapprove](#walletproposalapprove)
- [wallet/proposaldelete](#walletproposaldelete)
- [wallet/getpaginatedproposallist](#walletgetpaginatedproposallist)


#### wallet/proposalcreate
Description: Create a proposal transaction to modify dynamic network parameters.
```
curl -X POST  http://127.0.0.1:8090/wallet/proposalcreate -d {"owner_address" : "419844F7600E018FD0D710E2145351D607B3316CE9","parameters":[{"key": 0,"value": 100000},{"key": 1,"value": 2}] }
```
Parameters:

*   `owner_address`: The creator's address.
*   `parameters`: Proposal parameters.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned create proposal transaction object.

#### wallet/getproposalbyid
Description: Query detailed proposal information by ID.
```
curl -X POST  http://127.0.0.1:8090/wallet/getproposalbyid -d {"id":1}
```
Parameter: `id`: Proposal ID.

Return Value: The detailed information of the specified proposal.

#### wallet/listproposals
Description: Query a list of all current proposals on the network.
```
curl -X POST  http://127.0.0.1:8090/wallet/listproposals
```
Parameter: None

Return Value: An array containing all proposal objects.


#### wallet/proposalapprove
Description: Approve a proposal.
```
curl -X POST  http://127.0.0.1:8090/wallet/proposalapprove -d {"owner_address" : "419844F7600E018FD0D710E2145351D607B3316CE9", "proposal_id":1, "is_add_approval":true}
```
Parameters:

*   `owner_address`: The approver's address, defaults to HexString format.
*   `proposal_id`: Proposal ID.
*   `is_add_approval`: Whether to approve (add approval) or not.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned approve proposal transaction object.

#### wallet/proposaldelete
Description: Delete a proposal.
```
curl -X POST  http://127.0.0.1:8090/wallet/proposaldelete -d {"owner_address" : "419844F7600E018FD0D710E2145351D607B3316CE9", "proposal_id":1}
```
Parameters:

*   `owner_address`: The address of the deleter. Only the proposal owner is allowed to delete proposals, defaults to HexString format.
*   `proposal_id`: Proposal ID.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned delete proposal transaction object.

#### wallet/getpaginatedproposallist
Description: Query the list of all the proposals by pagination
```
curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedproposallist -d '{"offset": 0, "limit": 10}'
```
Parameters:

*   `offset`: The starting index for pagination.
*   `limit`: The desired number of proposals to return in this query.

Return Value: An array containing proposal objects for the paginated results.


<a id="dex"></a>
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
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangecreate -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", 、
"first_token_id":token_a, "first_token_balance":100, "second_token_id":token_b,"second_token_balance":200}
```
Parameters:

*   `owner_address`: The address of the exchange creator, defaults to HexString format.
*   `first_token_id`: The ID of the first token, defaults to HexString format.
*   `first_token_balance`: The balance of the first token.
*   `second_token_id`: The ID of the second token, defaults to HexString format.
*   `second_token_balance`: The balance of the second token.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.

Return Value: An unsigned create trading pair transaction object.

#### wallet/exchangeinject
Description: Inject capital into a trading pair. This can prevent large price fluctuations in the trading pair.
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangeinject -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", "exchange_id":1, "token_id":"74726f6e6e616d65", "quant":100}
```
Parameters:

*   `owner_address`: The address of the trading pair creator, defaults to HexString format.
*   `exchange_id`: The trading pair ID.
*   `token_id`: The token ID, typically the token name, defaults to HexString format.
*   `quant`: The quantity of tokens to inject.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned inject capital transaction object.

#### wallet/exchangewithdraw
Description: Withdraw capital from a trading pair.
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangewithdraw -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", "exchange_id":1, "token_id":"74726f6e6e616d65", "quant":100}
```
Parameters:

*   `owner_address`: The address of the trading pair creator, defaults to HexString format.
*   `exchange_id`: The trading pair ID.
*   `token_id`: The token ID, typically the token name, must be in HexString format.
*   `quant`: The quantity of tokens to withdraw.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned withdraw capital transaction object.

#### wallet/exchangetransaction
Description: Participate in a trading pair transaction.
```
curl -X POST  http://127.0.0.1:8090/wallet/exchangetransaction -d {"owner_address":"419844f7600e018fd0d710e2145351d607b3316ce9", "exchange_id":1, "token_id":"74726f6e6e616d65", "quant":100,"expected":10}
```
Parameters:

*   `owner_address`: The address of the trading pair creator, defaults to HexString format.
*   `exchange_id`: The trading pair ID.
*   `token_id`: The ID of the token to sell, typically the token name, defaults to HexString format.
*   `quant`: The quantity of tokens to sell.
*   `expected`: The expected quantity of tokens to buy.
*   `permission_id` (optional): Specifies the ID of the Account Management Permission used to sign the transaction.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned exchange transaction object.

#### wallet/getexchangebyid
Description: Query a trading pair by ID.
```
curl -X POST  http://127.0.0.1:8090/wallet/getexchangebyid -d {"id":1}
```
Parameter: `id`: The trading pair ID.

Return Value: The specified trading pair object.

#### wallet/listexchanges
Description: Query all trading pairs.
```
curl -X POST  http://127.0.0.1:8090/wallet/listexchanges
```
Parameter: None

Return Value: An array containing all trading pair objects.

#### wallet/getpaginatedexchangelist
Description: Query the list of all the exchange pairs by pagination
```
curl -X POST  http://127.0.0.1:8090/wallet/getpaginatedexchangelist -d '{"offset": 0, "limit":10}'
```
Parameters:

*   `offset`: The starting index for pagination.
*   `limit`: The desired number of trading pairs to return in this query.

Return Value: An array containing trading pair objects for the paginated results.

#### wallet/marketsellasset
Description: Create an order.
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
Parameters:

*   `owner_address`: The order initiator's address, defaults to HexString format.
*   `sell_token_id`: The ID of the asset to sell, defaults to HexString format.
*   `sell_token_quantity`: The quantity of the asset to sell.
*   `buy_token_id`: The ID of the asset to buy, defaults to HexString format.
*   `buy_token_quantity`: The minimum quantity of the asset to buy.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned order placement transaction object.


#### wallet/marketcancelorder
Description: Cancel an order.
```
curl -X POST  http://127.0.0.1:8090/wallet/marketcancelorder -d
'{
    "owner_address": "4184894b42f66dce8cb84aec2ed11604c991351ac8",
    "order_id": "0a7af584a53b612bcff1d0fc86feab05f69bc4528f26a4433bb344d453bd6eeb"
}'
```
Parameters:

*   `owner_address`: The order initiator's address, defaults to HexString format.
*   `order_id`: The ID of the order to cancel.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An unsigned cancel order transaction object.

#### wallet/getmarketorderbyaccount
Description: Query orders owned by an account.
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderbyaccount -d
'{
    "value": "4184894b42f66dce8cb84aec2ed11604c991351ac8"
}'
```
Parameters:

*   `value`: The address, defaults to HexString format.
*   `visible`: Sets the address format. `true` for Base58Check, `false` or omitted for HexString.

Return Value: An array containing all order objects for the account.


#### wallet/getmarketpairlist
Description: Query all existing trading pairs.
```
curl -X get  http://127.0.0.1:8090/wallet/getmarketpairlist
```
Parameter: None

Return Value: An array containing information for all trading pairs.

#### wallet/getmarketorderlistbypair
Description: Query all orders for a specific trading pair.
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderlistbypair -d
'{
    "sell_token_id": "5f" ,
    "buy_token_id": "31303030303031"
}'
```
Parameters:

*   `sell_token_id`: The ID of the asset to sell, defaults to HexString format.
*   `buy_token_id`: The ID of the asset to buy, defaults to HexString format.

Return Value: An array containing all order objects for the trading pair.


#### wallet/getmarketpricebypair
Description: Query all prices for a specific trading pair.
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketpricebypair -d
'{
    "sell_token_id": "5f"
    "buy_token_id": "31303030303031"
}'
```
Parameters:

*   `sell_token_id`: The ID of the asset to sell, defaults to HexString format.
*   `buy_token_id`: The ID of the asset to buy, defaults to HexString format.

Return Value: An array containing all price point objects for the trading pair.

#### wallet/getmarketorderbyid
Description: Query an order.
```
curl -X POST  http://127.0.0.1:8090/wallet/getmarketorderbyid -d
'{
   "value": "orderid"
}'
```
Parameter: `value`: The order ID, defaults to HexString format.

Return Value: The specified order object.


<a id="pending-pool"></a>
### Pending Pool
The following are the APIs related to the Pending Pool:

- [wallet/gettransactionfrompending](#walletgettransactionfrompending)
- [wallet/gettransactionlistfrompending](#walletgettransactionlistfrompending)
- [wallet/getpendingsize](#walletgetpendingsize)

#### wallet/gettransactionfrompending
Description: Queries information for a transaction in the pending pool.
```
curl -X POST  http://127.0.0.1:8090/wallet/gettransactionfrompending -d
'{
  "value": "txId"
}'
```
Parameter: `value`: The transaction ID, in hexString format by default.

Return Value: A complete transaction object. Returns an empty object if the transaction is not in the pending pool.


#### wallet/gettransactionlistfrompending
Description: Retrieves a list of all transaction IDs currently in the pending pool.
```
curl -X get  http://127.0.0.1:8090/wallet/gettransactionlistfrompending
```
Parameter: None

Return Value: An array containing all pending transaction IDs.

#### wallet/getpendingsize
Description: Queries the number of transactions currently in the pending pool.
```
curl -X get  http://127.0.0.1:8090/wallet/getpendingsize
```
Parameter: None

Return Value: An object containing the size of the pending pool.

## FullNode Solidity HTTP API

### Account Resources

#### walletsolidity/getaccount

Description: Queries and returns the complete on-chain information for a specified TRON account (including balance, resources, permissions, and assets).

```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getaccount -d '{"address": "41E552F6487585C2B58BC2C9BB4492BC1F17132CD0"}'
```
Parameters:

- `address`: The account address to query.
- `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: An `Account` object.

#### walletsolidity/getdelegatedresource
Description: In Stake 1.0, queries the resources (Energy or Bandwidth) delegated from one account to another.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getdelegatedresource -d '
{
"fromAddress": "419844f7600e018fd0d710e2145351d607b3316ce9",
"toAddress": "41c6600433381c731f22fc2b9f864b14fe518b322f"
}'
```
Parameters:

- `fromAddress`: The address of the delegating account.
- `toAddress`: The address of the recipient account.
- `visible` (optional): Sets the address format. true for Base58Check, false (or omitted) for HexString.

Return Value: A list of `DelegatedResource` objects.

#### walletsolidity/getdelegatedresourceaccountindex
Description: In Stake 1.0, queries the delegation relationships for a specified account.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getdelegatedresourceaccountindex -d '
{
"value": "419844f7600e018fd0d710e2145351d607b3316ce9",
}'
```
Parameters:

* `value`: The account address to query.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: A `DelegatedResourceAccountIndex` object showing the account's delegation overview.

#### walletsolidity/getaccountbyid
Description: Queries account information by its `account_id`.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getaccountbyid -d '{"account_id":"6161616162626262"}'
```
Parameter: `account_id` in hexString format by default.

Return Value: An Account object.

#### walletsolidity/getavailableunfreezecount

Description: Queries the remaining number of unstake operations an account can initiate. The TRON network limits each account to a maximum of 32 concurrent unstaking operations within the 14-day lock period. This API can be used to pre-check whether there is an available "unstaking quota" before calling `unfreezebalancev2`.

```
curl -X POST http://127.0.0.1:8090/walletsolidity/getavailableunfreezecount -d
'{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters:

* `owner_address`: The account address to query.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: A JSON object containing the remaining count.

#### walletsolidity/getcanwithdrawunfreezeamount

Description: Queries the total amount of unstaked principal that can be withdrawn at a specific point in time.

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

* `owner_address`: The address of the transaction initiator.
* `timestamp`: The timestamp (in milliseconds) at which to query the withdrawable amount.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: A JSON object containing the withdrawable amount.



#### walletsolidity/getcandelegatedmaxsize

Description: Queries the maximum amount of a specified resource type that a target address can delegate, in sun.
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

- `owner_address`: The account address to query.
- `type`: The resource type, `0` for Bandwidth, `1` for Energy.
- `visible` (optional): Sets the address format. true for Base58Check, false (or omitted) for HexString.

Return Value: 

* A JSON object containing the maximum delegatable share.

#### walletsolidity/getdelegatedresourcev2

Description: Queries the resource details delegated from one address to a target address under the Stake 2.0 mechanism.
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

* `fromAddress`: The delegating account address.
* `toAddress`: The recipient account address.
* `visible`(optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value: 

* An array of `delegatedResource` objects, containing all delegation records between the two addresses under Stake 2.0.

#### walletsolidity/getdelegatedresourceaccountindexv2

Description: Queries the resource delegation index for an address under the Stake 2.0 mechanism. It returns two lists: one of addresses to which the account has delegated resources (`toAccounts`), and one of addresses that have delegated resources to this account (`fromAccounts`).

```
curl -X POST http://127.0.0.1:8090/walletsolidity/getdelegatedresourceaccountindexv2 -d
'{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

Parameters:

* `value`: The account address.
* `visible` (optional): Sets the address format. `true` for Base58Check, `false` (or omitted) for HexString.

Return Value:

- This interface returns a JSON object containing a list of bidirectional proxy relationships. It contains two lists: one for the addresses to which the account delegates resources (`toAddress`), and one for the addresses that delegate resources to the account (`fromAddress`).

### Voting & SRs

#### walletsolidity/listwitnesses
Description: Query the current list of all Super Representatives (SRs).
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/listwitnesses
```
Parameter: None

Return Value: A list of all witness information.

### TRC-10 Token

#### walletsolidity/getassetissuelist
Description: Query a list of all TRC-10 tokens on the entire network.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuelist
```
Parameter: None

Return Value: An array containing objects for all TRC-10 tokens on the network.

#### walletsolidity/getpaginatedassetissuelist
Description: Paginate and query a list of TRC-10 tokens on the entire network.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getpaginatedassetissuelist -d '{"offset": 0, "limit":10}'
```
Parameters:

*  `offset`: The starting index for pagination.
*  `limit`: The desired number of tokens to return in this query.

Return Value: An array containing TRC-10 token objects for the paginated results.

#### walletsolidity/getassetissuebyname
Description: Query TRC-10 tokens by name.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuebyname -d '{"value": "44756354616E"}'
```
Parameter: `value`：Token name, defaults to HexString format.
 
Return Value: A TRC-10 token object.


Note: Starting from Odyssey-v3.2, it is recommended to use getassetissuebyid or getassetissuelistbyname to replace this interface, because starting from 3.2, tokens are allowed to have the same name. If identical token names exist, this interface will report an error.

#### walletsolidity/getassetissuelistbyname
Description: Query all matching TRC-10 token lists by name.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuelistbyname -d '{"value": "44756354616E"}'
```
Parameter: `value`：Token name, defaults to HexString format.

Return Value: An array containing all TRC-10 token objects with the same name.

#### walletsolidity/getassetissuebyid
Description: Query TRC-10 token by ID.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getassetissuebyid -d '{"value": "1000001"}'
```
Parameter：`value`: The ID of the TRC-10 token.

Return Value: The specified TRC-10 token object.



### Blocks

#### walletsolidity/getnowblock
Description: Query the latest block.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getnowblock
```
Parameter: None

Return Value: The latest block object on the SolidityNode.

#### walletsolidity/getblockbynum
Description: Query complete block information by a specified block height.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbynum -d '{"num" : 100}'
```
Parameter: `num`: Block height (integer).

Return Value: The Block object at the specified height.


#### walletsolidity/getblockbyid
Description: Query complete block information by a specified Block ID (hash).
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbyid-d '{"value":
"0000000000038809c59ee8409a3b6c051e369ef1096603c7ee723c16e2376c73"}'
```
Parameter: `value`: The Block ID (hash).

Return Value: The Block object with the specified ID.

#### walletsolidity/getblockbylimitnext
Description: Paginate and query a list of blocks within a specified height range.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbylimitnext -d '{"startNum": 1, "endNum": 2}'
```
Parameters:

* `startNum`: Starting block height (inclusive).
* `endNum`: Ending block height (exclusive).


Return Value: An array containing multiple Block objects (Block[]).

#### walletsolidity/getblockbylatestnum
Description: Queries the last N blocks from the SolidityNode, starting from the latest block.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getblockbylatestnum -d '{"num": 5}'
```
Parameter: `num`: The number of blocks to query.

Return Value: An array containing multiple Block objects (`Block[]`).

#### wallet/getnodeinfo
Description: View the current node's own operating status and information.
```
curl -X GET http://127.0.0.1:8091/wallet/getnodeinfo
```
Parameter: None

Return Value: An object containing information such as node version, network status, block synchronization status, etc.


### Transactions

#### walletsolidity/gettransactionbyid
Description: Queries the complete information of a confirmed transaction by its ID (hash).
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactionbyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
Parameter: `value`: Transaction ID (hash).

Return Value: The complete Transaction object. Returns an empty object if the transaction does not exist or is unconfirmed.

#### walletsolidity/gettransactioncountbyblocknum
Description: Query the total number of transactions contained in a specified block height.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioncountbyblocknum -d '{"num" : 100}'
```
Parameter: `num`: Block height.

Return Value: An object containing the transaction count, such as `{"count": 50}`.

#### walletsolidity/gettransactioninfobyid
Description: Query the summary information of a transaction, such as fees and block location, based on its Transaction ID (hash).
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioninfobyid -d '{"value" : "309b6fa3d01353e46f57dd8a8f27611f98e392b50d035cef213f2c55225a8bd2"}'
```
Parameter: `value`: Transaction ID (hash).

Return Value: A TransactionInfo object containing transaction fees, block height, block timestamp, contract execution results, etc.

#### walletsolidity/gettransactioninfobyblocknum
Description: Get a list of summary information for all transactions at a specified block height.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/gettransactioninfobyblocknum -d '{"num" : 100}'
```
Parameter: `num`: Block height.

Return Value: A list containing multiple TransactionInfo objects.


### DEX Exchanges

#### walletsolidity/getexchangebyid
Description: Query a trading pair by ID.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/getexchangebyid -d {"id":1}
```
Parameter: `id`: The trading pair ID.

Return Value: The specified trading pair object.

#### walletsolidity/listexchanges
Description: Query all trading pairs.
```
curl -X POST  http://127.0.0.1:8091/walletsolidity/listexchanges
```
Parameter: None

Return Value: An array containing all trading pair objects.


