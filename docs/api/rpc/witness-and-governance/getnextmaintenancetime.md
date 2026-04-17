# getNextMaintenanceTime

**Supported API**: `wallet`

TRON API method that retrieves the timestamp for the next scheduled maintenance window. Maintenance periods occur every 6 hours and are when witness elections, rewards distribution, and other network governance updates take effect.

```protobuf
rpc GetNextMaintenanceTime (EmptyMessage) returns (NumberMessage) {}
```
