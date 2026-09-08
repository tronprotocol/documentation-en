# Resources: bandwidth, energy & shares

TRON accounts obtain resources by freezing (staking) TRX. This page collects the mechanics that the operation pages refer to.

## Shares and bandwidth from freezing

After funds are frozen, the corresponding number of shares and bandwidth is obtained. Shares can be used for voting and bandwidth can be used for trading.

- **Share** — 1 unit of share can be obtained for every 1 TRX frozen. Shares are used for [voting](../commands/vote-reward.md#how-to-vote). After unfreezing, a previous vote will expire.
- **Bandwidth** — consumed by on-chain transactions (transfers, asset transfers, voting, freezing, etc.). Querying does not consume bandwidth.

## How to calculate bandwidth

A transaction consumes bandwidth equal to its **size in bytes** — a 200-byte transaction consumes 200 bandwidth. Every on-chain transaction consumes it (transfers, asset transfers, voting, freezing, etc.); querying does not.

Staking does not hand you a fixed quantity. Your allowance is a **share of a fixed network-wide pool**, proportional to what you have staked for bandwidth:

```text
allowance = (TRX you staked for bandwidth / total TRX staked for bandwidth network-wide) * total network bandwidth
```

Because both your stake and the network-wide total change over time, the allowance is **not a fixed value** and is recomputed rather than accumulated across freezes. In Stake 1.0 the freeze duration is a lock condition only; it does not enter this calculation. Full model: [resource model](../../../../mechanism-algorithm/resource.md).

Every activated account also gets a small free daily allowance, separate from the staked allowance — note that it cannot pay for account creation. When bandwidth runs short, the node burns TRX from the balance to cover the difference.

## Resource prices

Historical unit prices for bandwidth and energy, and the memo fee, are queryable — see [commands/resources](../commands/resources.md).

## See also

- [commands/stake-v2](../commands/stake-v2.md) — the current staking model
- [commands/stake-v1-legacy](../commands/stake-v1-legacy.md) — legacy freeze
- [concepts/staking-models](staking-models.md)
