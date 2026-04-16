# eth_newFilter

*Creates a filter object, based on filter options, to notify when the state changes (logs).*

**Parameters**  

Object - The filter options:

| Field     | Type                  | Description                                                               |
| :-------- | :-------------------- | :------------------------------------------------------------------------ |
| fromBlock | QUANTITY\|TAG         | Integer block number, or "latest"                                         |
| toBlock   | QUANTITY\|TAG         | Integer block number, or "latest"                                         |
| address   | DATA\|Array, 20 Bytes | Contract address or a list of addresses from which logs should originate. |
| topics    | Array of DATA         | Topics                                                                    |

**Returns**  

QUANTITY - A filter id.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_newFilter","params":[{"address":["cc2e32f2388f0096fae9b055acffd76d4b3e5532","E518C608A37E2A262050E10BE0C9D03C7A0877F3"],"fromBlock":"0x989680","toBlock":"0x9959d0","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",null,["0x0000000000000000000000001806c11be0f9b9af9e626a58904f3e5827b67be7","0x0000000000000000000000003c8fb6d064ceffc0f045f7b4aee6b3a4cefb4758"]]}],"id":1}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":"0x2bab51aee6345d2748e0a4a3f4569d80"}

```
