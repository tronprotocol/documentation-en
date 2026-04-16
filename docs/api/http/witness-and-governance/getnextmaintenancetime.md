# getnextmaintenancetime

TRON API method that retrieves the timestamp for the next scheduled maintenance window. Maintenance periods occur every 6 hours and are when witness elections, rewards distribution, and other network governance updates take effect.

## HTTP Request

`POST /wallet/getnextmaintenancetime`

## Supported Paths

- `/wallet/getnextmaintenancetime`

## Parameters

This method does not require any parameters.

## Response

- num — timestamp of the next maintenance window in milliseconds since Unix epoch

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getnextmaintenancetime \
  --header 'Content-Type: application/json' \
  --data '{}'
```

## Use Case

- Planning witness operations and vote changes before maintenance periods.
- Timing strategic voting decisions to take effect in the next election cycle.
- Building maintenance schedule tracking for automated systems.
- Coordinating network governance activities with maintenance windows.
- Calculating time remaining until witness election results are finalized.
