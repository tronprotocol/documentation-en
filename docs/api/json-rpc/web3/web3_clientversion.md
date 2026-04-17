# web3_clientVersion

*Returns the current client version.*

**Parameters**  

None

**Returns**  

String - The current client version

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "web3_clientVersion", "params": []}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"TRON/v4.3.0/Linux/Java1.8/GreatVoyage-v4.2.2.1-281-gc1d9dfd6c"}

```
