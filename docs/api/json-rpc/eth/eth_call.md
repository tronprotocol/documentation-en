# eth_call

*Executes a message call immediately without creating a transaction on the block chain.*

**Parameters**

1\. Object - The transaction call object, the items in it as below.

| Item Name | Data Type      | Description                                                   |
| :-------- | :------------- | :------------------------------------------------------------ |
| from      | DATA, 20 Bytes | Caller address. Hex format address, remove the prefix "41"    |
| to        | DATA, 20 Bytes | Contract address.  Hex format address, remove the prefix "41" |
| gas       | QUANTITY       | Not supported. The value is 0x0                               |
| gasPrice  | QUANTITY       | Not supported. The value is 0x0                               |
| value     | QUANTITY       | Amount of TRX sent with this transaction(Unit:sun, format: hex); default: 0x0                               |
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
