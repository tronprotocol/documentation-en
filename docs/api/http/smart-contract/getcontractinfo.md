# /wallet/getcontractinfo

Get the full runtime info for a contract (includes runtime code, state, and energy info).

- Source: `framework/src/main/java/org/tron/core/services/http/GetContractInfoServlet.java`
- Method: `GET` / `POST`
- Response: `protocol.SmartContractDataWrapper` (`smart_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Contract address |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getcontractinfo \
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
| `smart_contract` | SmartContract | Contract metadata (same as [`/wallet/getcontract`](getcontract.md)) |
| `runtimecode` | string(hex) | On-chain runtime bytecode (proto field name has no underscore) |
| `contract_state` | ContractState | Contract state: `energy_usage`, `energy_factor`, `update_cycle` |

Response example (Nile TetherToken):

```json
{
  "smart_contract": {
    "origin_address": "4165fa68800fff5a10346d1a3aa1fb2ce92f2e2971",
    "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
    "abi": { "entrys": [/* 46 entries */] },
    "bytecode": "60806040526000600260146101000a81548160ff021916908315150217905550...",
    "name": "TetherToken",
    "origin_energy_limit": 1000000000,
    "code_hash": "1c32379f645df32d2a8e45de37319983d01d47185588337985aeefb4672a91f2"
  },
  "runtimecode": "608060405234801561001057600080fd5b50d3801561001d57600080fd5b50d28...",
  "contract_state": {
    "energy_usage": 236150,
    "update_cycle": 256749
  }
}
```

> `contract_state.energy_factor` is omitted when 0 (proto default values are not serialized).

Returns `{}` if not found.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `value` is not valid base58check (`visible=true`) | If it contains non-base58 characters: `{"Error": "class java.lang.IllegalArgumentException : <details>"}`. If only the checksum is wrong, `Util.getHexAddress` silently returns an empty string → contract is not found and `{}` is returned. |
| `value` is not valid hex (`visible=false`) | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <details>"}` |
| Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
