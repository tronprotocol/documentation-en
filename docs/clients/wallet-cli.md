# wallet-cli

## Introduction
wallet-cli is an interactive command-line wallet that supports the TRON network for signing and broadcasting transactions in a secure local environment, as well as access to on-chain data. wallet-cli supports key management, you can import the private key into the wallet, wallet-cli will encrypt your private key with a symmetric encryption algorithm and store it in a keystore file. wallet-cli does not store on-chain data locally. It uses gRPC to communicate with a java-tron node. You need to configure the java-tron node to be linked in the configuration file. The following figure shows the process of the use of wallet-cli to sign and broadcast when transferring TRX:
![](https://i.imgur.com/NRKmZmE.png)

The user first runs the `Login` command to unlock the wallet, and then runs the `SendCoin` command to send TRX, wallet-cli will build and sign the transaction locally, and then call the BroadcastTransaction gRPC API of the java-tron node to broadcast the transaction to the network. After the broadcast is successful, the java-tron node will return the transaction hash to wallet-cli, and wallet-cli will display the transaction hash to the user.

Install and run: [wallet-cli](https://github.com/tronprotocol/wallet-cli)

## Commands
Below, please find all types of wallet-cli commands：

- [Wallet](#wallet)
- [Account](#account)
- [AccountResource](#accountresource)
- [Transaction](#transaction)
- [On-ChainInquire](#on-chaininquire)
- [SmartContract](#smartcontract)
- [TRC-10](#trc-10)
- [Governance](#governance)
- [DEX](#dex)


### Wallet
Here are all the wallet related commands ：

- [RegisterWallet](#registerwallet)
- [Login](#login)
- [BackupWallet](#backupwallet)
- [BackupWallet2Base64](#backupwallet2base64)
- [ChangePassword](#changepassword)
- [ImportWallet](#importwallet)
- [ImportWalletByBase64](#importwalletbybase64)


This section introduces commands related to wallet management. Let's start with`registerwallet`to get a new account.

#### RegisterWallet
To register your wallet, you need to set the wallet password and generate the address and private key. A .json keystore file will be generated under the path of `wallet-cli/wallet`. The file will be used for `login` and `backupwallet` later.
```shell
wallet> RegisterWallet 
Please input password.
password: 
Please input password again.
password: 
Register a wallet successful, keystore file name is UTC--2022-06-27T07-37-47.601000000Z--TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw.json
```
#### Login
When we have a keystore file, we can start to login. After enter the command, choose the keystore file and enter the password.
```shell
wallet> login
use user defined config file in current dir
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-06-22T08-31-57.735000000Z--TBnPDbw99BLzPUZuW8Rrcc3RGGQT3cnSfF.json
The 4th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 5th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 5
4
Please input your password.
password: 
Login successful !!!
```
#### BackupWallet

This will Back up your wallet. You need to enter your wallet password to export the privat key in hex string format, such as:
```
721d63b074f18d41c147e04c952ec93467777a30b6f16745bc47a8eae5076545
```

```shell
wallet> backupwallet
Please input your password.
password: 
BackupWallet successful !!
721d63b074f18d41c147e04c952ec93467777a30b6f16745bc47a8eae5076545
```
#### BackupWallet2Base64

This will Back up your wallet, you need to enter your wallet password to export the private key in base64 format, as below:
```
ch1jsHTxjUHBR+BMlS7JNGd3ejC28WdFvEeo6uUHZUU=
```

```shell
wallet> backupwallet
Please input your password.
password: 
BackupWallet successful !!
ch1jsHTxjUHBR+BMlS7JNGd3ejC28WdFvEeo6uUHZUU=
```
#### ChangePassword

Modify the password of an account
```shell
wallet> changepassword
Please input old password.
password: 
Please input new password.
Please input password.
password: 
Please input password again.
password: 
The 1th keystore file name is .DS_Store
The 2th keystore file name is UTC--2022-06-27T10-58-59.306000000Z--TBnPDbw99BLzPUZuW8Rrcc3RGGQT3cnSfF.json
Please choose between 1 and 2
2
ChangePassword successful !!
```


#### ImportWallet
Import a wallet, you need to set a password first and then enter your hex string private key.
```shell
wallet> importwallet
Please input password.
password: 
Please input password again.
password: 
Please input private key. Max retry time:3
bd1ff0f4f852db45316bf08755bf6eee45d0678bfbf852a00020a13d42a1fb5b
Import a wallet successful, keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
```
#### ImportWalletByBase64
To import a wallet, you need to set a password first and then enter your private key in base64 format.
```shell
wallet> importwalletbybase64
Please input password.
password: 
Please input password again.
password: 
Please input private key by base64. Max retry time:3
vR/w9PhS20Uxa/CHVb9u7kXQZ4v7+FKgACChPUKh+1s=   
Import a wallet successful, keystore file name is UTC--2022-06-28T06-51-56.154000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json

```

### Account 
Here are all the account related commands ：

- [GenerateAddress](#generateaddress)
- [GetAccount](#getaccount)
- [GetAddress](#getaddress)
- [GetBalance](#getbalance)
- [UpdateAccountPermission](#updateaccountpermission)

#### GenerateAddress
Generate an address and print out the public (address) and private key
```shell
wallet> generateaddress
{
	"address": "TQAvi6bemLa1t1irdV1KuaSC5vKc2EswTj",
	"privateKey": "610a8a809114a96140e1cb040a7813afc74603e58c3d7824c3f68ccc642c297e"
}
```
**Note:** address and private key generated by this command would not be saved in wallet-cli. Keep properly if you would like to use them.
#### GetAccount

Get account information by an address
```shell
wallet> getaccount [address]
```
```shell
wallet> getaccount TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
{
	"address": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
	"balance": 2665198240,
	"create_time": 1650363711000,
	"latest_opration_time": 1653578769000,
	"latest_consume_free_time": 1651228080000,
	"account_resource": {
		"latest_consume_time_for_energy": 1653578769000
	},
	"owner_permission": {
		"permission_name": "owner",
		"threshold": 1,
		"keys": [
			{
				"address": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
				"weight": 1
			}
		]
	},
	"active_permission": [
		{
			"type": "Active",
			"id": 2,
			"permission_name": "active",
			"threshold": 1,
			"operations": "7fff1fc0033e3b00000000000000000000000000000000000000000000000000",
			"keys": [
				{
					"address": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
					"weight": 1
				}
			]
		}
	]
}

```
#### GetAddress

Get the address of the current account
```shell
wallet> getaddress
GetAddress successful !!
address = TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
```

#### GetBalance
Get the TRX balance of the current account
```shell
wallet> getbalance
Balance = 2665198240
```

#### UpdateAccountPermission
```shell
wallet>UpdateAccountPermission [ownerAddress] [permissions]
```
This command is used to manage account permissions, assign permissions to other accounts, is utilized for multi-signature transactions, which allows other users to access the account with paritcular permission in order to better manage it. There are three types of permissions:

* owner: access to the owner of account
* active: access to other features of accounts, and access that authorizes a certain feature. Block production authorization is not included if it's for SR purposes.
* witness: only for super representatives, block production authorization will be granted to one of the other users.

**NOTE** the parameter`Permission` must written in JSON format and entered in line. If the owner account is not SR, then do not assign super representative permission. 
```shell
wallet> updateaccountpermission TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8 {"owner_permission":{"keys":[{"address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8","weight":1}],"threshold":1,"type":0,"permission_name":"owner"},"active_permissions":[{"operations":"7fff1fc0033e0000000000000000000000000000000000000000000000000000","keys":[{"address":"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej","weight":1},{"address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE","weight":1}],"threshold":2,"type":2,"permission_name":"active12323"}]}
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"owner":{
							"keys":[
								{
									"address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
									"weight":1
								}
							],
							"threshold":1,
							"permission_name":"owner"
						},
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
						"actives":[
							{
								"operations":"7fff1fc0033e0000000000000000000000000000000000000000000000000000",
								"keys":[
									{
										"address":"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej",
										"weight":1
									},
									{
										"address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
										"weight":1
									}
								],
								"threshold":2,
								"type":"Active",
								"permission_name":"active12323"
							}
						]
					},
					"type_url":"type.googleapis.com/protocol.AccountPermissionUpdateContract"
				},
				"type":"AccountPermissionUpdateContract"
			}
		],
		"ref_block_bytes":"4e88",
		"ref_block_hash":"11a47859be13f689",
		"expiration":1656423231000,
		"timestamp":1656423171818
	},
	"raw_data_hex":"0a024e88220811a47859be13f6894098dc92d49a305aee01082e12e9010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e747261637412a8010a1541babecec4d9f58f0df77f0728b9c53abb1f21d68412241a056f776e657220013a190a1541babecec4d9f58f0df77f0728b9c53abb1f21d6841001226908021a0b6163746976653132333233200232207fff1fc0033e00000000000000000000000000000000000000000000000000003a190a15410cfaec7164cbfe78dbb8d8fba7e23b4d745ed81310013a190a1541e8bd653015895947cec33d1670a88cf67ab277b9100170ea8d8fd49a30"
}
before sign transaction hex string is 0a8d020a024e88220811a47859be13f6894098dc92d49a305aee01082e12e9010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e747261637412a8010a1541babecec4d9f58f0df77f0728b9c53abb1f21d68412241a056f776e657220013a190a1541babecec4d9f58f0df77f0728b9c53abb1f21d6841001226908021a0b6163746976653132333233200232207fff1fc0033e00000000000000000000000000000000000000000000000000003a190a15410cfaec7164cbfe78dbb8d8fba7e23b4d745ed81310013a190a1541e8bd653015895947cec33d1670a88cf67ab277b9100170ea8d8fd49a30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
3
Please input your password.
password: 
after sign transaction hex string is 0a8d020a024e88220811a47859be13f6894096bcb5de9a305aee01082e12e9010a3c747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e745065726d697373696f6e557064617465436f6e747261637412a8010a1541babecec4d9f58f0df77f0728b9c53abb1f21d68412241a056f776e657220013a190a1541babecec4d9f58f0df77f0728b9c53abb1f21d6841001226908021a0b6163746976653132333233200232207fff1fc0033e00000000000000000000000000000000000000000000000000003a190a15410cfaec7164cbfe78dbb8d8fba7e23b4d745ed81310013a190a1541e8bd653015895947cec33d1670a88cf67ab277b9100170ea8d8fd49a301241881b00f8e8828d9347469fcbcec730093841c2363561243b7162a9669439266049ab82f20f97a136adc88feff0a4d5aa57b11f762eaa7e05105d27ec5d55a33900
txid is 3dce7f18f6cf6962c38904678947b3b32f9e94ba6460874679d8ed063bb1c0eb
UpdateAccountPermission successful !!!
```
---

### AccountResource
Here are all the account resource related commands ：

- [FreezeBalance](#freezebalance)
- [UnfreezeBalance](#unfreezebalance)
- [GetDelegatedResource](#getdelegatedresource)
- [FreezeBalanceV2](#freezebalancev2)
- [UnfreezeBalanceV2](#unfreezebalancev2)
- [DelegateResource](#delegateresource)
- [UndelegateResource](#undelegateresource)
- [WithdrawExpireUnfreeze](#withdrawexpireunfreeze)
- [GetAvailableUnfreezeCount](#getavailableunfreezecount)
- [GetCanWithdrawUnfreezeAmount](#getcanwithdrawunfreezeamount)
- [GetCanDelegatedMaxsize](#getcandelegatedmaxsize)
- [GetDelegatedResourceV2](#getdelegatedresourcev2)
- [GetDelegatedResourceAccountIndexV2](#getdelegatedresourceaccountindexv2)
- [GetAccountNet](#getaccountnet)
- [GetAccountResource](#getaccountresource)

#### FreezeBalance
This interface has been deprecated, please use freezeBalanceV2 to stake TRX to obtain resources.
```shell
wallet> freezeBalance [OwnerAddress] [frozen_balance] [frozen_duration] [ResourceCode:0 BANDWIDTH, 1 ENERGY] [receiverAddress]
```

`OwnerAddress`is the address of the account that initiated the transaction, optional, default is the address of the login account.`frozen_balance`is the amount of frozen TRX, the unit is the smallest unit (Sun), the minimum is 1000000sun.`frozen_duration` is frozen duration, only be specified as 3 days, indicates that you can unfreeze after 3 days.`ResourceCode` indicates the type of the acquired resource，0 BANDWIDTH and 1 ENERGY. `receiverAddress`is the address that will receive the resource.

`ResourceCode` and `receiverAddress`  are optional parameters. If `ResourceCode` is not set，default is 0. If `receiverAddress` is not set, the TRX is frozen to obtain resources for its `OwnerAddress` use; if it is not empty, the acquired resources are used by receiverAddress.

Example:
```shell
wallet> freezeBalance TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw 1000000 3 1 TCrkRWJuHP4VgQF3xwLNBAjVVXvxRRGpbA
{
	"raw_data":{
		...
	},
	"raw_data_hex":"0a02a9b822081db2070d39d2316640c095dda19a305a70080b126c0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e6365436f6e747261637412360a1541e65aca838a9e15dd81bd9532d2ad61300e58cf7110c0843d180350017a15411fafb1e96dfe4f609e2259bfaf8c77b60c535b9370c6c8d9a19a30"
}
before sign transaction hex string is 0a8e010a02a9b822081db2070d39d2316640c095dda19a305a70080b126c0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e6365436f6e747261637412360a1541e65aca838a9e15dd81bd9532d2ad61300e58cf7110c0843d180350017a15411fafb1e96dfe4f609e2259bfaf8c77b60c535b9370c6c8d9a19a30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-22T08-21-05.158000000Z--TDQgNvjrE6RH749f8aFGyJqEEGyhV4BDEU.json
The 2th keystore file name is UTC--2022-06-27T07-37-47.601000000Z--TWyDBTHsWJFhgywWkTNW7vh7jSUxeBaiAw.json
Please choose between 1 and 2
2
Please input your password.
password: 
after sign transaction hex string is 0a8e010a02a9b822081db2070d39d2316640e0f7ffab9a305a70080b126c0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e6365436f6e747261637412360a1541e65aca838a9e15dd81bd9532d2ad61300e58cf7110c0843d180350017a15411fafb1e96dfe4f609e2259bfaf8c77b60c535b9370c6c8d9a19a301241c45742648e6970e01b242c9b6eca2549c8721b860ced71abd331b9fe925f3c0f184768e0d2e3b580ce787cc6f67d186a0d583226fdb69c2cc8cfc6ec42e389f600
txid is f45cb5ae425796a492d4a9ecac8d60fd48bf78dbcdbe1d92725047c5dfbffba2
FreezeBalance successful !!!
```


#### UnfreezeBalance
unstake TRX which staked during stake1.0.
```shell
wallet>unfreezeBalance [OwnerAddress] ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER) [receiverAddress]
```
`OwnerAddress`is the address of the account that initiated the transaction, optional, default is the address of the login account. `ResourceCode`indicates the type of the acquired resource，0 stands for BANDWIDTH and 1 stands for ENERGY. `receiverAddress`is the address that will receive the resource.

```
wallet> unfreezebalance TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8 1 TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"resource":"ENERGY",
						"receiver_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8"
					},
					"type_url":"type.googleapis.com/protocol.UnfreezeBalanceContract"
				},
				"type":"UnfreezeBalanceContract"
			}
		],
		"ref_block_bytes":"c8b7",
		"ref_block_hash":"8842722f2845274d",
		"expiration":1656915213000,
		"timestamp":1656915154748
	},
	"raw_data_hex":"0a02c8b722088842722f2845274d40c8f5debe9c305a6c080c12680a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e6365436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d68450017a1541e8bd653015895947cec33d1670a88cf67ab277b970bcaedbbe9c30"
}
before sign transaction hex string is 0a8a010a02c8b722088842722f2845274d40c8f5debe9c305a6c080c12680a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e6365436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d68450017a1541e8bd653015895947cec33d1670a88cf67ab277b970bcaedbbe9c30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y               
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
3
Please input your password.
password: 
after sign transaction hex string is 0a8a010a02c8b722088842722f2845274d40e8dd81c99c305a6c080c12680a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e6365436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d68450017a1541e8bd653015895947cec33d1670a88cf67ab277b970bcaedbbe9c301241593a94650274df29619a6a6946258ea32a22f24a33445f943e3d72cd7d9b8ce7234d188f4bf3a6f0c90cb60af36fc77dc8d376afac9ed840f36dfd68c429fb7e00
txid is 3ea58b3ac2cb05868e70d40f58916312d927c40fd1e4c549554dc3e520c1efde
UnfreezeBalance successful !!!

```

#### GetDelegatedResource 
```
wallet>getdelegatedresource [fromAddress] [toAddress]
```
Get the information from the `fromAddress`, which is the resource owner's address, to the `toAddress`, which is the delegated address who is on behalf of the resource owner.
```shell
wallet> getdelegatedresource TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8 TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE
{
	"delegatedResource": [
		{
			"from": "TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
			"to": "TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
			"frozen_balance_for_energy": 1000000,
			"expire_time_for_energy": 1656660447000
		}
	]
}
```

#### FreezeBalanceV2
Stake 2.0 API: Stake TRX to obtain TRON Power (voting rights) and bandwidth or energy.

```shell
wallet> freezeBalanceV2 [OwnerAddress] frozen_balance ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER)
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.
* `frozen_balance` is the amount of frozen TRX, the unit is the smallest unit (Sun), the minimum is 1000000sun.
* `ResourceCode` indicates the type of the acquired resource，0 BANDWIDTH and 1 ENERGY.

Example:

```shell
wallet> freezeBalanceV2 1000000 1
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"resource":"ENERGY",
						"frozen_balance":1000000,
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM"
					},
					"type_url":"type.googleapis.com/protocol.FreezeBalanceV2Contract"
				},
				"type":"FreezeBalanceV2Contract"
			}
		],
		"ref_block_bytes":"00bb",
		"ref_block_hash":"0c237850e9e3c216",
		"expiration":1676620524000,
		"timestamp":1676620465372
	},
	"raw_data_hex":"0a0200bb22080c237850e9e3c21640e0d3fbf2e5305a59083612550a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d180170dc89f8f2e530"
}
before sign transaction hex string is 0a770a0200bb22080c237850e9e3c21640e0d3fbf2e5305a59083612550a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d180170dc89f8f2e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a770a0200bb22080c237850e9e3c21640dbb89efde5305a59083612550a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d180170dc89f8f2e53012419e46cc7b6706ee6a14a541df5f9c518fae9a71ac7a7cc484c48386eb0997a8ab10c41e09feb905c5cc370fe1d15968d22cec2fd2cdc5916adfd3a78c52f8d47000
txid is 1743aa098f5e10ac8b68ccbf0ca6b5f1364a63485e442e6cb03fd33e3331e3fb
freezeBalanceV2 successful !!!
```

#### UnfreezeBalanceV2
Stake 2.0 API: Unstake TRX to release bandwidth and energy and at the same time TRON Power will be reclaimed and corresponding votes will be revoked. 


```shell
wallet> unfreezeBalanceV2 [OwnerAddress] unfreezeBalance ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER)
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account. 
* `unfreezeBalance` Amount of TRX to be unstaked. the unit is sun.
* `ResourceCode` indicates the type of the acquired resource，0 stands for BANDWIDTH and 1 stands for ENERGY. 


Example:

```shell
wallet> unfreezeBalanceV2 1000000  1
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"resource":"ENERGY",
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
						"unfreeze_balance":1000000
					},
					"type_url":"type.googleapis.com/protocol.UnfreezeBalanceV2Contract"
				},
				"type":"UnfreezeBalanceV2Contract"
			}
		],
		"ref_block_bytes":"0132",
		"ref_block_hash":"0772c1a1727e2ef0",
		"expiration":1676620887000,
		"timestamp":1676620829314
	},
	"raw_data_hex":"0a02013222080772c1a1727e2ef040d8e791f3e5305a5b083712570a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d18017082a58ef3e530"
}
before sign transaction hex string is 0a790a02013222080772c1a1727e2ef040d8e791f3e5305a5b083712570a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d18017082a58ef3e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a790a02013222080772c1a1727e2ef040ecd2b4fde5305a5b083712570a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121d0a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca10c0843d18017082a58ef3e530124111bac22e9bc35e1a78c13796893e9f2b81dc99eb26d9ce7a95d0c6a0a9b5588739c52b999acd370b255d178f57bf2abef8881891f23e042ddf83c3551b8bd98e01
txid is f9e114347ea89c5d722d20226817bc41c8a39ea36be756ba216cf450ab3f1fb3
unfreezeBalanceV2 successful !!!
```

#### DelegateResource
Stake 2.0 API: delegate bandwidth or energy resource to other address.
```shell
wallet> delegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress [lock]
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.
* `balance` Amount of TRX staked for resources to be delegated, unit is sun.
* `ResourceCode` Resource type, "BANDWIDTH" is 0, "ENERGY" is 1.
* `ReceiverAddress` Receiver address of resource to be delegated to.
* `lock` Whether it is locked, if it is set to true, the delegated resources cannot be undelegated within 3 days. When the lock time is not over, if the owner delegates the same type of resources using the lock to the same address, the lock time will be reset to 3 days. optional, default is 0, 0-lock, 1-unlock.

Example:

```shell
wallet> delegateResource 1000000  1 TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g 0
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"balance":1000000,
						"resource":"ENERGY",
						"receiver_address":"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM"
					},
					"type_url":"type.googleapis.com/protocol.DelegateResourceContract"
				},
				"type":"DelegateResourceContract"
			}
		],
		"ref_block_bytes":"020c",
		"ref_block_hash":"54e32e95d11894f8",
		"expiration":1676621547000,
		"timestamp":1676621487525
	},
	"raw_data_hex":"0a02020c220854e32e95d11894f840f88bbaf3e5305a710839126d0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e70a5bbb6f3e530"
}
before sign transaction hex string is 0a8f010a02020c220854e32e95d11894f840f88bbaf3e5305a710839126d0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e70a5bbb6f3e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a8f010a02020c220854e32e95d11894f84093e9dcfde5305a710839126d0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e70a5bbb6f3e5301241414de060e9c104bb45d745e22b7b7a30b4a89a2635c62aab152fff5d2f10b7443023a9aa487be86652b74974ff6a7d82d3dbf94cea9ac1e0a7e48e682175e3f601
txid is 0917002d0068dde7ad4ffe46e75303d11192e17bfa78934a5f867c5ae20720ec
delegateResource successful !!!
```

#### UndelegateResource
Stake 2.0 API: undelegate resource.
```shell
wallet> unDelegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.
* `balance` Amount of TRX staked for resource to be undelegated, unit is sun.
* `ResourceCode` Resource type, "BANDWIDTH" is 0, "ENERGY" is 1.
* `ReceiverAddress` Receiver address of resource to be delegated to.



Example:

```shell
wallet> unDelegateResource 1000000  1 TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"balance":1000000,
						"resource":"ENERGY",
						"receiver_address":"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM"
					},
					"type_url":"type.googleapis.com/protocol.UnDelegateResourceContract"
				},
				"type":"UnDelegateResourceContract"
			}
		],
		"ref_block_bytes":"0251",
		"ref_block_hash":"68ac15256c213e71",
		"expiration":1676621754000,
		"timestamp":1676621695001
	},
	"raw_data_hex":"0a020251220868ac15256c213e714090ddc6f3e5305a73083a126f0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e709990c3f3e530"
}
before sign transaction hex string is 0a91010a020251220868ac15256c213e714090ddc6f3e5305a73083a126f0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e709990c3f3e530
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is UTC--2023-02-17T02-53-57.163000000Z--THLJLytz6UHwpmDFi5RC43D44dmnh4ZTeL.json
The 2th keystore file name is UTC--2023-02-17T07-40-47.121000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 2
2
Please input your password.
password:
after sign transaction hex string is 0a91010a020251220868ac15256c213e7140febde9fde5305a73083a126f0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412340a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca100118c0843d221541fd49eda0f23ff7ec1d03b52c3a45991c24cd440e709990c3f3e530124102ebde16d1abaccd976f8ead4b5acf92b05f7d9796c28ca6a26b4e51442e638e5e33e598bb03732da24dc761a39b9d307c045b55323128dc9b07510ffc48933a01
txid is 537a3f4461ab55c705b77503bc42f469bfc22c0cb8588b8f3641ab40117ebfd8
unDelegateResource successful !!!
```
#### WithdrawExpireUnfreeze
Stake 2.0 API: withdraw unfrozen balance.

```shell
wallet> withdrawExpireUnfreeze [OwnerAddress]
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.


Example:

```shell
wallet> withdrawExpireUnfreeze 
```

#### GetAvailableUnfreezeCount
Stake 2.0 API: remaining times of executing unstake operation.

```shell
wallet> getavailableunfreezecount [OwnerAddress]
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.



Example:

```shell
wallet> GetAvailableUnfreezeCount
{
	"count": 30
}
```
#### GetCanWithdrawUnfreezeAmount
Stake 2.0 API: query the withdrawable balance at the specified timestamp.

```shell
wallet> getcanwithdrawunfreezeamount ownerAddress timestamp
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.
* `timestamp` query cutoff timestamp, in milliseconds.

Example:

```shell
wallet> getcanwithdrawunfreezeamount 1776621695001
{
	"amount": 4000000
}
```

#### GetCanDelegatedMaxsize
Stake 2.0 API: query the amount of delegatable resources share of the specified resource type for an address, unit is sun.

```shell
wallet> getcandelegatedmaxsize ownerAddress type
```

* `OwnerAddress` is the address of the account that initiated the transaction, optional, default is the address of the login account.
* `type` resource type, 0 is bandwidth, 1 is energy


Example:

```shell
wallet> getcandelegatedmaxsize 1
{
	"max_size": 11000000
}
```
#### GetDelegatedResourceV2
Stake 2.0 API：query the detail of resource share delegated from fromAddress to toAddress.

```shell
wallet> getdelegatedresourcev2 fromAddress toAddress
```

* `fromAddress` resource from address.
* `toAddress`  resource to address.

Example:

```shell
wallet> getdelegatedresourcev2  TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g
{
	"delegatedResource": [
		{
			"from": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
			"to": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
			"frozen_balance_for_bandwidth": 7000000,
			"frozen_balance_for_energy": 3000000
		}
	]
}
```
#### GetDelegatedResourceAccountIndexV2
Stake 2.0 API：query the resource delegation index by an account. Two lists will return, one is the list of addresses the account has delegated its resources(toAddress), and the other is the list of addresses that have delegated resources to the account(fromAddress).

```shell
wallet> getdelegatedresourceaccountindexv2 ownerAddress
```

* `OwnerAddress` account address.

Example:

```shell
wallet> getdelegatedresourceaccountindexv2 TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
{
	"account": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
	"fromAccounts": [
		"TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
	],
	"toAccounts": [
		"TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"
	]
}
```


#### GetAccountNet
This command shows the usage of bandwidth for a certain account.
```shell
wallet> getaccountnet TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
{
	"freeNetUsed": 262,
	"freeNetLimit": 1500,
	"TotalNetLimit": 43200000000,
	"TotalNetWeight": 8725123062
}
```

#### GetAccountResource
This command shows the usage of bandwidth and energy for a certain account.
```shell
wallet> getaccountresource TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
{
	"freeNetUsed": 262,
	"freeNetLimit": 1500,
	"TotalNetLimit": 43200000000,
	"TotalNetWeight": 8725123062,
	"tronPowerLimit": 1,
	"TotalEnergyLimit": 90000000000,
	"TotalEnergyWeight": 328098231
}
```
---

### Transaction
Here are all the transaction related commands ：

- [SendCoin](#sendcoin)
- [AddTransactionSign](#addtransactionsign)
- [BroadcastTransaction](#broadcasttransaction)
- [BackupWallet2Base64](#backupwallet2base64)
- [GetTransactionApprovedList](#gettransactionapprovedlist)

#### SendCoin
```
> SendCoin [toAddress] [amount]
```
Here is an example of multi-signed transaction. The accounts permission have assigned as in [UpdateAccountPermission](#updateaccountpermission) section, please check for reference.
```shell
wallet> SendCoin TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE 10
{
	"raw_data":{
		"contract":[
	···
	"raw_data_hex":"0a029ca12208432ed1fe1357ff7f40c0c484f19a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a708a8481f19a30"
}
before sign transaction hex string is 0a83010a029ca12208432ed1fe1357ff7f40c0c484f19a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a708a8481f19a30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
2
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
1
Please input your password.
password: 
Current signWeight is:
{
	"result":{
		"code":"NOT_ENOUGH_PERMISSION"
	},
	"approved_list":[
		"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej"
	],
	"permission":{
		"operations":"7fff1fc0033e0000000000000000000000000000000000000000000000000000",
		"keys":[
			{
				"address":"TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej",
				"weight":1
			},
			{
				"address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
				"weight":1
			}
		],
		"threshold":2,
		"id":2,
		"type":"Active",
		"permission_name":"active12323"
	},
	"current_weight":1,
	"transaction":{
		"result":{
			"result":true
		},
		"txid":"ece603ec8ad11578450dc8adf29dd9d9833e733c313fe16a947c8c768f1e4483",
		"transaction":{
			"signature":[
				"990001e909e638bbaa5de9b392121971d25cabde1391f5e164cd8a14608812df01a273e867c2329b8adb233599c5d353c435e789c777fd3e0b9fe83f0737a91101"
			],
			"txID":"ece603ec8ad11578450dc8adf29dd9d9833e733c313fe16a947c8c768f1e4483",
			"raw_data":···,
			"raw_data_hex":"0a029ca12208432ed1fe1357ff7f40a2b3a7fb9a305a67080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a2802708a8481f19a30"
		}
	}
}
Please confirm if continue add signature enter y or Y, else any other
y
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
4
Please input your password.
password: 
after sign transaction hex string is 0a85010a029ca12208432ed1fe1357ff7f40a2b3a7fb9a305a67080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a2802708a8481f19a301241990001e909e638bbaa5de9b392121971d25cabde1391f5e164cd8a14608812df01a273e867c2329b8adb233599c5d353c435e789c777fd3e0b9fe83f0737a91101124141ba3ffe9c7bb1ed184df8bf635d8c987982b2f4b22c447666ac82726f4a97cb2ef4d3fabd64137b8d59239bd7173c74264733ed140ccd04934a88c438de1cab00
txid is ece603ec8ad11578450dc8adf29dd9d9833e733c313fe16a947c8c768f1e4483
Send 10 Sun to TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE successful !!
```
A`permission_id` is always required, it is "0" by default, which means this transaction only needed to be sign by owner. In the example above, we enter "2" to make a multi-signed transaction this time, needs the two accounts assigned `actives` permission in [UpdateAccountPermission](#updateaccountpermission) section above to sign this transaction.

In the example, we picked the account `TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej` to sign first,
after that, it asks you if want to add another sign 
,enter y and pick the account `TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE` to finish multi-signing.

The weight of each account is 1 and the granting threshold is 2. When the requirements are met, the transaction is done successfully! This example shows how to complete a multi-signed transaction using the same client. When using multiple clients, please refer to the following command.

#### AddTransactionSign
Use the instruction addTransactionSign according to the obtained transaction hex string if signing at multiple cli.
```shell
wallet> addtransactionsign 0a83010a0241aa2208b2d2c13c86e8bd884098acb1cf9a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a30
Please input permission id.
0
Please choose your key for sign.
The 1th keystore file name is UTC--2022-06-28T06-52-56.928000000Z--TB9qhqbev6DpX8mxdf3zDdtSQ6GC6Vb6Ej.json
The 2th keystore file name is .DS_Store
The 3th keystore file name is UTC--2022-04-06T09-43-20.710000000Z--TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8.json
The 4th keystore file name is UTC--2022-04-07T09-03-38.307000000Z--TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE.json
Please choose between 1 and 4
3
Please input your password.
password: 
{
	"signature":[
		"dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201"
	],
	"txID":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"amount":10,
						"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
						"to_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE"
					},
					"type_url":"type.googleapis.com/protocol.TransferContract"
				},
				"type":"TransferContract"
			}
		],
		"ref_block_bytes":"41aa",
		"ref_block_hash":"b2d2c13c86e8bd88",
		"expiration":1656434882649,
		"timestamp":1656413188328
	},
	"raw_data_hex":"0a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a30"
}
Transaction hex string is 0a83010a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a301241dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201
```


After signing, the users will need to broadcast final transactions manually.

#### BroadcastTransaction

Broadcast the transaction, where the transaction is in hex string format.
```shell
wallet> broadcasttransaction 0a83010a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a301241dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201
BroadcastTransaction successful !!!
```

#### GetTransactionApprovedList
Get signature information according to transactions.
```shell
wallet> getTransactionApprovedList
0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101
{
	"result":{
		
	},
	"approved_list":[
		"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8"
	],
	"transaction":{
		"result":{
			"result":true
		},
		"txid":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
		"transaction":{
			"signature":[
				"dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201"
			],
			"txID":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
			"raw_data":{
				"contract":[
					{
						"parameter":{
							"value":{
								"amount":10,
								"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
								"to_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE"
							},
							"type_url":"type.googleapis.com/protocol.TransferContract"
						},
						"type":"TransferContract"
					}
				],
				"ref_block_bytes":"41aa",
				"ref_block_hash":"b2d2c13c86e8bd88",
				"expiration":1656434882649,
				"timestamp":1656413188328
			},
			"raw_data_hex":"0a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a30"
		}
	}
}

```


---

### On-ChainInquire

Here are all the on-chain inquire commands ：

- [GetNextMaintenanceTime](#getnextmaintenancetime)
- [ListNodes](#listnodes)
- [GetBlock](#getblock)
- [GetBlockbyID](#getblockbyid)
- [GetBlockbyLatestNum](#getblockbylatestnum)
- [GetBlockbyLimitNext](#getblockbylimitnext)
- [GetTransactionbyID](#gettransactionbyid)
- [GetTransactionCountbyBlockNum](#gettransactioncountbyblocknum)
- [GetTransactionInfobyID](#gettransactioninfobyid)
- [GetTransactionInfobyBlockNum](#gettransactioninfobyblocknum)
- [GetTransactionSignWeight](#gettransactionsignweight)

#### GetNextMaintenanceTime

Get the start time of the next maintain period
```
wallet> GetNextMaintenanceTime
Next maintenance time is : 2022-06-29 16:40:00
```
#### ListNodes

Get other peers' information
```
wallet> listnodes
IP::1.23.456.789
Port::12345
IP::2.345.67.89
Port::12345
IP::345.678.901.234
Port::12345
···
```
#### GetBlock

Get the block by block height; if you do not pass the parameter, get the latest block
```shell
wallet> getblock
Get current block !!!
{
	"block_header":{
		"raw_data":{
			"number":27774469,
			"txTrieRoot":"0000000000000000000000000000000000000000000000000000000000000000",
			"witness_address":"TQuzjxWcqHSh1xDUw4wmMFmCcLjz4wSCBp",
			"parentHash":"0000000001a7ce048eb88d7c3c5e9c5f8e93a6cc568f47140e243d00d0f9280a",
			"version":24,
			"timestamp":1656919215000
		},
		"witness_signature":"3af25276891b1cf7f9f72e63ad956b50e5819fb3fa6f0b6393ed092e53a90a5438620b92b5d499e0068c6775b723e3c90677157b3e9f7b8933d1e863716145f500"
	}
}
```
#### GetBlockbyID

Get block based on blockID（block hash）
```
wallet> getblockbyid [blockID]
```
```shell
wallet> getblockbyid 0000000001a7cd54ee2b302cfd443cccec78e55a31902d2e7ea47e737c1a5ede
{
	"block_header":{
		"raw_data":{
			"number":27774292,
			"txTrieRoot":"a60f8cb160d06d5279cb463925274e18fec37f0414c4d8fdc4fb2299ccb0a8bf",
			"witness_address":"TGsdxpHNJaxsVNFFdb4R6Rib1TsKGon2Wp",
			"parentHash":"0000000001a7cd53685867286b17fa0f2389e1d3026bea0a0019c5fc37f873cb",
			"version":24,
			"timestamp":1656918678000
		},
		"witness_signature":"a93db1a8d989c6637d587369de2872a008f14d1df8f0aaeda8a54c324a44c269367ea31daf623834fd6a4ef3f6150ab8d370adff1df6c0e8c96af9cf34408d5600"
	},
	···

```
#### GetBlockByLatestNum

Get the latest n blocks, where 0 < n < 100
```
wallet> getblockbylatestnum [n]
```
#### GetBlockByLimitNext

Get the block in a set range by block height. `startBlock`is the starting block height, `endBlock`is the ending block height.
```
wallet> GetBlockByLimitNext [startBlock, endBlock]
```
```shell
wallet> getblockbylimitnext 27774670 27774674
[
	{
		"block_header":{
			"raw_data":{
				"number":27774670,
				"txTrieRoot":"0eb9ba48deda22fafa613c0aefa6d3e0b21261ad82a126ce99a6b80e8b68045c",
				"witness_address":"TVKfvNUMcZdZbxhPLb2CkQ4nyUUhvwhv1b",
				"parentHash":"0000000001a7cecd7a2cdc58fdfd2edbfeaeb530958879bf1a299cc30043cd0b",
				"version":24,
				"timestamp":1656919824000
			},
			"witness_signature":"ee6653289e24edd24d70f4975e12934573d6e798a2a5c5e26e0b13bc6d25138c49a0f55fb0e9a5c503622b5877811403577a5e278528293d05c5f0b9d5d5542401"
		},
···
```
#### GetTransactionbyID

Get transaction information based on transaction id (hash)
```
wallet> GetTransactionById [transactionID]
```
#### GetTransactionCountbyBlockNum

Get how many transactions contains in a block based on block height, see below
```
wallet> gettransactioncountbyblocknum 27633562
The block contains 4 transactions
```

#### GetTransactionInfobyID

Get transaction-info based on transaction id, generally used to check the result of a smart contract trigger
```
wallet> gettransactioninfobyid 6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87
{
	"id": "6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
	"blockNumber": 27609041,
	"blockTimeStamp": 1656417906000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 265
	}
}
```

#### GetTransactionInfobyBlockNum

Get the list of transaction information in the block based on the block height
```
wallet> gettransactioninfobyblocknum [blockNum]
```
#### GetTransactionSignWeight
Get the sign weight by transaction hex string.
```
>getTransactionSignWeight 
0a83010a0241aa2208b2d2c13c86e8bd8840d9f0d9d99a305a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541babecec4d9f58f0df77f0728b9c53abb1f21d684121541e8bd653015895947cec33d1670a88cf67ab277b9180a70e8e1adcf9a301241dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201
```
The information displays as follows:

```
{
	"result":{
		
	},
	"approved_list":[
		"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8"
	],
	"permission":{
		"keys":[
			{
				"address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
				"weight":1
			}
		],
		"threshold":1,
		"permission_name":"owner"
	},
	"current_weight":1,
	"transaction":{
		"result":{
			"result":true
		},
		"txid":"6e1d2460796f717b701e355734ac0e4e8b32e14c24ce569a60ad3f63afe46c87",
		"transaction":{
			"signature":[
				"dbfe007bb44e8db164f4c0cf9b586a8d6a65f0612c4d9ec5350adeae6cd97c7874e7254bbf4156b545a90c34e48c8f28bdb5c8f9258514233b9201b2844d7f9201"
			],
			···
		}
	}
}
```


---

### SmartContract
Below, please find all the commands for smart contract interactions:

- [DeployContract](#deploycontract)
- [TriggerContract](#triggercontract)
- [TriggerConstantContract](#triggerconstantcontract)
- [EstimateEnergy](#estimateenergy)
- [GetContract](#getcontract)
- [UpdateEnergyLimit](#updateenergylimit)
- [UpdateSetting](#updatesetting)


#### DeployContract
```shell 
wallet> DeployContract [ownerAddress] [contractName] [ABI] [byteCode] [constructor] [params] [isHex] [fee_limit] [consume_user_resource_percent] [origin_energy_limit] [value] [token_value] [token_id](e.g: TRXTOKEN, use # if don't provided) <library:address,library:address,...> <lib_compiler_version(e.g:v5)> library:address,...>
```

* `OwnerAddress`is the address of the account that initiated the transaction, optional, considered as the address of the login account by default.
* `contractName` is the name of smart contract.
* `ABI` is ABI code generated when compiling.
* `byteCode` is byte code generated when compiling.
* `constructor`, `params`, `isHex` These three parameters define the format of the bytecode, which determines the way to parse byteCode from parameters.
* `fee_limit` determines the limit of consumed TRX for each transaction.
* `consume_user_resource_percent` is the percentage of user consumed resource, in the range between [0, 100%].
* `origin_energy_limit` is the most amount of developer energy consumed by triggering the contract once.
* `value` is the amount of trx transferred to the contract account.
* `token_value` is the number of TRC-10 token.
* `token_id` is TRC-10 Id.

Example:
```shell
wallet> deployContract normalcontract544 [{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name": "findArgsByIndexTest","outputs":[{"name":"z","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]
608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029 # # false 1000000000 75 50000 0 0 #
```
Get the result of the contract execution with the getTransactionInfoById command:
```shell
wallet> getTransactionInfoById 4978dc64ff746ca208e51780cce93237ee444f598b24d5e9ce0da885fb3a3eb9
{
    "id": "8c1f57a5e53b15bb0a0a0a0d4740eda9c31fbdb6a63bc429ec2113a92e8ff361",
    "fee": 6170500,
    "blockNumber": 1867,
    "blockTimeStamp": 1567499757000,
    "contractResult": [
        "6080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029"
    ],
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "receipt": {
        "energy_fee": 6170500,
        "energy_usage_total": 61705,
        "net_usage": 704,
        "result": "SUCCESS"
    }
}
```

#### TriggerContract
The command is used to trigger smart contract that deployed.
```shell
wallet> TriggerContract [ownerAddress] [contractAddress] [method] [args] [isHex] [fee_limit] [value] [token_value] [token_id]
```

* `OwnerAddress `The address of the account that initiated the transaction, optional, default value is the address of the login account.
* `ContractAddress` is the smart contract address.
* `method` is the name of the function and parameters, please refer to the example below.
* `args` is a parameter for placeholding, pass '#' instead when `method` does not need extra parameters.
* `isHex` controls the format of the parameters method and args, whether they are in hex string or not.
* `fee_limit` is the most amount of trx allows for consumption.
* `token_value` indicate the number of TRC-10 token.
* `token_id` the TRC-10 token id, If not, use ‘#’ instead.

Here is an example:
```shell
wallet> triggerContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG findArgsByIndexTest(uint256) 0 false
1000000000 0 0 #
```
Get the result of the contract execution with the getTransactionInfoById command,
```shell
wallet> getTransactionInfoById 7d9c4e765ea53cf6749d8a89ac07d577141b93f83adc4015f0b266d8f5c2dec4
{
    "id": "de289f255aa2cdda95fbd430caf8fde3f9c989c544c4917cf1285a088115d0e8",
    "fee": 8500,
    "blockNumber": 2076,
    "blockTimeStamp": 1567500396000,
    "contractResult": [
        ""
    ],
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "receipt": {
        "energy_fee": 8500,
        "energy_usage_total": 85,
        "net_usage": 314,
        "result": "REVERT"
    },
    "result": "FAILED",
    "resMessage": "REVERT opcode executed"
}
```

#### TriggerConstantContract
Invoke the readonly function (modified by the view or pure modifier) of a contract for contract data query; or Invoke the non-readonly function of a contract for predicting whether the transaction can be successfully executed or estimating the energy consumption.

```
wallet> TriggerConstantContract ownerAddress(use # if you own) contractAddress method args isHex [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]

```

* `ownerAddress` Owner address that triggers the contract. If it is the login account, please input #.
* `contractAddress` Smart contract address.
* `method` Function call.
* `args` Parameters, if there is no parameter of `method`, please input #. 
* `isHex` `args`is hex string or not。
* `value` TRX amount to be transferred. Optional, if no value, # can be inplaced.
* `token_value` TRC-10 token amount to be transferred. Optional, if no value, # can be inplaced.
* `token_id` TRC-10 token id to be transferred. Optional, if no value, # can be inplaced.

Example:
```shell
wallet> TriggerConstantContract TTGhREx2pDSxFX555NWz1YwGpiBVPvQA7e  TVSvjZdyDSNocHm7dP3jvCmMNsCnMTPa5W transfer(address,uint256) 0000000000000000000000002ce5de57373427f799cc0a3dd03b841322514a8c00000000000000000000000000000000000000000000000000038d7ea4c68000 true

transfer(address,uint256):a9059cbb
Execution result = {
	"constant_result": [
		"0000000000000000000000000000000000000000000000000000000000000001"
	],
	"result": {
		"result": true
	},
	"energy_used": 13253,
	"logs": [
		{
			"address": "LUijWGF4iFrT7hV37Q2Q45DU5TUBvVZb7",
			"topics": [
				"ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
				"000000000000000000000000bdc8ee51fdd1b1e01d71f836481828f88463c838",
				"0000000000000000000000002ce5de57373427f799cc0a3dd03b841322514a8c"
			],
			"data": "00000000000000000000000000000000000000000000000000038d7ea4c68000"
		}
	]
}
```
#### EstimateEnergy
Estimate the energy required for the successful execution of smart contract transactions. But for FullNode, enabling the wallet/estimateEnergy API is optional. So please pay attention that when developers call wallet/estimateEnergy, if the error message shows that the node does not support this function when calling the new API (this node does not support estimate energy), it is recommended to continue using the wallet/triggerconstantcontract API to estimate energy consumption.

```
wallet> EstimateEnergy ownerAddress contractAddress method args isHex [value token_value token_id]
```

* `ownerAddress` Owner address that triggers the contract. If it is the login account, please input #.
* `contractAddress` Smart contract address.
* `method` Function call.
* `args` Parameters, if there is no parameter of `method`, please input #. 
* `isHex` `args`is hex string or not。
* `value` TRX amount to be transferred. Optional, if no value, # can be inplaced.
* `token_value` TRC-10 token amount to be transferred. Optional, if no value, # can be inplaced.
* `token_id` TRC-10 token id to be transferred. Optional, if no value, # can be inplaced.


Example:

```shell
wallet> EstimateEnergy TTGhREx2pDSxFX555NWz1YwGpiBVPvQA7e  TVSvjZdyDSNocHm7dP3jvCmMNsCnMTPa5W transfer(address,uint256) 0000000000000000000000002ce5de57373427f799cc0a3dd03b841322514a8c00000000000000000000000000000000000000000000000000038d7ea4c68000 true

transfer(address,uint256):a9059cbb
Estimate energy result = {
	"result": {
		"result": true
	},
	"energy_required": 14910
}
```



#### GetContract
Get the smart contract info by its address.
```
wallet> GetContract [contractAddress]
```

Example:
```shell
wallet> GetContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
{
    "origin_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
    "contract_address": "TJMKWmC6mwF1QVax8Sy2AcgT6MqaXmHEds",
    "abi": {
        "entrys": [
            {
                "name": "findArgsByIndexTest",
                "inputs": [
                    {
                        "name": "i",
                        "type": "uint256"
                    }
                ],
                "outputs": [
                    {
                        "name": "z",
                        "type": "uint256"
                    }
                ],
                "type": "Function",
                "stateMutability": "Nonpayable"
            }
        ]
    },
    "bytecode": "608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029",
    "consume_user_resource_percent": 75,
    "name": "normalcontract544",
    "origin_energy_limit": 50000,
    "code_hash": "23423cece3b4866263c15357b358e5ac261c218693b862bcdb90fa792d5714e6"
}
```

#### UpdateEnergyLimit
Update parameter energy limit，parameter are the same as above.
```shell
wallet> UpdateEnergyLimit [ownerAddress] [contract_address] [energy_limit]
```
#### UpdateSetting
Update parameter of energy consume percentage per user
```shell
wallet> UpdateSetting [ownerAddress] contract_address consume_user_resource_percent
```



---
### TRC-10

Below, please find all the commands for TRC-10:

- [AssetIssue](#assetissue)
- [UpdateAsset](#updateasset)
- [TransferAsset](#transferasset)
- [ParticipateAssetissue](#participateassetissue)
- [UnfreezeAsset](#unfreezeasset)
- [ListAssetIssue](#listassetissue)
- [GetAssetIssuebyAccount](#getassetissuebyaccount)
- [GetAssetIssuebyID](#getassetissuebyid)
- [GetAssetIssuebyName](#getassetissuebyname)
- [GetAssetIssueListbyName](#getassetissuelistbyname)


#### AssetIssue
Each account is allowed to issue only **ONE** TRC-10 token.

```shell
wallet> AssetIssue [OwnerAddress] [AssetName] [AbbrName] [TotalSupply] [TrxNum] [AssetNum] [Precision] [StartDate] [EndDate] [Description Url] [FreeNetLimitPerAccount] [PublicFreeNetLimit] [FrozenAmount0] [FrozenDays0] [...] [FrozenAmountN] [FrozenDaysN]
```
`OwnerAddress` (optional) is the address of the account which initiated the transaction. Default: the address of the login account.

`AssetName` is the name of the issued TRC-10 token.

`AbbrName` is the abbreviation of TRC-10 token you want to issue.

`TotalSupply` is total issuing amount of TRC-10 token.

* TotalSupply = Account Balance of Issuer + All Frozen Token Amount 
* Account Balance Of Issuer: balance at the time of issuance
* All Frozen Token Amount: Before asset transfer and the issuance

`TrxNum`, `AssetNum` are two parameters determine the exchange rate when the token is issued. 

* Exchange Rate = TrxNum / AssetNum 
* `AssetNum`: Unit in the base unit of the issued token 
* `TrxNum`: Unit in SUN (0.000001 TRX)

`Precision` indicates how many decimal places there is.

`FreeNetLimitPerAccount` determines the maximum amount of bandwidth each account is allowed to use. Token issuers can freeze TRX to obtain bandwidth (TransferAssetContract only)

`PublicFreeNetLimit` is the maximum total amount of bandwidth which is allowed to use for all accounts. Token issuers can freeze TRX to obtain bandwidth (TransferAssetContract only)

`StartDate`, `EndDate` is the start and end date of token issuance. Within this period time, other users can participate in token issuance.

`FrozenAmount0`, `FrozenDays0` determines the amount and days of token freeze. `FrozenAmount0`: Must be bigger than 0. `FrozenDays0`: Must between 1 and 3652.

Example:
```shell
wallet> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
wallet> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # View published information
{
    "assetIssue": [
        {
            "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "name": "TestTRX",
            "abbr": "TRX",
            "total_supply": 75000000000000000,
            "frozen_supply": [
                {
                    "frozen_amount": 10000,
                    "frozen_days": 1
                },
                {
                    "frozen_amount": 10000,
                    "frozen_days": 10
                }
            ],
            "trx_num": 1,
            "precision": 2,
            "num": 1,
            "start_time": 1570000200000,
            "end_time": 1594396800000,
            "description": "just for test121212",
            "url": "www.test.com",
            "free_asset_net_limit": 100,
            "public_free_asset_net_limit": 100000,
            "id": "1000001"
        }
    ]
}
```
#### UpdateAsset
```
wallet> UpdateAsset [OwnerAddress] [newLimit] [newPublicLimit] [description url]
```
Specific meaning of the parameters are the same as they are in AssetIssue.

Example:
```shell
wallet> UpdateAsset 1000 1000000 "change description" www.changetest.com
wallet> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # to check the modified information
{
    "assetIssue": [
        {
            "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "name": "TestTRX",
            "abbr": "TRX",
            "total_supply": 75000000000000000,
            "frozen_supply": [
                {
                    "frozen_amount": 10000,
                    "frozen_days": 1
                },
                {
                    "frozen_amount": 10000,
                    "frozen_days": 10
                }
            ],
            "trx_num": 1,
            "precision": 2,
            "num": 1,
            "start_time": 1570000200000,
            "end_time": 1594396800000,
            "description": "change description",
            "url": "www.changetest.com",
            "free_asset_net_limit": 1000,
            "public_free_asset_net_limit": 1000000,
            "id": "1000001"
        }
    ]
}
```
#### TransferAsset
```
> TransferAsset [OwnerAddress] [ToAddress] [AssertID] [Amount]
```
`OwnerAddress` (optional) is the address of the account which initiated the transaction. By default, the address of the login account.

`ToAddress` is the address of the target account.

`AssertName` is the TRC-10 token ID. Example: 1000001

`Amount` is the number of TRC10 token to transfer with.

Example:
```shell
wallet> TransferAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 1000001 1000
wallet> getaccount TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz  # to check target account information after the transfer
address: TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz
    assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```
#### ParticipateAssetissue
```
> ParticipateAssetIssue [OwnerAddress] [ToAddress] [AssetID] [Amount]
```
`OwnerAddress` (optional) is the address of the account which initiated the transaction. Default: the address of the login account.

`ToAddress` is the account address of TRC10 issuers.

`AssertName` is the TRC-10 token ID. Example: 1000001

`Amount` is the number of TRC10 token to transfers with.

The participation process must happen during the release of TRC10, otherwise an error may occur.

Example:
```shell
wallet> ParticipateAssetIssue TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 1000001 1000
wallet> getaccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  # View remaining balance
address: TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```
#### UnfreezeAsset

To unfreeze all TRC10 token which are supposed to be unfrozen after the freezing period.
```
wallet> unfreezeasset [OwnerAddress]
```
#### ListAssetIssue

Obtain all of the published TRC10 token information.
```shell
wallet> listassetissue
{
	"assetIssue": [
		{
			"owner_address": "TMWXhuxiT1KczhBxCseCDDsrhmpYGUcoA9",
			"name": "tronlink_token",
			"abbr": "tronlink_token",
			"total_supply": 1000000000000000,
			"frozen_supply": [
				{
					"frozen_amount": 1,
					"frozen_days": 1
				}
			],
			"trx_num": 1,
			"precision": 6,
			"num": 1,
			"start_time": 1574757000000,
			"end_time": 1757595000000,
			"description": "Description",
			"url": "https://blog.csdn.net/u010270891/article/details/82978260",
			"free_asset_net_limit": 1000,
			"public_free_asset_net_limit": 2000,
			"id": "1000001"
		},
···
```
#### GetAssetIssuebyAccount

Obtain TRC10 token information based on owner address.
```
wallet> getassetissuebyaccount [owneraddress]
```
```shell
wallet> getassetissuebyaccount TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN
{
	"assetIssue": [
		{
			"owner_address": "TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN",
			"name": "h00966",
			"abbr": "h00966",
			"total_supply": 100000000000,
			"trx_num": 1000000,
			"precision": 6,
			"num": 1000000,
			"start_time": 1656374400000,
			"end_time": 1656460800000,
			"description": "Automated gaming platform. 
TRC10 token h0966.
More info on website.  TRC10 token h0966.
More info on website.  More info on website.",
			"url": "https://h00966.com",
			"id": "1004901"
		}
	]
}
```

#### GetAssetIssuebyID

Obtain TRC10 token Information based on token ID.
```shell
wallet> GetAssetIssueById 1004901
{
	"owner_address": "TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN",
	"name": "h00966",
	"abbr": "h00966",
	"total_supply": 100000000000,
	"trx_num": 1000000,
	"precision": 6,
	"num": 1000000,
	"start_time": 1656374400000,
	"end_time": 1656460800000,
	"description": "Automated gaming platform. 
TRC10 token h0966.
More info on website.TRC10 token h0966.
More info on website.More info on website.",
	"url": "https://h00966.com",
	"id": "1004901"
}
```

#### GetAssetIssuebyName

Obtain TRC10 token Information based on token names.
```shell
wallet> GetAssetIssueByname h00966
{
	"owner_address": "TUwjpfqW7NG6BF3GCTrKy1aDvfchwSG4tN",
	"name": "h00966",
	"abbr": "h00966",
	"total_supply": 100000000000,
	"trx_num": 1000000,
	"precision": 6,
	"num": 1000000,
	"start_time": 1656374400000,
	"end_time": 1656460800000,
	"description": "Automated gaming platform. 
TRC10 token h0966.
More info on website.TRC10 token h0966.
More info on website.More info on website.",
	"url": "https://h00966.com",
	"id": "1004901"
}
```

#### GetAssetIssueListbyName

Obtain a list of TRC10 token information based on names.
```
wallet> GetAssetIssueListByName ROFLOTOKEN
{
	"assetIssue": [
		{
			"owner_address": "TLvQSVH9Hm7kxLFtTP228fN6pCrHmtVjpb",
			"name": "ROFLOTOKEN",
			"abbr": "roflotoken",
			"total_supply": 10000000000000000,
			"trx_num": 1000000,
			"precision": 6,
			"num": 100000000,
			"start_time": 1656349200000,
			"end_time": 1656435600000,
			"description": "roflotoken.com",
			"url": "https://haxibaibo.com/",
			"id": "1004898"
		}
	]
}
```


### Governance
Any proposal-related operations, except for viewing operations, must be performed by committee members. Please find all the commands for Governance:

- [CreateProposal](#creatproposal)
- [ApproveProposal](#approveproposal)
- [DeleteProposal](#deleteproposal)
- [ListProposals](#listproposals)
- [ListProposalsPaginated](#listproposalspaginated)
- [GetProposal](#getproposal)
- [VoteWitness](#votewitness)
- [ListWitnesses](#listwitnesses)
- [GetBrokerage](#getbrokerage)
- [GetReward](#getreward)
- [UpdateBrokerage](#updatebrokerage)

#### CreatProposal
Initiate a proposal with createProposal.
```shell
wallet> createProposal [OwnerAddress] [id0] [value0] ... [idN] [valueN]
```
`OwnerAddress` (optional) is the address of the account which initiated the transaction. By default, it is the address of the login account.

`id0` is the serial number of TRON Network Parameter. Of which, each one has a serial number corresponded. Please refer to [http://tronscan.org/#/sr/committee](http://tronscan.org/#/sr/committee).

`Value0` is the modified value.

In the example, modification No.4 (modifying token issuance fee) costs 1000TRX as follows:
```shell
wallet> createProposal 4 1000
wallet> listproposals  # to check initiated proposal
{
    "proposals": [
        {
            "proposal_id": 1,
            "proposer_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
            "parameters": [
                {
                    "key": 4,
                    "value": 1000
                }
            ],
            "expiration_time": 1567498800000,
            "create_time": 1567498308000
        }
    ]
}
```
The corresponding id is 1.

#### ApproveProposal
Approve or disapprove a proposal using approveProposal.
```shell
wallet> approveProposal [OwnerAddress] [id] [is_or_not_add_approval]
```
`OwnerAddress` (optional) is the address of the account which initiated the transaction. Default: the address of the login account.

`id` is the ID of the initiated proposal. Example: 1.

`is_or_not_add_approval` is true for approve; is false for disapprove.

Example:
```shell
wallet> ApproveProposal 1 true  # in favor of the offer
wallet> ApproveProposal 1 false  # Cancel the approved proposal
```
#### DeleteProposal
```
wallet> deleteProposal [OwnerAddress] [proposalId]
```
`proposalId` is the ID of the initiated proposal. Example: 1.

The proposal must be canceled by the supernode that initiated the proposal.

Example：
```
wallet> DeleteProposal 1
```
#### ListProposals

Obtain a list of initiated proposals
```shell
wallet> listproposals
{
	"proposals": [
		{
			"proposal_id": 12732,
			"proposer_address": "TQ4eBJna51sew13DBLd7YjEHHHW7fkNzc2",
			"parameters": [
				{
					"key": 65,
					"value": 1
				},
				{
					"key": 66,
					"value": 1
				},
				{
					"key": 62,
					"value": 432000000
				}
			],
			"expiration_time": 1656491400000,
			"create_time": 1656490794000,
			"approvals": [
				"TQ4eBJna51sew13DBLd7YjEHHHW7fkNzc2"
			],
			"state": "DISAPPROVED"
		},
		{
···
```
#### ListProposalsPaginated

Use the paging mode to obtain the initiated proposal. 
```
wallet> ListProposalsPaginated [offset] [limit] 
```
`offset` is the number of proposals you want to skip.
`limit` is the number of proposals you want to be listed.
By default, all proposals would be listed from `proposal_id` 1 to date. The parameter in the example below means you want to skip the first 33 proposals and list the 2 proposals right after that.
```shell
wallet> listproposalspaginated 33 2
{
	"proposals": [
		{
			"proposal_id": 34,
			"proposer_address": "TEDguVMSsFw3HSizQXFK1BsrGWeuRMNN7t",
			"parameters": [
				{
					"key": 1,
					"value": 9997000000
				}
			],
			"expiration_time": 1582381200000,
			"create_time": 1582380477000,
			"state": "DISAPPROVED"
		},
		{
			"proposal_id": 35,
			"proposer_address": "TDkSQtBhZx7Ua8qvenM4zuH52u2BsYTwzc",
			"parameters": [
				{
					"key": 1,
					"value": 9997000000
				}
			],
			"expiration_time": 1582381200000,
			"create_time": 1582380498000,
			"state": "DISAPPROVED"
		}
	]
}
```
#### GetProposal

Obtain proposal information based on the proposal ID.
```shell
wallet> getproposal 34
{
	"proposal_id": 34,
	"proposer_address": "TEDguVMSsFw3HSizQXFK1BsrGWeuRMNN7t",
	"parameters": [
		{
			"key": 1,
			"value": 9997000000
		}
	],
	"expiration_time": 1582381200000,
	"create_time": 1582380477000,
	"state": "DISAPPROVED"
}
```

#### VoteWitness

Voting requires TRON Power, which can be obtained by freezing funds.
```
wallet> votewitness [SR(Super Representatives) address] [TRON Power Amount]
```

* The share calculation method is: 1 unit of share can be obtained for every 1TRX frozen.
* After unfreezing, previous vote will expire. You can avoid the invalidation of the vote by re-freezing and voting.

**NOTE** The TRON Network only records the status of your last vote, which means that each of your votes will overwrite all previous voting results.

For example:
```shell
wallet> freezeBalance 100000000 3 1 address  # Freeze 10TRX and acquire 10 units of TRON Power

wallet> votewitness [SR1] 4 [SR2] 6  # Cast 4 votes for SR1 and 6 votes for SR2 at the same time

wallet> votewitness [SR1] 10  # Voted 10 votes for SR1
```
The final result of the above command was 10 votes for SR1 and 0 vote for SR2.

#### ListWitnesses

Get all miner node information
```shell
wallet> listwitnesses
{
	"witnesses": [
		{
			"address": "TPffmvjxEcvZefQqS7QYvL1Der3uiguikE",
			"voteCount": 324999518,
			"url": "http://sr-26.com",
			"totalProduced": 414028,
			"totalMissed": 20,
			"latestBlockNum": 27638663,
			"latestSlotNum": 552169224,
			"isJobs": true
		},
		{
			"address": "TFFLWM7tmKiwGtbh2mcz2rBssoFjHjSShG",
			"voteCount": 324759460,
			"url": "http://sr-27.com",
			"totalProduced": 414144,
			"totalMissed": 16,
			"latestBlockNum": 27638664,
			"latestSlotNum": 552169225,
			"isJobs": true
		},
···
```

#### GetBrokerage
View the ratio of brokerage of the SR(Super Representatives).

After voting for the super representative, you will receive the rewards. The super representative has the right to decide the ratio of brokerage. The default ratio is 20%, and the super representative can adjust it.

By default, if a super representative is rewarded, he will receive 20% of the whole rewards, and 80% of the rewards will be distributed to his voters.


`OwnerAddress` is the address of the SR's account, it is a base58check type address.
```shell
wallet> getbrokerage TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
The brokerage is : 20
```

#### GetReward
Query unclaimed reward.

`OwnerAddress` is the address of the voter's account, it is a base58check type address.
```shell
wallet> getreward TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8
The reward is : 0
``` 


#### UpdateBrokerage
Update the ratio of brokerage, this command is usually used by a super representative account.
``` shell
wallet> updateBrokerage [OwnerAddress] [brokerage]
```
`OwnerAddress` is the address of the super representative's account, it is a base58check type address.

`brokerage` is the ratio of brokerage you want to update to, the limit of it: 0-100.

For example:
```shell
wallet> updateBrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h 30
```

---
### DEX

The trading and price fluctuations of trading pairs are in accordance with the [Bancor Agreement](https://cryptopapers.info/assets/pdf/bancor.pdf).

Here are all the commands for DEX:

- [ExchangeCreate](#exchangecreate)
- [ExchangeInject](#exchangeinject)
- [ExchangeTransaction](#exchangetransaction)
- [ExchangeWithdraw](#exchangewithdraw)
- [ListExchanges](#listexchanges)
- [ListExchangesPaginated](#listexchangespaginated)
- [MarketSellAsset](#marketsellasset)
- [MarketCancelOrder](#marketcancelorder)
- [GetMarketOrderbyAccount](#getmarketorderbyaccount)
- [GetMarketOrderbyID](#getmarketorderbyid)
- [GetMarketPairList](#getmarketpairlist)
- [GetMarketOrderListbyPair](#getmarketorderlistbypair)
- [GetMarketPricebyPair](#getmarketpricebypair)

#### ExchangeCreate
Create a trading pair
```shell
wallet> exchangeCreate [OwnerAddress][first_token_id] [first_token_balance] [second_token_id] [second_token_balance]
```
`OwnerAddress` is the address of the account which initiated the transaction. Considered as the login account by default.

`First_token_id`, `first_token_balance` is the ID and amount of the first token.

`second_token_id`, `second_token_balance` is the ID and amount of the second token.

The ID is the ID of the issued TRC10 token. If it is TRX, the ID is "". The amount must be greater than 0, and less than 1,000,000,000,000,000.

Example:
```shell
wallet> exchangeCreate 1000001 10000 _ 10000
# Create trading pairs with the IDs of 1000001 and TRX, with amount 10000 for both.
```
#### ExchangeInject
Capital injection
```
wallet> exchangeInject [OwnerAddress] [exchange_id] [token_id] [quant]
```
`OwnerAddress` is the address of the account which initiated the transaction. Default: the address of the login account.

`exchange_id` is the ID of the trading pair to be funded.

`token_id, quant` is the token Id and quantity (unit in base unit) of capital injection.

When conducting a capital injection, depending on its quantity (quant), a proportion of each token in the trading pair will be withdrawn from the account, and injected into the trading pair. Depending on the difference in the balance of the transaction, the same amount of money for the same token would vary.

#### ExchangeTransaction
Making transaction
```shell
wallet> exchangeTransaction [OwnerAddress] [exchange_id] [token_id] [quant] [expected]
```
`OwnerAddress` is the address of the account which initiated the transaction. Default: the address of the login account.

`exchange_id` is the ID of the trading pair.

`token_id`, `quant` is the ID and quantity of tokens being exchanged, equivalent to selling.

`expected` is the expected quantity of another token. IT must be less than quant, or an error will be reported.

Example：
```
wallet> ExchangeTransaction 1 1000001 100 80
```
It is expected to acquire the 80 TRX by exchanging 1000001 from the trading pair ID of 1, and the amount is 100.(Equivalent to selling an amount of 100 tokenID - 1000001, at a price of 80 TRX, in trading pair ID - 1).

#### ExchangeWithdraw
```
wallet> exchangeWithdraw [OwnerAddress] [exchange_id] [token_id] [quant]
```
`OwnerAddress` is the address of the account which initiated the transaction. Default: the address of the login account.

`Exchange_id` is the ID of the trading pair to be withdrawn.

`Token_id`, `quant` is token Id and quantity (unit in base unit) of capital withdrawal.

When conducting a capital withdrawal, depending on its quantity (quant), a proportion of each token in the transaction pair is withdrawn from the trading pair, and injected into the account. Depending on the difference in the balance of the transaction, the same amount of money for the same token would vary.

You may obtain information on trading pairs by the following commands,

#### ListExchanges
List trading pairs
```shell
wallet> listexchanges
{
	"exchanges": [
		{
			"exchange_id": 14,
			"creator_address": "TCjuQbm5yab7ENTYb7tbdAKaiNa9Lrj4mo",
			"create_time": 1654154880000,
			"first_token_id": "1004852",
			"first_token_balance": 91,
			"second_token_id": "_",
			"second_token_balance": 110000000
		},
		{
			"exchange_id": 13,
			"creator_address": "TBpbKyKVUB1YLULrbhawUws69Gv33cmKDL",
			"create_time": 1648004214000,
			"first_token_id": "1000575",
			"first_token_balance": 991,
			"second_token_id": "1000184",
			"second_token_balance": 1010
		},
···
```

#### ListExchangesPaginated

List trading pairs by page
```
wallet> ListExchangesPaginated [offset] [limit]
```
`offset` is the number of exchange pair you want to skip.
`limit` is the number of exchange pair you want to be listed.

The parameters in the example below means to skip the first 3 exchange pairs and show the next 2 exchange pairs.
```shell
wallet> listexchangespaginated 3 2
{
	"exchanges": [
		{
			"exchange_id": 4,
			"creator_address": "TXmHTj3t5LXGvqGkr4jRNw7nf9GjquQ5yf",
			"create_time": 1601458377000,
			"first_token_id": "1000088",
			"first_token_balance": 1,
			"second_token_id": "_",
			"second_token_balance": 1
		},
		{
			"exchange_id": 5,
			"creator_address": "TTJJvoPKGVKnbUBPVTn1Zi8o6k3EfFDXVS",
			"create_time": 1602578613000,
			"first_token_id": "1000091",
			"first_token_balance": 456125,
			"second_token_id": "_",
			"second_token_balance": 106968111
		}
	]
}
```
#### MarketSellAsset
Create an order to sell asset
```shell
wallet> MarketSellAsset [owner_address] [sell_token_id] [sell_token_quantity] [buy_token_id] [buy_token_quantity]
```
`OwnerAddress` is the address of the account that initiated the transaction.

`sell_token_id` and `sell_token_quantity` are the ID and amount of the token want to sell.

`buy_token_id`, `buy_token_quantity` determines the ID and amount of the token want to buy.

Example:
```shell
wallet> MarketSellAsset TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  1000001 200 _ 100    
```
Then we use the command getTransactionInfoById to check the result of the contract execution as below,
```shell
wallet> getTransactionInfoById 10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374   

{
	"id": "10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374",
	"blockNumber": 669,
	"blockTimeStamp": 1578983493000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 264
	}
} 
```
#### MarketCancelOrder
This command cancels the order.
```shell
wallet> MarketCancelOrder [owner_address] [order_id]
```
`owner_address` is the account address who have created the order.

`order_id` is the order id which want to cancel.

Example:
```shell
wallet> MarketCancelOrder TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0  
```
Get the result of the contract execution with the getTransactionInfoById command:
```shell
wallet> getTransactionInfoById b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27   
{
	"id": "b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27",
	"blockNumber": 1582,
	"blockTimeStamp": 1578986232000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 283
	}
}
```
#### GetMarketOrderbyAccount
Use this command to get the order created by account(just include active status).
```shell
wallet> GetMarketOrderByAccount [ownerAddress]
```
`ownerAddress` is the address of the account that created market order.

Example:
```shell
wallet> GetMarketOrderByAccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW   
{
	"orders": [
		{
			"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
			"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
			"create_time": 1578983490000,
			"sell_token_id": "_",
			"sell_token_quantity": 100,
			"buy_token_id": "1000001",
			"buy_token_quantity": 200,
			"sell_token_quantity_remain": 100
		}
	]
}  
```
#### GetMarketOrderbyID
Get the specific order by order_id
```shell
wallet> GetMarketOrderById [orderId]
```
Example:
```shell
wallet> GetMarketOrderById fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0   
{
	"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
	"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
	"create_time": 1578983490000,
	"sell_token_id": "_",
	"sell_token_quantity": 100,
	"buy_token_id": "1000001",
	"buy_token_quantity": 200,
}
```
#### GetMarketPairList
This command is to get market pair listed

```shell
wallet> getmarketpairlist
{
	"orderPair": [
		{
			"sell_token_id": "1000012",
			"buy_token_id": "_"
		},
		{
			"sell_token_id": "1000094",
			"buy_token_id": "1000095"
		},
		{
			"sell_token_id": "1000099",
			"buy_token_id": "1000100"
		},
···
```
#### GetMarketOrderListbyPair
This command is to get market order list by c pair,
```shell
wallet> GetMarketOrderListByPair [sell_token_id] [buy_token_id]
```
`sell_token_id` is the ID of the token want to sell.

`buy_token_id` is the ID of the token want to buy.

Example:
```shell
wallet> GetMarketOrderListByPair _ 1000001   
{
	"orders": [
		{
			"order_id": "fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0",
			"owner_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW",
			"create_time": 1578983490000,
			"sell_token_id": "_",
			"sell_token_quantity": 100,
			"buy_token_id": "1000001",
			"buy_token_quantity": 200,
			"sell_token_quantity_remain": 100
		}
	]
}
```
#### GetMarketPricebyPair
Use this command to get market price by exchange pair.
```shell
wallet> GetMarketPriceByPair [sell_token_id] [buy_token_id]
```
`sell_token_id` is the ID of the token want to sell.

`buy_token_id` is the ID of the token want to buy.

Example:
```shell
wallet> GetMarketPriceByPair _ 1000001   
{
	"sell_token_id": "_",
	"buy_token_id": "1000001",
	"prices": [
		{
			"sell_token_quantity": 100,
			"buy_token_quantity": 200
		}
	]
}
```


