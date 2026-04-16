# unDelegateResource

**Supported API**: `wallet`

TRON API method that revokes delegated bandwidth or energy resources from another address. This method allows you to reclaim resources that were previously delegated to another account using delegateresource, making those resources available to your own account again.

```protobuf
rpc UnDelegateResource (UnDelegateResourceContract) returns (TransactionExtention) {}
```
