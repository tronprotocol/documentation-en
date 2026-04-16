# eth_coinbase

Returns the super representative address of the current node.

**Parameters**  

None

**Returns**  

DATA - The super representative address of the node.   (Note: Return the first address If more than one super representative address is configured, return error if there is no valid address or the address did not generate any block, the error will be “etherbase must be explicitly specified” . )

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "eth_coinbase", "params": []}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"error":{"code":-32000,"message":"etherbase must be explicitly specified","data":"{}"}}

```
