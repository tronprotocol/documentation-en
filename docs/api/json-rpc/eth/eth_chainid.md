# eth_chainId

*Returns the chainId of the TRON network which is the last four bytes of the genesis block hash*

**Parameters**  

None

**Returns**  

DATA - The chainId of the TRON network

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":79}'

```

Result

```json

{"jsonrpc":"2.0","id":79,"result":"0x2b6653dc"}

```
