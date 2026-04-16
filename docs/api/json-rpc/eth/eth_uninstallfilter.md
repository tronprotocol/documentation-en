# eth_uninstallFilter

*Uninstalls a filter with given id. Should always be called when watch is no longer needed. Additionally Filters timeout when they aren't requested with eth_getFilterChanges for a period of time.*

**Parameters**  

QUANTITY - the filter id.

**Returns**

 Boolean - true if the filter was successfully uninstalled, otherwise false.

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "jsonrpc": "2.0",

    "method": "eth_uninstallFilter",

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

    "result": true

}

```
