# net_listening

*Returns true if the client is actively listening for network connections.*

**Parameters**  

None

**Returns**  

Boolean - true when listening, otherwise false.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_listening","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":true}

```
