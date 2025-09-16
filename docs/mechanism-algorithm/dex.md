# Decentralized Exchange (DEX)

The TRON network natively supports **Decentralized Exchanges (DEX)**, with its core consisting of multiple trading pairs. This article introduces the basic concepts of trading pairs, creation methods, trading processes, funding and withdrawal mechanisms, and includes common query methods and price calculation methods.

## What is a Trading Pair

A trading pair (`Exchange`) represents a trading market between any two TRC-10 tokens, which can be:

- Between any two TRC-10 tokens;
- Between a TRC-10 token and TRX.

Any account can create any combination of trading pairs, even if the same combination already exists on the network. All trading pairs on the TRON network follow the **Bancor protocol** for asset exchange, with the default weight of the two tokens being equal. Therefore, the balance ratio of the two tokens in the trading pair represents the current price.

**Example:**  
Suppose a trading pair contains two tokens, ABC and DEF:

- ABC balance is `10,000,000`;
- DEF balance is `1,000,000`;

Then the current exchange rate is: 10 ABC = 1 DEF

## Creating a Trading Pair

Any account can initiate the creation of a trading pair. **The fee for creating a trading pair is 1024 TRX, which will be burned.**  

When creating a trading pair, the initial balances of the two tokens must be provided, and upon successful creation, the system will automatically deduct the corresponding tokens from the initiator’s account.

### Contract: `ExchangeCreateContract`

Parameters are as follows:

- `first_token_id`: The ID of the first token;
- `first_token_balance`: The initial balance of the first token;
- `second_token_id`: The ID of the second token;
- `second_token_balance`: The initial balance of the second token.

> **Note:** If TRX is included, use `_` to represent it; the unit for TRX is `sun` (1 TRX = 1,000,000 sun).

### Example:

```
ExchangeCreate abc 10000000 _ 1000000000000
```
The above command creates a trading pair between `abc` and `TRX`, with an initial injection of 10,000,000 abc tokens (token precision 0-6) and 1,000,000,000,000 sun (i.e., 1,000,000 TRX). If the account balance is insufficient, the creation transaction will fail.

## Trading
All accounts can perform instant trades in any trading pair. Trading does not require order placement, and the price and quantity are calculated entirely based on the Bancor protocol.

### Contract: `ExchangeTransactionContract`
Parameters are as follows:

- `exchange_id`: The ID of the trading pair (the system assigns a unique ID based on creation time);
- `token_id`: The ID of the token to be sold;
- `quant`: The quantity to be sold;
- `expected`: The minimum quantity of the other token expected to be received (if the actual amount received is less than this value, the transaction fails).

#### Example:
Suppose the trading pair ID for `abc` and `TRX` is 1, with the current state:

- abc balance is 10,000,000;
- TRX balance is 1,000,000;

If a user wishes to spend 100 TRX (100,000,000 sun) to buy at least 990 abc, they execute:
```
ExchangeTransaction 1 _ 100000000 990
```
Upon a successful transaction, the user's TRX balance will **decrease** and their abc balance will **increase**; the trading pair's TRX balance will **increase** and their abc balance will **decrease**.
The actual amount of `abc` received by the user can be queried using the `gettransactioninfobyid` interface, checking the `exchange_received_amount` field.

## Adding Liquidity (Funding)
When the balance of one token in a trading pair is low, transactions may cause significant price fluctuations. At this point, **the creator of the trading pair can choose to inject more assets** to improve stability.

>**Funding Guidelines:**
>
>- Only the trading pair creator can perform this action;
>- No fees are required;
>- The system calculates the required amount of the other token based on the current price ratio to maintain the price.

### Contract: `ExchangeInjectContract`
Parameters are as follows:

- `exchange_id`: The ID of the trading pair;
- `token_id`: The ID of the token to be injected;
- `quant`: The quantity of the token to be injected.

### Example:
Suppose the trading pair ID for `abc` and `TRX` is 1, with the current state:
- `abc` balance is 10,000,000,
- `TRX` balance is 1,000,000,

If the creator wishes to increase `abc` by 10% (i.e., add 1,000,000 abc), they execute:

```
ExchangeInject 1 abc 1000000
```
If successful, the trading pair will gain 1,000,000 abc and the corresponding proportion amount of 100,000 TRX, which will be deducted from the creator’s account.

## Withdrawing Liquidity (Withdraw)
The assets in a trading pair belong entirely to the creator. The creator can withdraw a portion of the assets from the trading pair at any time.

>**Withdrawal Rules:**
>- Only the trading pair creator can perform this action;
>- No fees are required;
>- The system withdraws the other token in proportion to the current token ratio, ensuring the price remains unchanged but increasing price volatility.

### Contract: `ExchangeWithdrawContract`
Parameters are as follows:

- `exchange_id`: The ID of the trading pair;
- `token_id`: The ID of the token to be withdrawn;
- `quant`: The quantity of the token to be withdrawn.

### Example:
Suppose the trading pair ID for `abc` and `TRX` is 1, with the current state:
- `abc` balance is 10,000,000,
- `TRX` balance is 1,000,000,

If the creator wishes to withdraw 10% of abc (i.e., reduce 1,000,000 abc), they execute:

```
ExchangeWithdraw 1 abc 1000000
```
Upon successful transaction, the trading pair will lose 1,000,000 abc and the corresponding proportion of 100,000 TRX, which will be added to the creator’s account.

## Queries and Calculations
### Querying Trading Pair Information
TRON provides multiple interfaces for querying trading pairs:

**1. Query all trading pair information:** `ListExchanges`
**2. Paginated query of trading pair list:** `GetPaginatedExchangeList`
**3. Query details of a specific trading pair:** `GetExchangeById`

For detailed API documentation, refer to [RPC-API ](https://tronprotocol.github.io/documentation-en/api/rpc/).

### Price Calculation
Suppose in a trading pair:

- `first_token_price = 100 sun`;
- `first_token_balance = 1,000,000`;
- `second_token_balance = 2,000,000`;

Then the `second_token_price` is:

```
second_token_price = first_token_price * (first_token_balance / second_token_balance)
                   = 100 * (1,000,000 / 2,000,000)
                   = 50 sun
```

### Exchange Quantity Calculation
Suppose `first_token` is used to exchange for `second_token`:

- `sellTokenQuant`: The quantity of `first_token` to be sold;
- `buyTokenQuant`: The quantity of `second_token` obtained through exchange;
- `balance`: The current balance of `second_token` in the trading pair;
- `supply`: A fixed constant of `10^18` used in the Bancor protocol formula.

The calculation process is as follows:

```
supplyQuant = -supply * (1.0 - Math.pow(1.0 + (double) sellTokenQuant / (firstTokenBalance + sellTokenQuant), 0.0005));
buyTokenQuant = (long)(balance * (Math.pow(1.0 + (double) supplyQuant / supply, 2000.0) - 1.0));
```

>**Note**: Market prices may fluctuate in real-time due to other trading activities on the network.

For more interface details, refer to: [HTTP API Documentation](https://tronprotocol.github.io/documentation-en/api/http/).

