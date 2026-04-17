# eth_getFilterLogs

*Returns an array of all logs matching filter with given id.*

**Parameters**  

QUANTITY - the filter id.

**Returns**

See [eth_getFilterChanges](#eth_getfilterchanges)。

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "jsonrpc": "2.0",

    "method": "eth_getFilterLogs",

    "params": [

        "0xc11a84d5e906ecb9f5c1eb65ee940b154ad37dce8f5ac29c80764508b901d996"

    ],

    "id": 71

}'

```

Result

```json

{

    "jsonrpc": "2.0",

    "id": 71,

    "error": {

        "code": -32000,

        "message": "filter not found",

        "data": "{}"

    }

}

```
