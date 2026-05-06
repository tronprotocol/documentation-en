# /wallet/getnowblock

Returns the current latest block.

- Source: `framework/src/main/java/org/tron/core/services/http/GetNowBlockServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getnowblock`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnowblock \
     --header 'accept: application/json'
```

## Response

Returns `protocol.Block` (`Tron.proto`):

| Field | Type | Description |
|---|---|---|
| `blockID` | string | Block hash (extra field added by HTTP output) |
| `block_header.raw_data.timestamp` | int64 | Block timestamp in milliseconds |
| `block_header.raw_data.txTrieRoot` | bytes | Transaction Merkle root |
| `block_header.raw_data.parentHash` | bytes | Parent block hash |
| `block_header.raw_data.number` | int64 | Block number |
| `block_header.raw_data.witness_address` | bytes | Producing witness address |
| `block_header.raw_data.version` | int32 | Block version |
| `block_header.witness_signature` | bytes | Witness signature |
| `transactions` | repeated Transaction | Transactions included in this block |

Response example (real Nile block, `transactions` body omitted):

```json
{
  "blockID": "0000000003fe266bf6b6d392f654dc2e5011601546ed04623d9fcc4e9d439a25",
  "block_header": {
    "raw_data": {
      "number": 66987627,
      "txTrieRoot": "f8156964cc3e5793a368f938a18ea45c02bd48fe3a412f7091ce8d9ef56df174",
      "witness_address": "41e7860196ad5b5718c1d6326babab039b70b8c1cd",
      "parentHash": "0000000003fe266a65d5194c947f6f7a059d4646c8e9a5293226bc7fdcfc775e",
      "version": 34,
      "timestamp": 1777445307000
    },
    "witness_signature": "55a29981b2ba121613788de5d1b6bd87579ef63479f4fbb7bc99b1c721769487023cb74ea3b604778ed448bf1c90db3db0fd8fedc85102cfda4231fd1c75d6e100"
  },
  "transactions": [ /* see /wallet/gettransactionbyid for a single-transaction example */ ]
}
```

Returns `{}` when no block is available.

### Error responses

| Trigger | Response |
|---|---|
| Internal node error (failed to read latest block or serialize) | `{"Error": "<exceptionClass> : <message>"}` |
