# /wallet/getcandelegatedmaxsize

Query the maximum amount of resource an account can currently delegate (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetCanDelegatedMaxSizeServlet.java`
- Method: `GET` / `POST`
- Response: `api.CanDelegatedMaxSizeResponseMessage`
- Solidity endpoint: `/walletsolidity/getcandelegatedmaxsize`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `owner_address` | GET | string | Yes | Account address |
| `owner_address` | POST | string | No | Account address; omitted uses empty bytes and returns the default result |
| `type` | GET / POST | int32 | No | Resource type: `0`=BANDWIDTH (default), `1`=ENERGY |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcandelegatedmaxsize \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "type": 1
}
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `max_size` | int64 | Maximum frozen amount that can be delegated (sun) |

Response example (account has 0 delegatable ENERGY; proto default is not serialized, returns empty `{}`; when there is delegatable resource it looks like `{"max_size": 5000000000}`):

```json
{}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET | `type` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| GET / POST | `owner_address` is not valid base58check (`visible=true`) | GET: non-base58 characters throw `{"Error": "class java.lang.IllegalArgumentException : <details>"}` only when the input is exactly 34 characters long. Incorrect input length, bad checksum, or an invalid decoded address causes `Util.getHexAddress` to return an empty hex string, so no account is found and `{}` is returned. POST (via `JsonFormat.merge`): illegal characters, bad checksum, or invalid address length return `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: <fully-qualified proto field>"}` |
| GET / POST | `owner_address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
