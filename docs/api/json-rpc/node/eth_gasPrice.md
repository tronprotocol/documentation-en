# eth_gasPrice

Current energy unit price (Tron's counterpart of Ethereum gas price).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#gasPrice`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":1}'
```

## Response

Hex-encoded `wallet.getEnergyFee()`, in sun (1 TRX = 1e6 sun). The value comes from the chain parameter `getEnergyFee` and can be modified by an on-chain proposal.

The example below is the real response captured from the Nile testnet curl above (Nile's current energy price = 100 sun/energy):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x64"
}
```

> Mainnet and testnets may have different energy prices, which can change via proposals. The `gas` parameter passed to `buildTransaction` multiplied by this value gives `feeLimit`.

### Error responses

None.
