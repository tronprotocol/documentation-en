# /wallet/listwitnesses

Get the list of all SR candidates.

- Source: `framework/src/main/java/org/tron/core/services/http/ListWitnessesServlet.java`
- Method: `GET` / `POST`
- Response: `api.WitnessList`
- Solidity endpoint: `/walletsolidity/listwitnesses`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `visible` | bool | No | Address format (`url` in the response is a proto `string` and is not affected by `visible`) |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/listwitnesses \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `witnesses` | repeated Witness | Candidate list |

`Witness` (`Tron.proto`) fields:

| Field | Type | Description |
|---|---|---|
| `address` | string | Candidate address |
| `voteCount` | int64 | Current vote count |
| `pubKey` | string(hex) | Public key |
| `url` | string | Candidate URL |
| `totalProduced` | int64 | Cumulative blocks produced |
| `totalMissed` | int64 | Cumulative missed blocks |
| `latestBlockNum` | int64 | Latest produced block height |
| `latestSlotNum` | int64 | Latest slot |
| `isJobs` | bool | Whether currently an active SR (top 27) |

Response example (Nile has 800+ candidates, only the first one is shown; `voteCount`, `latestBlockNum`, `latestSlotNum` change over time):

```json
{
  "witnesses": [
    {
      "address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
      "voteCount": 2320142029,
      "url": "http://sr-15.com",
      "totalProduced": 1897834,
      "totalMissed": 252,
      "latestBlockNum": 66987961,
      "latestSlotNum": 592482103,
      "isJobs": true
    }
    /* ... other candidates */
  ]
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Internal node error (failed to read Witness storage) | `{"Error": "<exceptionClass> : <message>"}` |
