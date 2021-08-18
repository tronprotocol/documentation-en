# TRC-10

TRON network supports two types of tokens, one is TRC-20 token issued by smart contract, the other one is TRC-10 token issued by system contract.

## How to Issue a TRC-10 Token

HTTP API:

```text
wallet/createassetissue
Description: Issue a token
demo: curl -X POST http://127.0.0.1:8090/wallet/createassetissue -d '{
  "owner_address":"41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
  "name":"0x6173736574497373756531353330383934333132313538",
  "abbr": "0x6162627231353330383934333132313538",
  "total_supply" :4321,
  "trx_num":1,
  "num":1,
  "start_time" : 1530894315158,
  "end_time":1533894312158,
  "description":"007570646174654e616d6531353330363038383733343633",
  "url":"007570646174654e616d6531353330363038383733343633",
  "free_asset_net_limit":10000,
  "public_free_asset_net_limit":10000,
  "frozen_supply":{"frozen_amount":1, "frozen_days":2}
}'

Parameter owner_address: Owner address, default hexString
Parameter name: Token name, default hexString
Parameter abbr: Token name abbreviation, default hexString
Parameter total_supply: Token total supply
Parameter trx_num: Define the price by the ratio of trx_num/num,
Parameter num: Define the price by the ratio of trx_num/num
Parameter start_time: ICO start time
Parameter end_time: ICO end time
Parameter description: Token description, default hexString
Parameter url: Token official website url, default hexString
Parameter free_asset_net_limit: The free bandwidth limit of each token holder 
Parameter public_free_asset_net_limit: The total free bandwidth limit of the Token
Parameter frozen_supply: Token staked supply
Parameter permission_id: Optional, for multi-signature use
Return: Transaction object
Note: The unit of 'trx_num' is SUN
```

## Participate TRC-10 Token Issuing

HTTP API:

```text
wallet/participateassetissue
Description: Participate a token issuing
demo: curl -X POST http://127.0.0.1:8090/wallet/participateassetissue -d '{
  "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
  "owner_address":"41e472f387585c2b58bc2c9bb4492bc1f17342cd1",
  "amount":100,
  "asset_name":"3230313271756265696a696e67"
}'

Parameter to_address: The issuer address of the token, default hexString
Parameter owner_address: The participant address, default hexString
Parameter amount: Participate token amount
Parameter asset_name: Token id, default hexString
Parameter permission_id: Optional, for multi-signature use
Return: Transaction object
Note: The unit of 'amount' is the smallest unit of the token
```

## TRC-10 Token Transfer

HTTP API:

```text
wallet/transferasset
Description: Transfer token
demo: curl -X POST http://127.0.0.1:8090/wallet/transferasset -d '{
  "owner_address":"41d1e7a6bc354106cb410e65ff8b181c600ff14292",
  "to_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
  "asset_name": "31303030303031",
  "amount": 100
}'

Parameter owner_address: Owner address, default hexString
Parameter to_address: To address, default hexString
Parameter asset_name: Token id number encoded as hexString
Parameter amount: Token transfer amount
Parameter permission_id: Optional, for multi-signature use
Return: Transaction object
Note: The unit of 'amount' is the smallest unit of the token
```
