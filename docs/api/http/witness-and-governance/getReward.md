# /wallet/getReward

Query the unclaimed voting rewards for an account.

- Source: `framework/src/main/java/org/tron/core/services/http/GetRewardServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getReward`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `address` | string | Yes | Voter account address |
| `visible` | bool | No | No effect (the servlet auto-detects address format via the `41` prefix; the response has no bytes fields) |

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

Withdraw via [`/wallet/withdrawbalance`](withdrawbalance.md).

### Error responses

| Trigger | Response |
|---|---|
| `address` parse failure (invalid hex / base58) | `{"Error": "INVALID address, <details>"}` |
| Request body is not valid JSON (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
