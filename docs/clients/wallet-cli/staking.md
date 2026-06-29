# Staking & Resources

TRON accounts stake (freeze) TRX to obtain **bandwidth** and **energy**, and to gain voting power.
There are two staking mechanisms:

- **Stake 1.0** — `freeze-balance` / `unfreeze-balance`. Staked TRX is locked for a fixed duration.
- **Stake 2.0** — `freeze-balance-v2` / `unfreeze-balance-v2` and resource **delegation**. This is
  the current mechanism; unstaking goes through a withdrawable waiting period.

Resource codes used throughout:

| Code | Resource |
|------|----------|
| `0` | BANDWIDTH |
| `1` | ENERGY |
| `2` | TRON_POWER (voting power; REPL freeze/unfreeze only, network-gated) |

Code `2` (TRON_POWER) is accepted only by the **REPL** freeze/unfreeze commands —
`FreezeBalance`/`UnfreezeBalance` (Stake 1.0) and `FreezeBalanceV2`/`UnfreezeBalanceV2` (Stake 2.0).
Even there it is network-gated: the node only allows a code-`2` freeze when the chain parameter
`getAllowNewResourceModel` is enabled, which is **not** the case on mainnet — so in practice only
`0`/`1` are usable. Every Standard CLI command that takes a `--resource` rejects anything other than
`0` (BANDWIDTH) or `1` (ENERGY) up front with a usage error. Delegation commands (both modes)
likewise accept only `0` or `1`.

Amounts are in **SUN** (1 TRX = 1,000,000 SUN).

As elsewhere, the REPL uses an optional leading `[OwnerAddress]` for multi-sig; the Standard CLI uses
`--owner` + `--multi`. All state-changing staking/delegation commands on this page require auth; the
resource queries at the end of the page do not.

## Stake 1.0

### Freeze balance — `freeze-balance` / `FreezeBalance`

!!! warning "Deprecated"
    `freeze-balance` is **deprecated** — use `freeze-balance-v2` (Stake 2.0) for new stakes. It is
    kept only for compatibility. (`unfreeze-balance` remains available to release existing Stake 1.0
    positions.)

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile freeze-balance \
      --amount 1000000 --duration 3 --resource 1
    ```

    - `--amount` (required, SUN), `--duration` (required, days).
    - `--resource` (optional, `0`/`1`, default `0`). Standard CLI accepts only `0`/`1`; to freeze
      for TRON_POWER (voting power, code `2`) use the REPL `FreezeBalance`.
    - `--receiver` (optional) — delegate the obtained resource to another address.
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    FreezeBalance [OwnerAddress] frozen_balance frozen_duration [ResourceCode] [receiverAddress]
    ```

    `ResourceCode`: `0` BANDWIDTH, `1` ENERGY, `2` TRON_POWER.

### Unfreeze balance — `unfreeze-balance` / `UnfreezeBalance`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile unfreeze-balance --resource 1
    ```

    - `--resource` (optional, default `0`).
    - `--receiver` (optional) — required if the resource was delegated.
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UnfreezeBalance [OwnerAddress] ResourceCode [receiverAddress]
    ```

## Stake 2.0

### Freeze balance v2 — `freeze-balance-v2` / `FreezeBalanceV2`

No duration: staked TRX stays staked until you explicitly unstake it.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile freeze-balance-v2 \
      --amount 1000000 --resource 1
    ```

    - `--amount` (required, SUN), `--resource` (optional, default `0`).
    - `--owner`, `--permission-id`, `--multi` (optional).

=== "REPL"

    ```
    FreezeBalanceV2 [OwnerAddress] frozen_balance [ResourceCode]
    ```

### Unfreeze balance v2 — `unfreeze-balance-v2` / `UnfreezeBalanceV2`

Begins unstaking a specified amount. The TRX becomes withdrawable after the network's unfreeze
waiting period (see `withdraw-expire-unfreeze`).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile unfreeze-balance-v2 \
      --amount 1000000 --resource 1
    ```

    - `--amount` (required, SUN), `--resource` (optional, default `0`).
    - `--owner`, `--permission-id`, `--multi` (optional).

=== "REPL"

    ```
    UnfreezeBalanceV2 [OwnerAddress] unfreezeBalance ResourceCode
    ```

### Withdraw expired unfreeze — `withdraw-expire-unfreeze` / `WithdrawExpireUnfreeze`

Withdraws TRX whose unfreeze waiting period has elapsed, returning it to the spendable balance.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile withdraw-expire-unfreeze
    ```

    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    WithdrawExpireUnfreeze [OwnerAddress]
    ```

### Cancel all unfreezes — `cancel-all-unfreeze-v2` / `CancelAllUnfreezeV2`

Cancels all pending v2 unstaking requests, returning that TRX to the staked state.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile cancel-all-unfreeze-v2
    ```

    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    CancelAllUnfreezeV2 [owner_address]
    ```

## Resource delegation

### Delegate resource — `delegate-resource` / `DelegateResource`

Lends staked bandwidth/energy to another account.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile delegate-resource \
      --amount 1000000 --resource 1 --receiver TXyz... --lock --lock-period 86400
    ```

    - `--amount` (required, SUN), `--resource` (required, `0`/`1`), `--receiver` (required).
    - `--lock` (optional flag) — lock the delegation; `--lock-period` (optional) sets the lock
      duration in blocks.
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    DelegateResource [OwnerAddress] balance ResourceCode ReceiverAddress [lock] [lockPeriod]
    ```

    `ResourceCode`: `0` BANDWIDTH, `1` ENERGY. `lock` is `true`/`false`.

### Undelegate resource — `undelegate-resource` / `UnDelegateResource`

Recalls previously delegated resources.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile undelegate-resource \
      --amount 1000000 --resource 1 --receiver TXyz...
    ```

    - `--amount` (required), `--resource` (required), `--receiver` (required).
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UnDelegateResource [OwnerAddress] balance ResourceCode ReceiverAddress
    ```

## Resource queries (no auth required)

### Account bandwidth — `get-account-net` / `GetAccountNet`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account-net --address TXyz...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetAccountNet Address
    ```

### Account resources — `get-account-resource` / `GetAccountResource`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account-resource --address TXyz...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetAccountResource Address
    ```

### Delegated resource — `get-delegated-resource(-v2)` / `GetDelegatedResource(V2)`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-delegated-resource \
      --from TFrom... --to TTo...
    java -jar build/libs/wallet-cli.jar --network nile get-delegated-resource-v2 \
      --from TFrom... --to TTo...
    ```

    - `--from` (required), `--to` (required).

=== "REPL"

    ```
    GetDelegatedResource   FromAddress ToAddress
    GetDelegatedResourceV2 FromAddress ToAddress
    ```

### Delegated resource account index — `get-delegated-resource-account-index(-v2)`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile \
      get-delegated-resource-account-index --address TXyz...
    java -jar build/libs/wallet-cli.jar --network nile \
      get-delegated-resource-account-index-v2 --address TXyz...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetDelegatedResourceAccountIndex   Address
    GetDelegatedResourceAccountIndexV2 Address
    ```

### Max delegatable size — `get-can-delegated-max-size` / `GetCanDelegatedMaxSize`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-can-delegated-max-size \
      --owner TXyz... --type 1
    ```

    - `--owner` (required), `--type` (required, `0` BANDWIDTH / `1` ENERGY).

=== "REPL"

    ```
    GetCanDelegatedMaxSize [OwnerAddress] type
    ```

    `type`: `0` BANDWIDTH, `1` ENERGY. With only `type`, the logged-in address is used.

### Available unfreeze count — `get-available-unfreeze-count` / `GetAvailableUnfreezeCount`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-available-unfreeze-count --address TXyz...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetAvailableUnfreezeCount [OwnerAddress]
    ```

### Withdrawable unfreeze amount — `get-can-withdraw-unfreeze-amount` / `GetCanWithdrawUnfreezeAmount`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-can-withdraw-unfreeze-amount \
      --address TXyz... --timestamp 1700000000000
    ```

    - `--address` (required), `--timestamp` (optional, ms; defaults to now).

=== "REPL"

    ```
    GetCanWithdrawUnfreezeAmount [OwnerAddress] timestamp
    ```

    `timestamp` (ms) is required. With only `timestamp`, the logged-in address is used.
