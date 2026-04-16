# eth_getCode

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
