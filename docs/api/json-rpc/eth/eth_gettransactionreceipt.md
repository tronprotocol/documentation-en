# eth_getTransactionReceipt

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
