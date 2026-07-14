# eth_getTransactionByHash

Query a transaction by txid.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTransactionByHash`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | 32-byte txid, hex-encoded |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionByHash","params":["0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"],"id":1}'
```

## Response

`TransactionResult` (see `TransactionResult.java`); returns `null` if not found.

| Field | Type | Description |
|---|---|---|
| `hash` | hex | txid |
| `nonce` | hex | Constant 8 bytes of zeros with `0x` prefix (Tron has no account nonce) |
| `blockHash` | hex | Block hash; returns `0x` when **not yet on-chain** or when the caller treats it as a pending transaction |
| `blockNumber` | hex | Same as above; `0x` when not yet on-chain |
| `transactionIndex` | hex | In-block transaction index; `0x` when not yet on-chain |
| `from` | hex | Sender address |
| `to` | hex \| null | Target address; `null` for contract creation |
| `gas` | hex | Actual energy used by the transaction (**not** `feeLimit`) |
| `gasPrice` | hex | Energy unit price at block time |
| `value` | hex | Transfer amount (sun; non-zero for TRX transfers; may be 0 for other contract types) |
| `input` | hex | Call data (selector + args for smart contract triggers; `0x` for other contract types) |
| `type` | hex | Constant `0x0` (legacy type) |
| `v` / `r` / `s` | hex | Signature components (first signature); all zeros if unsigned |

The example below is the real response captured from the Nile testnet curl above (a contract call type, the transaction is at index `0x0` of block `0x3fe1ca0`; cross-check at [Nile Tronscan](https://nile.tronscan.org/#/transaction/01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca)):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "hash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
    "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "blockNumber": "0x3fe1ca0",
    "transactionIndex": "0x0",
    "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
    "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
    "value": "0x0",
    "gas": "0xae29",
    "gasPrice": "0x64",
    "input": "0xa6bd98ac0000...0000",
    "type": "0x0",
    "nonce": "0x0000000000000000",
    "v": "0x1b",
    "r": "0x2154e8ef08f014063de8a88bafe748c8cbb48633c1657c083dca1a73439b289f",
    "s": "0x6aa796bfa58797da6354d35fb7334a8c145c48ae266e4a885f7ee44791b5a3c3"
  }
}
```

> The actual `input` is 580 bytes (contract selector `0xa6bd98ac` + arguments); only the head and tail are kept here for brevity. Other fields are the node's real return values.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` does not match `(0x)?[0-9a-fA-F]{64}` | `-32602` | `invalid hash value` |
