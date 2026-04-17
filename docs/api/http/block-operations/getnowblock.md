# getnowblock

TRON API method that retrieves the current latest block from the TRON blockchain. This method returns the most recently produced block with all its transactions and metadata.

## HTTP Request

`POST /wallet/getnowblock`

## Supported Paths

- `/wallet/getnowblock`
- `/walletsolidity/getnowblock`

## Parameters

This method accepts no parameters.

## Response

- blockID — the block hash identifier
- block_header — block header information containing:
  - raw_data — raw block header data including:
    - timestamp — block generation timestamp
    - txTrieRoot — transaction trie root hash
    - parentHash — parent block hash
    - number — block height
    - witness_address — address of the block producer
    - version — block version
  - witness_signature — block producer’s signature
- transactions — array of transactions included in the block

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getnowblock \
  --header 'Content-Type: application/json' \
  --data '{}'
```

### Response

```json
{
  "blockID": "<string>",
  "block_header": {
    "raw_data": {},
    "witness_signature": "<string>"
  },
  "transactions": "<array>"
}
```

## Use Case

- Monitoring the latest state of the blockchain in real-time.
- Retrieving the current block height and latest transactions.
- Synchronizing applications with the blockchain’s current state.
- Implementing block explorers and monitoring tools.
- Watching for new transactions as they are confirmed.
