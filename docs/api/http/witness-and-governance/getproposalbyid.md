# getproposalbyid

TRON API method that retrieves detailed information about a specific governance proposal using its ID.

## HTTP Request

`POST /wallet/getproposalbyid`

## Supported Paths

- `/wallet/getproposalbyid`

## Parameters

- id — the ID of the proposal to retrieve information for.

## Response

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
  --url https://api.shasta.trongrid.io/wallet/getproposalbyid \
  --header 'Content-Type: application/json' \
  --data '{
  "id": 1
}'
```

### Response

```json
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
```

## Use Case

- Retrieving detailed proposal information for governance interfaces
- Checking proposal status and approval progress
- Monitoring proposal parameters and voting results
- Building governance dashboards and voting applications
