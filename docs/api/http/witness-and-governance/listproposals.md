# listproposals

TRON API method that retrieves all governance proposals on the TRON network, providing a comprehensive view of current and past proposals.

## HTTP Request

`POST /wallet/listproposals`

## Supported Paths

- `/wallet/listproposals`

## Parameters

This method does not require any parameters.

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
  --url https://api.shasta.trongrid.io/wallet/listproposals \
  --header 'Content-Type: application/json' \
  --data '{}'
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

- Displaying all governance proposals in management interfaces
- Building comprehensive governance dashboards
- Analyzing proposal trends and voting patterns
- Creating proposal monitoring and notification systems
