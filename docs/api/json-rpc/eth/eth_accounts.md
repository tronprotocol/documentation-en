# eth_accounts

*Returns a list of addresses owned by the client.*

**Parameters**  

None

**Returns**  

Empty List

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '

{"jsonrpc": "2.0", "id": 1, "method": "eth_accounts", "params": []}'

```

```json

{"jsonrpc":"2.0","id":1,"result":[]}

```
