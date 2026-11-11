# GetNodeInfo

Return this node's status, version, CPU, memory, thread/JVM/OS information, latest block, and peer statistics.

- Service: `Wallet` only

```protobuf
rpc GetNodeInfo (EmptyMessage) returns (NodeInfo) {}
```

See the corresponding HTTP endpoint at [/wallet/getnodeinfo](../../http/node-and-tools/getnodeinfo.md).
