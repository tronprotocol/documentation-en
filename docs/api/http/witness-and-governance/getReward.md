# /wallet/getReward

Query the unclaimed voting rewards for an account.

- Source: `framework/src/main/java/org/tron/core/services/http/GetRewardServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getReward`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `address` | string | No | Voter account address; omitted or empty returns `reward: 0` |
| `visible` | bool | No | No effect (the servlet auto-detects address format via the `41` prefix; the response has no bytes fields) |
| `int64_as_string` | bool | No | GET only; when `true`, returns `reward` as a JSON string |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getReward \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `reward` | int64 | Unit: sun (1 TRX = 1e6 sun) |

Response example (Nile, sr-15 currently accumulated reward, ~29994831 TRX):

```json
{ "reward": 29994831460307 }
```

> Note: when `address` is missing or empty, no error is reported; `reward` is `0` (or `"0"` when `int64_as_string=true` on GET).

With `?int64_as_string=true` on a GET request:

```json
{ "reward": "29994831460307" }
```

Withdraw via [`/wallet/withdrawbalance`](withdrawbalance.md).

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `address` parse failure (invalid hex / base58) | `{"Error": "INVALID address, <details>"}` |
| Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
