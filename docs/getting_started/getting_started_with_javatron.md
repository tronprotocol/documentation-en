# Getting Started with java-tron

This page mainly explains how to start the java-tron node and use the command line tool `wallet-cli` to execute basic commands to interact with the java-tron node. Regarding the installation of java-tron, you can download the runnable file directly or build it from source code. Instructions for installing java-tron can be found on the [Install and Build](../using_javatron/installing_javatron.md) page. This tutorial on this page assumes java-tron and associated developer tools have been successfully installed.

This page covers the basics of using java-tron, which includes generating accounts, joining the TRON Nile testnet, and sending TRX between accounts. wallet-cli is also used in this document. wallet-cli is a command-line tool of the TRON network. This tool provides user interactive commands, which can be used to interact with java-tron more conveniently.

java-tron is a TRON network client written in Java. This means a computer running java-tron will become a TRON network node. TRON is a distributed network where information is shared directly between nodes rather than being managed by a central server. After the super representative's node generates a new block, it will send the block to its peers. On receiving a new block, each node checks that it is valid and adds it to their database. java-tron uses the information provided by each block to update its "state" - the balance of each account on the TRON network. There are two types of accounts on the TRON network: externally owned accounts and contract accounts. The contract account executes the contract code when a transaction is received. An external account is an account that a user manages locally in order to sign and submit transactions. Each external account is a public-private key pair, where the public key is used to derive a unique address for the user, and the private key is used to protect the account and securely sign messages. Therefore, in order to use the TRON network, it is first necessary to generate an external account (hereinafter referred to as "account"). This tutorial will guide users on how to create an account, deposit TRX tokens, and transfer TRX.

## Generate account
There are various ways to generate a TRON network account, here we will demonstrate how to generate an account using wallet-cli. An account is a pair of keys (public and private keys).

Enter the command `java -jar wallet-cli.jar` in the terminal to start a wallet-cli:
```
$ java -jar wallet-cli.jar

Welcome to TRON wallet-cli
Please type one of the following commands to proceed.
Login, RegisterWallet or ImportWallet
 
You may also use the Help command at anytime to display a full list of commands.
 
wallet> 
```

Enter the command: `registerwallet`, and then enter the password as prompted. This command will generate a TRON network account and register it with wallet-cli, that is, wallet-cli will save the private key of this account, and then you can use the private key to sign transactions.
```
wallet> registerwallet
Please input password.
password: 
user defined config file doesn't exists, use default config file in jar
WalletApi getRpcVsersion: 2
Please input password again.
password: 
Register a wallet successful, keystore file name is UTC--2022-07-04T06-35-35.304000000Z--TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz.json
wallet> 
```

## Login wallet-cli
After the registration is complete, enter the `login` command to log in to wallet-cli.
```
wallet> login
```

Select the account you want to login, and then enter the password. If the password is entered correctly, you will see the following result to the terminal: "Login successful !!!".
```
Please choose between 1 and 3
2
Please input your password.
password: 
Login successful !!!
wallet> 
```

After logging in, you can view the login account address through the `getaddress` command:
```
wallet> getaddress
GetAddress successful !!
address = TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz
wallet> 
```
Then you can use the `backupwallet` command to view the private key of the account, you need to enter the password according to the prompt. It is recommended to save the private key.


## Run a java-tron node
java-tron is a TRON network client that enables computers to connect to the TRON network. The network in this tutorial refers to the TRON Nile testnet. To start java-tron, you need first obtain the java-tron executable file, please refer to the [Installation and Deployment](../using_javatron/installing_javatron.md) chapter, and then run the following command to start java-tron.
```
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c nile_net_config.conf
```
After java-tron starts, the logs will include the following:
```
11:07:58.758 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
11:07:58.758 INFO  [main] [app](Args.java:1144) P2P version: 201910292
11:07:58.758 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
11:07:58.758 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
11:07:58.758 INFO  [main] [app](Args.java:1147) Listen port: 18888
11:07:58.758 INFO  [main] [app](Args.java:1148) Discover enable: true
```


The above logs indicate that java-tron has started and connected to the Nile testnet, then it will look for peers to connect to. Once it has found peers, it can request blocks from them, and the logs confirm this:
```
11:08:42.547 INFO  [TronJClientWorker-1] [net](Channel.java:116) Finish handshake with /123.56.3.74:18888.
11:08:42.547 INFO  [TronJClientWorker-1] [net](ChannelManager.java:161) Add active peer /123.56.3.74:18888 | fea80a0298b465a54fd332ff36819545d850115e77b327858b5306c9a58c6b8c2e7c08df76ab508a7594ed3577a8f4157727108442877077ab499b102b488467, total active peers: 1
11:08:42.549 INFO  [TronJClientWorker-1] [net](Channel.java:208) Peer /123.56.3.74:18888 status change to SYNCING.
11:08:42.566 INFO  [TronJClientWorker-1] [DB](Manager.java:1636) headNumber:23113867
11:08:42.566 INFO  [TronJClientWorker-1] [DB](Manager.java:1638) syncBeginNumber:23113867
11:08:42.567 INFO  [TronJClientWorker-1] [DB](Manager.java:1642) solidBlockNumber:23113849
11:08:42.567 INFO  [TronJClientWorker-1] [net](SyncService.java:179) Get block chain summary, low: 23113867, highNoFork: 23113867, high: 23113867, realHigh: 23113867
11:08:42.572 INFO  [TronJClientWorker-1] [net](MessageQueue.java:106) Send to /123.56.3.74:18888, type: SYNC_BLOCK_CHAIN
size: 1, start block: Num:23113867,ID:000000000160b08b510b6c501c980a2567bff1229eed62ca79874c9ca7828e9c 
11:08:42.631 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK_CHAIN_INVENTORY
size: 2001, first blockId: Num:23113867,ID:000000000160b08b510b6c501c980a2567bff1229eed62ca79874c9ca7828e9c, end blockId: Num:23115867,ID:000000000160b85b587ef18d00a1905d8022ec0a8fd174f3980b78f6aacf0ede

......

11:08:43.478 INFO  [pool-49-thread-1] [net](MessageQueue.java:106) Send to /123.56.3.74:18888, type: FETCH_INV_DATA
invType: BLOCK, size: 100, First hash: 000000000160b08c6eeba60eced4fb13d7c56e46a3c5220a67bb2801a05e5679, End hash: 000000000160b0efd90560e389d1f6e5b3c8d3877709ce375a8e063f5db73af9 
11:08:43.502 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK
Num:23113868,ID:000000000160b08c6eeba60eced4fb13d7c56e46a3c5220a67bb2801a05e5679, trx size: 1

11:08:43.504 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK
Num:23113869,ID:000000000160b08d231e450ae1993a72ba19eb8f3c748fa70d105dadd0c9fd5f, trx size: 0

11:08:43.504 INFO  [TronJClientWorker-1] [net](MessageQueue.java:121) Receive from /123.56.3.74:18888, type: BLOCK
Num:23113870,ID:000000000160b08e37cb9951d31a4233f106c7e77e0535c597dbb6a16f163699, trx size: 0
```


These logs show that java-tron is running as expected. You can determine whether the node has been started and check the status of the node by sending the following http request to the java-tron node:
```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```
If no error messages are reported in the node logs, everything is fine. In order for users to interact with the TRON network, the java-tron node must be running and in a normal state of synchronization. Whether the node is synchronized with other nodes in the network, you can query the current block height in Tronscan and compare it with the result of the local java-tron node `/wallet/getnowblock`. If they are equal, it means that the synchronization status of the local node is normal.

If you want to shut down java-tron node, please use this command: `kill -15 process id`.

## Obtain TRX
In order to make some transactions, the user must fund their account with TRX. On TRON mainnet, TRX can only be obtained in three ways:
1. Rewards for block production by SRs/rewards for voting for SRs；
2. Another TRON account transfers TRX to it;
3. Obtained from the exchange.

In the TRON testnet, TRX has no real value and can be obtained for free through [faucet](https://nileex.io/join/getJoinPage).


## Interact with java-tron node

### Interact by using wallet-cli
java-tron provides http interface and grpc interface externally, which is convenient for users to interact with TRON network. wallet-cli uses the grpc interface.
#### Get account information
After entering the `getaccount` command in wallet-cli, it will request account information data from the java-tron node, and then display the result in the terminal.
```
wallet> getaccount TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
```
Result:
```
{
	"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
	"balance": 93643857919,
	"create_time": 1619681898000,
	"latest_opration_time": 1655358327000,
	"is_witness": true,
	"asset_issued_name": "TestTRC10T",
	"latest_consume_free_time": 1652948766000,
	"account_resource": {
		"latest_consume_time_for_energy": 1655358327000
	},
    
        ......
}

```
#### Get account balance
Get the balance of an account with the `getbalance` command:
```
wallet> getbalance
Balance = 93642857919
wallet> 
```


#### Transferring TRX
To transfer TRX through the `sendcoin` command, enter the transfer address, and the amount:
```
wallet> sendcoin TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf 1000000
{
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"amount":1000000,
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
						"to_address":"TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
					},
					"type_url":"type.googleapis.com/protocol.TransferContract"
				},
				"type":"TransferContract"
			}
		],
		"ref_block_bytes":"cbc3",
		"ref_block_hash":"8581ae7e29258a52",
		"expiration":1656917577000,
		"timestamp":1656917518232
	},
	"raw_data_hex":"0a02cbc322088581ae7e29258a5240a89aefbf9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c30"
}
before sign transaction hex string is 0a85010a02cbc322088581ae7e29258a5240a89aefbf9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c30
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
```

This command returns the transaction of transferring TRX. After confirmation, enter `y` to confirm, and other letters indicate to cancel the transaction. If you enter `y`, then according to the prompt, choose which account's private key to use for signing, and finally enter the password to complete the signing of the transaction, and wallet-cli will send the signed transaction to the java-tron node.
```
Please confirm and input your permission id, if input y or Y means default 0, other non-numeric characters will cancel transaction.
y
Please choose your key for sign.
The 1th keystore file name is .DS_Store
The 2th keystore file name is UTC--2022-07-04T06-35-35.304000000Z--TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz.json
The 3th keystore file name is UTC--2022-06-21T09-51-26.367000000Z--TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM.json
Please choose between 1 and 3
3
Please input your password.
password: 
after sign transaction hex string is 0a85010a02cbc322088581ae7e29258a5240dbfc91ca9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c301241241a3ce4797ccc2fedf49ae41af28b49df1e15a476e4948af4df5aadf23a1e940ad5cc2133f501c08f2bab6a2231cdc82a745fed0fc6a012dc19310532d9138600
txid is 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
Send 1000000 Sun to TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf successful !!
wallet> 
```

#### Query transaction by transaction id
The above step sends a transferring TRX transaction through the `sendcoin` command, and prints the id of the transaction on the wallet-cli terminal:`21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4`. Next, you can query the transaction through `gettransactionbyid`, or query the result of the transaction through `gettransactioninfobyid`.

```
wallet> gettransactionbyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
{
	"ret":[
		{
			"contractRet":"SUCCESS"
		}
	],
	"signature":[
		"241a3ce4797ccc2fedf49ae41af28b49df1e15a476e4948af4df5aadf23a1e940ad5cc2133f501c08f2bab6a2231cdc82a745fed0fc6a012dc19310532d9138600"
	],
	"txID":"21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4",
	"raw_data":{
		"contract":[
			{
				"parameter":{
					"value":{
						"amount":1000000,
						"owner_address":"TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
						"to_address":"TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
					},
					"type_url":"type.googleapis.com/protocol.TransferContract"
				},
				"type":"TransferContract"
			}
		],
		"ref_block_bytes":"cbc3",
		"ref_block_hash":"8581ae7e29258a52",
		"expiration":1656939118171,
		"timestamp":1656917518232
	},
	"raw_data_hex":"0a02cbc322088581ae7e29258a5240dbfc91ca9c305a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541ce8a0cf0c16d48bcf22825f6053248df653c89ca121541d0b69631440f0a494bb51f7eee68ff5c593c00f018c0843d7098cfebbf9c30"
}
wallet> 

```

```
wallet> gettransactioninfobyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
{
	"id": "21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4",
	"blockNumber": 27773932,
	"blockTimeStamp": 1656917586000,
	"contractResult": [
		""
	],
	"receipt": {
		"net_usage": 267
	}
}
wallet> 
```
### Interact by using Curl
The above describes how to use wallet-cli to interact with java-tron. Compared with sending grpc/http commands directly, this tool provides more friendly interactive commands, allowing users to send commands to java-tron more conveniently. But, how to send HTTP requests directly to the java-tron node? Curl is a command line tool for sending HTTP requests. This chapter will explain how to check account balances and send transactions through Curl.


#### Get account balance
You can query the TRX balance information of the account through the node HTTP interface `wallet/getaccount`. The `balance` field in the returned result is the TRX balance, in sun:
```
 curl -X POST http://127.0.0.1:16887/wallet/getaccount -d 
     '{"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
       "visible": true
     }'
```
Result：
```
{"account_name": "testacc2","address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM","balance": 1000000000000000,"account_resource": {}}
```

#### Send transactions
Sending a transaction through the http interface requires a total of three steps:

1. Create a transaction
2. Sign the transaction
3. Broadcast transaction

The following takes the transferring TRX as an example to illustrate how to send a transaction to java-tron node.

Create an unsigned TRX transferring transaction through the fullnode HTTP interface [`wallet/createtransaction`](https://developers.tron.network/reference/createtransaction):

```
curl -X POST  http://127.0.0.1:16887/wallet/createtransaction -d 
    '{
        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf", 
        "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM", 
        "amount": 10000000,
        "visible":true
    }'
```
Returns an unsigned TRX transferring transaction:
```
{
    "visible": true,
    "txID": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "raw_data": {
        "contract": [
            {
                "parameter": {
                    "value": {
                        "amount": 10000000,
                        "owner_address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
                        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
                    },
                    "type_url": "type.googleapis.com/protocol.TransferContract"
                },
                "type": "TransferContract"
            }
        ],
        "ref_block_bytes": "193b",
        "ref_block_hash": "aaecd88e4e0e7528",
        "expiration": 1656580476000,
        "timestamp": 1656580418228
    },
    "raw_data_hex": "0a02193b2208aaecd88e4e0e752840e098909f9b305a68080112640a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412330a154198927ffb9f554dc4a453c64b2e553a02d6df514b121541d0b69631440f0a494bb51f7eee68ff5c593c00f01880ade20470b4d58c9f9b30"
}
```
Then sign the transaction offline. 

Finally, Broadcast the signed transaction to the java-tron node through the [`wallet/broadcasttransaction`](https://developers.tron.network/reference/broadcasttransaction) interface to complete the sending of the TRX transferring transaction.


```
curl --location --request POST 'http://127.0.0.1:16887/wallet/broadcasttransaction' \
--header 'Content-Type: application/json' \
--data-raw '{
    "visible": true,
    "signature": [
        "e12996cfaf52f8b49e64400987f9158a87b1aa809a11a75e01bb230722db97a26204334aea945b1ece0851a89c96459872e56229b0bd725c4f6a0577bfe331c301"
    ],
    "txID": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "raw_data": {
        "contract": [
            {
                "parameter": {
                    "value": {
                        "amount": 10000000,
                        "owner_address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
                        "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf"
                    },
                    "type_url": "type.googleapis.com/protocol.TransferContract"
                },
                "type": "TransferContract"
            }
        ],
        "ref_block_bytes": "193b",
        "ref_block_hash": "aaecd88e4e0e7528",
        "expiration": 1656580476000,
        "timestamp": 1656580418228
    },
    "raw_data_hex": "0a02193b2208aaecd88e4e0e752840e098909f9b305a68080112640a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412330a154198927ffb9f554dc4a453c64b2e553a02d6df514b121541d0b69631440f0a494bb51f7eee68ff5c593c00f01880ade20470b4d58c9f9b30"
}'
```
Result：
```
{
    "result": true,
    "txid": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}
```
The return result is true, indicating that the transaction broadcast was successful.

#### Query transaction by transaction id
Query the content of the transaction through the http interface `wallet/gettransactionbyid`:
```
curl --location --request POST 'http://127.0.0.1:16887/wallet/gettransactionbyid' \
--header 'Content-Type: application/json' \
--data-raw '{
     "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}'
```
Result:
```json
{
    "ret": [
        {
            "contractRet": "SUCCESS"
        }
    ],
    "signature": [
        "e12996cfaf52f8b49e64400987f9158a87b1aa809a11a75e01bb230722db97a26204334aea945b1ece0851a89c96459872e56229b0bd725c4f6a0577bfe331c301"
    ],
    "txID": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "raw_data": {
        "contract": [
            {
                "parameter": {
                    "value": {
                        "amount": 10000000,
                        "owner_address": "4198927ffb9f554dc4a453c64b2e553a02d6df514b",
                        "to_address": "41d0b69631440f0a494bb51f7eee68ff5c593c00f0"
                    },
                    "type_url": "type.googleapis.com/protocol.TransferContract"
                },
                "type": "TransferContract"
            }
        ],
        "ref_block_bytes": "193b",
        "ref_block_hash": "aaecd88e4e0e7528",
        "expiration": 1656580476000,
        "timestamp": 1656580418228
    },
    "raw_data_hex": "0a02193b2208aaecd88e4e0e752840e098909f9b305a68080112640a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412330a154198927ffb9f554dc4a453c64b2e553a02d6df514b121541d0b69631440f0a494bb51f7eee68ff5c593c00f01880ade20470b4d58c9f9b30"
}
```


Query transaction results and transaction receipts through the http interface `wallet/gettransactioninfobyid`:

```
curl --location --request POST 'http://127.0.0.1:16887/wallet/gettransactioninfobyid' \
--header 'Content-Type: application/json' \
--data-raw '{
     "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
}'
```
Result:
```
{
    "id": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0",
    "blockNumber": 27662687,
    "blockTimeStamp": 1656580470000,
    "contractResult": [
        ""
    ],
    "receipt": {
        "net_usage": 268
    }
}
```




