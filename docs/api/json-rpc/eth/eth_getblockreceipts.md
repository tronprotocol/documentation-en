# eth_getBlockReceipts

*Returns transaction receipts for all transactions in the specified block. Returns null for the genesis block, blocks that have been pruned by light nodes, or blocks that have not yet been produced.*

**Parameters**

String - block number, it supports three types: block number represented as hexadecimal string, blockHash (with or without the "0x" prefix), or tags ("latest", "earliest", "finalized").

**Returns**

An array of objects - An array of transaction receipt objects, each object matches the return value of [eth_getTransactionReceipt](#eth_gettransactionreceipt)

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getBlockReceipts",

	"params": ["0x311110"],

	"id": 64

}'

```

Result

```json
{
    "jsonrpc": "2.0",
    "id": 64,
    "result": [
      {
        "blockHash": "0x0000000000311110a1bdce5bbd0bd790c27ac9681f1b3db6abd62bcc1c05dbe9",
        "blockNumber": "0x311110",
        "contractAddress": null,
        "cumulativeGasUsed": "0x13dc7",
        "effectiveGasPrice": "0xa",
        "from": "0x702f9b337aeb8be3e767345cc4954f20fa100b21",
        "gasUsed": "0x13dc7",
        "logs": [],
        "logsBloom": "0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "status": "0x1",
        "to": "0x970cabfb1ca0cdd5dae19e309f0226061ed28753",
        "transactionHash": "0x2bd303c0e75a705ee51fb16695dd7654588db968bc1735b9f7d8f6ce6b56a41b",
        "transactionIndex": "0x0",
        "type": "0x0"
      }
    ]
}
```
