# eth_getBlockByNumber

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
