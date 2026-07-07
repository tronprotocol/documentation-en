# /wallet/getproposalbyid

Query a proposal by ID.

- Source: `framework/src/main/java/org/tron/core/services/http/GetProposalByIdServlet.java`
- Method: `GET` / `POST`
- Response: `protocol.Proposal` (`Tron.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | int64 | Yes | Proposal ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getproposalbyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "id": 70
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `proposal_id` | int64 | Proposal ID |
| `proposer_address` | string | Proposer address |
| `parameters` | map<int64, int64> | Parameter entries |
| `expiration_time` | int64 | Expiration time (millisecond timestamp) |
| `create_time` | int64 | Creation time (millisecond timestamp) |
| `approvals` | repeated string | Addresses of SRs that approved |
| `state` | enum | `PENDING` / `DISAPPROVED` / `APPROVED` / `CANCELED` |

Response example (Nile, `id=70`, lowering `getAccountUpgradeCost` from 9999 TRX to 9997 TRX; did not reach the approval threshold before expiry, the `approvals` field is absent):

```json
{
  "proposal_id": 70,
  "proposer_address": "412e9d9ea27e51b0307afc7ce64654cf9359b74cec",
  "parameters": [
    { "key": 1, "value": 9997000000 }
  ],
  "expiration_time": 1582381800000,
  "create_time": 1582381197000,
  "state": "DISAPPROVED"
}
```

Returns `{}` when not found.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `id` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| `id` missing (POST) | `{"Error": "class java.security.InvalidParameterException : key [id] does not exist"}` |
| `id` is not numeric (POST, including string/bool/array/object) | `{"Error": "class java.lang.NumberFormatException : null"}` (`Util.getJsonLongValue` uses `org.tron.json.JSONObject#getBigDecimal`) |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
