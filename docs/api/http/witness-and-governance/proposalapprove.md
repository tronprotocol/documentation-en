# /wallet/proposalapprove

SR votes on a proposal (approve / withdraw approval).

- Source: `framework/src/main/java/org/tron/core/services/http/ProposalApproveServlet.java`
- Method: `POST`
- Contract: `protocol.ProposalApproveContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | SR address |
| `proposal_id` | int64 | Yes | Proposal ID |
| `is_add_approval` | bool | No | `true` = approve, `false` = withdraw approval; omitted defaults to `false` |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/proposalapprove \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":   "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "proposal_id":     1,
  "is_add_approval": true
}
'
```

## Response

The validator checks the proposal's current state before construction, so a real call must use a non-expired / non-canceled proposal ID (an entry with `state=PENDING` from `/wallet/listproposals`). The example's `proposal_id=1` has long since expired on Nile; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : Proposal[1] expired"}
```

When `is_add_approval` is omitted, the request follows the withdraw-approval branch. It succeeds only if the witness previously approved the proposal.

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
            "owner_address":   "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "proposal_id":     1,
            "is_add_approval": true
          },
          "type_url": "type.googleapis.com/protocol.ProposalApproveContract"
        },
        "type": "ProposalApproveContract"
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
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| owner is not an SR | `{"Error": "... : Witness[<address>] not exists"}` |
| `proposal_id` > latest proposal number | `{"Error": "... : Proposal[<id>] not exists"}` |
| Proposal ID not in storage | `{"Error": "... : Proposal[<id>] not exists"}` |
| Proposal expired | `{"Error": "... : Proposal[<id>] expired"}` |
| Proposal canceled | `{"Error": "... : Proposal[<id>] canceled"}` |
| `is_add_approval=false` but no prior approval | `{"Error": "... : Witness[<address>]has not approved proposal[<id>] before"}` |
| `is_add_approval=true` but already approved | `{"Error": "... : Witness[<address>]has approved proposal[<id>] before"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
