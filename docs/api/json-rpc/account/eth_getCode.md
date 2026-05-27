# eth_getCode

Query a contract's runtime bytecode.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getABIOfSmartContract`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Contract address (20-byte hex or base58check) |
| `params[1]` | string | yes | Block tag, **only `latest` is supported** |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getCode","params":["0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825","latest"],"id":1}'
```

## Response

Hex-encoded `SmartContractDataWrapper.runtimecode` (with `0x` prefix). Returns `0x` if the address is not a contract or the contract does not exist.

The example below is the real response captured from the Nile testnet curl above (this address is an ERC-1167 minimal proxy clone with the implementation contract embedded mid-bytecode):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x363d3d373d3d3d363d73337d2c535241e1bc38e9c1fc2181843aef31dfaa5af43d82803e903d91602b57fd5bf30000000000000000000000003804c9c36c304d3d3d40bcc1a7c8d47591eda1b0"
}
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[1]` is `earliest` / `pending` / `finalized` | `-32602` | `TAG [earliest \| pending \| finalized] not supported` |
| `params[1]` is a valid hex number | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `params[1]` is neither a valid tag nor a valid hex | `-32602` | `invalid block number` |
| `params[0]` is not a valid address | `-32602` | passes through the message |
