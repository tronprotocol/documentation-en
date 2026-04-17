# eth_getTransactionByHash

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
