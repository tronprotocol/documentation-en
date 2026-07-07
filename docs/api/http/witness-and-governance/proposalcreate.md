# /wallet/proposalcreate

Create a chain-parameter proposal (SRs only).

- Source: `framework/src/main/java/org/tron/core/services/http/ProposalCreateServlet.java`
- Method: `POST`
- Contract: `protocol.ProposalCreateContract` (`proposal_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | SR address |
| `parameters` | array<{key, value}> | Yes | Proposal parameter entries; `key` is the parameter index, `value` is the target value |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Parameter indices are the keys returned by [`/wallet/getchainparameters`](getchainparameters.md).

> Note: the servlet uses `JsonFormat` to parse protobuf; `parameters` must be in array form `[{"key":N,"value":V}]`. With map form `{"<N>": V}` all keys are parsed as 0, triggering the range check on parameter 0.

Example (proposal that sets parameter 31 `getAllowMultiSign` to 1):

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/proposalcreate \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "parameters": [
    {"key": 31, "value": 1}
  ]
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, `raw_data_hex` vary with construction moment):

```json
{
  "visible": false,
  "txID": "d749a445802ea86230d52fb35645ab497612dec59794f815d1418c1b03b67d02",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "parameters": [
              { "key": 31, "value": 1 }
            ]
          },
          "type_url": "type.googleapis.com/protocol.ProposalCreateContract"
        },
        "type": "ProposalCreateContract"
      }
    ],
    "ref_block_bytes": "27e2",
    "ref_block_hash": "c4c88851291881b3",
    "expiration": 1777446546000,
    "timestamp": 1777446488573
  },
  "raw_data_hex": "0a0227e22208c4c88851291881b340d0d4c7c0dd335a58081012540a33747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e50726f706f73616c437265617465436f6e7472616374121d0a15419c7c7049d26108be0dcb5f78479c6ff27ba101d11204081f100170fd93c4c0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| owner is not an SR | `{"Error": "... : Witness[<address>] not exists"}` |
| `parameters` is empty | `{"Error": "... : This proposal has no parameter."}` |
| Invalid parameter key/value (index out of range, value out of bounds, prerequisites not met, etc.) | `{"Error": "... : <ProposalUtil validation message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
