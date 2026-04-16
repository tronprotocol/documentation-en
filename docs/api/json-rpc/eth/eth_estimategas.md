# eth_estimateGas

*Get the required energy through triggerConstantContract.*

**Parameters**  

object - The transaction call object, the items in it as below

| Item Name | Data Type      | Description                                          |
| :-------- | :------------- | :--------------------------------------------------- |
| from      | DATA, 20 Bytes | address of the sender                                |
| to        | DATA, 20 Bytes | address of the receiver                              |
| gas       | QUANTITY       | unused.                                              |
| gasPrice  | QUANTITY       | unused.                                              |
| value     | QUANTITY       | Integer of the value sent with this transaction      |
| data      | DATA           | Hash of the method signature and encoded parameters. |

**Returns**  

The amount of energy used.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"id": 1,

	"method": "eth_estimateGas",

	"params": [{

		"from": "0x41F0CC5A2A84CD0F68ED1667070934542D673ACBD8",

		"to": "0x4170082243784DCDF3042034E7B044D6D342A91360",

		"gas": "0x01",

		"gasPrice": "0x8c",

		"value": "0x01",

		"data": "0x70a08231000000000000000000000041f0cc5a2a84cd0f68ed1667070934542d673acbd8"

	}]

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x0"}

```
