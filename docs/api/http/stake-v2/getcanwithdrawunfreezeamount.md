# /wallet/getcanwithdrawunfreezeamount

Query the unfreeze amount the account can withdraw at a given timestamp (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetCanWithdrawUnfreezeAmountServlet.java`
- Method: `GET` / `POST`
- Response: `api.CanWithdrawUnfreezeAmountResponseMessage`
- Solidity endpoint: `/walletsolidity/getcanwithdrawunfreezeamount`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `owner_address` | GET | string | Yes | Account address |
| `owner_address` | POST | string | No | Account address; omitted uses empty bytes and returns the default empty result |
| `timestamp` | GET / POST | int64 | No | Cutoff timestamp (ms); when missing or `0`, uses latest block time; when negative, returns `{}` |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcanwithdrawunfreezeamount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "timestamp":     1900000000000
}
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `amount` | int64 | Total unfreeze amount withdrawable up to that timestamp (sun) |

Response example (no in-progress unfreeze entries on the account; proto default is not serialized, returns empty `{}`; when there is a withdrawable amount it looks like `{"amount": 1500000000}`):

```json
{}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET | `timestamp` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| GET / POST | `owner_address` is not valid base58check (`visible=true`) | GET: non-base58 characters throw `{"Error": "class java.lang.IllegalArgumentException : <details>"}` only when the input is exactly 34 characters long. Incorrect input length, bad checksum, or an invalid decoded address causes `Util.getHexAddress` to return an empty hex string, so no account is found and `{}` is returned. POST (via `JsonFormat.merge`): illegal characters, bad checksum, or invalid address length return `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: <fully-qualified proto field>"}` |
| GET / POST | `owner_address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
