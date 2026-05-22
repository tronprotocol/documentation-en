# web3_clientVersion

Returns the node client version string.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#web3ClientVersion`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None (`params: []`).

Example request:

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"web3_clientVersion","params":[],"id":1}'
```

## Response

Format `TRON/v<version>/<os.name>/Java<javaSpecVersion>`, built by concatenating `Version.getVersion()` + `System.getProperty("os.name")` + `System.getProperty("java.specification.version")`.

The example below is the real response captured from a Nile testnet call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "TRON/v4.8.1/Linux/Java1.8"
}
```

> The version changes with node upgrades; `os.name` / `java.specification.version` depend on the host environment.

### Error responses

No business errors.
