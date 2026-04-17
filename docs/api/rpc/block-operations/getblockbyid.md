# getBlockById

**Supported API**: `wallet`

TRON API method that retrieves a specific block from the TRON blockchain using its block ID (hash). This method allows you to fetch detailed information about a particular block, including its header, transactions, and metadata.

```protobuf
rpc GetBlockById (BytesMessage) returns (Block) {}
```
