# eth_getTransactionByBlockHashAndIndex

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
