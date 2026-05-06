# /wallet/proposaldelete

Cancel a proposal you created (proposer only).

- Source: `framework/src/main/java/org/tron/core/services/http/ProposalDeleteServlet.java`
- Method: `POST`
- Contract: `protocol.ProposalDeleteContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Proposer address |
| `proposal_id` | int64 | Yes | Proposal ID |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/proposaldelete \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "proposal_id":   1
}
'
```

## Response

The validator checks that the caller is the proposer and that the proposal is not expired or canceled, so a real call must use a proposal from `/wallet/listproposals` whose `state=PENDING` and `proposer_address` equals `owner_address`. The example account is not the proposer of `proposal_id=1`; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : Proposal[1] is not proposed by 419c7c7049d26108be0dcb5f78479c6ff27ba101d1"}
```

When validation passes, returns an unsigned `protocol.Transaction`. Structure outline (`txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` semantics are the same as [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)):

```json
{
  "visible": false,
  "txID": "<computed from raw_data>",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "proposal_id":   1
          },
          "type_url": "type.googleapis.com/protocol.ProposalDeleteContract"
        },
        "type": "ProposalDeleteContract"
      }
    ],
    "ref_block_bytes": "<latest solidified block at construction time>",
    "ref_block_hash":  "<latest solidified block at construction time>",
    "expiration":      "<timestamp + 60_000>",
    "timestamp":       "<construction moment>"
  },
  "raw_data_hex": "<protobuf encoding of raw_data>"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| `proposal_id` > latest proposal number | `{"Error": "... : Proposal[<id>] not exists"}` |
| Proposal ID not in storage | `{"Error": "... : Proposal[<id>] not exists"}` |
| Caller is not the proposer | `{"Error": "... : Proposal[<id>] is not proposed by <address>"}` |
| Proposal expired | `{"Error": "... : Proposal[<id>] expired"}` |
| Proposal canceled | `{"Error": "... : Proposal[<id>] canceled"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
