# /wallet/deploycontract

Deploy a smart contract. Returns the unsigned deployment transaction.

- Source: `framework/src/main/java/org/tron/core/services/http/DeployContractServlet.java`
- Method: `POST`
- Contract: `protocol.CreateSmartContract` (`smart_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Deployer address |
| `name` | string | No | Contract name |
| `abi` | json string | No | Contract ABI (JSON-array string) |
| `bytecode` | string | Yes | Contract bytecode (hex) |
| `parameter` | string | No | Constructor parameters (hex, appended to bytecode) |
| `fee_limit` | int64 | Yes | Transaction fee limit (sun) |
| `call_value` | int64 | No | TRX (sun) sent with the deployment |
| `consume_user_resource_percent` | int64 | Yes | Caller-paid energy percentage 0–100 |
| `origin_energy_limit` | int64 | Yes | Deployer's energy limit |
| `token_id` | int64 | No | TRC10 token id sent with the deployment |
| `call_token_value` | int64 | No | TRC10 amount sent with the deployment |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/deploycontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "name": "MyContract",
  "abi":  "[]",
  "bytecode": "608060405234801561001057600080fd5b5060f78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80636d4ce63c14602d575b600080fd5b60336047565b604051603e9190606b565b60405180910390f35b6000600190565b6000819050919050565b6065816052565b82525050565b6000602082019050607e6000830184605c565b9291505056fea264697066735822122000000000000000000000000000000000000000000000000000000000000000006c6578706572696d656e74616cf564736f6c63430008100033",
  "fee_limit": 1000000000,
  "consume_user_resource_percent": 100,
  "origin_energy_limit": 10000000
}
'
```

## Response

Returns an unsigned `protocol.Transaction` (contract type `CreateSmartContract`).

Special: when `Util.printTransactionToJSON` detects a `CreateSmartContract`, it injects an extra top-level `contract_address` (hex; derived from `owner_address` + nonce, **not affected by `visible`**) into the transaction. After signing and broadcasting, that address takes effect.

Response example (real Nile capture):

```json
{
  "visible": false,
  "txID": "7fe721c3f85b6c1c9491df43778c98903b565bc4210592f449f41342041729b3",
  "contract_address": "41584587b353166787b37d1b05a4a91e59c5370bcf",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "new_contract": {
              "origin_address":                "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "consume_user_resource_percent": 100,
              "name":                          "MyContract",
              "bytecode":                      "608060405234801561001057600080fd5b5060f78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80636d4ce63c14602d575b600080fd5b60336047565b604051603e9190606b565b60405180910390f35b6000600190565b6000819050919050565b6065816052565b82525050565b6000602082019050607e6000830184605c565b9291505056fea264697066735822122000000000000000000000000000000000000000000000000000000000000000006c6578706572696d656e74616cf564736f6c63430008100033",
              "abi":                           {},
              "origin_energy_limit":           10000000
            }
          },
          "type_url": "type.googleapis.com/protocol.CreateSmartContract"
        },
        "type": "CreateSmartContract"
      }
    ],
    "ref_block_bytes": "28c7",
    "ref_block_hash":  "b89ca57e9cbb96dd",
    "fee_limit":       1000000000,
    "expiration":      1777447239000,
    "timestamp":       1777447181980
  },
  "raw_data_hex": "0a0228c72208b89ca57e9cbb96dd40d8faf1c0dd335ae402081e12df020a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e437265617465536d617274436f6e747261637412aa020a1541dd791d6b49e190062d650e6a23c575510d35f2f91290020a1541dd791d6b49e190062d650e6a23c575510d35f2f91a0022e101608060405234801561001057600080fd5b5060f78061001f6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c80636d4ce63c14602d575b600080fd5b60336047565b604051603e9190606b565b60405180910390f35b6000600190565b6000819050919050565b6065816052565b82525050565b6000602082019050607e6000830184605c565b9291505056fea264697066735822122000000000000000000000000000000000000000000000000000000000000000006c6578706572696d656e74616cf564736f6c6343000810003330643a0a4d79436f6e74726163744080ade204709cbdeec0dd3390018094ebdc03"
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` / `contract_address` vary by construction time; the other ephemeral-field semantics are the same as [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md). `contract_address` is derived locally on the server side from `owner_address + nonce` — **it is not an on-chain result**: the address only takes effect after broadcasting.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `owner_address` is not valid base58check (`visible=true`) | If it contains non-base58 characters: `{"Error": "class java.lang.IllegalArgumentException : <details>"}`. If only the checksum is wrong, `Util.getHexAddress` silently returns an empty string; `CreateSmartContract` construction does not validate non-empty owner, and returns a valid transaction with the `owner_address` field missing (signing/broadcasting will fail later). |
| `owner_address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (direct call to `ByteArray.fromHexString`) |
| `bytecode` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (direct call to `ByteArray.fromHexString`) |
| `abi` is not valid JSON | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `consume_user_resource_percent` not in [0, 100] | `{"Error": "class org.tron.core.exception.ContractValidateException : percent must be >= 0 and <= 100"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |

> Deployment-side errors (e.g. insufficient origin energy, oversized contract code, constructor revert) are only triggered during broadcast or block packing, not by this endpoint.
