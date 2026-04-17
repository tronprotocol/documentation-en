# eth_getBlockByHash

*Returns information about a block by hash.*

**Parameters**

| Index | Data Type      | Description                                                                                    |
| :---- | :------------- | :--------------------------------------------------------------------------------------------- |
| 1     | DATA, 32 Bytes | hash of a block                                                                                |
| 2     | Boolean        | If true it returns the full transaction objects, if false only the hashes of the transactions. |

**Returns**

object - a block object  or null when no block was found. The block includes items as below.

| Item Name        | Data Type       | Description                                                                                         |
| :--------------- | :-------------- | :-------------------------------------------------------------------------------------------------- |
| number           | QUANTITY        | block number                                                                                        |
| hash             | DATA, 32 Bytes  | hash of the block                                                                                   |
| parentHash       | DATA, 32 Bytes  | hash of the parent block                                                                            |
| nonce            | QUANTITY        | unused                                                                                              |
| sha3Uncles       | DATA, 32 Bytes  | SHA3 of the uncles data in the block                                                                |
| logsBloom        | DATA, 256 Bytes | the bloom filter for the logs of the block.                                                         |
| transactionsRoot | DATA, 32 Bytes  | the root of the transaction trie of the block                                                       |
| stateRoot        | DATA, 32 Bytes  | the root of the final state trie of the block                                                       |
| receiptsRoot     | DATA, 32 Bytes  | the root of the receipts trie of the block                                                          |
| miner            | DATA, 20 Bytes  | the address of the beneficiary to whom the mining rewards were given                                |
| difficulty       | QUANTITY        | integer of the difficulty for this block                                                            |
| totalDifficulty  | QUANTITY        | integer of the total difficulty of the chain until this block                                       |
| extraData        | DATA            | the “extra data” field of this block                                                                |
| size             | QUANTITY        | integer the size of this block in bytes                                                             |
| gasLimit         | QUANTITY        | the maximum gas allowed in this block                                                               |
| gasUsed          | QUANTITY        | the total used gas by all transactions in this block                                                |
| timestamp        | QUANTITY        | the unix timestamp for when the block was created, the unit is second.                              |
| transactions     | Array           | Array of transaction objects, or 32 Bytes transaction hashes depending on the last given parameter. |
| uncles           | Array           | Array of uncle hashes                                                                               |

**Example**

```curl

curl -X POST 'https://api.shasta.trongrid.io/jsonrpc' --data '{

	"jsonrpc": "2.0",

	"method": "eth_getBlockByHash",

	"params": ["0x0000000000f9cc56243898cbe88685678855e07f51c5af91322c225ce3693868", false],

	"id": 1

}'

```

Result

```json

{"jsonrpc":"2.0","id":1,"result":null}

```
