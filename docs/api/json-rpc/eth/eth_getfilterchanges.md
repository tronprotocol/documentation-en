# eth_getFilterChanges

*Polling method for a filter, which returns an array of logs which occurred since last poll.*

**Parameters**  

QUANTITY - the filter id.

**Returns**

- For filters created with eth_newFilte, return logs object list, each log object with following params:

| Field            | Type           | Description                                                                                 |
| :--------------- | :------------- | :------------------------------------------------------------------------------------------ |
| removed          | TAG            | true when the log was removed, due to a chain reorganization. false if its a valid log.     |
| logIndex         | QUANTITY       | Integer of the log index position in the block. null when its pending log.                  |
| transactionIndex | QUANTITY       | Integer of the transactions index position log was created from. null when its pending log. |
| transactionHash  | DATA, 32Bytes  | Hash of the transactions this log was created from.                                         |
| blockHash        | DATA, 32 Bytes | Hash of the block where this log was in. null when its pending.                             |
| blockNumber      | QUANTITY       | The block number where this log was in.                                                     |
| address          | DATA, 32 Bytes | Address from which this log originated.                                                     |
| data             | DATA           | Contains one or more 32 Bytes non-indexed arguments of the log.                             |
| topics           | DATA\[]        | Event topic and indexed arguments.                                                          |

- For filters created with eth_newBlockFilter the return are block hashes (DATA, 32 Bytes).

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "jsonrpc": "2.0",

    "method": "eth_getFilterChanges",

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
