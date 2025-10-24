# Getting Started with java-tron

This guide will walk you through a series of fundamental operations for java-tron. We recommend learning in the following order:

- [**Create a TRON Account**](#create-account):
    - Obtain your digital identity in the blockchain world. Learn how to securely generate and manage your address and private key, which are your sole credentials for holding TRX assets, sending transactions, and interacting with smart contracts.
- [**Start and Run a java-tron Node**](#start-node):
    - Set up your dedicated gateway to the TRON network. Connect your computer to the TRON network, making it a part of the ecosystem. This is crucial for developers who want to maintain the network or require a local, high-availability API service.
- [**Interact with the TRON Network Using a Java-tron Node**](#interact-with-tron):
    - Learn how to send transactions and query on-chain data using client tools like `wallet-cli` or `cURL`. (This skill does not require you to run your own node; you can use public node services to complete these operations).

## Core Concepts

java-tron is a TRON network client written in Java. Running java-tron transforms your computer into a TRON network node. The TRON network is a distributed system where information is shared among nodes rather than managed by a centralized server. When a Super Representative (SR)'s node produces a new block, it broadcasts it to other nodes in the network. Each node validates the new block upon receipt and, if it passes verification, stores it in its local database.

java-tron continuously updates its "state" - the real-time balance of all accounts on the TRON network - by synchronizing blocks.

The first step in interacting with any blockchain is connecting to the correct network. The TRON network is primarily divided into:

- **Mainnet**: The production environment for handling real-asset transactions.
- **Nile/Shasta Testnet**: A public environment for developers to test applications and smart contracts for free.

For development and learning, we must use a testnet to avoid any real financial loss. The network used in this guide is the TRON [Nile Testnet](https://nileex.io/).


<a id="create-account"></a>
## Skill 1: Creating Your TRON Account

There are two main types of accounts on the TRON network:

- **Externally Owned Accounts (EOAs)**: Controlled by users through locally managed public-private key pairs. Each EOA consists of a public-private key pair, where the public key is used to derive a unique account address, and the private key is used to secure the account and safely sign and authorize transactions. The account you will create in this tutorial is of this type.
- **Contract Accounts**: These accounts execute their smart contract code when they receive a transaction.

To begin interacting with the TRON network, you first need to create an Externally Owned Account (hereafter referred to as an "account"). There are several ways to create a TRON account, including using Software Development Kits (SDKs) like [Trident-java](https://tronprotocol.github.io/trident/) and [TronWeb](https://tronweb.network/), or various wallet applications (such as the browser extension wallet, [TronLink](https://www.tronlink.org/)). 

This guide will use the command-line tool `wallet-cli` to demonstrate the most fundamental account operations.

> **About `wallet-cli`**
>
>`wallet-cli` is an interactive command-line tool that supports the TRON network. It simplifies complex operations by wrapping the node's gRPC interface into developer-friendly commands. It is used to sign and broadcast transactions in a secure local environment and can also be used to fetch on-chain data.
>
> Before proceeding, ensure you have downloaded and compiled `wallet-cli`. This guide only covers a few basic commands as examples. For more information, please refer to the official [GitHub documentation](https://github.com/tronprotocol/wallet-cli).
 
Now, please complete the following three preparation steps in order.

### Step A: Start `wallet-cli` and Configure Network

**1. Start `wallet-cli`**

In your terminal, start a `wallet-cli` instance with the command `java -jar wallet-cli.jar`:

```
$ java -jar wallet-cli.jar

Welcome to TRON wallet-cli
Please type one of the following commands to proceed.
Login, RegisterWallet or ImportWallet

You may also use the Help command at anytime to display a full list of commands.

wallet> 
```

**2. Configure the Network**

By default, `wallet-cli` operates on the TRON Mainnet. You must first switch the environment to the Nile Testnet to avoid interacting with real assets in this guide.

Use the `switchnetwork` command to switch networks and `currentnetwork` to verify the status. When prompted, enter `2` to select `NILE`.
```
wallet> switchnetwork
Please select network：
1. MAIN
2. NILE
3. SHASTA
Enter numbers to select a network (1-3): 2
Now, current network is : NILE
SwitchNetwork successful !!!
wallet> currentnetwork
currentNetwork: NILE
```

### Step B: Register a New Account

**1. Register Account**

At the prompt, enter the `registerwallet` command and follow the instructions to set a secure password. This command generates a new TRON network account and registers it with `wallet-cli`, which means its encrypted private key is stored in the local keystore for future use in signing transactions.


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

**2. Log in and View Account Details**

First, use the `login` command in `wallet-cli`. The system will list the available accounts for you to choose from.

```
wallet> login
```
If multiple accounts are available, when prompted, enter the number for the account you want to log in with (such as `2`), then enter the account's password.

```
Please choose between 1 and 3
2
Please input your password.
password: 
Login successful !!!
wallet> 
```
The `Login successful !!!` message indicates a successful login.

After logging in, you can use the `getaddress` command at any time to view the current account's address.


```
wallet> getaddress
GetAddress successful !!
address = TQXjm2J8K2DKTV49MdfT2anjUehbU3WDJz
wallet> 
```

**3. Back Up the Private Key (Critical Security Step)**:

This is the most crucial step to ensure the security of your assets. We strongly recommend you back up your private key immediately after creating your account to safeguard your assets.

Use the `backupwallet` command and enter your password when prompted to view the account's private key. Be sure to store the private key in an absolutely secure location.


### Step C: Fund Your Account with TRX

Executing any transaction on the TRON network (e.g., transfers, contract calls) consumes network resources, which are acquired by staking or burning TRX. Therefore, before performing any on-chain operations, you must ensure your account holds sufficient TRX. The method for obtaining TRX varies by network:

- **On the TRON Mainnet**, TRX is a real asset and is primarily obtained by:
    - Earning block rewards as a Super Representative or voting rewards.
    - Receiving TRX transfers from other TRON accounts.
    - Purchasing from cryptocurrency exchanges.
- **On the Nile Testnet**, TRX has no real value. You can obtain it for free by visiting a [Faucet](https://nileex.io/join/getJoinPage). For a detailed guide, refer to [How to Get Testnet Tokens](https://developers.tron.network/docs/getting-testnet-tokens-on-tron).

After completing all the above preparations, you now have a properly configured TRON account on a secure network with test tokens.

<a id="start-node"></a>
## Skill 2: Start and Run a Java-tron Node

This module will guide you through launching a java-tron instance, turning your computer into a TRON FullNode. Running your own node provides you with the most stable, reliable, and rate-unlimited network access. The network used in this module is the TRON [Nile Testnet](https://nileex.io/).

> Tips:
> 
> - Before performing the operations in this guide, ensure you have installed java-tron and its related development tools. If you haven't, see the [Installation](../using_javatron/installing_javatron.md) page for detailed steps. 
> - The startup command in this guide is for basic demonstration purposes only. For more detailed deployment and configuration, see the official [Nile Node Deployment Guide](https://nileex.io/run/getRunPage). 
> - The Nile testnet does not support syncing data from the genesis block (block 0). To start your node quickly, download the officially provided data snapshot. For specific instructions, refer to [Deploying a Node Using a Data Snapshot](../using_javatron/backup_restore.md).

**1. Start the Node**

Please use the following command to start the node. The `-Xmx24g` flag allocates 24GB of memory to the JVM; you can adjust this according to your machine's configuration.

> Tip: Before running this command, make sure you have installed java-tron as described in the introduction.

```
$  java -Xmx24g -XX:+UseConcMarkSweepGC -jar FullNode.jar -c nile_net_config.conf
```

**2. Verify Node Status**

**2.1 Check Startup and Sync Logs**

When the node starts, you will first see the network configuration information in the logs. The following logs indicate that java-tron has started and connected to the Nile testnet:


```
11:07:58.758 INFO  [main] [app](Args.java:1143) ************************ Net config ************************
11:07:58.758 INFO  [main] [app](Args.java:1144) P2P version: 201910292
11:07:58.758 INFO  [main] [app](Args.java:1145) Bind IP: 192.168.20.101
11:07:58.758 INFO  [main] [app](Args.java:1146) External IP: 203.12.203.3
11:07:58.758 INFO  [main] [app](Args.java:1147) Listen port: 18888
11:07:58.758 INFO  [main] [app](Args.java:1148) Discover enable: true
```
Next, the node will begin searching for other connectable peers in the network and will continuously request blocks from them to synchronize the entire on-chain data. Successfully connected peers are called "active peers." The following logs indicate that the node has successfully connected to other nodes and has started syncing data:

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
You can determine if the sync is progressing normally by observing whether the block number (the number after `Num:`) in the logs is increasing steadily. If the logs stop scrolling for an extended period or repeatedly show errors or warnings, the node may have encountered an issue.



**2.2 Confirm Sync Status Using the API**

To interact with the TRON network, your java-tron node must be running and properly synchronized.

You can send the following HTTP requests to your java-tron node to verify that it has started successfully and to check its current status:

- Get a node overview via the `/wallet/getnodeinfo` API:
`curl http://127.0.0.1:8090/wallet/getnodeinfo`
- Get the current block height via the `/wallet/getnowblock` API:
`curl http://127.0.0.1:8090/wallet/getnowblock`

To confirm that your node is fully synchronized with the network, compare your local node's block height with the latest block height displayed on the [Tronscan block explorer](https://tronscan.org/). If they match, your local node is properly synchronized.

To shut down java-tron, use `kill -15 <process_id>` to stop the node.

<a id="interact-with-tron"></a>
##  Skill 3: Interacting with the TRON Network

The core of this module is learning how to communicate with the TRON network using the API interfaces provided by a java-tron node. The java-tron node serves as your gateway to the blockchain, offering powerful HTTP and gRPC interfaces that allow any client application to query on-chain data or broadcast transactions.

Before you begin, you can choose between two ways to connect to a node:

- **Use a Public Node** (Recommended for beginners): Start instantly without waiting for synchronization.
- **Use Your Own Node** (If you completed Skill 2): Get more stable, rate-limit-free access.

The examples in this module will primarily be demonstrated using a **public node**.

### Method One: Using `wallet-cli` (Recommended)

#### Query Account Information

You can use the `getaccount <address>` command to query detailed information for a specific address. When this command is executed, `wallet-cli` sends a request to the java-tron node in the background and then displays the retrieved account data in the terminal.

```
wallet> getaccount TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM
```
The result is as follows:

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
#### Query Account Balance

Use the `getbalance` command to quickly check the TRX balance of the currently logged-in account.


```
wallet> getbalance
Balance = 93642857919
wallet> 
```

#### Transfer TRX

Use the `sendcoin <recipient_address> <amount>` command to initiate a TRX transfer. The amount is in sun (1 TRX = 1,000,000 sun).


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

This command returns a transaction pending confirmation. Please follow the steps below to complete the signing and broadcasting:

1. Confirm the Transaction: After verifying the transaction details, enter `y` and press Enter (entering any other character will cancel the transaction).
2. Select Signing Account: Follow the prompts to select the account that will sign this transaction (i.e., the sending account).
3. Authorize with Password: Enter the password for the selected account. `wallet-cli` will then sign the transaction and broadcast it to the java-tron node, completing the transaction.

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

#### Query Transaction Details by ID

After you send a transaction, the `wallet-cli` terminal returns a unique transaction ID (txid). You can use this `txid` to query all information about the transaction.



1. Use `gettransactionbyid <txid>` to view the raw content of the transaction:
  ```
  wallet> gettransactionbyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
  ```
  The returned JSON data contains all the transaction details, such as the contract type (`TransferContract`), transfer amount, sender and recipient addresses, etc. `"contractRet":"SUCCESS"` indicates that the transaction's contract is syntactically correct.
  ```
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
2. Use `gettransactioninfobyid <txid>` to view the transaction's processing result and receipt information (i.e., whether the transaction has been included in a block, its execution result, and resource consumption):
  ```
  wallet> gettransactioninfobyid 21851bcf1faf22c99a7a49c4f246d709cf9f54db2f264ca145adcd464ea155a4
  ```
  In the returned result, the most important field is `blockNumber`, which indicates the block height at which the transaction was confirmed. If this value exists, the transaction has been successfully recorded on the blockchain. Additionally, the `receipt` object records the resources consumed by the transaction, such as bandwidth (`net_usage`).
  ```
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

### Method Two: Using `cURL` (Direct HTTP API Call)

While `wallet-cli` provides user-friendly interactive commands, more advanced developers or those working in automated scripting scenarios may find it more flexible and efficient to interact with a java-tron node directly via its HTTP API. This section demonstrates how to use `cURL` (a command-line tool for sending HTTP requests) to call the java-tron node's HTTP API to perform core functions like querying account balances and sending transactions.

Unlike `wallet-cli`, which automatically handles signing and broadcasting, sending a transaction by directly calling the API requires you to manually complete a standard three-step process: **Create -> Sign -> Broadcast**. This section will show you how to execute this process.

#### Prerequisite: Query Account Balance

Before sending a transaction, let's first use the node's `wallet/getaccount` HTTP endpoint to query an account's TRX balance.

Send a `POST` request to the node's `8090` port, including the address you want to query in the request body.

```
 curl -X POST http://127.0.0.1:8090/wallet/getaccount -d 
     '{"address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
       "visible": true
     }'
```

In the returned JSON data, the `balance` field represents the TRX balance of the address, in sun (1 TRX = 1,000,000 sun).


```
{
    "account_name": "testacc2",
    "address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM",
    "balance": 1000000000000000,"account_resource": {}
}
```
#### The Three-Step Process for Sending a Transaction

Now, let's use a TRX transfer as an example to fully demonstrate the "Create-Sign-Broadcast" three-step process for sending a transaction to java-tron.

Srtep 1 - Create a Transaction

  Use the FullNode's `wallet/createtransaction` HTTP endpoint to create an unsigned TRX transfer transaction. In the request body, specify the sender (`owner_address`), recipient (`to_address`), and amount (`amount`).
    
    ```
    curl -X POST  http://127.0.0.1:8090/wallet/createtransaction -d 
        '{
            "to_address": "TUznHJfHe6gdYY7gvWmf6bNZHuPHDZtowf", 
            "owner_address": "TUoHaVjx7n5xz8LwPRDckgFrDWhMhuSuJM", 
            "amount": 10000000,
            "visible":true
        }'
    ```
  The node will return an unsigned TRX transfer transaction. Take note of the `txid` and `raw_data_hex` fields, as they will be used in subsequent steps.
    
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

Step 2 - Sign the Transaction
  
  Use the sender's private key to sign the transaction data (`raw_data_hex` or `txid`) generated in the previous step, proving your ownership of the account.  
  **Important Note**: 
  
  - To ensure the security of your private key, it is strongly recommended that you perform all signing operations in a local or secure server environment using official TRON SDKs (e.g., `TronWeb`, `java-tron-sdk`).
  - `cURL` cannot perform signing operations. This step is for procedural explanation only.

  After signing, you will get a long string, which is the transaction's Signature Hash.

Step 3 - Broadcast the Transaction
    
  The final step is to broadcast the signed transaction. Call the [wallet/broadcasttransaction](../api/http.md/#walletbroadcasttransaction) endpoint, providing the transaction object from step one and the signature hash from step two in the request body. Upon submission, the node will verify the signature and then broadcast the transaction to the entire TRON network for confirmation, completing the transfer process.
    
    ```
    curl --location --request POST 'http://127.0.0.1:8090/wallet/broadcasttransaction' \
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
    If the response contains `"result": true`, your transaction has been successfully broadcast:
    
    ```
    {
        "result": true,
        "txid": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
    }
    ```

#### Query a Transaction by ID

Querying a broadcast transaction via the HTTP API follows the same principle as with `wallet-cli`.

**`wallet/gettransactionbyid`**

  Use the `wallet/gettransactionbyid` HTTP endpoint to get the full data of a broadcast transaction. In the request body, pass the `txid` you want to query in the `value` field:

  ```
  curl --location --request POST 'http://127.0.0.1:8090/wallet/gettransactionbyid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
       "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
  }'
  ```
  The data structure of the response is nearly identical to that of the `wallet-cli` `gettransactionbyid` command:
  
  ```
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

**`wallet/gettransactioninfobyid`**

  Use the `wallet/gettransactioninfobyid` HTTP endpoint to view the transaction's processing result and receipt information (i.e., whether the transaction has been included in a block, its execution result, and resource consumption).

  Pass the target `txid` in the request body:
  
  ```
  curl --location --request POST 'http://127.0.0.1:8090/wallet/gettransactioninfobyid' \
  --header 'Content-Type: application/json' \
  --data-raw '{
       "value": "c558bd35978267d8999baf6148703cbc94786f3f2e22893637588ca05437d7f0"
  }'
  ```
  
  The `blockNumber` field in the response is the key proof of a successful transaction. As long as this field has a value, it means your transaction is successfully and irreversibly recorded on the blockchain. The `receipt` field provides a detailed execution receipt.
  
  
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


## Next Steps

Congratulations on completing your introductory journey with java-tron! You have now mastered core skills like running a node, creating an account, and sending transactions, laying a solid foundation for deeper exploration of the TRON ecosystem.

