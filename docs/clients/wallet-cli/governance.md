# Governance

TRON governance: registering and updating witnesses (Super Representative candidates), voting,
managing on-chain parameter proposals, brokerage, and reward withdrawal.

Voting power comes from staked TRX (TRON_POWER). REPL transaction-building commands use an optional
leading `[OwnerAddress]` for multi-sig; the Standard CLI uses `--owner` + `--multi`. State-changing
commands require auth; queries do not.

## Witnesses

### Create a witness — `create-witness` / `CreateWitness`

Registers the account as a witness (SR candidate).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile create-witness --url https://my-sr.example
    ```

    - `--url` (required). `--owner`, `--multi` (optional).

=== "REPL"

    ```
    CreateWitness [OwnerAddress] Url
    ```

### Update a witness — `update-witness` / `UpdateWitness`

Updates the witness's URL.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-witness --url https://my-sr.example
    ```

    - `--url` (required). `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UpdateWitness [OwnerAddress] Url
    ```

### List witnesses — `list-witnesses` / `ListWitnesses`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-witnesses
    ```

=== "REPL"

    ```
    ListWitnesses
    ```

### List current witnesses (paginated) — `GetPaginatedNowWitnessList` (REPL only)

```
GetPaginatedNowWitnessList offset limit
```

## Voting

### Vote for witnesses — `vote-witness` / `VoteWitness`

Casts votes across one or more witnesses. Each vote allocates part of your voting power; voting
replaces your previous votes.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile vote-witness \
      --votes "TWitnessA... 100 TWitnessB... 50"
    ```

    - `--votes` (required) — space-separated `address count` pairs.
    - `--owner`, `--permission-id`, `--multi` (optional).

=== "REPL"

    ```
    VoteWitness [OwnerAddress] Address0 Count0 ... AddressN CountN
    ```

## Rewards & brokerage

### Withdraw rewards — `withdraw-balance` / `WithdrawBalance`

Withdraws accumulated voting/witness rewards to the spendable balance.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile withdraw-balance
    ```

    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    WithdrawBalance [OwnerAddress]
    ```

### Query reward — `get-reward` / `GetReward`

Shows the currently claimable reward for an address.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-reward --address TXyz...
    ```

    - `--address` (required). No auth required.

=== "REPL"

    ```
    GetReward Address
    ```

### Query brokerage — `get-brokerage` / `GetBrokerage`

Shows a witness's brokerage percentage (the share of rewards the SR keeps).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-brokerage --address TWitness...
    ```

    - `--address` (required). No auth required.

=== "REPL"

    ```
    GetBrokerage Address
    ```

### Update brokerage — `update-brokerage` / `UpdateBrokerage`

Sets the witness's brokerage percentage (0–100).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-brokerage --brokerage 20
    ```

    - `--brokerage` (required, 0–100). `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UpdateBrokerage OwnerAddress BrokeragePercent
    ```

    In the REPL the owner address is required (it is the witness whose brokerage is being set).

## Proposals

Proposals change on-chain network parameters; they are created by SRs, approved by SRs, and take
effect when enough approvals are gathered. Each proposal is a set of `parameter_id value` pairs.

### Create a proposal — `create-proposal` / `CreateProposal`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile create-proposal \
      --parameters "9 1 18 1"
    ```

    - `--parameters` (required) — space-separated `id value` pairs.
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    CreateProposal [OwnerAddress] id0 value0 ... idN valueN
    ```

### Approve a proposal — `approve-proposal` / `ApproveProposal`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile approve-proposal --id 42 --approve true
    ```

    - `--id` (required), `--approve` (required, `true` to add approval / `false` to withdraw it).
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    ApproveProposal [OwnerAddress] id is_or_not_add_approval
    ```

    `is_or_not_add_approval`: `true` to add your approval, `false` to remove it.

### Delete a proposal — `delete-proposal` / `DeleteProposal`

Cancels a proposal (proposer only).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile delete-proposal --id 42
    ```

    - `--id` (required). `--owner`, `--multi` (optional).

=== "REPL"

    ```
    DeleteProposal [OwnerAddress] proposalId
    ```

### List proposals — `list-proposals` / `ListProposals`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-proposals
    ```

=== "REPL"

    ```
    ListProposals
    ```

### List proposals (paginated) — `list-proposals-paginated` / `ListProposalsPaginated`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-proposals-paginated --offset 0 --limit 20
    ```

    - `--offset` (required), `--limit` (required).

=== "REPL"

    ```
    ListProposalsPaginated offset limit
    ```

### Get a proposal — `get-proposal` / `GetProposal`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-proposal --id 42
    ```

    - `--id` (required).

=== "REPL"

    ```
    GetProposal proposalId
    ```
