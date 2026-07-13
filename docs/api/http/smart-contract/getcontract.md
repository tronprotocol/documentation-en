# /wallet/getcontract

Get contract metadata by contract address. Returns the `SmartContract` itself (including the deploy-time `bytecode`), but **not the runtime code (`runtimecode`) or `contract_state`**. For runtime info, use [`/wallet/getcontractinfo`](getcontractinfo.md).

- Source: `framework/src/main/java/org/tron/core/services/http/GetContractServlet.java`
- Method: `GET` / `POST`
- Response: `protocol.SmartContract` (`smart_contract.proto`)

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `value` | GET / POST | string | Yes | Contract address |
| `visible` | GET / POST | bool | No | Address format (`name` is a proto `string` and is not affected by `visible`) |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
}
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `origin_address` | string | Deployer address |
| `contract_address` | string | Contract address |
| `abi` | ABI | Contract ABI |
| `bytecode` | string(hex) | Deployment bytecode (creation bytecode + constructor arguments concatenated, identical to what was passed at deploy time; not runtime code — see [`/wallet/getcontractinfo`](getcontractinfo.md)) |
| `call_value` | int64 | TRX sent with deployment |
| `consume_user_resource_percent` | int64 | Caller-paid energy percentage |
| `name` | string | Contract name |
| `origin_energy_limit` | int64 | Deployer's energy limit |
| `code_hash` | string(hex) | Bytecode hash |
| `trx_hash` | string(hex) | Deployment transaction hash |
| `version` | int32 | Version |

> Proto default values are not serialized: `call_value=0`, `consume_user_resource_percent=0`, `version=0`, and empty `trx_hash` are omitted from the response.

Response example (Nile TetherToken):

```json
{
  "origin_address": "4165fa68800fff5a10346d1a3aa1fb2ce92f2e2971",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "abi": {
    "entrys": [
      {
        "outputs": [{ "type": "string" }],
        "constant": true,
        "name": "name",
        "stateMutability": "View",
        "type": "Function"
      }
    ]
  },
  "bytecode": "60806040526000600260146101000a81548160ff02191690831515021790555060...",
  "name": "TetherToken",
  "origin_energy_limit": 1000000000,
  "code_hash": "1c32379f645df32d2a8e45de37319983d01d47185588337985aeefb4672a91f2"
}
```

Returns `{}` if not found.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `value` is not valid base58check (`visible=true`) | If it contains non-base58 characters: `{"Error": "class java.lang.IllegalArgumentException : <details>"}`. If only the checksum is wrong, `Util.getHexAddress` silently returns an empty string → contract is not found and `{}` is returned. |
| GET / POST | `value` is not valid hex (`visible=false`) | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <details>"}` |
| POST | Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
