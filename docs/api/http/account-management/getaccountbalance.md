# getaccountbalance

TRON API method that retrieves the TRX balance and related balance information for a specific account. This method provides comprehensive balance data including available balance, frozen balance, and delegated resources.

## HTTP Request

`POST /wallet/getaccountbalance`

## Supported Paths

- `/wallet/getaccountbalance`

## Parameters

- account_identifier.address — the account address to query. Use base58 with visible: true, or hex with visible: false.
- block_identifier — required object specifying the block to query. Provide both the 32‑byte hash (64 hex chars) and the matching number.
- visible — optional boolean for address format. Default is false (hex).

## Response

- balance — available TRX balance (in sun, where 1 TRX = 1,000,000 sun)
- frozen — array of frozen balance information
  - frozen_balance — amount of TRX frozen
  - expire_time — expiration timestamp for frozen balance
- delegated_frozenV2 — delegated frozen balance information for v2 staking
- undelegated_frozenV2 — undelegated frozen balance information for v2 staking

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getaccountbalance \
  --header 'Content-Type: application/json' \
  --data '
{
  "account_identifier": {
    "address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e"
  },
  "block_identifier": {
    "hash": "0000000004986736812cbf15ffbcdd229bd3d76a595db895719867cc2da3a5bd",
    "number": 77096758
  },
  "visible": false
}
'
```

### Response

```json
{
  "balance": 123,
  "frozen": [
    {
      "frozen_balance": 123,
      "expire_time": 123
    }
  ],
  "delegated_frozenV2": [
    {
      "type": "<string>",
      "frozen_balance": 123
    }
  ],
  "undelegated_frozenV2": [
    {
      "type": "<string>",
      "unfreeze_amount": 123,
      "unfreeze_expire_time": 123
    }
  ]
}
```

## Use Case

- Checking available TRX balance for transactions and transfers.
- Monitoring frozen balance and staking information.
- Analyzing delegated resource allocations.
- Managing account liquidity and resource planning.

## Curl Examples

- avoid INVALID hex String by providing a real 32‑byte block hash (64 hex chars).
- avoid account_identifier is null by passing account_identifier: { address: ... } rather than a top‑level address.
- avoid block_identifier null and hash length not equals 32 by always including block_identifier.hash with 64 hex chars, and block_identifier.number that matches the same block.

## Working Example Auto Picks Latest Block

Run this to fetch the latest blockID, resolve its block number, and immediately query the balance at that block.Shell# requires jq
BLOCK_ID=$(curl -s -X POST \
 'https://api.shasta.trongrid.io/wallet/getnowblock' \
 -H 'Content-Type: application/json' | jq -r '.blockID')
NUMBER=$(curl -s -X POST \
 'https://api.shasta.trongrid.io/wallet/getblockbyid' \
 -H 'Content-Type: application/json' \
 --data "{\"value\": \"$BLOCK_ID\"}" | jq -r '.block_header.raw_data.number')

curl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/getaccountbalance' \
 --header 'Content-Type: application/json' \
 --data "{\n \"account_identifier\": { \"address\": \"41608f8da72479edc7dd921e4c30bb7e7cddbe722e\" },\n \"block_identifier\": { \"hash\": \"$BLOCK_ID\", \"number\": $NUMBER },\n \"visible\": false\n}"
If jq is not available, use Python instead:ShellBLOCK_ID=$(curl -s -X POST \
 'https://api.shasta.trongrid.io/wallet/getnowblock' \
 -H 'Content-Type: application/json' | python3 -c 'import sys,json; print(json.load(sys.stdin)["blockID"])')
NUMBER=$(curl -s -X POST \
 'https://api.shasta.trongrid.io/wallet/getblockbyid' \
 -H 'Content-Type: application/json' \
 --data "{\"value\": \"$BLOCK_ID\"}" | python3 -c 'import sys,json; print(json.load(sys.stdin)["block_header"]["raw_data"]["number"])')

curl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/getaccountbalance' \
 --header 'Content-Type: application/json' \
 --data "{\n \"account_identifier\": { \"address\": \"41608f8da72479edc7dd921e4c30bb7e7cddbe722e\" },\n \"block_identifier\": { \"hash\": \"$BLOCK_ID\", \"number\": $NUMBER },\n \"visible\": false\n}"
Bodyapplication/jsonaccount_identifierobjectrequiredShow child attributesblock_identifierobjectrequiredBlock to query the balance at. Provide both the 32-byte block hash (64 hex chars) and its number; the node validates they match.Show child attributesvisiblebooleandefault:falseResponse200 - application/jsonAccount balance informationbalanceintegerAvailable TRX balance in sunfrozenobject[]Frozen balance informationShow child attributesdelegated_frozenV2object[]Delegated frozen balance v2Show child attributesundelegated_frozenV2object[]Undelegated frozen balance v2Show child attributesLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/getaccount | TRONwallet/getaccountnet | TRON
