# getchainparameters

TRON API method that retrieves the current blockchain parameters and configuration settings. This method provides access to important network constants, fees, limits, and other configurable parameters that govern the TRON blockchain operation.

## HTTP Request

`GET /wallet/getchainparameters`

## Supported Paths

- `/wallet/getchainparameters`

## Parameters

This method does not require any parameters.

## Response

- chainParameter — array of blockchain parameters
  - key — parameter name
  - value — parameter value
- Common parameters include:
  - getMaintenanceTimeInterval — maintenance period interval
  - getAccountUpgradeCost — cost to upgrade account
  - getCreateAccountFee — fee for creating new accounts
  - getTransactionFee — base transaction fee
  - getAssetIssueFee — fee for issuing assets/tokens
  - getWitnessPayPerBlock — witness reward per block
  - getWitnessStandbyAllowance — standby witness allowance
  - getCreateNewAccountFeeInSystemContract — system contract account creation fee
  - getCreateNewAccountBandwidthRate — bandwidth rate for account creation
  - getAllowCreationOfContracts — whether contract creation is allowed
  - getRemoveThePowerOfTheGr — governance parameter
  - getEnergyFee — energy fee rate
  - getExchangeCreateFee — fee for creating exchanges
  - getMaxCpuTimeOfOneTx — maximum CPU time per transaction
  - getAllowUpdateAccountName — whether account name updates are allowed
  - getAllowSameTokenName — whether duplicate token names are allowed
  - getAllowDelegateResource — whether resource delegation is allowed
  - getTotalEnergyLimit — total energy limit for the network
  - getAllowTvmTransferTrc10 — whether TVM can transfer TRC10 tokens
  - getTotalEnergyCurrentLimit — current total energy limit
  - getAllowMultiSign — whether multi-signature is allowed
  - getAllowAdaptiveEnergy — whether adaptive energy is enabled
  - getUpdateAccountPermissionFee — fee for updating account permissions
  - getMultiSignFee — fee for multi-signature transactions

## Example

### Request

```shell
curl --request GET \
  --url https://api.shasta.trongrid.io/wallet/getchainparameters
```

### Response

```json
{
  "chainParameter": [
    {
      "key": "getMaintenanceTimeInterval",
      "value": 21600000
    },
    {
      "key": "getAccountUpgradeCost",
      "value": 9999000000
    },
    {
      "key": "getCreateAccountFee",
      "value": 100000
    },
    {
      "key": "getTransactionFee",
      "value": 10
    },
    {
      "key": "getAssetIssueFee",
      "value": 1024000000
    },
    {
      "key": "getWitnessPayPerBlock",
      "value": 16000000
    },
    {
      "key": "getWitnessStandbyAllowance",
      "value": 115200000000
    },
    {
      "key": "getCreateNewAccountFeeInSystemContract",
      "value": 1000000
    },
    {
      "key": "getCreateNewAccountBandwidthRate",
      "value": 1
    },
    {
      "key": "getAllowCreationOfContracts",
      "value": 1
    },
    {
      "key": "getRemoveThePowerOfTheGr",
      "value": 1
    },
    {
      "key": "getEnergyFee",
      "value": 140
    },
    {
      "key": "getExchangeCreateFee",
      "value": 1024000000
    },
    {
      "key": "getMaxCpuTimeOfOneTx",
      "value": 80
    },
    {
      "key": "getAllowUpdateAccountName",
      "value": 0
    },
    {
      "key": "getAllowSameTokenName",
      "value": 1
    },
    {
      "key": "getAllowDelegateResource",
      "value": 1
    },
    {
      "key": "getTotalEnergyLimit",
      "value": 90000000000
    },
    {
      "key": "getAllowTvmTransferTrc10",
      "value": 1
    },
    {
      "key": "getTotalEnergyCurrentLimit",
      "value": 90000000000
    },
    {
      "key": "getAllowMultiSign",
      "value": 1
    },
    {
      "key": "getAllowAdaptiveEnergy",
      "value": 1
    },
    {
      "key": "getUpdateAccountPermissionFee",
      "value": 100000000
    },
    {
      "key": "getMultiSignFee",
      "value": 1000000
    }
  ]
}
```

## Use Case

- Retrieving current network fees and limits for transaction planning.
- Checking governance parameters and network settings.
- Understanding network constraints for application development.
- Monitoring parameter changes and network upgrades.
