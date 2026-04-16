# clearContractABI

**Supported API**: `wallet`

TRON API method that clears (removes) the ABI (Application Binary Interface) information from a smart contract. This operation removes the contract’s ABI data from the blockchain, making the contract functions less discoverable but still executable if the function signatures are known.

```protobuf
rpc ClearContractABI (ClearABIContract) returns (TransactionExtention) {}
```
