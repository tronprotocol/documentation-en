# eth_protocolVersion

*Returns the java-tron block version*

**Parameters**  

None

**Returns**  

String - The current java-tron block version

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_protocolVersion","params":[],"id":64}'

```

Result

```json

{"jsonrpc":"2.0","id":64,"result":"0x16"}

```
