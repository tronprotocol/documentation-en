# getblockbyid

TRON API method that retrieves a specific block from the TRON blockchain using its block ID (hash). This method allows you to fetch detailed information about a particular block, including its header, transactions, and metadata.

## HTTP Request

`POST /wallet/getblockbyid`

## Supported Paths

- `/wallet/getblockbyid`
- `/walletsolidity/getblockbyid`

## Parameters

- value — the block ID (hash) in hexadecimal format to retrieve

## Response

- blockID — the block hash identifier
- block_header — block header information containing:
  - raw_data — raw block header data including:
    - timestamp — block generation timestamp in milliseconds
    - txTrieRoot — transaction trie root hash
    - parentHash — parent block hash
    - number — block height/number
    - witness_address — address of the block producer (witness)
    - version — block version
  - witness_signature — digital signature of the block producer
- transactions — array of all transactions included in the block

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getblockbyid \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "0000000000f4245300b88ffeb9bdb95b88c66b5ce6bb0ee79d85d5ce14b6a2a7ca"
}
'
```

### Response

```json
{
  "blockID": "<string>",
  "block_header": {
    "raw_data": {
      "timestamp": 123,
      "txTrieRoot": "<string>",
      "parentHash": "<string>",
      "number": 123,
      "witness_address": "<string>",
      "version": 123
    },
    "witness_signature": "<string>"
  },
  "transactions": [
    {}
  ]
}
```

## Use Case

- Retrieving detailed information about a specific block using its hash.
- Building block explorers that need to display block details by ID.
- Verifying block contents and validating transactions within a specific block.
- Analyzing historical blockchain data for auditing and compliance purposes.
- Implementing blockchain synchronization tools that need to fetch blocks by their identifiers.
