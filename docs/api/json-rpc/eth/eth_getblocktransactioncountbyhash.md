# eth_getBlockTransactionCountByHash

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
