# buildTransaction

Tron private extension. Constructs an **unsigned** Tron transaction; sign it and broadcast via HTTP [`/wallet/broadcasttransaction`](../../http/tx-build-and-broadcast/broadcasttransaction.md) or [`/wallet/broadcasthex`](../../http/tx-build-and-broadcast/broadcasthex.md) (JSON-RPC itself does not provide a broadcast endpoint).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#buildTransaction`
- Ports: **FullNode `8545` only** (the Solidity port throws `-32601`)

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | object | yes | `BuildArguments` (extends `CallArguments`; fields below) |

`BuildArguments` fields (`framework/src/main/java/org/tron/core/services/jsonrpc/types/BuildArguments.java`):

| Field | Default | Description |
|---|---|---|
| `from` | required | Sender address (hex or base58check) |
| `to` | depends | Target address; empty for contract deployment |
| `gas` | `0x0` | Maximum energy consumed by the transaction; ultimately `feeLimit = gas × eth_gasPrice` (sun) |
| `value` | null | TRX amount (sun, hex) |
| `data` | null | Contract bytecode (deployment) or calldata (trigger) |
| `tokenId` | `0` | TRC10 token id (used for `TransferAssetContract`) |
| `tokenValue` | `0` | TRC10 amount |
| `abi` | `""` | ABI JSON string for contract deployment (e.g. `[{...}]`) |
| `name` | `""` | Contract name when deploying |
| `consumeUserResourcePercent` | `0` | User-shared resource percentage (0–100) |
| `originEnergyLimit` | `0` | Deployer's max energy per call |
| `permissionId` | `0` | Multi-sig permission id |
| `extraData` | `""` | Memo data written into the transaction |
| `visible` | `false` | Whether output addresses / strings use base58 / UTF-8 |

Contract type inference (`BuildArguments.getContractType`):

| Condition | ContractType |
|---|---|
| `to` empty + `data` non-empty | `CreateSmartContract` |
| `to` is a contract address | `TriggerSmartContract` |
| `to` is a regular account + `tokenId>0` + `tokenValue>0` + `value` empty | `TransferAssetContract` |
| `to` is a regular account + `value` non-empty | `TransferContract` |
| Otherwise | throws `-32600 invalid json request` |

```bash
# Example: build a TRX transfer (1 TRX = 1e6 sun)
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"buildTransaction",
    "params":[{
      "from":"0x41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
      "to":"0x4112ab345eafdc9af9eaad7c97a2e9c3d4ddc0d7e1",
      "value":"0xf4240"
    }]
  }'
```

## Response

`{"transaction": {...}}` — directly maps to Tron `protocol.Transaction` (the hex field encoding matches the format returned by HTTP `/wallet/createtransaction`). The example below is the real response captured from the Nile testnet curl above:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "transaction": {
      "visible": false,
      "txID": "231371e531760758ea3a74dd4bce4934ad6d4cc71dfae1907f072c39de4c0c2f",
      "raw_data": {
        "contract": [
          {
            "parameter": {
              "value": {
                "amount": 1000000,
                "owner_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
                "to_address": "4112ab345eafdc9af9eaad7c97a2e9c3d4ddc0d7e1"
              },
              "type_url": "type.googleapis.com/protocol.TransferContract"
            },
            "type": "TransferContract"
          }
        ],
        "ref_block_bytes": "1d00",
        "ref_block_hash": "081a3fe1f1440f1d",
        "expiration": 1777438164000,
        "timestamp": 1777438106738
      },
      "raw_data_hex": "0a021d002208081a3fe1f1440f1d40a088c8bcdd335a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541a614f803b6fd780986a42c78ec9c7f77e6ded13c12154112ab345eafdc9af9eaad7c97a2e9c3d4ddc0d7e118c0843d70f2c8c4bcdd33"
    }
  }
}
```

> `ref_block_bytes` / `ref_block_hash` come from the latest block at construction time; `expiration` = `timestamp` + 60s; `txID` is the SHA256 hash of `raw_data`, so it changes whenever the above fields change — two calls of the same request will produce different `txID` values.
>
> `feeLimit` = `gas × wallet.getEnergyFee()`, automatically written to `raw_data.fee_limit` only for `CreateSmartContract` / `TriggerSmartContract`; `TransferContract` / `TransferAssetContract` don't need `feeLimit` (this is why the `raw_data` above has no `fee_limit` field).

### Error responses

| Trigger | Code | message |
|---|---|---|
| The current node is not a FullNode (Solidity) | `-32601` | `the method buildTransaction does not exist/is not available in SOLIDITY` |
| `from` missing / invalid | `-32600` | `invalid json request` |
| Contract type inference fails (e.g. `to` + `data` + `value` all empty) | `-32600` | `invalid json request` |
| `to` non-empty but invalid hex / wrong length | `-32602` | passes through `addressCompatibleToByteArray` message |
| `value` is not valid hex | `-32602` | `invalid param value: invalid hex number` |
| `gas` is not valid hex | `-32602` | `invalid param value: invalid hex number` |
| `tokenId` invalid after string conversion (TRC10 path only) | `-32602` | `invalid param value: invalid tokenId` |
| Contract validation fails (`ContractValidateException`) | `-32600` | passes through message |
| Internal exception | `-32000` | passes through message |
