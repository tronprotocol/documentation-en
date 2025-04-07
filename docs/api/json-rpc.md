# jsonRPC API

## Overview

JSON-RPC is a stateless, lightweight remote procedure call (RPC) protocol. The JSON-RPC interface supported by the TRON network is compatible with Ethereum's. However, due to the difference in chain mechanism and design, TRON cannot support some interfaces on Ethereum. At the same time, TRON also provides dedicated APIs to create different types of transactions.

**Please pay attention**

- The JSON-RPC service needs to be enabled and set the port in the node configuration file. If not configured, the service is disable by default. 

### How to enable or disable JSON-RPC service of a node

Add below items in node's [configuration file](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/resources/config.conf), then enable or disable it:  
```
node.jsonrpc {  
    httpFullNodeEnable = true  
    httpFullNodePort = 50545  
    httpSolidityEnable = true  
    httpSolidityPort = 50555  
}
```

### HEX value encoding

At present there are two key data types that are passed over JSON: unformatted byte arrays and quantities. Both are passed with a hex encoding, however with different requirements to formatting:

When encoding QUANTITIES (integers, numbers): encode as hex, prefix with “0x”, the most compact representation (slight exception: zero should be represented as “0x0”).  
Examples:

- 0x41 (65 in decimal)
- 0x400 (1024 in decimal)
- WRONG: 0x (should always have at least one digit - zero is “0x0”)
- WRONG: 0x0400 (no leading zeros allowed)
- WRONG: ff (must be prefixed 0x)

When encoding UNFORMATTED DATA (byte arrays, account addresses, hashes, bytecode arrays): encode as hex, prefix with “0x”, two hex digits per byte.  
Examples:

- 0x41 (size 1, “A”)
- 0x004200 (size 3, “\\0B\\0”)
- 0x (size 0, “”)
- WRONG: 0xf0f0f (must be even number of digits)
- WRONG: 004200 (must be prefixed 0x)



## eth

### eth_accounts

*Returns a list of addresses owned by the client.*

**Parameters**  

None

**Returns**  

Empty List

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '

{"jsonrpc": "2.0", "id": 1, "method": "eth_accounts", "params": []}'

```

```json

{"jsonrpc":"2.0","id":1,"result":[]}

```


### eth_blockNumber

*Returns the number of the most recent block.*

**Parameters**  

None

**Returns**  

The latest block number.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":64}'

```

```json

{"jsonrpc":"2.0","id":64,"result":"0x20e0cf0"}

```


### eth_call

*Executes a message call immediately without creating a transaction on the block chain.*

**Parameters**

1\. Object - The transaction call object, the items in it as below.

| Item Name | Data Type      | Description                                                   |
| :-------- | :------------- | :------------------------------------------------------------ |
| from      | DATA, 20 Bytes | Caller address. Hex format address, remove the prefix "41"    |
| to        | DATA, 20 Bytes | Contract address.  Hex format address, remove the prefix "41" |
| gas       | QUANTITY       | Not supported. The value is 0x0                               |
| gasPrice  | QUANTITY       | Not supported. The value is 0x0                               |
| value     | QUANTITY       | Not supported. The value is 0x0                               |
| data      | DATA           | Hash of the method signature and encoded parameters.          |

2\. QUANTITY|TAG - currently, only "latest" is available. 

**Returns**

DATA - the return value of executed contract function.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_call",

	"params": [{

		"from": "0xF0CC5A2A84CD0F68ED1667070934542D673ACBD8",

		"to": "0x70082243784DCDF3042034E7B044D6D342A91360",

		"gas": "0x0",

		"gasPrice": "0x0",

		"value": "0x0",

		"data": "0x70a08231000000000000000000000041f0cc5a2a84cd0f68ed1667070934542d673acbd8"

	}, "latest"],

	"id": 1

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x"}

```

```


### eth_chainId

*Returns the chainId of the TRON network which is the last four bytes of the genesis block hash*

**Parameters**  

None

**Returns**  

DATA - The chainId of the TRON network

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":79}'

```

Result

```json

{"jsonrpc":"2.0","id":79,"result":"0x2b6653dc"}

```


### eth_coinbase

Returns the super representative address of the current node.

**Parameters**  

None

**Returns**  

DATA - The super representative address of the node.   (Note: Return the first address If more than one super representative address is configured, return error if there is no valid address or the address did not generate any block, the error will be “etherbase must be explicitly specified” . )

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_coinbase", "params": []}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"etherbase must be explicitly specified","data":"{}"}}

```


### eth_estimateGas

*Get the required energy through triggerConstantContract.*

**Parameters**  

object - The transaction call object, the items in it as below

| Item Name | Data Type      | Description                                          |
| :-------- | :------------- | :--------------------------------------------------- |
| from      | DATA, 20 Bytes | address of the sender                                |
| to        | DATA, 20 Bytes | address of the receiver                              |
| gas       | QUANTITY       | unused.                                              |
| gasPrice  | QUANTITY       | unused.                                              |
| value     | QUANTITY       | Integer of the value sent with this transaction      |
| data      | DATA           | Hash of the method signature and encoded parameters. |

**Returns**  

The amount of energy used.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"id": 1,

	"method": "eth_estimateGas",

	"params": [{

		"from": "0x41F0CC5A2A84CD0F68ED1667070934542D673ACBD8",

		"to": "0x4170082243784DCDF3042034E7B044D6D342A91360",

		"gas": "0x01",

		"gasPrice": "0x8c",

		"value": "0x01",

		"data": "0x70a08231000000000000000000000041f0cc5a2a84cd0f68ed1667070934542d673acbd8"

	}]

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x0"}

```


### eth_gasPrice

Returns the current energy price in sun.

**Parameters**  

None

**Returns**  

Integer of the current energy price in sun.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_gasPrice", "params": []}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x8c"}

```


### eth_getBalance

Returns the balance of the account of the given address.

**Parameters**

| Index | Data Type      | Description                    |
| :---- | :------------- | :----------------------------- |
| 1     | DATA, 20 Bytes | address to check for balance.  |
| 2     | QUANTITY       | only "latest" is available now |

**Returns**

QUANTITY - integer of the current balance in sun.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getBalance",

	"params": ["0x41f0cc5a2a84cd0f68ed1667070934542d673acbd8", "latest"],

	"id": 64

}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x492780"}

```


### eth_getBlockByHash

*Returns information about a block by hash.*

**Parameters**

| Index | Data Type      | Description                                                                                    |
| :---- | :------------- | :--------------------------------------------------------------------------------------------- |
| 1     | DATA, 32 Bytes | hash of a block                                                                                |
| 2     | Boolean        | If true it returns the full transaction objects, if false only the hashes of the transactions. |

**Returns**

object - a block object  or null when no block was found. The block includes items as below.

| Item Name        | Data Type       | Description                                                                                         |
| :--------------- | :-------------- | :-------------------------------------------------------------------------------------------------- |
| number           | QUANTITY        | block number                                                                                        |
| hash             | DATA, 32 Bytes  | hash of the block                                                                                   |
| parentHash       | DATA, 32 Bytes  | hash of the parent block                                                                            |
| nonce            | QUANTITY        | unused                                                                                              |
| sha3Uncles       | DATA, 32 Bytes  | SHA3 of the uncles data in the block                                                                |
| logsBloom        | DATA, 256 Bytes | the bloom filter for the logs of the block.                                                         |
| transactionsRoot | DATA, 32 Bytes  | the root of the transaction trie of the block                                                       |
| stateRoot        | DATA, 32 Bytes  | the root of the final state trie of the block                                                       |
| receiptsRoot     | DATA, 32 Bytes  | the root of the receipts trie of the block                                                          |
| miner            | DATA, 20 Bytes  | the address of the beneficiary to whom the mining rewards were given                                |
| difficulty       | QUANTITY        | integer of the difficulty for this block                                                            |
| totalDifficulty  | QUANTITY        | integer of the total difficulty of the chain until this block                                       |
| extraData        | DATA            | the “extra data” field of this block                                                                |
| size             | QUANTITY        | integer the size of this block in bytes                                                             |
| gasLimit         | QUANTITY        | the maximum gas allowed in this block                                                               |
| gasUsed          | QUANTITY        | the total used gas by all transactions in this block                                                |
| timestamp        | QUANTITY        | the unix timestamp for when the block was created, the unit is second.                              |
| transactions     | Array           | Array of transaction objects, or 32 Bytes transaction hashes depending on the last given parameter. |
| uncles           | Array           | Array of uncle hashes                                                                               |

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getBlockByHash",

	"params": ["0x0000000000f9cc56243898cbe88685678855e07f51c5af91322c225ce3693868", false],

	"id": 1

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":null}

```


### eth_getBlockByNumber

*Returns information about a block by hash.*

**Parameters**

| Index | Data Type     | Description                                                                                    |
| :---- | :------------ | :--------------------------------------------------------------------------------------------- |
| 1     | QUANTITY\|TAG | Integer of a block number, or the string "earliest", "latest"                                  |
| 2     | Boolean       | If true it returns the full transaction objects, if false only the hashes of the transactions. |

**Returns**

object - a block object  or null when no block was found. See [eth_getBlockByHash](https://developers.tron.network/reference#eth_getblockbyhash)

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getBlockByNumber",

	"params": ["0xF9CC56", true],

	"id": 1

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":null}

```


### eth_getBlockTransactionCountByHash

*Returns the number of transactions in a block from a block matching the given block hash.*

**Parameters**

DATA, 32 Bytes - hash of a block

**Returns**

QUANTITY - integer of the number of transactions in this block.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"id": 1,

	"method": "eth_getBlockTransactionCountByHash",

	"params": ["0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b"]

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x39"}

```


### eth_getBlockTransactionCountByNumber

*Returns the number of transactions in a block matching the given block number.*

**Parameters**

QUANTITY|TAG - integer of a block number, or the string "earliest" or "latest".  

**Returns**

QUANTITY - integer of the number of transactions in this block.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getBlockTransactionCountByNumber",

	"params": ["0xF96B0F"],

	"id": 1

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x23"}

```


### eth_getCode

*Returns runtime code of a given smart contract address.*

**Parameters**

| Index | Data Type      | Description                           |
| :---- | :------------- | :------------------------------------ |
| 1     | DATA, 20 Bytes | contract address                      |
| 2     | QUANTITY\|TAG  | currently, only "latest" is available |

**Returns**

DATA - the runtime code from the given address.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getCode",

	"params": ["0x4170082243784DCDF3042034E7B044D6D342A91360", "latest"],

	"id": 64

}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x"}

```


### eth_getStorageAt

*Returns the value from a storage position at a given address. It can be used to get the value of a variable in a contract.*

**Parameters**

| Index | Data Type      | Description                            |
| :---- | :------------- | :------------------------------------- |
| 1     | DATA, 20 Bytes | address                                |
| 2     | QUANTITY       | integer of the position in the storage |
| 3     | QUANTITY\|TAG  | currently only support "latest"        |

**Returns**

DATA - the value at this storage position.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getStorageAt",

	"params": ["0xE94EAD5F4CA072A25B2E5500934709F1AEE3C64B", "0x29313b34b1b4beab0d3bad2b8824e9e6317c8625dd4d9e9e0f8f61d7b69d1f26", "latest"],

	"id": 1

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x0000000000000000000000000000000000000000000000000000000000000000"}

```


### eth_getTransactionByBlockHashAndIndex

*Returns information about a transaction by block hash and transaction index position.*

**Parameters**

| Index | Data Type      | Description                    |
| :---- | :------------- | :----------------------------- |
| 1     | DATA, 32 Bytes | hash of a block                |
| 2     | QUANTITY       | the transaction index position |

**Returns**

object - a transaction object  or null when no transaction was found. The transaction includes items as below.

| Item Name        | Data Type      | Description                                             |
| :--------------- | :------------- | :------------------------------------------------------ |
| blockHash        | DATA, 32 Bytes | hash of the block where this transaction was in.        |
| blockNumber      | QUANTITY       | block number where this transaction was in.             |
| from             | DATA, 20 Bytes | address of the sender                                   |
| gas              | QUANTITY       | unused.                                                 |
| gasPrice         | QUANTITY       | energy price                                            |
| hash             | DATA, 32 Bytes | hash of the transaction                                 |
| input            | DATA           | the data sent along with the transaction                |
| nonce            | QUANTITY       | unused                                                  |
| to               | DATA, 20 Bytes | address of the receiver                                 |
| transactionIndex | QUANTITY       | integer of the transactions index position in the block |
| value            | QUANTITY       | value transferred in sun                                |
| v                | QUANTITY       | ECDSA recovery id                                       |
| r                | DATA, 32 Bytes | ECDSA signature r                                       |
| s                | DATA, 32 Bytes | ECDSA signature s                                       |

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getTransactionByBlockHashAndIndex",

	"params": ["00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b", "0x0"],

	"id": 64

}'

```

Result

```json

{

	"jsonrpc": "2.0",

	"id": 64,

	"result": {

		"blockHash": "0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b",

		"blockNumber": "0x20ef11c",

		"from": "0xb4f1b6e3a1461266b01c2c4ff9237191d5c3d5ce",

		"gas": "0x0",

		"gasPrice": "0x8c",

		"hash": "0x8dd26d1772231569f022adb42f7d7161dee88b97b4b35eeef6ce73fcd6613bc2",

		"input": "0x",

		"nonce": null,

		"r": "0x6212a53b962345fb8ab02215879a2de05f32e822c54e257498f0b70d33825cc5",

		"s": "0x6e04221f5311cf2b70d3aacfc444e43a5cf14d0bf31d9227218efaabd9b5a812",

		"to": "0x047d4a0a1b7a9d495d6503536e2a49bb5cc72cfe",

		"transactionIndex": "0x0",

		"type": "0x0",

		"v": "0x1b",

		"value": "0x203226"

	}

}

```


### eth_getTransactionByBlockNumberAndIndex

*Returns information about a transaction by block number and transaction index position.*

**Parameters**

| Index | Data Type     | Description                                         |
| :---- | :------------ | :-------------------------------------------------- |
| 1     | QUANTITY\|TAG | a block number, or the string "earliest", "latest", |
| 2     | QUANTITY      | the transaction index position                      |

**Returns**

object - a transaction object  or null when no transaction was found. See [eth_getTransactionByBlockHashAndIndex](https://developers.tron.network/reference#eth_gettransactionbyblockhashandindex)

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getTransactionByBlockNumberAndIndex",

	"params": ["0xfb82f0", "0x0"],

	"id": 64

}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":null}

```


### eth_getTransactionByHash

*Returns the information about a transaction requested by transaction hash.*

**Parameters**

DATA, 32 Bytes - hash of a transaction

**Returns**

object - a transaction object  or null when no transaction was found. See [eth_getTransactionByBlockHashAndIndex](https://developers.tron.network/reference#eth_gettransactionbyblockhashandindex)

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getTransactionByHash",

	"params": ["c9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0"],

	"id": 64

}'

```

Result

```json

{

	"jsonrpc": "2.0",

	"id": 64,

	"result": {

		"blockHash": "0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b",

		"blockNumber": "0x20ef11c",

		"from": "0x6eced5214d62c3bc9eaa742e2f86d5c516785e14",

		"gas": "0x0",

		"gasPrice": "0x8c",

		"hash": "0xc9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0",

		"input": "0x",

		"nonce": null,

		"r": "0x433eaf0a7df3a08c8828a2180987146d39d44de4ac327c4447d0eeda42230ea8",

		"s": "0x6f91f63b37f4d1cd9342f570205beefaa5b5ba18d616fec643107f8c1ae1339d",

		"to": "0x0697250b9d73b460a9d2bbfd8c4cacebb05dd1f1",

		"transactionIndex": "0x6",

		"type": "0x0",

		"v": "0x1b",

		"value": "0x1cb2310"

	}

}

```


### eth_getTransactionReceipt

*Returns the  transaction info: receipt, transaction fee, block height ... by transaction hash. Please refer to http api: [wallet/gettransactioninfobyid](https://developers.tron.network/reference#transaction-info-by-id)*

**Parameters**

DATA, 32 Bytes - hash of a transaction

**Returns**

object - A transaction receipt object, or null when no receipt was found. The items in transaction receipt as below.

| Item Name         | Data Type       | Description                                                                               |
| :---------------- | :-------------- | :---------------------------------------------------------------------------------------- |
| transactionHash   | DATA, 32 Bytes  | hash of the transaction                                                                   |
| transactionIndex  | QUANTITY        | integer of the transactions index position in the block                                   |
| blockHash         | DATA, 32 Bytes  | hash of the block where this transaction was in.                                          |
| blockNumber       | QUANTITY        | block number where this transaction was in.                                               |
| from              | DATA, 20 Bytes  | address of the sender                                                                     |
| to                | DATA, 20 Bytes  | address of the receiver                                                                   |
| cumulativeGasUsed | QUANTITY        | The total amount of gas used when this transaction was executed in the block.             |
| gasUsed           | QUANTITY        | The amount of gas used by this specific transaction alone.                                |
| contractAddress   | DATA, 20 Bytes  | The contract address created, if the transaction was a contract creation, otherwise null. |
| logs              | Array           | Array of log objects, which this transaction generated.                                   |
| logsBloom         | DATA, 256 Bytes | Bloom filter for light clients to quickly retrieve related logs.                          |
| root              | DATA            | 32 bytes of post-transaction stateroot (pre Byzantium)                                    |
| status            | QUANTITY        | either 1 (success) or 0 (failure)                                                         |

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getTransactionReceipt",

	"params": ["c9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0"],

	"id": 64

}'

```

Result

```json

{

	"jsonrpc": "2.0",

	"id": 64,

	"result": {

		"blockHash": "0x00000000020ef11c87517739090601aa0a7be1de6faebf35ddb14e7ab7d1cc5b",

		"blockNumber": "0x20ef11c",

		"contractAddress": null,

		"cumulativeGasUsed": "0x646e2",

		"effectiveGasPrice": "0x8c",

		"from": "0x6eced5214d62c3bc9eaa742e2f86d5c516785e14",

		"gasUsed": "0x0",

		"logs": [],

		"logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",

		"status": "0x1",

		"to": "0x0697250b9d73b460a9d2bbfd8c4cacebb05dd1f1",

		"transactionHash": "0xc9af231ad59bcd7e8dcf827afd45020a02112704dce74ec5f72cb090aa07eef0",

		"transactionIndex": "0x6",

		"type": "0x0"

	}

}

```


### eth_getWork

*Returns the hash of the current block*

**Parameters**  

None

**Returns**  

Array - Array with the following properties:

| Index | Data Type      | Description       |
| :---- | :------------- | :---------------- |
| 1     | DATA, 32 Bytes | hash of the block |
| 2     | DATA           | unused            |
| 3     | DATA           | unused            |

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getWork",

	"params": [],

	"id": 73

}'

```

Result

```json

{

	"jsonrpc": "2.0",

	"id": 73,

	"result": ["0x00000000020e73915413df0c816e327dc4b9d17069887aef1fff0e854f8d9ad0", null, null]

}

```


### eth_protocolVersion

*Returns the java-tron block version*

**Parameters**  

None

**Returns**  

String - The current java-tron block version

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_protocolVersion","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x16"}

```


### eth_syncing

*Returns an object with data about the sync status of the node*

**Parameters**  

None

**Returns**  

Object|Boolean, An object with sync status data or FALSE, when not syncing, the items in object includes:

|               |          |                                                                                             |
| :------------ | :------- | :------------------------------------------------------------------------------------------ |
| startingBlock | QUANTITY | The block at which the import started (will only be reset, after the sync reached his head) |
| currentBlock  | QUANTITY | The current block                                                                           |
| highestBlock  | QUANTITY | The estimated highest block                                                                 |

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":64}'

```

Result

```json

{

	"jsonrpc": "2.0",

	"id": 64,

	"result": {

		"startingBlock": "0x20e76cc",

		"currentBlock": "0x20e76df",

		"highestBlock": "0x20e76e0"

	}

}

```


### eth_newFilter

*Creates a filter object, based on filter options, to notify when the state changes (logs).*

**Parameters**  

Object - The filter options:

| Field     | Type                  | Description                                                               |
| :-------- | :-------------------- | :------------------------------------------------------------------------ |
| fromBlock | QUANTITY\|TAG         | Integer block number, or "latest"                                         |
| toBlock   | QUANTITY\|TAG         | Integer block number, or "latest"                                         |
| address   | DATA\|Array, 20 Bytes | Contract address or a list of addresses from which logs should originate. |
| topics    | Array of DATA         | Topics                                                                    |

**Returns**  

QUANTITY - A filter id.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_newFilter","params":[{"address":["cc2e32f2388f0096fae9b055acffd76d4b3e5532","E518C608A37E2A262050E10BE0C9D03C7A0877F3"],"fromBlock":"0x989680","toBlock":"0x9959d0","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",null,["0x0000000000000000000000001806c11be0f9b9af9e626a58904f3e5827b67be7","0x0000000000000000000000003c8fb6d064ceffc0f045f7b4aee6b3a4cefb4758"]]}],"id":1}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x2bab51aee6345d2748e0a4a3f4569d80"}

```


### eth_newBlockFilter

*Creates a filter in the node, to notify when a new block arrives.*

**Parameters**  

None.

**Returns**  

QUANTITY - A filter id.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x2bab51aee6345d2748e0a4a3f4569d80"}

```


### eth_getFilterChanges

*Polling method for a filter, which returns an array of logs which occurred since last poll.*

**Parameters**  

QUANTITY - the filter id.

**Returns**

- For filters created with eth_newFilte, return logs object list, each log object with following params:

| Field            | Type           | Description                                                                                 |
| :--------------- | :------------- | :------------------------------------------------------------------------------------------ |
| removed          | TAG            | true when the log was removed, due to a chain reorganization. false if its a valid log.     |
| logIndex         | QUANTITY       | Integer of the log index position in the block. null when its pending log.                  |
| transactionIndex | QUANTITY       | Integer of the transactions index position log was created from. null when its pending log. |
| transactionHash  | DATA, 32Bytes  | Hash of the transactions this log was created from.                                         |
| blockHash        | DATA, 32 Bytes | Hash of the block where this log was in. null when its pending.                             |
| blockNumber      | QUANTITY       | The block number where this log was in.                                                     |
| address          | DATA, 32 Bytes | Address from which this log originated.                                                     |
| data             | DATA           | Contains one or more 32 Bytes non-indexed arguments of the log.                             |
| topics           | DATA\[]        | Event topic and indexed arguments.                                                          |

- For filters created with eth_newBlockFilter the return are block hashes (DATA, 32 Bytes).

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "jsonrpc": "2.0",

    "method": "eth_getFilterChanges",

    "params": [

        "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"

    ],

    "id": 71

}'

```

Result

```json

{

    "jsonrpc": "2.0",

    "id": 71,

    "error": {

        "code": -32000,

        "message": "filter not found",

        "data": "{}"

    }

}

```


### eth_getFilterLogs

*Returns an array of all logs matching filter with given id.*

**Parameters**  

QUANTITY - the filter id.

**Returns**

See [eth_getFilterChanges](#eth_getfilterchanges)。

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "jsonrpc": "2.0",

    "method": "eth_getFilterLogs",

    "params": [

        "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"

    ],

    "id": 71

}'

```

Result

```json

{

    "jsonrpc": "2.0",

    "id": 71,

    "error": {

        "code": -32000,

        "message": "filter not found",

        "data": "{}"

    }

}

```


### eth_uninstallFilter

*Uninstalls a filter with given id. Should always be called when watch is no longer needed. Additionally Filters timeout when they aren't requested with eth_getFilterChanges for a period of time.*

**Parameters**  

QUANTITY - the filter id.

**Returns**

 Boolean - true if the filter was successfully uninstalled, otherwise false.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "jsonrpc": "2.0",

    "method": "eth_uninstallFilter",

    "params": [

        "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"

    ],

    "id": 71

}'

```

Result

```json

{

    "jsonrpc": "2.0",

    "id": 71,

    "result": true

}

```


### eth_getLogs

*Returns an array of all logs matching a given filter object.*

**Parameters**  

Object - The filter options which include below fields:

| Field     | Type                  | Description                                                                                                                      |
| :-------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| fromBlock | QUANTITY\|TAG         | (optional, default: "latest") Integer block number, or "latest" for the last mined block                                         |
| toBlock   | QUANTITY\|TAG         | (optional, default: "latest") Integer block number, or "latest" for the last mined block                                         |
| address   | DATA\|Array, 20 Bytes | (optional) Contract address or a list of addresses from which logs should originate.                                             |
| topics    | Array of DATA         | (optional) Array of 32 Bytes DATA topics. Topics are order-dependent. Each topic can also be an array of DATA with "or" options. |
| blockhash | DATA, 32 Bytes        | (optional) Block hash                                                                                                            |

**Returns**

 See [eth_getFilterChanges](#eth_getfilterchanges).

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_getLogs","params":[{"address":["cc2e32f2388f0096fae9b055acffd76d4b3e5532","E518C608A37E2A262050E10BE0C9D03C7A0877F3"],"fromBlock":"0x989680","toBlock":"0x9959d0","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",null,["0x0000000000000000000000001806c11be0f9b9af9e626a58904f3e5827b67be7","0x0000000000000000000000003c8fb6d064ceffc0f045f7b4aee6b3a4cefb4758"]]}],"id":1}'

```

Result

```json

{

    "jsonrpc": "2.0",

    "id": 71,

    "result": []

}

```


## net

### net_listening

*Returns true if the client is actively listening for network connections.*

**Parameters**  

None

**Returns**  

Boolean - true when listening, otherwise false.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_listening","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":true}

```


### net_peerCount

*Returns number of peers currently connected to the client.*

**Parameters**  

None

**Returns**  

QUANTITY - integer of the number of connected peers.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x9"}

```


### net_version

*Returns the hash of the genesis block.*

**Parameters**  

None

**Returns**  

String - The hash of genesis block

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_version","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x2b6653dc"}

```


## web3

### web3_clientVersion

*Returns the current client version.*

**Parameters**  

None

**Returns**  

String - The current client version

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "web3_clientVersion", "params": []}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"TRON/v4.3.0/Linux/Java1.8/GreatVoyage-v4.2.2.1-281-gc1d9dfd6c"}

```


### web3_sha3

*Returns Keccak-256 (not the standardized SHA3-256) of the given data.*

**Parameters**  

DATA - the data to convert into a SHA3 hash

**Returns**  

DATA - The SHA3 result of the given string.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "web3_sha3", "params": ["0x68656c6c6f20776f726c64"]}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad"}

```



## buildTransaction

*Create a transaction, different transaction types have different parameters*

### TransferContract

**Parameters**  

Object - the items in object as below: 

| Param Name | Data Type      | Description                                 |
| :--------- | :------------- | :------------------------------------------ |
| from       | DATA, 20 Bytes | The address the transaction is sent from.   |
| to         | DATA, 20 Bytes | The address the transaction is directed to. |
| value      | DATA           | the transfer amount                         |

**Returns**

Object - transaction of TransferContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "id": 1337,

    "jsonrpc": "2.0",

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "to": "0x95FD23D3D2221CFEF64167938DE5E62074719E54",

            "value": "0x1f4"

        }]}'

```

Result

```json

{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"ae02a80abd985a6f05478b9bbf04706f00cdbf71e38c77d21ed77e44c634cef9","raw_data":{"contract":[{"parameter":{"value":{"amount":500,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","to_address":"4195fd23d3d2221cfef64167938de5e62074719e54"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"957e","ref_block_hash":"3922d8c0d28b5283","expiration":1684469286000,"timestamp":1684469226841},"raw_data_hex":"0a02957e22083922d8c0d28b528340f088c69183315a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d812154195fd23d3d2221cfef64167938de5e62074719e5418f40370d9bac2918331"}}}

```

### TransferAssetContract

**Parameters**  

Object - the items in object as below: 

|            |                |                                            |
| :--------- | :------------- | :----------------------------------------- |
| from       | DATA, 20 Bytes | The address the transaction is sent from   |
| to         | DATA, 20 Bytes | The address the transaction is directed to |
| tokenId    | QUANTITY       | Token ID                                   |
| tokenValue | QUANTITY       | The transfer amount of TRC10               |

**Returns**

Object - transaction of TransferAssetContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "to": "0x95FD23D3D2221CFEF64167938DE5E62074719E54",

            "tokenId": 1000016,

            "tokenValue": 20

        }

    ],

    "id": 44,

    "jsonrpc": "2.0"

}

'

```

Result

```json

{"jsonrpc":"2.0","id":44,"error":{"code":-32600,"message":"assetBalance must be greater than 0.","data":"{}"}}

```

### CreateSmartContract

**Parameters**  

Object - the items in object as below: 

|                            |                |                                          |
| :------------------------- | :------------- | :--------------------------------------- |
| from                       | DATA, 20 Bytes | The address the transaction is sent from |
| name                       | DATA           | The name of the smart contract.          |
| gas                        | DATA           | Fee limit                                |
| abi                        | DATA           | The ABI of the smart contract.           |
| data                       | DATA           | The byte code of the smart contract.     |
| consumeUserResourcePercent | QUANTITY       | The consume user resource percent.       |
| originEnergyLimit          | QUANTITY       | The origin energy limit.                 |
| value                      | DATA           | The data passed through call_value.      |
| tokenId                    | QUANTITY       | Token ID                                 |
| tokenValue                 | QUANTITY       | The transfer amount of TRC10             |

**Returns**

Object - transaction of CreateSmartContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "id": 1337,

    "jsonrpc": "2.0",

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "name": "transferTokenContract",

            "gas": "0x245498",

            "abi": "[{\"constant\":false,\"inputs\":[],\"name\":\"getResultInCon\",\"outputs\":[{\"name\":\"\",\"type\":\"trcToken\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[{\"name\":\"toAddress\",\"type\":\"address\"},{\"name\":\"id\",\"type\":\"trcToken\"},{\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"TransferTokenTo\",\"outputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"constant\":false,\"inputs\":[],\"name\":\"msgTokenValueAndTokenIdTest\",\"outputs\":[{\"name\":\"\",\"type\":\"trcToken\"},{\"name\":\"\",\"type\":\"uint256\"},{\"name\":\"\",\"type\":\"uint256\"}],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[],\"payable\":true,\"stateMutability\":\"payable\",\"type\":\"constructor\"}]\n",

            "data": "6080604052d3600055d2600155346002556101418061001f6000396000f3006080604052600436106100565763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166305c24200811461005b5780633be9ece71461008157806371dc08ce146100aa575b600080fd5b6100636100b2565b60408051938452602084019290925282820152519081900360600190f35b6100a873ffffffffffffffffffffffffffffffffffffffff600435166024356044356100c0565b005b61006361010d565b600054600154600254909192565b60405173ffffffffffffffffffffffffffffffffffffffff84169082156108fc029083908590600081818185878a8ad0945050505050158015610107573d6000803e3d6000fd5b50505050565bd3d2349091925600a165627a7a72305820a2fb39541e90eda9a2f5f9e7905ef98e66e60dd4b38e00b05de418da3154e7570029",

            "consumeUserResourcePercent": 100,

            "originEnergyLimit": 11111111111111,

            "value": "0x1f4",

            "tokenId": 1000033,

            "tokenValue": 100000

        }

    ]

}

'

```

Result

```json

{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"598d8aafbf9340e92c8f72a38389ce9661b643ff37dd2a609f393336a76025b9","contract_address":"41dfd93697c0a978db343fe7a92333e11eeb2f967d","raw_data":{"contract":[{"parameter":{"value":{"token_id":1000033,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","call_token_value":100000,"new_contract":{"bytecode":"6080604052d3600055d2600155346002556101418061001f6000396000f3006080604052600436106100565763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166305c24200811461005b5780633be9ece71461008157806371dc08ce146100aa575b600080fd5b6100636100b2565b60408051938452602084019290925282820152519081900360600190f35b6100a873ffffffffffffffffffffffffffffffffffffffff600435166024356044356100c0565b005b61006361010d565b600054600154600254909192565b60405173ffffffffffffffffffffffffffffffffffffffff84169082156108fc029083908590600081818185878a8ad0945050505050158015610107573d6000803e3d6000fd5b50505050565bd3d2349091925600a165627a7a72305820a2fb39541e90eda9a2f5f9e7905ef98e66e60dd4b38e00b05de418da3154e7570029","consume_user_resource_percent":100,"name":"transferTokenContract","origin_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","abi":{"entrys":[{"outputs":[{"type":"trcToken"},{"type":"uint256"},{"type":"uint256"}],"payable":true,"name":"getResultInCon","stateMutability":"Payable","type":"Function"},{"payable":true,"inputs":[{"name":"toAddress","type":"address"},{"name":"id","type":"trcToken"},{"name":"amount","type":"uint256"}],"name":"TransferTokenTo","stateMutability":"Payable","type":"Function"},{"outputs":[{"type":"trcToken"},{"type":"uint256"},{"type":"uint256"}],"payable":true,"name":"msgTokenValueAndTokenIdTest","stateMutability":"Payable","type":"Function"},{"payable":true,"stateMutability":"Payable","type":"Constructor"}]},"origin_energy_limit":11111111111111,"call_value":500}},"type_url":"type.googleapis.com/protocol.CreateSmartContract"},"type":"CreateSmartContract"}],"ref_block_bytes":"80be","ref_block_hash":"ac7c3d59c55ac92c","expiration":1634030190000,"fee_limit":333333280,"timestamp":1634030131693},"raw_data_hex":"0a0280be2208ac7c3d59c55ac92c40b0fba79ec72f5ad805081e12d3050a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e437265617465536d617274436f6e7472616374129e050a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d812fc040a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d81adb010a381a0e676574526573756c74496e436f6e2a0a1a08747263546f6b656e2a091a0775696e743235362a091a0775696e743235363002380140040a501a0f5472616e73666572546f6b656e546f22141209746f416464726573731a0761646472657373220e120269641a08747263546f6b656e22111206616d6f756e741a0775696e743235363002380140040a451a1b6d7367546f6b656e56616c7565416e64546f6b656e4964546573742a0a1a08747263546f6b656e2a091a0775696e743235362a091a0775696e743235363002380140040a0630013801400422e0026080604052d3600055d2600155346002556101418061001f6000396000f3006080604052600436106100565763ffffffff7c010000000000000000000000000000000000000000000000000000000060003504166305c24200811461005b5780633be9ece71461008157806371dc08ce146100aa575b600080fd5b6100636100b2565b60408051938452602084019290925282820152519081900360600190f35b6100a873ffffffffffffffffffffffffffffffffffffffff600435166024356044356100c0565b005b61006361010d565b600054600154600254909192565b60405173ffffffffffffffffffffffffffffffffffffffff84169082156108fc029083908590600081818185878a8ad0945050505050158015610107573d6000803e3d6000fd5b50505050565bd3d2349091925600a165627a7a72305820a2fb39541e90eda9a2f5f9e7905ef98e66e60dd4b38e00b05de418da3154e757002928f40330643a157472616e73666572546f6b656e436f6e747261637440c7e3d28eb0c30218a08d0620e1843d70edb3a49ec72f9001a086f99e01"}}}

```

### TriggerSmartContract

**Parameters**  

Object - the items in object as below: 

|            |                |                                              |
| :--------- | :------------- | :------------------------------------------- |
| from       | DATA, 20 Bytes | The address the transaction is sent from     |
| to         | DATA, 20 Bytes | The address of the smart contract            |
| data       | DATA           | The invoked contract function and parameters |
| gas        | DATA           | Fee limit                                    |
| value      | DATA           | The data passed through call_value           |
| tokenId    | QUANTITY       | Token ID                                     |
| tokenValue | QUANTITY       | The transfer amount of TRC10                 |

**Returns**

Object - transaction of TriggerSmartContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"id": 1337,

    "jsonrpc": "2.0",

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "to": "0xf859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd",

            "data": "0x3be9ece7000000000000000000000000ba8e28bdb6e49fbb3f5cd82a9f5ce8363587f1f600000000000000000000000000000000000000000000000000000000000f42630000000000000000000000000000000000000000000000000000000000000001",

            "gas": "0x245498",

            "value": "0xA",

            "tokenId": 1000035,

            "tokenValue": 20

        }

    ]

    }

'

```

Result

```json

{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"c3c746beb86ffc366ec0ff8bf6c9504c88f8714e47bc0009e4f7e2b1d49eb967","raw_data":{"contract":[{"parameter":{"value":{"amount":10,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","to_address":"41f859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"958c","ref_block_hash":"9d8c6bae734a2281","expiration":1684469328000,"timestamp":1684469270364},"raw_data_hex":"0a02958c22089d8c6bae734a22814080d1c89183315a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d8121541f859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd180a70dc8ec5918331"}}}

```

