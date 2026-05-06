# GetNodeInfo

Return this node's status, version, memory, disk, latest block, peer statistics, and so on.

- Service: `Wallet` only

```protobuf
rpc GetNodeInfo (EmptyMessage) returns (NodeInfo) {}
```

See the corresponding HTTP endpoint at [/wallet/getnodeinfo](../../http/node-and-tools/getnodeinfo.md).
