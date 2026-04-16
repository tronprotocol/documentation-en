# net_peerCount

*Returns number of peers currently connected to the client.*

**Parameters**  

None

**Returns**  

QUANTITY - integer of the number of connected peers.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x9"}

```
