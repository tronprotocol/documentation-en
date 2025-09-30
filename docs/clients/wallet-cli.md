# wallet-cli

## Introduction

**wallet-cli** is an interactive command-line wallet designed specifically for the **TRON** network. It allows you to sign and broadcast transactions and query on-chain data in a secure, local environment.

**wallet-cli** supports key management. It uses a symmetric encryption algorithm to encrypt your private key and stores it in a local Keystore file. Since **wallet-cli** does not store on-chain data, it communicates with your configured **java-tron** node via gRPC. The following diagram illustrates the process of using **wallet-cli** to sign and broadcast a TRX transfer transaction:

![avatar](https://i.imgur.com/NRKmZmE.png)

1. First, run the `Login` command to unlock the wallet.
2. Next, run the `SendCoin` command to send TRX.
3. **wallet-cli** builds and signs the transaction locally.
4. It then calls the **java-tron** node's `BroadcastTransaction` gRPC API to broadcast the transaction to the network.
5. After a successful broadcast, the **java-tron** node returns a transaction success result and an object containing the transaction hash.
6. Finally, **wallet-cli** displays the transaction hash to the user.

For detailed installation and running instructions, please visit: [GitHub Repository](https://github.com/tronprotocol/wallet-cli)

## Command-Line Operation Example

```
$ cd wallet-cli
$ ./gradlew build
$ ./gradlew run
> RegisterWallet 123456      (password = 123456)
> login 123456
> getAddress
address = TRfwwLDpr4excH4V4QzghLEsdYwkapTxnm'  # Back it up!
> BackupWallet 123456
priKey = 1234567890123456789012345678901234567890123456789012345678901234  # Back it up! (BackupWallet2Base64 option)
> getbalance
Balance = 0
> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
> getaccount TRfwwLDpr4excH4V4QzghLEsdYwkapTxnm
(Prints balance: 9999900000
"assetV2": [
    {
        "key": "1000001",
        "value": 74999999999980000
    }
],)
  # (AssetIssue costs 1000 TRX)
  # (You can query the TRX balance and other asset balances of any account)
> TransferAsset TWzrEZYtwzkAxXJ8PatVrGuoSNsexejRiM 1000001 10000
```



## Commands

**wallet-cli** supports the following command categories:

- [Key Management](#key-management)
- [On-chain Accounts](#on-chain-accounts)
- [Account Resources](#account-resources)
- [Transactions](#transactions)
- [Querying On-chain Data](#querying-on-chain-data)
- [Smart Contracts](#smart-contracts)
- [TRC-10 Assets](#trc-10-assets)
- [Governance](#governance)
- [Decentralized Exchange](#defi)
- [GasFree Support](#gasfree)
- [Other Utility Commands](#other)



<a id="key-management"></a>
### Key Management

#### Log Out - `Logout`
> Logs out of the current wallet account.

Example:
```
wallet> Logout
Logout successful !!!
```

#### Log in to All Accounts - `LoginAll`
> Multiple keystore accounts can be logged in with a single password.

Example:
```
wallet> loginall
Please input your password.
password:
Use user defined config file in current dir
WalletApi getRpcVsersion: 2
[========================================] 100%
The 1th keystore file name is TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
The 2th keystore file name is TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
The 3th keystore file name is TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
The 4th keystore file name is Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
The 5th keystore file name is TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose between 1 and 5
5
LoginAll successful !!!
```

#### Lock Account - `Lock`
> To use the lock feature for a logged-in account, you need to configure `lockAccount = true` in `config.conf`.
> The current logged-in account is locked, which means signing and transactions are not allowed.

Example:
```
wallet> lock
lock successful !!!
```

#### Unlock Account - `Unlock`
> To use the unlock feature for a logged-in account, you need to configure `lockAccount = true` in `config.conf`.
> A currently locked account can be unlocked. By default, it will lock again after 300 seconds. You can specify the number of seconds when unlocking.

Example:
```
wallet> unlock 60
Please input your password.
password:
unlock successful !!!
```

#### Generate Address - `GenerateAddress`
> Generates an address and prints the address and private key.

#### Generate Sub-Account - `GenerateSubAccount`
> Generates a sub-account using the mnemonic words in the wallet.

Example:
```
wallet> GenerateSubAccount
Please input your password.
password:

=== Sub Account Generator ===
-----------------------------
Default Address: TYEhEg7b7tXm92UDbRDXPtJNU6T9xVGbbo
Default Path: m/44'/195'/0'/0/1
-----------------------------

1. Generate Default Path
2. Change Account
3. Custom Path

Enter your choice (1-3): 1
mnemonic file : ./Mnemonic/TYEhEg7b7tXm92UDbRDXPtJNU6T9xVGbbo.json
Generate a sub account successful, keystore file name is TYEhEg7b7tXm92UDbRDXPtJNU6T9xVGbbo.json
generateSubAccount successful.
```

#### Reset Wallet - `ResetWallet`

> Use this command to delete all local wallet Keystore files and mnemonic files, and guide you to re-register or import a wallet.

Example:

```
wallet> resetwallet
User defined config file doesn't exists, use default config file in jar

Warning: Dangerous operation!
This operation will permanently delete the Wallet&Mnemonic files
Warning: The private key and mnemonic words will be permanently lost and cannot be recovered!
Continue? (y/Y to proceed, c/C to cancel):
y

Final confirmation:
Please enter: 'DELETE' to confirm the delete operation:
Confirm: (DELETE): DELETE
resetWallet successful !!!
Now, you can RegisterWallet or ImportWallet again. Or import the wallet through other means.
```

#### Register Wallet - `RegisterWallet`
> Registers your wallet, and you need to set a wallet password and generate an address and a private key.

#### Change Account Password - `ChangePassword`
> Changes the password of an account.

#### Modify Wallet Name - `ModifyWalletName new_wallet_name`

> Modifies the name of the wallet.

Example:
```
wallet> ModifyWalletName new-name
Modify Wallet Name successful !!
```

#### Import Wallet - `ImportWallet`
> Imports a wallet. You need to set a password and provide the private key in hexadecimal string format.

#### Import Wallet by Base64 - `ImportWalletByBase64`
> Imports a wallet. You need to set a password and provide the private key in Base64 format.

#### Import Wallet by Mnemonic - `ImportWalletByMnemonic`
> Imports a wallet. You need to set a password and provide the mnemonic words.

Example:
```
wallet> ImportWalletByMnemonic
Please input password.
password:
Please input password again.
password:
Please enter 12 words (separated by spaces) [Attempt 1/3]:
```

#### Export Wallet Mnemonic - `ExportWalletMnemonic`
> Exports the mnemonic words for the address in the wallet.

Example:
```
wallet> ExportWalletMnemonic
Please input your password.
password:
exportWalletMnemonic successful !!
a*ert tw*st co*rect mat*er pa*s g*ther p*t p*sition s*op em*ty coc*nut aband*n
```

#### Export Wallet Keystore - ExportWalletKeystore
> Exports the wallet keystore in TronLink wallet format.

Example:
```
wallet> ExportWalletKeystore tronlink /tmp
Please input your password.
password:
exported keystore file : /tmp/TYdhEg8b7tXm92UDbRDXPtJNU6T9xVGbbo.json
exportWalletKeystore successful !!
```

#### Import Wallet Keystore -     `ImportWalletByKeystore`
> Imports a TronLink wallet's keystore file into wallet-cli.

Example:
```
wallet> ImportWalletByKeystore tronlink /tmp/tronlink.json
Please input password.
password:
Please input password again.
password:
fileName = TYQq6zp51unQDNELmT4xKMWh5WLcwpCDZJ.json
importWalletByKeystore successful !!
```

#### Import Wallet by Ledger - ImportWalletByLedger
> Imports a Ledger-derived account into wallet-cli.

Example:
```
wallet> ImportWalletByLedger
((Note:This will pair Ledger to user your hardward wallet)
Only one Ledger device is supported. If you have multiple devices, please ensure only one is connected.
Ledger device found: Nano X
Please input password.
password:
Please input password again.
password:
-------------------------------------------------
Default Account Address: TAT1dA8F9HXGqmhvMCjxCKAD29YxDRw81y
Default Path: m/44'/195'/0'/0/0
-------------------------------------------------
1. Import Default Account
2. Change Path
3. Custom Path
Select an option: 1
Import a wallet by Ledger successful, keystore file : ./Wallet/Ledger-TAT1dA8F9HXGqmhvMCjxCKAD29YxDRw81y.json
You are now logged in, and you can perform operations using this account.
```

#### Backup Wallet - BackupWallet**
> Backs up your wallet. You need to enter the wallet password and export the private key in hexadecimal string format, for example: 1234567890123456789012345678901234567890123456789012345678901234

#### Backup Wallet (Base64) - BackupWallet2Base64**
> Backs up your wallet. You need to enter the wallet password and export the private key in Base64 format, for example: ch1jsHTxjUHBR+BMlS7JNGd3ejC28WdFvEeo6uUHZUU=

#### Clear Wallet Keystore - ClearWalletKeystore
> Clears the wallet keystore file of the logged-in account.

Example:
```
wallet> ClearWalletKeystore

Warning: Dangerous operation!
This operation will permanently delete the Wallet&Mnemonic files of the Address: TABWx7yFhWrvZHbwKcCmFLyPLWjd2dZ2Rq
Warning: The private key and mnemonic words will be permanently lost and cannot be recovered!
Continue? (y/Y to proceed):y

Final confirmation:
Please enter: 'DELETE' to confirm the delete operation:
Confirm: (DELETE): DELETE

File deleted successfully:
- /wallet-cli/Wallet/TABWx8yFhWrvZHbwKcCmFLyPLWjd2dZ2Rq.json
- /wallet-cli/Mnemonic/TABWx8yFhWrvZHbwKcCmFLyPLWjd2dZ2Rq.json
ClearWalletKeystore successful !!!
```

<a id="on-chain-accounts"></a>
### On-chain Accounts

#### Create Account - CreateAccount
> This command can create a new inactive address account and burn 1 TRX as a fee.

Example:
```
wallet> createaccount TDJ13zZzT3w91WMBm98gC3mwL7NbA6sQPA
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"owner_address":"TQLaB7L8o3ikjRVcN7tTjMZsRYPJ23XZbd",
						"account_address":"TDJ13zZzT3w91WMBm98gC3mwL7NbA6sQPA"
					},
					"type_url":"type.googleapis.com/protocol.AccountCreateContract"
				},
				"type":"AccountCreateContract"
			}
		],
		"ref_block_bytes":"91a4",
		"ref_block_hash":"2bfcd3bb597f3d40",
		"expiration":1745333676000,
		"timestamp":1745333618318
	},
	"raw_data_hex":"0a0291a422082bfcd3bb597f3d4040e0cff9efe5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe532"
}
Before sign transaction hex string is 0a84010a0291a422082bfcd3bb597f3d4040e0cff9efe5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe532
Please confirm and input your permission id, if input y/Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
The 2th keystore file name is TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
The 3th keystore file name is TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
The 4th keystore file name is Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
The 5th keystore file name is TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose between 1 and 5
1
After sign transaction hex string is 0a84010a0291a422082bfcd3bb597f3d404083bd9cfae5325a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a15419d9c2bb5ee381a4396dd49ce42292e756b2e5e4b12154124764e4674179d4578cfc4c833c1ac1a09f6ce56708e8df6efe5321241ce53add4f75fe1838aa7e0a4e2411b3bbfce1d2164d68dac18507ed87e22ae503f65592a1161640834b3c0cef43c28f20b2d335120cc78b6f745a82ea95e451100
TxId is 26d6fcdfdc0018097ec4166eb140e19ebd597bea2212579d2f6d921b0ad6e56f
CreateAccount successful !!
```

#### Set Account ID - `SetAccountId [owner_address] account_id`

> Sets a custom, unique identifier (Account ID) for an account.

Example:

```
> SetAccountId TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 100
```

#### Update Account - `UpdateAccount [owner_address] account_name`

> Changes the name of an account.

Example:

```
> UpdateAccount test-name
```

#### Get Account Information - `GetAccount`
> Retrieves account information based on the address.

#### Get Account Address - `GetAddress`
> Retrieves the address of the current logged-in account.

#### Get Account Balance - `GetBalance`
> Retrieves the balance of the current logged-in account.

#### Modify Account Permissions

##### How to Use `wallet-cli`'s Account Permission Management Feature?

Account Permission Management allows other users to access an account for better account management. There are three access types:

* `owner`: The access permission for the account owner.
* `active`: Access permissions for other account functions, as well as permissions for specific functions. If used for an SR, this does not include block production authorization.
* `witness`: Used exclusively for SRs, granting one of the users block production authorization.

Other users will be granted permissions.

```
> Updateaccountpermission TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 
{
  "owner_permission": {
    "type": 0,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      {
        "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
        "weight": 1
      }
    ]
  },
  "witness_permission": {
    "type": 1,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      {
        "address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
        "weight": 1
      }
    ]
  },
  "active_permissions": [
    {
      "type": 2,
      "permission_name": "active12323",
      "threshold": 2,
      "operations": "7fff1fc0033e0000000000000000000000000000000000000000000000000000",
      "keys": [
        {
          "address": "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR",
          "weight": 1
        },
        {
          "address": "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
          "weight": 1
        }
      ]
    }
  ]
}
```

Account `TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ` grants itself Owner access, and grants `TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR` and `TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP` Active access. Active access requires signatures from both accounts to take effect.

If the account is not a **Super Representative** (SR), you do not need to set the `witness_permission`, or an error will occur.


<a id="account-resources"></a>
### Account Resources

#### How to Freeze/Unfreeze Balance

After funds are frozen, you will get a corresponding amount of **TRON Power** (TP) and Bandwidth. TP can be used for voting, and Bandwidth can be used for transactions.

The usage and calculation rules for TP and Bandwidth will be introduced later in this document.

**The freeze operation is as follows:**

##### `freezev2` Resource

```
freezeBalanceV2 [OwnerAddress] frozen_balance [ResourceCode:0 BANDWIDTH,1 ENERGY,2 TRON_POWER]
```

- `OwnerAddress` - The account address initiating the transaction. This is optional and defaults to the address of the logged-in account.
- `frozen_balance` - The amount to freeze in sun (the smallest unit). The minimum value is 1,000,000 sun.
- `ResourceCode` - 0 represents BANDWIDTH; 1 represents ENERGY.

Example:
```
wallet> FreezeBalanceV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 1000000000000000 0
txid is 82244829971b4235d98a9f09ba67ddb09690ac2f879ad93e09ba3ec1ab29177d
wallet> GetTransactionById 82244829971b4235d98a9f09ba67ddb09690ac2f879ad93e09ba3ec1ab29177d
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "4faa3772fa3d3e4792e8126cafed2dc2c5c069cd09c29532f0119bc982bf356004772e16fad86e401f5818c35b96d214d693efab06997ca2f07044d4494f12fd01"
    ],
    "txID":"82244829971b4235d98a9f09ba67ddb09690ac2f879ad93e09ba3ec1ab29177d",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "frozen_balance":1000000000000000,
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.FreezeBalanceV2Contract"
                },
                "type":"FreezeBalanceV2Contract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671109891800,
        "timestamp":1671088291796
    },
    "raw_data_hex":"0a020000220819b59068c6058ff440d8ada5afd1305a5c083612580a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e747261637412200a154159e3741a68ec3e1ebba80ad809d5ccd31674236e1080809aa6eaafe30170d4fffea4d130"
}
```

After a freeze operation, the frozen funds will be transferred from the "Account Balance" to "Frozen."

You can view the frozen funds in your account information.

After unfreezing, the funds will be transferred back from "Frozen" to "Balance." Frozen funds cannot be used for transactions.

When you need to temporarily gain more TP or Bandwidth, you can freeze additional funds to receive extra TP and Bandwidth.
The unfreeze time will be postponed to 3 days after the last freeze operation.

After the freeze time expires, the funds can be unfrozen.

**The unfreeze operation is as follows:**

##### `unfreezev2` Resource

```
unfreezeBalanceV2 [OwnerAddress] unfreezeBalance ResourceCode(0 BANDWIDTH,1 ENERGY,2 TRON_POWER)
```

- `OwnerAddress` - The account address initiating the transaction. This is optional and defaults to the address of the logged-in account.
- `unfreezeBalance` - The amount to unfreeze in sun (the smallest unit).
- `ResourceCode` - 0 represents BANDWIDTH; 1 represents ENERGY.

Example:
```
wallet> UnFreezeBalanceV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 9000000 0
txid is dcfea1d92fc928d24c88f7f71a03ae8105d0b5b112d6d48be93d3b9c73bea634
wallet> GetTransactionById dcfea1d92fc928d24c88f7f71a03ae8105d0b5b112d6d48be93d3b9c73bea634
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "f73a278f742c11e8e5ede693ca09b0447a804fcb28ea2bfdfd8545bb05da7be44bd08cfaa92bd4d159178f763fcf753f28d5296bd0c3d4557532cce3b256b9da00"
    ],
    "txID":"dcfea1d92fc928d24c88f7f71a03ae8105d0b5b112d6d48be93d3b9c73bea634",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e",
                        "unfreeze_balance":9000000
                    },
                    "type_url":"type.googleapis.com/protocol.UnfreezeBalanceV2Contract"
                },
                "type":"UnfreezeBalanceV2Contract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671119916913,
        "timestamp":1671098316907
    },
    "raw_data_hex":"0a020000220819b59068c6058ff440f19e89b4d1305a5a083712560a36747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a6542616c616e63655632436f6e7472616374121c0a154159e3741a68ec3e1ebba80ad809d5ccd31674236e10c0a8a50470ebf0e2a9d130"
}
```

**Note: Currently, staking is only allowed using the v2 interface. If you still have unfrozen v1 assets, please use the method below to unfreeze them as soon as possible.**

```
> unfreezeBalance [OwnerAddress] ResourceCode(0 BANDWIDTH, 1 CPU) [receiverAddress]
```


#### Withdraw Expired Unfrozen Amounts - `withdrawExpireUnfreeze [OwnerAddress]`

- `OwnerAddress` - The account address initiating the transaction. This is optional and defaults to the address of the logged-in account.

Example:
```
wallet> withdrawexpireunfreeze TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
txid is e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
wallet> GetTransactionById e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "f8f02b5aa634b8666862a6d2ed68fcfd90afc616d14062952b0b09f0404d9bca6c4d3dc6dab082784950ff1ded235a07dab0d738c8a202be9451d5ca92b8eece01"
    ],
    "txID":"e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.WithdrawExpireUnfreezeContract"
                },
                "type":"WithdrawExpireUnfreezeContract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671122055318,
        "timestamp":1671100455315
    },
    "raw_data_hex":"0a020000220819b59068c6058ff44096e18bb5d1305a5a083812560a3b747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5769746864726177457870697265556e667265657a65436f6e747261637412170a154159e3741a68ec3e1ebba80ad809d5ccd31674236e7093b3e5aad130"
}
```

#### Cancel All Unfreezing - `cancelAllUnfreezeV2 [OwnerAddress]`

- `OwnerAddress` - The account address initiating the transaction. This is optional and defaults to the address of the logged-in account.

Example:
```
wallet> cancelAllUnfreezeV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
txid is e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
wallet> GetTransactionById e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "f8f02b5aa634b8666862a6d2ed68fcfd90afc616d14062952b0b09f0404d9bca6c4d3dc6dab082784950ff1ded235a07dab0d738c8a202be9451d5ca92b8eece01"
    ],
    "txID":"e5763ab8dfb1e7ed076770d55cf3c1ddaf36d75e23ec8330f99df7e98f54a147",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.CancelAllUnfreezeV2"
                },
                "type":"CancelAllUnfreezeV2Contract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671122055318,
        "timestamp":1671100455315
    },
    "raw_data_hex":"0a020000220819b59068c6058ff44096e18bb5d1305a5a083812560a3b747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5769746864726177457870697265556e667265657a65436f6e747261637412170a154159e3741a68ec3e1ebba80ad809d5ccd31674236e7093b3e5aad130"
}
```

#### Resources Delegation

##### Delegating Resources

```
delegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress [lock]
```

- `OwnerAddress` - The account address initiating the transaction。 Optional, defaults to the address of the logged-in account。
- `balance` - The amount to delegate, in the smallest unit, sun。 The minimum value is 1,000,000 sun。
- `ResourceCode` - 0 for BANDWIDTH; 1 for ENERGY。
- `ReceiverAddress` - The account address。
- `lock` - Defaults to `false`。 Set to `true` to lock the delegation for 3 days。
- `lock_period` - The maximum lock period for delegation。 It can be any time between (0, 86400] blocks。

Example:
```

wallet> DelegateResource TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 10000000 0 TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3 true 10000
txid is 363ac0b82b6ad3e0d3cad90f7d72b3eceafe36585432a3e013389db36152b6ed
wallet> GetTransactionById 363ac0b82b6ad3e0d3cad90f7d72b3eceafe36585432a3e013389db36152b6ed
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "1f57fd78456136faadc5091b47f5fd27a8e1181621e49129df6a4062499429fb48ee72e5f9a9ff5bfb7f2575f01f4076f7d4b89ca382d36af46a6fa4bc749f4301"
    ],
    "txID":"363ac0b82b6ad3e0d3cad90f7d72b3eceafe36585432a3e013389db36152b6ed",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "balance":10000000,
                        "receiver_address":"419a9afe56e155ef0ff3f680d00ecf19deff60bdca",
                        "lock":true,
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.DelegateResourceContract"
                },
                "type":"DelegateResourceContract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671120059226,
        "timestamp":1671098459216
    },
    "raw_data_hex":"0a020000220819b59068c6058ff440daf691b4d1305a720839126e0a35747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e44656c65676174655265736f75726365436f6e747261637412350a154159e3741a68ec3e1ebba80ad809d5ccd31674236e1880ade2042215419a9afe56e155ef0ff3f680d00ecf19deff60bdca280170d0c8eba9d130"
}
```

##### Undelegating Resources

```
unDelegateResource [OwnerAddress] balance ResourceCode(0 BANDWIDTH,1 ENERGY), ReceiverAddress
```

- `OwnerAddress` - The account address initiating the transaction。 Optional, defaults to the address of the logged-in account。
- `balance` - The amount to undelegate, in the smallest unit, sun。
- `ResourceCode` - 0 for BANDWIDTH; 1 for ENERGY。
- `ReceiverAddress` - The account address。

Example:
```
wallet> UnDelegateResource TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 1000000 0 TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3
txid is feb334794cf361fd351728026ccf7319e6ae90eba622b9eb53c626cdcae4965c
wallet> GetTransactionById feb334794cf361fd351728026ccf7319e6ae90eba622b9eb53c626cdcae4965c
{
    "ret":[
        {
            "contractRet":"SUCCESS"
        }
    ],
    "signature":[
        "85a41a4e44780ffbe0841a44fd71cf621f129d98e84984cfca68e03364f781aa7f9d44177af0b40d82da052feec9f47a399ed6e51be66c5db07cb13477dcde8c01"
    ],
    "txID":"feb334794cf361fd351728026ccf7319e6ae90eba622b9eb53c626cdcae4965c",
    "raw_data":{
        "contract":[
            {
                "parameter":{
                    "value":{
                        "balance":1000000,
                        "receiver_address":"419a9afe56e155ef0ff3f680d00ecf19deff60bdca",
                        "owner_address":"4159e3741a68ec3e1ebba80ad809d5ccd31674236e"
                    },
                    "type_url":"type.googleapis.com/protocol.UnDelegateResourceContract"
                },
                "type":"UnDelegateResourceContract"
            }
        ],
        "ref_block_bytes":"0000",
        "ref_block_hash":"19b59068c6058ff4",
        "expiration":1671120342283,
        "timestamp":1671098742280
    },
    "raw_data_hex":"0a020000220819b59068c6058ff4408b9aa3b4d1305a71083a126d0a37747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e44656c65676174655265736f75726365436f6e747261637412320a154159e3741a68ec3e1ebba80ad809d5ccd31674236e18c0843d2215419a9afe56e155ef0ff3f680d00ecf19deff60bdca7088ecfca9d130"
}
```


#### Getting Account Bandwidth - `GetAccountNet`
> Gets the usage of bandwidth。

#### Getting Account Resources - `GetAccountResource`
> Gets the usage of bandwidth and energy。

#### Getting Delegated Resource Information
`getDelegatedResource fromAddress toAddress`
> Gets the delegated resource information from `fromAddress` to `toAddress`。

`getDelegatedResourceAccountIndex address`
> Gets the resource information that `address` has delegated to other accounts。

#### Getting Delegated Resource Information using v2 API
`getDelegatedResourceV2 fromAddress toAddress`
> Gets the delegated resource information from `fromAddress` to `toAddress` using the v2 API。

- `fromAddress` - The account address initiating the delegation。
- `toAddress` - The account address receiving the delegation。

Example:
```
wallet> getDelegatedResourceV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3
{
	"delegatedResource": [
		{
			"from": "TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh",
			"to": "TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3",
			"frozen_balance_for_bandwidth": 10000000
		}
	]
}
```

`getDelegatedResourceAccountIndexV2 address`

> Gets the delegated resource information that the `address` has delegated to other accounts using the v2 API。

- `address` - The account address that initiated or received the delegation。

Example:
```
wallet> getDelegatedResourceAccountIndexV2 TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
{
	"account": "TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh",
	"toAccounts": [
		"TQ4gjjpAjLNnE67UFbmK5wVt5fzLfyEVs3"
	]
}
```

`getcandelegatedmaxsize ownerAddress type`
> Gets the maximum amount of resources `ownerAddress` can delegate (using `delegateResource`)。

- `ownerAddress` - The account address initiating the delegation。 Optional, defaults to the address of the logged-in account。
- `type` - 0 for Bandwidth, 1 for Energy。

Example:
```
wallet> getCanDelegatedMaxSize TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 0
{
	"max_size": 999999978708334
}
```

`getavailableunfreezecount ownerAddress`
> Gets the number of available unfreeze attempts for `ownerAddress` using `unfreezeBalanceV2`。

- `ownerAddress` - The account address initiating the transaction. Optional, defaults to the address of the logged-in account。

Example:
```
wallet> getAvailableUnfreezeCount TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh
{
	"count": 31
}
```

`getcanwithdrawunfreezeamount ownerAddress timestamp`
> Gets the unfreeze amount `ownerAddress` can withdraw using `withdrawexpireunfreeze`.

- `ownerAddress` - The account address initiating the transaction. Optional, defaults to the address of the logged-in account.
- `timestamp` - Gets the withdrawable unfreeze amount before this timestamp.

Example:
```
wallet> getCanWithdrawUnfreezeAmount TJAVcszse667FmSNCwU2fm6DmfM5D4AyDh 1671100335000
{
	"amount": 9000000
}
```

<a id="transactions"></a>
### Transactions

#### Signing a Transaction

```
> SendCoin TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW 10000000000000000
```

The following is an example of a transaction using Account Permission Management. For details on the authorization of the signing accounts, please refer to the example in the Modifying Account Permissions section.

```
wallet> sendcoin TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE 10
{
	"raw_data":{
		"contract":[
	...
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
		"raw_data":{
			"contract":[
				{
					"parameter":{
						"value":{
							"owner_address":"TSzdGHnhYnQKFF4LKrRLztkjYAvbNoxnQ8",
							"to_address":"TXBpeye7UQ4dDZEnmGDv4vX37mBYDo1tUE",
							"amount":10
						},
						"type_url":"type.googleapis.com/protocol.TransferContract"
					},
					"type":"TransferContract"
				}
			],
			"ref_block_bytes":"9ca1",
			"ref_block_hash":"432ed1fe1357ff7f",
			"expiration":1656403217000,
			"timestamp":1656403157297
		},
		"signature":[
			"a32b906a5b6f00f023d5a4208a0d2445c75463f822a16d56f6c0f836f3325e6488d57d76a08605330e2f3d532a849f2b389ed94819d9b4b0051e5052994f0e0d01"
		]
	},
	"permission_id":2
}
```


#### Broadcasting a Transaction

**BroadcastTransaction**
> Broadcasts a transaction, where the transaction is in hex string format。

#### Getting Transaction Signature Weight - `getTransactionSignWeight`

> 0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101

The information displayed is as follows:

```
{
    "result":{
        "code":"PERMISSION_ERROR",
        "message":"Signature count is 2 more than key counts of permission : 1"
    },
    "permission":{
        "operations":"7fff1fc0033e0100000000000000000000000000000000000000000000000000",
        "keys":[
            {
                "address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                "weight":1
            }
        ],
        "threshold":1,
        "id":2,
        "type":"Active",
        "permission_name":"active"
    },
    "transaction":{
        "result":{
            "result":true
        },
        "txid":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
        "transaction":{
            "signature":[
                "c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b01",
                "3d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101"
            ],
            "txID":"7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
            "raw_data":{
                "contract":[
                    {
                        "parameter":{
                            "value":{
                                "amount":10000000000000000,
                                "owner_address":"TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                                "to_address":"TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                            },
                            "type_url":"type.googleapis.com/protocol.TransferContract"
                        },
                        "type":"TransferContract",
                        "Permission_id":2
                    }
                ],
                "ref_block_bytes":"0318",
                "ref_block_hash":"60e195d3609c8661",
                "expiration":1554123306262,
                "timestamp":1554101706260
            },
            "raw_data_hex":"0a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d"
        }
    }
}
```

#### Get Signature Information from a Transaction - `getTransactionApprovedList`

> 0a8c010a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d1241c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b0112413d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101

```
{
    "result": {},
    "approved_list": [
        "TKwhcDup8L2PH5r6hxp5CQvQzZqJLmKvZP",
        "TNhXo1GbRNCuorvYu5JFWN3m2NYr9QQpVR"
    ],
    "transaction": {
        "result": {
            "result": true
        },
        "txid": "7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
        "transaction": {
            "signature": [
                "c18ca91f1533ecdd83041eb0005683c4a39a2310ec60456b1f0075b4517443cf4f601a69788f001d4bc03872e892a5e25c618e38e7b81b8b1e69d07823625c2b01",
                "3d61eb0f8868990cfa138b19878e607af957c37b51961d8be16168d7796675384e24043d121d01569895fcc7deb37648c59f538a8909115e64da167ff659c26101"
            ],
            "txID": "7da63b6a1f008d03ef86fa871b24a56a501a8bbf15effd7aca635de6c738df4b",
            "raw_data": {
                "contract": [
                    {
                        "parameter": {
                            "value": {
                                "amount": 10000000000000000,
                                "owner_address": "TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ",
                                "to_address": "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"
                            },
                            "type_url": "type.googleapis.com/protocol.TransferContract"
                        },
                        "type": "TransferContract",
                        "Permission_id": 2
                    }
                ],
                "ref_block_bytes": "0318",
                "ref_block_hash": "60e195d3609c8661",
                "expiration": 1554123306262,
                "timestamp": 1554101706260
            },
            "raw_data_hex": "0a020318220860e195d3609c86614096eadec79d2d5a6e080112680a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412370a1541a7d8a35b260395c14aa456297662092ba3b76fc01215415a523b449890854c8fc460ab602df9f31fe4293f18808084fea6dee11128027094bcb8bd9d2d"
        }
    }
}
```

<a id="querying-on-chain-data"></a>
### Querying On-chain Data

#### View Transaction History - `ViewTransactionHistory`

> View transaction history. You can configure the maximum number of records to keep in `config.conf` with `maxRecords`, not including buffer records.

Example:
```
wallet> ViewTransactionHistory
====================================
        TRANSACTION VIEWER
====================================

MAIN MENU:
1. View all transactions
2. Filter by time range
3. Help
4. Exit
Select option: 1
```

#### How to Get Transaction Information

`GetTransactionById`
> Get transaction information by transaction ID.

`GetTransactionCountByBlockNum`
> Get the number of transactions in a block by block height.

`GetTransactionInfoById`
> Get transaction-info by transaction ID, commonly used to check the result of a Smart Contract trigger.

`GetTransactionInfoByBlockNum`
> Get the list of transaction information in a block by block height.

#### Get Chain Parameters - `GetChainParameters`

> Display all parameters that can be set by the blockchain committee.


#### Get Resource Prices and Memo Fee - `getbandwidthprices`
> Get the historical unit price of **Bandwidth**.

Example:
```
wallet> getBandwidthPrices
{
    "prices": "0:10,1606537680000:40,1614238080000:140,1626581880000:1000,1626925680000:140,1627731480000:1000"
}
```

`getenergyprices`
> Get the historical unit price of **Energy**.

Example:
```
wallet> getEnergyPrices
{
    "prices": "0:100,1575871200000:10,1606537680000:40,1614238080000:140,1635739080000:280,1681895880000:420"
}
```

`getmemofee`
> Get the memo fee.

Example:
```
wallet> getMemoFee
{
    "prices": "0:0,1675492680000:1000000"
}
```

#### How to Get Block Information

`GetBlock`
> Get a block by block number; if no parameter is passed, the latest block is retrieved.

`GetBlockById`
> Get a block by block ID.

`GetBlockByIdOrNum`
> Get a block by ID or block height. If no parameter is passed, the header block is retrieved.

`GetBlockByLatestNum n`
> Get the latest `n` blocks, where 0 < n < 100.

`GetBlockByLimitNext startBlockId endBlockId`
> Get blocks within the range [startBlockId, endBlockId).

#### Other On-chain Data Commands

`GetNextMaintenanceTime`
> Get the start time of the next maintenance period.

`ListNodes`
> Get information about other peers.

`ListWitnesses`
> Get information about all **Super Representative** nodes.

#### Current Network - `CurrentNetwork`
> View the current network.

Example:
```
wallet> currentnetwork
currentNetwork: NILE
```
```
wallet> currentnetwork
current network: CUSTOM
fullNode: EMPTY, solidityNode: localhost:50052
```

<a id="smart-contracts"></a>
### Smart Contract

#### Deploying a Smart Contract

```
DeployContract [ownerAddress] contractName ABI byteCode constructor params isHex fee_limit consume_user_resource_percent origin_energy_limit value token_value token_id(e.g: TRXTOKEN, use # if don't provided) <library:address,library:address,...> <lib_compiler_version(e.g:v5)> library:address,...>
```

- `OwnerAddress` - The account address initiating the transaction. Optional, defaults to the address of the logged-in account.
- `contractName` - The **Smart Contract** name.
- `ABI` - The compiled ABI code.
- `byteCode` - The compiled bytecode.
- `constructor`, `params`, `isHex` - Defines the bytecode format and how it is parsed from parameters
- `fee_limit` - Maximum TRX that can be consumed by the transaction
- `consume_user_resource_percent` - Percentage of the user's resources to be consumed, in the range [0, 100]
- `origin_energy_limit` - Maximum Energy a developer can consume for one contract trigger
- `value` - Amount of TRX to transfer to the contract account
- `token_value` - Amount of the TRC-10 token
- `token_id` - ID of the TRC-10 token

Example:

```
> deployContract normalcontract544 [{"constant":false,"inputs":[{"name":"i","type":"uint256"}],"name": "findArgsByIndexTest","outputs":[{"name":"z","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]
608060405234801561001057600080fd5b50610134806100206000396000f3006080604052600436106100405763ffffffff7c0100000000000000000000000000000000000000000000000000000000600035041663329000b58114610045575b600080fd5b34801561005157600080fd5b5061005d60043561006f565b60408051918252519081900360200190f35b604080516003808252608082019092526000916060919060208201838038833901905050905060018160008151811015156100a657fe5b602090810290910101528051600290829060019081106100c257fe5b602090810290910101528051600390829060029081106100de57fe5b6020908102909101015280518190849081106100f657fe5b906020019060200201519150509190505600a165627a7a72305820b24fc247fdaf3644b3c4c94fcee380aa610ed83415061ff9e65d7fa94a5a50a00029 # # false 1000000000 75 50000 0 0 #
```

Use `getTransactionInfoById` to get the contract execution result:

```
> getTransactionInfoById 4978dc64ff746ca208e51780cce93237ee444f598b24d5e9ce0da885fb3a3eb9
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

#### Trigger a Smart Contract -  `TriggerContract [ownerAddress] contractAddress method args isHex fee_limit value token_value token_id`

- `OwnerAddress` - The account address initiating the transaction; optional, defaults to the logged-in account's address.
- `contractAddress` - The smart contract address.
- `method` - The function name and its parameters; refer to the example for formatting.
- `args` - The parameter values. To call the `receive` function, pass '#'.
- `isHex` - Specifies if `method` and `args` are provided as hexadecimal strings.
- `fee_limit` - The maximum amount of TRX that can be consumed by the transaction.
- `token_value` - The amount of the TRC-10 token.
- `token_id` - The ID of the TRC-10 token. Use '#' if not applicable.

Example:

```
> triggerContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG findArgsByIndexTest(uint256) 0 false
1000000000 0 0 #
# Use `getTransactionInfoById` to get the contract execution result
> getTransactionInfoById 7d9c4e765ea53cf6749d8a89ac07d577141b93f83adc4015f0b266d8f5c2dec4
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

#### Trigger a Constant Contract

```
TriggerConstantContract [ownerAddress] contractAddress method args isHex fee_limit value token_value token_id
```

- `OwnerAddress` - The account address initiating the transaction; optional, defaults to the logged-in account's address.
- `contractAddress` - The smart contract address.
- `method` - The function name and its parameters; refer to the example for formatting.
- `args` - The parameter values. To call the `receive` function, pass '#'.
- `isHex` - Specifies if `method` and `args` are provided as hexadecimal strings.
- `fee_limit` - The maximum amount of TRX that can be consumed by the transaction.
- `token_value` - The amount of the TRC-10 token.
- `token_id` - The ID of the TRC-10 token. Use '#' if not applicable.

Example:
```
> TriggerConstantContract TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs "balanceOf(address)" 000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c true
```

#### Predict Contract Address - `Create2 <address> <code> <salt>`
> Predicts the address of a contract before it is deployed using `CREATE2`.

- `address` - The creator's address
- `code` - The bytecode of the new contract
- `salt` - A user-defined salt value.

Example:
```
> Create2 TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 5f805460ff1916600190811790915560649055606319600255 2132
```
#### Estimate Energy
```
EstimateEnergy <owner_address> <contract_address> <method> <args> <isHex> [value] [token_value] [token_id]
```
> Estimates the Energy required for a smart contract transaction to execute successfully. This simulates the execution without creating an on-chain transaction.
> Note: `#` can be used for `<owner_address>` to refer to the logged-in account.

Example:
```
> EstimateEnergy TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs "balanceOf(address)" 000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c true
```

#### Clear Contract ABI - `ClearContractABI [ownerAddress] <contractAddress>`

- `ownerAddress` (Optional) - The account address initiating the transaction. Defaults to the logged-in account's address.
- `contractAddress` - The address of the smart contract.

Example:
```
> ClearContractABI TSNEe5Tf4rnc9zPMNXfaTF5fZfHDDH8oyW TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs
```

#### Get Contract - `GetContract <contractAddress>`

- `contractAddress` - The address of the smart contract to query.

Example:
```
> GetContract TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
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

#### Get Contract Info - `GetContractInfo <contractAddress>`

- `contractAddress` - The address of the smart contract to query.

Example:
```
> GetContractInfo TGdtALTPZ1FWQcc5MW7aK3o1ASaookkJxG
```

#### Update Contract Parameters
```
# Updates the origin_energy_limit parameter
> UpdateEnergyLimit [ownerAddress] <contract_address> <energy_limit>

# Updates the consume_user_resource_percent parameter
> UpdateSetting [ownerAddress] <contract_address> <consume_user_resource_percent>
```

<a id="trc-10-assets"></a>
### TRC-10 Assets

#### How to Issue a TRC-10 Token

Each account can only issue **one** TRC-10 token.

##### Issue a TRC-10 Token
```
AssetIssue [OwnerAddress] AssetName AbbrName TotalSupply TrxNum AssetNum Precision StartDate EndDate Description Url FreeNetLimitPerAccount PublicFreeNetLimit FrozenAmount0 FrozenDays0 [...] FrozenAmountN FrozenDaysN
```

- `OwnerAddress` (Optional) - The account address initiating the transaction. Default: The address of the logged-in account.
- `AssetName` - The name of the TRC-10 token being issued.
- `AbbrName` - The abbreviation of the TRC-10 token.
- `TotalSupply` - Total issuance amount.
  > `TotalSupply` = Issuer's account balance + all frozen token amounts.
  > Issuer's account balance: At the time of issuance.
  > All frozen token amounts: Before the asset transfer and issuance.
- `TrxNum`, `AssetNum` - These two parameters determine the exchange rate at the time of token issuance.
  > Exchange Rate = `TrxNum` / `AssetNum`
  > `AssetNum`: The unit of the issued token, calculated in its base unit.
  > `TrxNum`: The unit is sun (0.000001 TRX).
- `Precision` - The number of decimal places.
- `FreeNetLimitPerAccount` - The maximum amount of Bandwidth an account is allowed to use. The token issuer can freeze TRX to obtain Bandwidth (limited to TransferAssetContract).
- `PublicFreeNetLimit` - The maximum total Bandwidth allowed for all accounts. The token issuer can freeze TRX to obtain Bandwidth (limited to TransferAssetContract).
- `StartDate`, `EndDate` - The start and end dates of the token issuance. During this period, other users can participate in the token issuance.
- `FrozenAmount0`, `FrozenDays0` - The amount of token frozen and the number of days.
  > `FrozenAmount0`: Must be greater than 0.
  > `FrozenDays0`: Must be between 1 and 3653.

Example:

```
> AssetIssue TestTRX TRX 75000000000000000 1 1 2 "2019-10-02 15:10:00" "2020-07-11" "just for test121212" www.test.com 100 100000 10000 10 10000 1
> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # Check the published information
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

##### Update TRC-10 Token Parameters - `UpdateAsset [OwnerAddress] newLimit newPublicLimit description url`

> The specific meanings of the parameters are the same as in `AssetIssue`.

Example:

```
> UpdateAsset 1000 1000000 "change description" www.changetest.com
> GetAssetIssueByAccount TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ  # View the modified information
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

#### Participate in TRC-10 Token Issuance - `ParticipateAssetIssue [OwnerAddress] ToAddress AssetID Amount`

- `OwnerAddress` (Optional) - The account address initiating the transaction. Default: The address of the logged-in account.
- `ToAddress` - The account address of the TRC-10 issuer.
- `AssertName` - The TRC-10 token ID. Example: 1000001
- `Amount` - The number of TRC-10 tokens to be transferred.

Participation must take place during the TRC-10 token issuance period, otherwise an error may occur.

Example:

```
> ParticipateAssetIssue TRGhNNfnmgLegT4zHNjEqDSADjgmnHvubJ 1000001 1000
> getaccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW  # View the remaining balance
address: TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```

#### Unfreeze TRC-10 Tokens - `unfreezeasset [OwnerAddress]`

> Used to unfreeze all TRC-10 tokens that should be unfrozen after the freezing period.

#### TRC-10 Token Transfer -` TransferAsset [OwnerAddress] ToAddress AssertID Amount`

- `OwnerAddress` (Optional) - The account address initiating the transaction. Default: The address of the logged-in account.
-`ToAddress` - The address of the destination account.
- `AssertName` - The TRC-10 token ID. Example: 1000001
- `Amount` - The number of TRC-10 tokens to be transferred.

Example:

```
> TransferAsset TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz 1000001 1000
> getaccount TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz  # View the destination account information after the transfer
address: TN3zfjYUmMFK3ZsHSsrdJoNRtGkQmZLBLz
    assetV2
    {
    id: 1000001
    balance: 1000
    latest_asset_operation_timeV2: null
    free_asset_net_usageV2: 0
    }
```

#### How to Get TRC-10 Token Information

`ListAssetIssue`
> Get information about all published TRC-10 tokens.

`GetAssetIssueByAccount`
> Get TRC-10 token information based on the issuer's address.

`GetAssetIssueById`
> Get TRC-10 token information based on the ID.

`GetAssetIssueByName`
> Get TRC-10 token information based on the name.

`GetAssetIssueListByName`
> Get a list of TRC-10 token information based on the name.

#### List Asset Issuance by Page - `ListAssetIssuePaginated address code salt`

> Query all token lists by page. Return the token list starting from the offset position.

Example:

```
> ListAssetIssuePaginated 0 1
```

<a id="governance"></a>
### Governance

#### How to Vote

Voting requires Shares, which can be obtained by freezing funds.

* Share Calculation: For every **1 TRX** frozen, you get **1** unit of Share.
* After unfreezing, previous votes will become invalid. You can avoid this by re-freezing and re-voting.

**Note:** The TRON Network only records your last voting state, which means each vote you cast will overwrite all previous voting results.

Example:

```
> freezeBalance 100000000 3 1 address # Freeze 10 TRX to get 10 units of Shares

> votewitness 123455 witness1 4 witness2 6 # Vote for witness1 with 4 votes and witness2 with 6 votes simultaneously

> votewitness 123455 witness1 10 # Vote for witness1 with 10 votes
```

The final result of the commands above is 10 votes for `witness1` and 0 votes for `witness2`.

#### Brokerage

You will receive rewards after voting for an SR. The SR has the right to decide the brokerage percentage. The default percentage is 20%, which the SR can adjust.

By default, if an SR receives a reward, they will get 20% of the total reward, and the remaining 80% will be distributed to their voters.

##### Get Brokerage - `getbrokerage OwnerAddress`

> Check the SR's brokerage percentage.

- `OwnerAddress` - The address of the SR account, which is a base58check address.

##### Get Reward - `getreward OwnerAddress`

> Query for unclaimed rewards.

- `OwnerAddress` - The address of the voter's account, which is a base58check address.

##### Update the brokerage percentage - `updateBrokerage OwnerAddress brokerage`

> This command is typically used by the witness account.

- `OwnerAddress` - The address of the witness account, which is a base58check address.
- `brokerage` - The brokerage percentage you want to update, ranging from 0 to 100. If you enter 10, it means 10% of the total rewards will be allocated to the SR, and the rest (90% in this case) will be rewarded to all voters.

Example:

```
> getbrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h

> getreward TNfu3u8jo1LDWerHGbzs2Pv88Biqd85wEY

> updateBrokerage TZ7U1WVBRLZ2umjizxqz3XfearEHhXKX7h 30
```

##### Withdraw Balance - `WithdrawBalance [owner_address]`

> Withdraw vote or block rewards.

Example:

```
> WithdrawBalance TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp
```

#### How to Create a Witness

Applying to become a witness account requires a fee of **100,000 TRX**. This portion of the funds will be burned directly.

##### Create a Witness - `CreateWitness [owner_address] url`
> Apply to become a Super Representative candidate.

Example:
```
> CreateWitness TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 007570646174654e616d6531353330363038383733343633
```

##### Update a Witness - `UpdateWitness`
> Edit the SR official website URL.

Example:
```
> UpdateWitness TEDapYSVvAZ3aYH7w8N9tMEEFKaNKUD5Bp 007570646174654e616d6531353330363038383733343633
```

#### How to Withdraw Balance

After each block is generated, the block rewards are sent to the account's **allowance**, and it is allowed to withdraw from the allowance to the balance once every **24 hours**. Funds in the allowance cannot be locked or traded.

#### How to Operate on Proposals

Any proposal-related operation (except for viewing) must be executed by a Committee member.

##### Create a Proposal - `createProposal [OwnerAddress] id0 value0 ... idN valueN`

- `OwnerAddress` (Optional) - The account address initiating the transaction. Default: The address of the logged-in account.
- `id0` - The parameter's ID number. Each parameter in the TRON network has an ID number. Please refer to "http://tronscan.org/#/sr/committee".
- `Value0` - The modified value.

In this example, to modify parameter ID 4 (the cost of issuing a token) to 1,000 TRX:

```
> createProposal 4 1000
> listproposals # View the initiated proposals
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

The corresponding ID is 1.

##### Approve/Unapprove a Proposal

> approveProposal [OwnerAddress] id is_or_not_add_approval

- `OwnerAddress` (Optional) - The account address initiating the transaction. Default: The address of the logged-in account.
- `id` - The ID of the initiated proposal. Example: 1
- `is_or_not_add_approval` - `true` means approve; `false` means unapprove.

Example:

```
> ApproveProposal 1 true # Approve the proposal
> ApproveProposal 1 false # Cancel the approved proposal
```

##### Delete an Existing Proposal - `deleteProposal [OwnerAddress] proposalId`

- `proposalId` - The ID of the initiated proposal. Example: `1`

> The proposal must be canceled by the Super Representative who initiated it.

Example: `DeleteProposal 1`

##### Get Proposal Information

`ListProposals`
> Get a list of initiated proposals.

`ListProposalsPaginated`
> Get initiated proposals using a paginated mode.

`GetProposal`
> Get proposal information based on the proposal ID.


<a id="defi"></a>
### Decentralized Exchange (DEX)

Trading and price fluctuations of trading pairs follow the Bancor protocol.

#### Create a Trading Pair

> exchangeCreate [OwnerAddress] first_token_id first_token_balance second_token_id second_token_balance

- `OwnerAddress` - (Optional) The account address initiating the transaction. Defaults to the logged-in account's address.
- `first_token_id`, `first_token_balance` - The ID and amount of the first token.
- `second_token_id`, `second_token_balance` - The ID and amount of the second token. 
    > The ID is the ID of an already issued TRC-10 token.
    > If it's TRX, the ID is "_".
    > The amount must be greater than 0 and less than 1,000,000,000,000,000.

Example:

```
> exchangeCreate 1000001 10000 _ 10000
> Create a trading pair of ID 1000001 and TRX, with a quantity of 10,000 for both.
```

#### Get Exchange Information by ID

`getExchange`
> Query for a trading pair by ID (in a confirmed state).

Example:

```
> getExchange 1
```

#### Inject Liquidity -`exchangeInject [OwnerAddress] exchange_id token_id quant`

- `OwnerAddress` - (Optional) The account address initiating the transaction. Default: The address of the logged-in account.
- `exchange_id` - The ID of the trading pair to inject liquidity into.
- `token_id`, `quant` - The token ID and quantity to inject (counted in base units).


When injecting liquidity, based on its quantity (`quant`), a portion of each token in the trading pair will be withdrawn from the account and injected into the trading pair. Due to differences in the exchange balance, the same quantity of funds for the same token may also vary.

#### Trade - `exchangeTransaction [OwnerAddress] exchange_id token_id quant expected`

- `OwnerAddress` - (Optional) The account address initiating the transaction. Default: The address of the logged-in account.
- `exchange_id` - The ID of the trading pair.
- `token_id`, `quant` - The token ID and quantity to trade, equivalent to selling.
- `expected` - The expected quantity of the other token.
  > `expected` must be less than `quant`, otherwise, an error will occur.

Example:

> ExchangeTransaction 1 1000001 100 80

This is expected to trade 100 units of token 1000001 from trading pair ID 1 for 80 TRX, with a price of 80 TRX. (This is equivalent to selling 100 units of token 1000001 for 80 TRX in the trading pair with ID 1).

#### Withdraw Liquidity - `exchangeWithdraw [OwnerAddress] exchange_id token_id quant`

- `OwnerAddress` - (Optional) The account address initiating the transaction. Default: The address of the logged-in account.
- `Exchange_id` - The ID of the trading pair to withdraw liquidity from.
- `Token_id`, `quant` - The token ID and quantity to withdraw (counted in base units).

When withdrawing liquidity, based on its quantity (`quant`), a portion of each token in the trading pair will be withdrawn from the trading pair and injected into the account. Due to differences in the exchange balance, the same quantity of funds for the same token may also vary.

#### Get Trading Pair Information

`ListExchanges`
> List trading pairs.

`ListExchangesPaginated`
> List trading pairs by page.

#### How to Use tron-dex to Sell Assets

##### Create an order to sell assets

```
MarketSellAsset owner_address sell_token_id sell_token_quantity buy_token_id buy_token_quantity
```

- `ownerAddress` - The account address initiating the transaction.
- `sell_token_id`, `sell_token_quantity` - The token ID and quantity you want to sell.
- `buy_token_id`, `buy_token_quantity` - The token ID and quantity you want to buy.

Example:

```
MarketSellAsset TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW 1000001 200 _ 100

Use the `getTransactionInfoById` command to get the contract execution result:
getTransactionInfoById 10040f993cd9452b25bf367f38edadf11176355802baf61f3c49b96b4480d374

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

##### `GetMarketOrderByAccount ownerAddress`

> Get orders created by an account (only includes active status).

- `ownerAddress` - The address of the account that created the market order.

Example:

```
GetMarketOrderByAccount TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW
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

##### `GetMarketOrderById orderId`

> Get a specific **order** by `order_id`.

Example:

```
GetMarketOrderById fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0
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

##### `GetMarketPairList`

> Get a list of market **trading pairs**.

Example:

```
GetMarketPairList
{
	"orderPair": [
		{
			"sell_token_id": "_",
			"buy_token_id": "1000001"
		}
	]
}
```

##### `GetMarketOrderListByPair sell_token_id buy_token_id`

> Get a list of **orders** based on the **trading pair**.

- `sell_token_id` - The token ID you want to sell.
- `buy_token_id` - The token ID you want to buy.

Example:

```
GetMarketOrderListByPair _ 1000001
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

##### `GetMarketPriceByPair sell_token_id buy_token_id`

> Get the market price based on the **trading pair**.

- `sell_token_id` - The token ID you want to sell.
- `buy_token_id` - The token ID you want to buy.

Example:

```
GetMarketPriceByPair _ 1000001
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

##### `MarketCancelOrder owner_address order_id`

> Cancel an **order**. 

- `owner_address` - The account address that created the order.
- `order_id` - The order ID you want to cancel.


Example:

```
MarketCancelOrder TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW fc9c64dfd48ae58952e85f05ecb8ec87f55e19402493bb2df501ae9d2da75db0
```
Use the `getTransactionInfoById` command to get the contract execution result:
```
getTransactionInfoById b375787a098498623403c755b1399e82910385251b643811936d914c9f37bd27
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

<a id="gasfree"></a>
### GasFree Support

`wallet-cli` now supports **GasFree** integration. This guide explains the new commands and provides instructions on how to use them.

For more details, please refer to the [GasFree Documentation](https://gasfree.io/specification) and the [TronLink User Guide For GasFree](https://support.tronlink.org/hc/en-us/articles/38903684778393-GasFree-User-Guide).

**Prerequisites**
API Credentials: Users must obtain an API Key and API Secret from **GasFree** for authentication. Please refer to the official [application form](https://docs.google.com/forms/d/e/1FAIpQLSc5EB1X8JN7LA4SAVAG99VziXEY6Kv6JxmlBry9rUBlwI-GaQ/viewform) for instructions on how to set up API authentication.

#### Query GasFree Information - `GasFreeInfo`
> Function: Retrieve basic information, including the **GasFree** address associated with the current wallet address.
> 
> Note: A **GasFree** address is automatically activated on the first transfer and may incur an activation fee.

Example:
```
wallet> gasfreeinfo
balanceOf(address):70a08231
{
	"gasFreeAddress":"TCtSt8fCkZcVdrGpaVHUr6P8EmdjysswMF",
	"active":true,
	"tokenBalance":998696000,
	"activateFee":0,
	"transferFee":2000,
	"maxTransferValue":998694000
}
gasFreeInfo: successful !!
```
```
wallet> gasfreeinfo TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe
balanceOf(address):70a08231
{
	"gasFreeAddress":"TCtSt8fCkZcVdrGpaVHUr6P8EmdjysswMF",
	"active":true,
	"tokenBalance":998696000,
	"activateFee":0,
	"transferFee":2000,
	"maxTransferValue":998694000
}
gasFreeInfo: successful !!
```

#### GasFree Transfer - `GasFreeTransfer`
> Submits a **GasFree** transfer。
> Function: Submits a request for a gas-free token transfer。

Example:
```
wallet> gasfreetransfer TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT 100000

GasFreeTransfer result: {
	"code":200,
	"data":{
		"amount":100000,
		"providerAddress":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E",
		"apiKey":"",
		"accountAddress":"TUUSMd58eC3fKx3fn7whxJyr1FR56tgaP8",
		"signature":"",
		"targetAddress":"TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT",
		"maxFee":2000000,
		"version":1,
		"nonce":8,
		"tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
		"createdAt":1747909635678,
		"expiredAt":1747909695000,
		"estimatedTransferFee":2000,
		"id":"6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0",
		"state":"WAITING",
		"estimatedActivateFee":0,
		"gasFreeAddress":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER",
		"updatedAt":1747909635678
	}
}
GasFreeTransfer successful !!!
```

#### GasFree Trace - `GasFreeTrace`

> Traces the transfer status。
> Function: Checks the progress of a **GasFree** transfer using the `traceId` obtained from `GasFreeTransfer`。

Example:
```
wallet> gasfreetrace 6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0
GasFreeTrace result: {
	"code":200,
	"data":{
		"amount":100000,
		"providerAddress":"TKtWbdzEq5ss9vTS9kwRhBp5mXmBfBns3E",
		"txnTotalCost":102000,
		"accountAddress":"TUUSMd58eC3fKx3fn7whxJyr1FR56tgaP8",
		"txnActivateFee":0,
		"estimatedTotalCost":102000,
		"targetAddress":"TEkj3ndMVEmFLYaFrATMwMjBRZ1EAZkucT",
		"txnBlockTimestamp":1747909638000,
		"txnTotalFee":2000,
		"nonce":8,
		"estimatedTotalFee":2000,
		"tokenAddress":"TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf",
		"txnHash":"858f9a00776163b1f8a34467b9c5727657f8971a9f4e9d492f0a247fac0384f9",
		"txnBlockNum":57175988,
		"createdAt":1747909635678,
		"expiredAt":1747909695000,
		"estimatedTransferFee":2000,
		"txnState":"ON_CHAIN",
		"id":"6c3ff67e-0bf4-4c09-91ca-0c7c254b01a0",
		"state":"CONFIRMING",
		"estimatedActivateFee":0,
		"gasFreeAddress":"TNER12mMVWruqopsW9FQtKxCGfZcEtb3ER",
		"txnTransferFee":2000,
		"txnAmount":100000
	}
}
GasFreeTrace: successful!!
```



<a id="other"></a>

### Other Useful Commands

#### Switch Network - `SwitchNetwork`

> This command allows for flexible **network** switching at any time.
> `switchnetwork local` will switch to the network configured in the local `config.conf` file.

Example:

```
wallet> switchnetwork
Please select network：
1. MAIN
2. NILE
3. SHASTA
Enter numbers to select a network (1-3):1
Now, current network is : MAIN
SwitchNetwork successful !!!
```
```
wallet> switchnetwork main
Now, current network is : MAIN
SwitchNetwork successful !!!
```
```
wallet> switchnetwork empty localhost:50052
Now, current network is : CUSTOM
SwitchNetwork successful !!!
```

#### Switch Wallet - `SwitchWallet`
> You can **switch wallets** after logging in with the **LoginAll** command.

Example:
```
wallet> switchwallet
The 1th keystore file name is TJEEKTmaVTYSpJAxahtyuofnDSpe2seajB.json
The 2th keystore file name is TX1L9xonuUo1AHsjUZ3QzH8wCRmKm56Xew.json
The 3th keystore file name is TVuVqnJFuuDxN36bhEbgDQS7rNGA5dSJB7.json
The 4th keystore file name is Ledger-TRvVXgqddDGYRMx3FWf2tpVxXQQXDZxJQe.json
The 5th keystore file name is TYXFDtn86VPFKg4mkwMs45DKDcpAyqsada.json
Please choose between 1 and 5
5
SwitchWallet successful !!!
```

#### View Backup Records - `ViewBackupRecords`
> View **backup records**. You can configure the maximum number of records to keep in `config.conf` with `maxRecords`, not including buffer records.

Example:
```
wallet> ViewBackupRecords

=== View Backup Records ===
1. View all records
2. Filter by time range
Choose an option (1-2): 1
```

