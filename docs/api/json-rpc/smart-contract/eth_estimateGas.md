# eth_estimateGas

Estimate a transaction's energy consumption (Tron's counterpart of Ethereum gas).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#estimateGas`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | object | yes | `CallArguments` (same as [`eth_call`](eth_call.md)); `from` / `to` / `value` / `data` / `input` are used to infer the contract type |

`CallArguments.getContractType` inference rules:

- `to` is empty and calldata is non-empty → `CreateSmartContract`
- `to` is a contract address → `TriggerSmartContract`
- `to` is a regular account and `value` is non-empty → `TransferContract` (returns `0x0` directly without entering EVM estimation)
- Otherwise → throws `-32600 invalid json request[: invalid value]`

```bash
# Example: estimate energy consumption of a TRX transfer on Nile testnet
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"eth_estimateGas",
    "params":[{
      "from":"0xdd791d6b49e190062d650e6a23c575510d35f2f9",
      "to":"0xb06b4139895c9f51c967c9f3d9089ca721e8e34c",
      "value":"0xf4240"
    }]
  }'
```

## Response

Hex-encoded energy usage:

- Plain TRX transfer (`TransferContract`) → `0x0`
- Contract call / deployment → depends on node config:
    - `node.supportEstimateEnergy = true` returns `EstimateEnergyMessage.energyRequired`
    - Default (false) → returns `TransactionExtention.energyUsed` (the actual usage of one constant-call)

The example below is the real response captured from the Nile testnet curl above (the TRX transfer takes the `TransferContract` path and returns `0x0` directly without entering the EVM):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x0" }
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `from` is not valid hex / wrong length | `-32602` | passes through `addressCompatibleToByteArray` message |
| `to` is not valid hex / wrong length | `-32602` | passes through `addressCompatibleToByteArray` message |
| `to` is empty and the resolved calldata is missing, `""`, or `"0x"` (`input` takes precedence over `data` when non-null) | `-32600` | `invalid json request` |
| `to` is not a contract and `value` is missing | `-32600` | `invalid json request: invalid value` |
| Contract validation fails (`ContractValidateException`) | `-32600` | passes through message (fallback `invalid contract`) |
| EVM execution `REVERT` | `-32000` | message + the parsed revert string; `error.data` carries the original revert hex |
| `input` is not strict hex | `-32602` | passes through `JsonRpcApiUtil.requireValidHex` validation message |
| `data` is not valid lenient hex | `-32602` | passes through `JsonRpcApiUtil.requireValidHex` validation message |
| `value` is not a valid non-negative hex long on the ordinary transfer path | `-32602` | `invalid param value: invalid hex number` or `invalid param value: negative` |
| `value` is not a valid non-negative hex long on the contract call or deployment path | `-32000` | passes through the parsing message |
| Other internal exceptions during contract call or deployment estimation | `-32000` | passes through message (double quotes are replaced with single quotes) |
