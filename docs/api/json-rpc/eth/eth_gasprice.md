# eth_gasPrice

Returns the current energy price in sun.

**Parameters**  

None

**Returns**  

Integer of the current energy price in sun.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_gasPrice", "params": []}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x8c"}

```
