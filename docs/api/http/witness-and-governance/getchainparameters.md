# /wallet/getchainparameters

Get the current values of all chain parameters.

- Source: `framework/src/main/java/org/tron/core/services/http/GetChainParametersServlet.java`
- Method: `GET` / `POST`
- Response: `protocol.ChainParameters`

## Request parameters

None (only `visible`).

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getchainparameters \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `chainParameter` | repeated {key, value} | List of chain-parameter key/value pairs |

The parameter `key` corresponds to the parameter index settable via proposals (e.g., `getMaintenanceTimeInterval`, `getEnergyFee`).

Response example (Nile, first 8 entries; full list has 75 entries):

```json
{
  "chainParameter": [
    { "key": "getMaintenanceTimeInterval",        "value": 1800000 },
    { "key": "getAccountUpgradeCost",             "value": 9999000000 },
    { "key": "getCreateAccountFee",               "value": 100000 },
    { "key": "getTransactionFee",                 "value": 1000 },
    { "key": "getAssetIssueFee",                  "value": 1024000000 },
    { "key": "getWitnessPayPerBlock",             "value": 8000000 },
    { "key": "getWitnessStandbyAllowance",        "value": 100000000 },
    { "key": "getCreateNewAccountFeeInSystemContract", "value": 1000000 }
    /* ... remaining parameters */
  ]
}
```

### Error responses

| Trigger | Response |
|---|---|
| Internal node error (failed to read DynamicProperties) | `{"Error": "<exceptionClass> : <message>"}` |
