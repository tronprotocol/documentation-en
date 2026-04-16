# getpaginatedproposallist

TRON API method that retrieves governance proposals with pagination support, allowing efficient browsing of large proposal lists.

## HTTP Request

`POST /wallet/getpaginatedproposallist`

## Supported Paths

- `/wallet/getpaginatedproposallist`

## Parameters

- offset — the starting index for pagination (default: 0).
- limit — the maximum number of proposals to return (default: 10, max: 100).

## Response

- proposals — array of proposal objects, each containing:
  - proposal_id — the unique identifier of the proposal
  - proposer_address — the address of the Super Representative who created the proposal
  - parameters — object containing the parameter changes proposed
  - expiration_time — timestamp when the proposal expires
  - create_time — timestamp when the proposal was created
  - approvals — array of Super Representatives who have approved the proposal
  - state — current state of the proposal (PENDING, DISAPPROVED, APPROVED, CANCELED)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getpaginatedproposallist \
  --header 'Content-Type: application/json' \
  --data '
{
  "offset": 0,
  "limit": 10
}
'
```

### Response

```json
{
  "proposals": [
    {
      "proposal_id": 123,
      "proposer_address": "<string>",
      "parameters": {},
      "expiration_time": 123,
      "create_time": 123,
      "approvals": [
        "<string>"
      ],
      "state": "PENDING"
    }
  ]
}
```

## Use Case

- Implementing paginated proposal browsing in applications
- Efficiently loading large proposal datasets
- Building scalable governance interfaces with pagination
- Creating proposal exploration tools with performance optimization
