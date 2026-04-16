# eth_getWork

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
