# eth_newBlockFilter

*Creates a filter in the node, to notify when a new block arrives.*

**Parameters**  

None.

**Returns**  

QUANTITY - A filter id.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x2bab51aee6345d2748e0a4a3f4569d80"}

```
