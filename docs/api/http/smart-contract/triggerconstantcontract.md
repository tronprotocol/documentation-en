# /wallet/triggerconstantcontract

Read-only contract call (does not go on-chain). Used to read view/pure functions or simulate transactions.

- Source: `framework/src/main/java/org/tron/core/services/http/TriggerConstantContractServlet.java`
- Method: `POST`
- Contract: `protocol.TriggerSmartContract`
- Response: `api.TransactionExtention`
- Solidity endpoint: `/walletsolidity/triggerconstantcontract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Caller address (`msg.sender` in the contract) |
| `contract_address` | string | Conditional | Target contract address; `contract_address` or `data` must be provided |
| `function_selector` | string | No | Function signature |
| `parameter` | string | No | ABI-encoded parameters (hex) |
| `data` | string | No | Call data (hex); use either this or `function_selector` |
| `call_value` | int64 | No | TRX (sun) sent with the call |
| `token_id` | int64 | No | TRC-10 token id sent with the call |
| `call_token_value` | int64 | No | TRC-10 amount sent with the call |
| `extra_data` | string | No | Transaction memo (hex; UTF-8 text when `visible=true`) |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields (response includes `result.message`, which is affected by `visible`) |

The required-field constraint is `owner_address AND (contract_address OR data)`. Omitting `contract_address` is valid when `data` is supplied, for example when simulating contract deployment.

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/triggerconstantcontract \
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

`TransactionExtention`:

| Field | Type | Description |
|---|---|---|
| `transaction` | Transaction | Unsigned transaction (context only — should not be signed and broadcast) |
| `txid` | string(hex) | Transaction hash |
| `constant_result` | repeated bytes(hex) | ABI-encoded hex of the function return value; **on revert, this is the ABI-encoded revert reason** (the leading 4 bytes `08c379a0` are the `Error(string)` selector) |
| `result` | Return | Status; on revert / failed `require`, `result.result=false` and `result.message` contains `REVERT opcode executed` or `runtime error` |
| `energy_used` | int64 | Estimated energy consumed |
| `energy_penalty` | int64 | Energy penalty (if any) |
| `logs` | repeated TransactionLog | Event logs (if emitted) |
| `internal_transactions` | repeated InternalTransaction | Internal calls (if any) |

!!! note "Understanding simulation results"
    The execution context used for this simulation includes the state view available to the node when it processes the request and the TVM rules in effect at that time. Because the node continuously processes blocks and pending transactions and may run other constant calls concurrently, a transaction submitted later may execute on-chain in a different execution context, and its result may differ from the result of this simulation. This is an expected characteristic of point-in-time simulation.

    The execution context used for a simulation is primarily affected by the following:

    - **Processing blocks:** A node executes the transactions in a block sequentially, updating accounts, contract storage, resources, and chain parameters as it proceeds. A simulation initiated during this process uses the data visible to the node at that moment.
    - **Processing pending transactions:** `/wallet` provides a view of the latest state. While a node validates or replays pending transactions, this view may include local state updates and may continue to change as transactions are included in blocks or new blocks arrive.
    - **Other constant calls:** Calls made through `/wallet` and `/walletsolidity` may use different proposal activation states and TVM rules. When calls with different execution contexts run concurrently, in rare cases a simulation may reflect the proposal activation state and TVM rules being applied by the node at that moment.

    `constant_result`, `energy_used`, `logs`, and `internal_transactions` are produced by the current simulation. If the simulation reads different state or applies different TVM rules, the contract may follow a different execution path, and the values returned in these fields may also differ. The top-level `result` reports the status of the API request, while `transaction.ret[0].ret` reports the TVM execution result of the simulation.

    Choose the endpoint based on the state view you need: `/wallet` provides the latest state, whereas `/walletsolidity` provides a slightly older, solidified state. When preparing a transaction, treat the simulation results as a reference and leave an appropriate margin in `fee_limit` to account for changes in Energy consumption as state changes. After broadcasting the transaction, rely on the transaction receipt for the actual on-chain execution result.

Response example (real Nile capture):

```json
{
  "result": { "result": true },
  "energy_used": 935,
  "constant_result": ["0000000000000000000000000000000000000000000000000000000040cfcc00"],
  "transaction": {
    "ret": [{}],
    "visible": false,
    "txID": "cff6488e738ce77f7325572fe0aa2470f87dbf1c95eeeb2c25feec59d5afa35c",
    "raw_data": {
      "contract": [
        {
          "parameter": {
            "value": {
              "data":             "70a08231000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
            },
            "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
          },
          "type": "TriggerSmartContract"
        }
      ],
      "ref_block_bytes": "28c0",
      "ref_block_hash":  "9eabbe133123b34c",
      "expiration":      1777447218000,
      "timestamp":       1777447160779
    },
    "raw_data_hex": "0a0228c022089eabbe133123b34c40d0d6f0c0dd335a8e01081f1289010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412540a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541eca9bc828a3005b9a3b909f2cc5c2a54794de05f222470a08231000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f970cb97edc0dd33"
  }
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` and other ephemeral fields share semantics with [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md). Constant calls do not go on-chain; the `transaction` field is provided only as context.

> **Execution timeout:** This endpoint uses the node's constant-call execution
> deadline. `vm.constantCallTimeoutMs = 0` uses the network's
> `MAX_CPU_TIME_OF_ONE_TX` limit; a positive value sets a constant-call-only
> deadline in milliseconds. See
> [TVM and constant-call configuration](../../../using_javatron/configuration.md#tvm-and-constant-call-configuration).

### Error responses

This endpoint never writes `{"Error": ...}` after the request reaches the servlet. Servlet-handled exceptions are caught and written into `result.code` / `result.message`; the HTTP body is still a `TransactionExtention`. Note: **EVM revert / runtime errors do not go through `result.code`** — instead `result.result=true`, `message` carries the revert/runtime info, and the failure is marked at `transaction.ret[0].ret="FAILED"`.

Before the request reaches this servlet, shared layers can still return a different shape: `SizeLimitHandler` usually returns HTTP 413 `Payload Too Large` for an oversized body, and a non-blocking rate-limit rejection returns HTTP 200 with `{"Error":"class java.lang.IllegalAccessException : lack of computing resources"}`.

| Trigger | `result.result` | `result.code` | `result.message` | Other |
|---|---|---|---|---|
| `contract_address` is set but the contract does not exist | default (false) | `CONTRACT_VALIDATE_ERROR` | `Smart contract is not exist.` | — |
| The node has constant-call support disabled | default (false) | `CONTRACT_VALIDATE_ERROR` | `this node does not support constant` | — |
| EVM revert / failed `require` | true | default (`SUCCESS`, omitted) | `REVERT opcode executed` | `transaction.ret[0].ret="FAILED"`; `constant_result[0]` is the `Error(string)` ABI encoding (when the contract supplies a reason) |
| EVM runtime error (OOG, illegal opcode, etc., no `result.getException()`) | true | default (`SUCCESS`, omitted) | Raw `result.getRuntimeError()` string | Same as above |
| `result.getException() != null` (e.g. `OutOfTimeException`) | default (false) | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) | — |
| Other (hex parsing, missing parameters, proto merge, etc.) | default (false) | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) | — |

On revert, `result.message` does not carry the original reason string; you must decode it from `constant_result[0]`: skip the leading 4-byte `08c379a0` selector and ABI-decode the remaining bytes as `string`.
