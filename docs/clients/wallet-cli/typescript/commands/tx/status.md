# wallet-cli tx status

Show confirmation status of a transaction.

## Synopsis

```
wallet-cli tx status --txid <id> [options]
```

## Description

Reports which step a transaction is at, using **four states**. After sending, scripts and agents poll it to learn whether the tx made it on-chain and succeeded. These four state values are **stable — they won't be renamed or dropped across versions** — so you can program against them (see the `wallet-cli.result.v1` output contract in [machine-interface](../../machine-interface.md)).

| `data.state` | Meaning | Terminal? |
|---|---|---|
| `confirmed` | Mined with an execution receipt; `blockNumber` present | yes — treat as success |
| `failed` | Included and reverted / rejected | yes |
| `pending` | Seen by the node, not yet mined | no — keep polling |
| `not_found` | Unknown to the queried node (wrong network? not propagated yet?) | no — past your deadline this is **unknown**, not failed |

!!! warning "`confirmed` means mined, not irreversible"

    This command and `--wait` both read the FullNode's *unconfirmed* view. `confirmed` says the
    transaction is in a block and its receipt is settled — it does **not** say the block is
    solidified and can no longer be reverted. When you need finality, query a SolidityNode.

!!! warning "A `not_found` timeout is not a failure"

    It says only that *the node you asked* does not know the transaction; it may still be in
    another node's mempool. Never resend on that basis — that is how double payments happen. Past
    your deadline, treat it as **unknown state** and reconcile via a SolidityNode or a block
    explorer before deciding.

## Options

| Option | Description |
|---|---|
| `--txid <string>` | **Required.** TRON transaction id/hash |

Plus the [global options](../index.md#global-options-every-command).

## Examples

```bash
wallet-cli tx status --txid 7d9b6a08505537f7fd51ed4fb4223ce89098403d26e8d3fe07bdb3d625a46364 --network tron:nile
```

```console
TxID    7d9b6a08505537f7fd51ed4fb4223ce89098403d26e8d3fe07bdb3d625a46364
Status  confirmed ✅
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"7d9b6a08505537f7fd51ed4fb4223ce89098403d26e8d3fe07bdb3d625a46364","state":"confirmed","confirmed":true,"failed":false,"blockNumber":68822193},"meta":{"durationMs":1006,"warnings":[]},"chain":{"family":"tron","network":"tron:nile","chainId":"nile"}}
```

An unknown txid is a **success** with `state: "not_found"` (exit 0) — the query worked; the answer is "not there":

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"tx.status","data":{"txid":"0000…0000","state":"not_found","confirmed":false,"failed":false},"meta":{"durationMs":1022,"warnings":[]},"chain":{"family":"tron","network":"tron:nile","chainId":"nile"}}
```

## Output

| Field | Type | Meaning |
|---|---|---|
| `txid` | string | Echo of the queried id |
| `state` | string | `confirmed` / `failed` / `pending` / `not_found` |
| `confirmed` / `failed` | boolean | Direct-branch conveniences mirroring `state` |
| `blockNumber` | number | Present when confirmed |

## Exit status

`0` query answered (including `not_found`) · `1` execution failure (node unreachable, timeout) · `2` usage error.

## See also

[`tx info`](info.md) — full detail + receipt · [`tx send`](send.md) · [Script safety](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
