# eth_protocolVersion

Returns the protocol version from the latest block header.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getProtocolVersion`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_protocolVersion","params":[],"id":1}'
```

## Response

Hex-encoded `wallet.getNowBlock().getBlockHeader().getRawData().getVersion()`. This field is the Tron chain protocol version (`BlockHeader.raw_data.version`); it does not have the same meaning as Ethereum's network protocol version.

The example below is the real response captured from the Nile testnet curl above (`0x22` = 34, matching Nile's current protocol version):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x22"
}
```

### Error responses

None.
