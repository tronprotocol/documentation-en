# votewitnessaccount

TRON API method that creates a transaction to vote for witnesses (validators) using frozen TRX balance. Voting is essential for TRON’s Delegated Proof of Stake (DPoS) governance system and helps determine which witnesses become Super Representatives.

## HTTP Request

`POST /wallet/votewitnessaccount`

## Supported Paths

- `/wallet/votewitnessaccount`

## Parameters

- owner_address — address of the account casting votes. Use base58 with visible: true, or hex with visible: false.
- votes — array of vote allocations, each containing:
  - vote_address — witness address to vote for (base58 with visible: true, or a 21‑byte hex address starting with 41 when visible: false).
  - vote_count — number of votes to allocate to this witness.
- visible — optional boolean. When true, addresses are base58; when false, hex. Default is true.

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the voting transaction
- raw_data — raw transaction data containing:
  - contract — array with witness voting contract details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/votewitnessaccount \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "votes": [
    {
      "vote_address": "TDdeM7G4HSxhn2MfovsiMWwXZkiFaHhjMB",
      "vote_count": 1000000
    },
    {
      "vote_address": "TAybtvPZCSj5kumiU4myD28xBy6WFtkgCu",
      "vote_count": 500000
    }
  ],
  "visible": true
}
'
```

### Response

```json
{
  "visible": true,
  "txID": "<string>",
  "raw_data": {
    "contract": "<array>",
    "ref_block_bytes": "<string>",
    "ref_block_hash": "<string>",
    "expiration": 123,
    "timestamp": 123
  },
  "raw_data_hex": "<string>"
}
```

## Use Case

- Participating in TRON network governance by voting for preferred witnesses.
- Supporting witnesses that align with your vision for network development.
- Earning voting rewards from witnesses who share profits with their voters.
- Influencing which witnesses become the top 27 Super Representatives.
- Distributing voting power across multiple witnesses for diversification.
- Contributing to network decentralization through democratic participation.

## Curl Example

- base58 addresses → set visible: true (recommended for humans)
- hex addresses → set visible: false and use 21‑byte hex (42 hex chars) starting with 41
