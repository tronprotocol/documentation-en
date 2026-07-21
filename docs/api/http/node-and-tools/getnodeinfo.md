# /wallet/getnodeinfo

Get the running status, version, memory, disk, latest block, and peer-statistics of this node.

- Source: `framework/src/main/java/org/tron/core/services/http/GetNodeInfoServlet.java`
- Method: `GET` / `POST`
- Alias path: `/monitor/getnodeinfo`
- Response handling: the servlet calls `JSON.toJSONString(NodeInfo)` to serialize the Java entity directly (`common/src/main/java/org/tron/common/entity/NodeInfo.java`) — it does **not** go through `JsonFormat`. Field names follow the Java POJO (and do not exactly match the `NodeInfo` proto in `Tron.proto`). `visible` has no effect.
- Solidity endpoint: `/walletsolidity/getnodeinfo`

## Request parameters

None.

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnodeinfo \
     --header 'accept: application/json'
```

## Response

Main fields:

| Field | Type | Description |
|---|---|---|
| `beginSyncNum` | int64 | Block height where syncing began |
| `block` | string | Current latest block (`"Num:height,ID:hash"`) |
| `solidityBlock` | string | Current solidified block |
| `currentConnectCount` | int32 | Current peer connections |
| `activeConnectCount` | int32 | Outbound (active) connections |
| `passiveConnectCount` | int32 | Inbound (passive) connections |
| `totalFlow` | int64 | Total traffic |
| `peerList` | repeated PeerInfo | Per-peer details |
| `configNodeInfo` | ConfigNodeInfo | Config (`codeVersion`, `versionNum`, `p2pVersion`, `listenPort`, etc.) |
| `machineInfo` | MachineInfo | Machine info (CPU, memory, disk) |
| `cheatWitnessInfoMap` | map<string,string> | SR cheating statistics (key is the witness hex address with `41` prefix) |

Response example (key fields only; `peerList`, full `memoryDescInfoList`, `cheatWitnessInfoMap`, etc. omitted):

```json
{
  "activeConnectCount": 3,
  "beginSyncNum": 66987546,
  "block": "Num:66987565,ID:0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
  "solidityBlock": "Num:66987547,ID:0000000003fe261b9e6e8091f5bd92dc67816890ec4739f6fe5109ad7779120c",
  "currentConnectCount": 60,
  "passiveConnectCount": 57,
  "totalFlow": 0,
  "configNodeInfo": {
    "codeVersion": "4.8.1",
    "versionNum": "18636",
    "p2pVersion": "201910292",
    "listenPort": 18888,
    "discoverEnable": true,
    "maxConnectCount": 60,
    "supportConstant": true,
    "dbVersion": 2
  },
  "machineInfo": {
    "cpuCount": 16,
    "cpuRate": 0.06666666666666667,
    "totalMemory": 32726257664,
    "freeMemory": 232448000,
    "jvmTotalMemory": 18683133952,
    "jvmFreeMemory": 7802853696,
    "javaVersion": "1.8.0_291",
    "osName": "Linux 3.10.0-1160.49.1.el7.x86_64",
    "threadCount": 361,
    "deadLockThreadCount": 0
  }
}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to collect node info or serialize) | `{"Error": "<exceptionClass> : <message>"}` |
