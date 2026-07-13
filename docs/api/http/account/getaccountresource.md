# /wallet/getaccountresource

Query an account's bandwidth (Net) + energy + TronPower usage.

- Source: `framework/src/main/java/org/tron/core/services/http/GetAccountResourceServlet.java`
- Method: `GET` / `POST`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `address` | GET / POST | string | Yes | Account address |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccountresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```
## Response

Returns `api.AccountResourceMessage` (`api.proto`):

| Field | Type | Description |
|---|---|---|
| `freeNetUsed` / `freeNetLimit` | int64 | Free bandwidth (resets every 24h) |
| `NetUsed` / `NetLimit` | int64 | Staked bandwidth |
| `assetNetUsed` / `assetNetLimit` | map | Per-TRC-10 bandwidth |
| `TotalNetLimit` / `TotalNetWeight` | int64 | Network-wide bandwidth quota / total staked TRX |
| `EnergyUsed` / `EnergyLimit` | int64 | Energy |
| `TotalEnergyLimit` / `TotalEnergyWeight` | int64 | Network-wide energy quota / total staked TRX |
| `tronPowerUsed` / `tronPowerLimit` | int64 | Voting power |
| `TotalTronPowerWeight` | int64 | Network-wide total voting power |
| `storageUsed` / `storageLimit` | int64 | Storage (no longer used) |

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
  "TotalNetWeight": 68305209098,
  "TotalEnergyLimit": 180000000000,
  "TotalEnergyWeight": 2411528185
}
```

Returns `{}` if `address` is missing or the account does not exist.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : exception decoding Hex string: <details>"}` |
| GET / POST | `address` is not valid base58check (`visible=true`) | `{"Error": "class java.lang.IllegalArgumentException : <details>"}` |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
