# createAccount

**Supported API**: `wallet`

TRON API method that creates a new account on the TRON blockchain. This method generates an unsigned transaction to activate a new account address by sending it TRX for the first time.

```protobuf
rpc CreateAccount (AccountCreateContract) returns (Transaction) {}
```
