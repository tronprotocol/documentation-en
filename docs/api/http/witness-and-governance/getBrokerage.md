# getBrokerage

TRON API method that returns a witness’s brokerage percentage (0–100). Witnesses set this rate to determine how much of their block rewards they keep before sharing the remainder with voters.

## HTTP Request

`GET /wallet/getBrokerage`

## Supported Paths

- `/wallet/getBrokerage`
- `/walletsolidity/getBrokerage`

## Parameters

- address — witness address in hex format (21‑byte, starts with 41).

## Response

- brokerage — percentage (0–100) kept by the witness.

## Example

### Request

```shell
curl --request GET \
  --url https://api.shasta.trongrid.io/wallet/getBrokerage
```

## Use Case

- Checking the current reward sharing rate of a witness before voting.
- Comparing brokerage rates between different witnesses to maximize voting rewards.
- Monitoring changes in witness brokerage policies over time.
- Building witness comparison tools and voting recommendation systems.

## Curl Example

Shellcurl --request GET \
 --url 'https://api.shasta.trongrid.io/wallet/getBrokerage?address=41928c9af0651632157ef27a2cf17ca72c575a4d21' \
 --header 'accept: application/json'

if you have a base58 witness address, convert it to a 21‑byte hex address (leading 41…) before calling this endpoint. You can obtain witness addresses via wallet/listwitnesses.Query ParametersaddressstringrequiredWitness address in hex format (21-byte, starts with 41)Response200 - application/jsonBrokerage percentage for witness rewardsbrokeragenumberBrokerage percentage (0-100)Last modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/votewitnessaccount | TRONwallet/updateBrokerage | TRON
