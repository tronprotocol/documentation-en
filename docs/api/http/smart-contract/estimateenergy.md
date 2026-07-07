# /wallet/estimateenergy

Estimate the energy required for a contract call. Requires `vm.estimateEnergy=true` on the node.

- Source: `framework/src/main/java/org/tron/core/services/http/EstimateEnergyServlet.java`
- Method: `POST`
- Contract: `protocol.TriggerSmartContract`
- Response: `api.EstimateEnergyMessage`
- Solidity endpoint: `/walletsolidity/estimateenergy`

## Request parameters

Same as [`/wallet/triggerconstantcontract`](triggerconstantcontract.md).

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/estimateenergy \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "function_selector": "balanceOf(address)",
  "parameter":         "000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `result` | Return | Call status (success/error) |
| `energy_required` | int64 | Estimated energy required |

Response example:

```json
{
  "result": { "result": true },
  "energy_required": 1870
}
```

When `vm.estimateEnergy=true` is not enabled, the call goes through the `ContractValidateException` branch (see below): `result.code = CONTRACT_VALIDATE_ERROR` and `result.message` is `this node does not support estimate energy`.

### Error responses

This endpoint never writes `{"Error": ...}` after the request reaches the servlet. Servlet-handled exceptions are caught and written into `result.code` / `result.message`; the HTTP body is still an `EstimateEnergyMessage`.

If the request body is rejected earlier by the shared HTTP transport layer, for example because it exceeds `node.http.maxMessageSize`, the node usually returns HTTP 413 `Payload Too Large` from `SizeLimitHandler` instead of entering this servlet.

| Trigger | `result.result` | `result.code` | `result.message` |
|---|---|---|---|
| The node does not have `vm.estimateEnergy` enabled | false | `CONTRACT_VALIDATE_ERROR` | `this node does not support estimate energy` |
| The node has constant-call support disabled | false | `CONTRACT_VALIDATE_ERROR` | `this node does not support constant, so estimate energy cannot work` |
| `contract_address` is set but the contract does not exist | false | `CONTRACT_VALIDATE_ERROR` | `Smart contract is not exist.` |
| EVM exception / retry exhausted / other non-validation exception | false | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) |

On the exception path `energy_required` is not populated (value is 0).
