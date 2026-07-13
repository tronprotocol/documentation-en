# /wallet/listproposals

Get the list of all proposals.

- Source: `framework/src/main/java/org/tron/core/services/http/ListProposalsServlet.java`
- Method: `GET` / `POST`
- Response: `api.ProposalList`

## Request parameters

Both GET and POST read these fields from URL query parameters; the servlet does not parse the POST body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `visible` | GET / POST | bool | No | Address format |

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

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to read Proposal storage) | `{"Error": "<exceptionClass> : <message>"}` |
