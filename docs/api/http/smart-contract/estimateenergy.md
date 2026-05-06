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

When `vm.estimateEnergy=true` is not enabled, the call goes through the exception branch (see below); typically `result.code = OTHER_ERROR` and `result.message` contains `this node does not support estimate energy`.

### Error responses

This endpoint never writes `{"Error": ...}`. All exceptions are caught and written into `result.code` / `result.message`; the HTTP body is still an `EstimateEnergyMessage`:

| Trigger | `result.result` | `result.code` | `result.message` |
|---|---|---|---|
| Contract does not exist / validation failed (`ContractValidateException`) | false | `CONTRACT_VALIDATE_ERROR` | Original validator message |
| Node does not have `vm.estimateEnergy` enabled / EVM revert / other | false | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) |

On the exception path `energy_required` is not populated (value is 0).
