# eth_blockNumber

*Returns the number of the most recent block.*

**Parameters**  

None

**Returns**  

The latest block number.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":64}'

```

```json

{"jsonrpc":"2.0","id":64,"result":"0x20e0cf0"}

```
