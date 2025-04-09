# Decentralized Exchange(DEX)

TRON network supports decentralized exchange(DEX) using Bancor protocol. DEX is composed of many exchange pairs. You can find the api below in [HTTP API](../api/http.md).

## What is an Exchange Pair

The term of 'Exchange Pair' describes a trade between one token with another, like A/B, A/TRX.

## Exchange Pair Creation

Any account can create an exchange pair, it burns 1024 TRX.

Please refer to 'wallet/exchangecreate'.

## Exchange Pair Transaction

Any account can trade in the DEX. The trade follows Bancor protocol.

Please refer to 'wallet/exchangetransaction'.

## Exchange Pair Injection

The exchange pair creator can inject more tokens into the exchange pair. Injection can decrease the range of ratio fluctuation. If one token is injected, the other one will be injected automatically to keep the current ratio of the two tokens unchanged.

Please refer to 'wallet/exchangeinject'.

## Exchange Pair Withdrawal

The exchange pair creator can withdraw tokens from the exchange pair. Withdrawal can increase the range of ratio fluctuation. If one token is withdrawn, the other one will be withdrawn automatically to keep the current ratio of the two tokens unchanged.

Please refer to 'wallet/exchangewithdraw'.

## Query

### Transaction Query

`ListExchanges`: Query the list of all the exchange pairs.

`GetPaginatedExchangeList`: Query the list of all the exchange pairs by pagination.

`GetExchangeById`: Query an exchange pair by exchange pair id.

### Price Calculation

The token price is determined by the ratio of the balance of the two tokens.

### Calculate the Amount of Token You Can Get

`sellTokenQuant` is the amount of the `first_token` you want to sell.

`buyTokenQuant` is the amount of `second_token` you can get.

```java
supply = 1,000,000,000,000,000,000L

supplyQuant = -supply * (1.0 - Math.pow(1.0 + (double) sellTokenQuant/(firstTokenBalance + sellTokenQuant, 0.0005))

buyTokenQuant = (long)balance * (Math.pow(1.0 + (double) supplyQuant / supply, 2000.0) - 1.0)
```
