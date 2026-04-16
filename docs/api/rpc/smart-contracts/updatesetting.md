# updateSetting

**Supported API**: `wallet`

TRON API method that updates the consume user resource percentage setting for a smart contract. This setting determines what percentage of the contract caller’s resources (bandwidth and energy) should be consumed when executing the contract.

```protobuf
rpc UpdateSetting (UpdateSettingContract) returns (TransactionExtention) {}
```
