# /wallet/getpaginatedproposallist

Paginated query of proposals.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPaginatedProposalListServlet.java`
- Method: `GET` / `POST`
- Response: `api.ProposalList`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `offset` | GET | int64 | Yes | Starting offset; omission reaches `Long.parseLong(null)` and fails |
| `offset` | POST | int64 | No | Starting offset; Protobuf default is `0` |
| `limit` | GET | int64 | Yes | Page size; omission reaches `Long.parseLong(null)` and fails |
| `limit` | POST | int64 | No | Page size; Protobuf default is `0`, which returns an empty list |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpaginatedproposallist \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "offset": 0,
  "limit": 1
}
'
```
## Response

Same fields as [`/wallet/listproposals`](listproposals.md).

Response example (Nile, limit=1; `approvals` actually contains 27 SR addresses, omitted here):

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
  ]
}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET | `offset` / `limit` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
