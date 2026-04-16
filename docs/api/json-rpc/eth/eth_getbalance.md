# eth_getBalance

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
