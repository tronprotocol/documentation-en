# eth_getLogs

*Returns an array of all logs matching a given filter object.*

**Parameters**  

Object - The filter options which include below fields:

| Field     | Type                  | Description                                                                                                                      |
| :-------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| fromBlock | QUANTITY\|TAG         | (optional, default: "latest") Integer block number, or "latest" for the last mined block                                         |
| toBlock   | QUANTITY\|TAG         | (optional, default: "latest") Integer block number, or "latest" for the last mined block                                         |
| address   | DATA\|Array, 20 Bytes | (optional) Contract address or a list of addresses from which logs should originate.                                             |
| topics    | Array of DATA         | (optional) Array of 32 Bytes DATA topics. Topics are order-dependent. Each topic can also be an array of DATA with "or" options. |
| blockhash | DATA, 32 Bytes        | (optional) Block hash                                                                                                            |

**Returns**

 See [eth_getFilterChanges](#eth_getfilterchanges).

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"jsonrpc":"2.0","method":"eth_getLogs","params":[{"address":["cc2e32f2388f0096fae9b055acffd76d4b3e5532","E518C608A37E2A262050E10BE0C9D03C7A0877F3"],"fromBlock":"0x989680","toBlock":"0x9959d0","topics":["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",null,["0x0000000000000000000000001806c11be0f9b9af9e626a58904f3e5827b67be7","0x0000000000000000000000003c8fb6d064ceffc0f045f7b4aee6b3a4cefb4758"]]}],"id":1}'

```

Result

```json

{

    "jsonrpc": "2.0",

    "id": 71,

    "result": []

}

```
