# eth_syncing

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
