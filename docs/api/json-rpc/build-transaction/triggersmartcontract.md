# TriggerSmartContract

**Parameters**  

Object - the items in object as below: 

|            |                |                                              |
| :--------- | :------------- | :------------------------------------------- |
| from       | DATA, 20 Bytes | The address the transaction is sent from     |
| to         | DATA, 20 Bytes | The address of the smart contract            |
| data       | DATA           | The invoked contract function and parameters |
| gas        | DATA           | Fee limit                                    |
| value      | DATA           | The data passed through call_value           |
| tokenId    | QUANTITY       | Token ID                                     |
| tokenValue | QUANTITY       | The transfer amount of TRC10                 |

**Returns**

Object - transaction of TriggerSmartContract or an error

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{"id": 1337,

    "jsonrpc": "2.0",

    "method": "buildTransaction",

    "params": [

        {

            "from": "0xC4DB2C9DFBCB6AA344793F1DDA7BD656598A06D8",

            "to": "0xf859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd",

            "data": "0x3be9ece7000000000000000000000000ba8e28bdb6e49fbb3f5cd82a9f5ce8363587f1f600000000000000000000000000000000000000000000000000000000000f42630000000000000000000000000000000000000000000000000000000000000001",

            "gas": "0x245498",

            "value": "0xA",

            "tokenId": 1000035,

            "tokenValue": 20

        }

    ]

    }

'

```

Result

```json

{"jsonrpc":"2.0","id":1337,"result":{"transaction":{"visible":false,"txID":"c3c746beb86ffc366ec0ff8bf6c9504c88f8714e47bc0009e4f7e2b1d49eb967","raw_data":{"contract":[{"parameter":{"value":{"amount":10,"owner_address":"41c4db2c9dfbcb6aa344793f1dda7bd656598a06d8","to_address":"41f859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd"},"type_url":"type.googleapis.com/protocol.TransferContract"},"type":"TransferContract"}],"ref_block_bytes":"958c","ref_block_hash":"9d8c6bae734a2281","expiration":1684469328000,"timestamp":1684469270364},"raw_data_hex":"0a02958c22089d8c6bae734a22814080d1c89183315a65080112610a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412300a1541c4db2c9dfbcb6aa344793f1dda7bd656598a06d8121541f859b5c93f789f4bcffbe7cc95a71e28e5e6a5bd180a70dc8ec5918331"}}}

```
