# /wallet/votewitnessaccount

Vote for Super Representatives (SRs). Each call replaces all current votes from the account.

- Source: `framework/src/main/java/org/tron/core/services/http/VoteWitnessAccountServlet.java`
- Method: `POST`
- Contract: `protocol.VoteWitnessContract` (`witness_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Voter account address |
| `votes` | array<Vote> | Yes | Vote list |
| `votes[].vote_address` | string | Yes | SR candidate address |
| `votes[].vote_count` | int64 | Yes | Vote count (consumes TRON Power) |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/votewitnessaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "votes": [
    {
      "vote_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
      "vote_count": 100
    }
  ]
}
'
```

## Response

The validator checks that the account's current TRON Power covers the total votes; an account that has not staked TRX cannot vote. The example account has 0 TRON Power; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : The total number of votes[100000000] is greater than the tronPower[0]"}
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
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "votes": [
              {
                "vote_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
                "vote_count": 100
              }
            ]
          },
          "type_url": "type.googleapis.com/protocol.VoteWitnessContract"
        },
        "type": "VoteWitnessContract"
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
| `votes` list is empty | `{"Error": "... : VoteNumber must more than 0"}` |
| `votes` length exceeds `MAX_VOTE_NUMBER` | `{"Error": "... : VoteNumber more than maxVoteNumber <N>"}` |
| Invalid `votes[].vote_address` | `{"Error": "... : Invalid vote address!"}` |
| `votes[].vote_count <= 0` | `{"Error": "... : vote count must be greater than 0"}` |
| Candidate address has no corresponding account | `{"Error": "... : Account[<address>] not exists"}` |
| Candidate is not an SR | `{"Error": "... : Witness[<address>] not exists"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| Total votes exceeds account TRON Power | `{"Error": "... : The total number of votes[<n>] is greater than the tronPower[<m>]"}` |
| Vote count accumulation overflow | `{"Error": "... : <ArithmeticException message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
