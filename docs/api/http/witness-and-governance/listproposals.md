# /wallet/listproposals

Get the list of all proposals.

- Source: `framework/src/main/java/org/tron/core/services/http/ListProposalsServlet.java`
- Method: `GET` / `POST`
- Response: `api.ProposalList`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/listproposals \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `proposals` | repeated Proposal | Proposal list (same structure as [`/wallet/getproposalbyid`](getproposalbyid.md)) |

Response example (Nile currently has 20000+ proposals, only the first one from genesis is shown; `approvals` truncated):

```json
{
  "proposals": [
    {
      "proposal_id": 1,
      "proposer_address": "41217179d498883cdbda5699402905d1feb258796c",
      "parameters": [
        { "key": 9,  "value": 1 },
        { "key": 10, "value": 1 }
      ],
      "expiration_time": 1572597600000,
      "create_time": 1572596523000,
      "approvals": [
        "41217179d498883cdbda5699402905d1feb258796c"
        /* ... other SRs */
      ],
      "state": "APPROVED"
    }
    /* ... other proposals */
  ]
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Internal node error (failed to read Proposal storage) | `{"Error": "<exceptionClass> : <message>"}` |
