# getReward

TRON API method that retrieves witness rewards information for a specific account. This includes both unclaimed voting rewards and witness block production rewards.

## HTTP Request

`GET /wallet/getReward`

## Supported Paths

- `/wallet/getReward`
- `/walletsolidity/getReward`

## Parameters

- address — account address in hex format (21‑byte, starts with 41).

## Response

- reward — total amount of TRX rewards available for withdrawal (in sun units, where 1 TRX = 1,000,000 sun)

## Example

### Request

```shell
curl --request GET \
  --url https://api.shasta.trongrid.io/wallet/getReward
```

## Use Case

- Checking available voting rewards before claiming them.
- Monitoring reward accumulation from witness voting activities.
- Building reward tracking dashboards for voter accounts.
- Calculating potential returns from voting for specific witnesses.
- Automating reward claim notifications and processes.

## Curl Example

Shellcurl --request GET \
 --url 'https://api.shasta.trongrid.io/wallet/getReward?address=41b487cdb2d8dc7b2a8e5e7e7b4e3e8b8b8b8b8b' \
 --header 'accept: application/json'

rewards are returned in sun (1 TRX = 1,000,000 sun). If you have a base58 address, convert it to a 21‑byte hex address (leading 41…) before calling this endpoint. Claim rewards with wallet/withdrawbalance.Query ParametersaddressstringrequiredAccount address in hex format (21-byte, starts with 41)Response200 - application/jsonWitness rewards informationrewardnumberTotal reward amount in sun (1 TRX = 1,000,000 sun)Last modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/updateBrokerage | TRONwallet/withdrawbalance | TRON
