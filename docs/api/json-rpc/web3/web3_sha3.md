# web3_sha3

*Returns Keccak-256 (not the standardized SHA3-256) of the given data.*

**Parameters**  

DATA - the data to convert into a SHA3 hash

**Returns**  

DATA - The SHA3 result of the given string.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc": "2.0", "id": 1, "method": "web3_sha3", "params": ["0x68656c6c6f20776f726c64"]}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x47173285a8d7341e5e972fc677286384f802f8ef42a5ec5f03bbfa254cb01fad"}

```
