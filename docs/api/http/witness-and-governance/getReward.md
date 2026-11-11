# /wallet/getReward

Query an account's total claimable rewards in sun.

- Source: `framework/src/main/java/org/tron/core/services/http/GetRewardServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getReward`

## Request parameters

GET reads `address` from the URL query; POST reads it from a JSON request body. `visible` is ignored.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `address` | GET / POST | string | No | Account address (voter or SR); omitted or empty returns `reward: 0` |
| `visible` | GET / POST | bool | No | No effect (the servlet auto-detects address format via the `41` prefix; the response has no bytes fields) |
| `int64_as_string` | GET | bool | No | GET only; when `true`, returns `reward` as a JSON string |

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
| `reward` | int64 | Total claimable rewards; unit: sun (1 TRX = 1e6 sun) |

Response example (Nile, sr-15 currently accumulated reward, ~29994831 TRX):

```json
{ "reward": 29994831460307 }
```

> Missing or empty addresses, and Base58Check addresses rejected for length, checksum, or decoded-address validity, return a zero reward. This is indistinguishable from an account with no claimable rewards. Validate the address before using the result; parser exceptions follow the error table below.

With `?int64_as_string=true` on a GET request:

```json
{ "reward": "29994831460307" }
```

Withdraw via [`/wallet/withdrawbalance`](withdrawbalance.md).

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Hex decoding throws, or Base58 decoding throws (for example, an illegal character in an address of the expected length) | `{"Error": "INVALID address, <details>"}` |
| GET / POST | Base58Check address has the wrong length, checksum, or decoded-address validity | `{"reward": 0}` (or `{"reward": "0"}` with GET `int64_as_string=true`) |
| POST | Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
