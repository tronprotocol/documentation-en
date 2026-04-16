# getnodeinfo

TRON API method that retrieves information about the current TRON node. This method provides details about the node’s version, configuration, network status, and operational parameters.

## HTTP Request

`GET /wallet/getnodeinfo`

## Supported Paths

- `/wallet/getnodeinfo`
- `/walletsolidity/getnodeinfo`

## Parameters

This method does not require any parameters.

## Response

- beginSyncNum — the block number from which synchronization started
- block — current block height information
- solidityBlock — current solidity block height information
- currentConnectCount — number of current peer connections
- activeConnectCount — number of active peer connections
- passiveConnectCount — number of passive peer connections
- totalFlow — total network traffic flow
- peerInfoList — list of connected peer information
- configNodeInfo — node configuration information
- machineInfo — machine and system information
- cheatWitnessInfoMap — information about witnesses flagged for cheating

## Example

### Request

```shell
curl --request GET \
  --url https://api.shasta.trongrid.io/wallet/getnodeinfo
```

### Response

```json
{
  "beginSyncNum": 123,
  "block": "<string>",
  "solidityBlock": "<string>",
  "currentConnectCount": 123,
  "activeConnectCount": 123,
  "passiveConnectCount": 123,
  "totalFlow": 123,
  "peerInfoList": [
    {
      "lastSyncBlock": "<string>",
      "remainNum": 123,
      "lastBlockUpdateTime": 123,
      "syncFlag": true,
      "headBlockTimeWeBothHave": 123,
      "needSyncFromPeer": true,
      "needSyncFromUs": true,
      "host": "<string>",
      "port": 123,
      "nodeId": "<string>"
    }
  ],
  "configNodeInfo": {
    "codeVersion": "<string>",
    "p2pVersion": "<string>",
    "listenPort": 123,
    "discoverEnable": true,
    "activeNodeSize": 123,
    "passiveNodeSize": 123,
    "sendNodeSize": 123,
    "maxConnectCount": 123,
    "sameIpMaxConnectCount": 123,
    "backupListenPort": 123,
    "backupMemberSize": 123,
    "backupPriority": 123,
    "dbVersion": 123,
    "minParticipationRate": 123,
    "supportConstant": true,
    "minTimeRatio": 123,
    "maxTimeRatio": 123,
    "allowCreationOfContracts": 123,
    "allowAdaptiveEnergy": 123
  },
  "machineInfo": {
    "threadCount": 123,
    "deadLockThreadCount": 123,
    "cpuCount": 123,
    "totalMemory": 123,
    "freeMemory": 123,
    "cpuRate": 123,
    "javaVersion": "<string>",
    "osName": "<string>",
    "jvmTotalMemory": 123,
    "jvmFreeMemory": 123,
    "processCpuRate": 123
  },
  "cheatWitnessInfoMap": {}
}
```

## Use Case

- Monitoring node health and synchronization status.
- Checking network connectivity and peer connections.
- Gathering node configuration and version information.
- Debugging network issues and performance monitoring.
