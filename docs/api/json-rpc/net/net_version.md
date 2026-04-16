# net_version

*Returns the hash of the genesis block.*

**Parameters**  

None

**Returns**  

String - The hash of genesis block

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"net_version","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x2b6653dc"}

```
