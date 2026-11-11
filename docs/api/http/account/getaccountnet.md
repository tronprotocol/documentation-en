# /wallet/getaccountnet

Query an account's bandwidth (Net) usage. **Deprecated** — prefer [`/wallet/getaccountresource`](getaccountresource.md).

- Source: `framework/src/main/java/org/tron/core/services/http/GetAccountNetServlet.java`
- Method: `GET` / `POST`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `address` | GET | string | Yes | Account address |
| `address` | POST | string | No | Account address; omitted uses the Protobuf empty address and returns `{}` |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccountnet \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```
## Response

Returns `api.AccountNetMessage` (`protocol/src/main/protos/api/api.proto`):

| Field | Type | Description |
|---|---|---|
| `freeNetUsed` | int64 | Free bandwidth used |
| `freeNetLimit` | int64 | The total free bandwidth allowance per account, set by a chain parameter that can be changed through governance proposals. Used free bandwidth gradually becomes available again over a 24-hour recovery window. |
| `NetUsed` | int64 | Staked bandwidth used |
| `NetLimit` | int64 | Staked bandwidth quota |
| `assetNetUsed` | map\<string,int64\> | Per-TRC-10 bandwidth used |
| `assetNetLimit` | map\<string,int64\> | Per-TRC-10 bandwidth quota |
| `TotalNetLimit` | int64 | Network-wide total bandwidth quota |
| `TotalNetWeight` | int64 | Network-wide total staked TRX for bandwidth |

Response example:

```json
{
  "freeNetUsed": 441,
  "freeNetLimit": 600,
  "assetNetUsed": [
    { "key": "1005416", "value": 0 }
  ],
  "assetNetLimit": [
    { "key": "1005416", "value": 10000 }
  ],
  "TotalNetLimit": 43200000000,
  "TotalNetWeight": 68305209098
}
```

Returns `{}` if `address` is missing or the account does not exist.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `address` is not valid base58check (`visible=true`) | GET: a 34-character value containing non-base58 characters → `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; an empty value, a length other than 34, an invalid address prefix, or a bad checksum makes `Util.getHexAddress` return an empty string, the lookup misses and `{}` is returned. POST (via `JsonFormat.merge`): illegal characters, invalid length, or a bad checksum → `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: invalid address for field: protocol.Account.address"}` |
| GET / POST | `address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
