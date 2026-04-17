# TransferAssetContract

**Parameters**  

Object - the items in object as below: 

|            |                |                                            |
| :--------- | :------------- | :----------------------------------------- |
| from       | DATA, 20 Bytes | The address the transaction is sent from   |
| to         | DATA, 20 Bytes | The address the transaction is directed to |
| tokenId    | QUANTITY       | Token ID                                   |
| tokenValue | QUANTITY       | The transfer amount of TRC10               |

**Returns**

Object - transaction of TransferAssetContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "to": "0x95FD23D3D2221CFEF64167938DE5E62074719E54",

            "tokenId": 1000016,

            "tokenValue": 20

        }

    ],

    "id": 44,

    "jsonrpc": "2.0"

}

'

```

Result

```json

{"jsonrpc":"2.0","id":44,"error":{"code":-32600,"message":"assetBalance must be greater than 0.","data":"{}"}}

```
