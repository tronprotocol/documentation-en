# TransferContract

**Parameters**  

Object - the items in object as below: 

| Param Name | Data Type      | Description                                 |
| :--------- | :------------- | :------------------------------------------ |
| from       | DATA, 20 Bytes | The address the transaction is sent from.   |
| to         | DATA, 20 Bytes | The address the transaction is directed to. |
| value      | DATA           | the transfer amount                         |

**Returns**

Object - transaction of TransferContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

    "id": 1337,

    "jsonrpc": "2.0",

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "to": "0x95FD23D3D2221CFEF64167938DE5E62074719E54",

            "value": "0x1f4"

        }]}'

```

Result

```json

{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"ae02a80abd985a6f05478b9bbf04706f00cdbf71e38c77d21ed77e44c634cef9","raw_data":{"contract":[{"parameter":{"value":{"amount":500,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","to_address":"4195fd23d3d2221cfef64167938de5e62074719e54"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"957e","ref_block_hash":"3922d8c0d28b5283","expiration":1684469286000,"timestamp":1684469226841},"raw_data_hex":"0a02957e22083922d8c0d28b528340f088c69183315a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d812154195fd23d3d2221cfef64167938de5e62074719e5418f40370d9bac2918331"}}}

```
