# Smart Contracts

Deploy and interact with TVM smart contracts: deployment, state-changing calls, read-only
(constant) calls, energy estimation, and contract metadata management.

Common concepts:

- **`fee_limit`** — the maximum TRX (in SUN) you are willing to spend on energy for the call.
- **`method`** — a function selector/signature, e.g. `transfer(address,uint256)`.
- **`params` / `args`** — the call arguments. In the REPL, the `isHex` flag says whether `args` are
  already ABI-hex-encoded (`true`) or plain comma-separated values (`false`).
- **`value`** — TRX (SUN) to send with the call; **`token_value`/`token_id`** send a TRC-10 token
  with the call (`token_id` `#` or `TRXTOKEN` means none).
- **`consume_user_resource_percent`** — share (0–100) of resources paid by the caller.
- **`origin_energy_limit`** — max energy the contract owner will provide per call.

REPL transaction-building commands use an optional leading `[OwnerAddress]` for multi-sig; the
Standard CLI uses `--owner` + `--multi`. Deployment and state-changing calls require auth; constant
calls, energy estimation, and contract queries do not.

## Deploy a contract — `deploy-contract` / `DeployContract`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile deploy-contract \
      --name MyToken \
      --abi '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"}, ...]' \
      --bytecode 608060405234801561001057600080fd5b50... \
      --fee-limit 1000000000 \
      --consume-user-resource-percent 100 \
      --origin-energy-limit 10000000
    ```

    - Required: `--name`, `--abi` (JSON), `--bytecode` (hex), `--fee-limit` (SUN).
    - Optional: `--constructor`, `--params`, `--consume-user-resource-percent` (0–100),
      `--origin-energy-limit`, `--value`, `--token-value`, `--token-id`, `--library`,
      `--compiler-version`, `--owner`, `--multi`.
    - In JSON mode the response `data` includes the deployed `contract_address`.

=== "REPL"

    ```
    DeployContract [ownerAddress] contractName ABI byteCode constructor params isHex \
      fee_limit consume_user_resource_percent origin_energy_limit value token_value \
      token_id(e.g: TRXTOKEN, use # if don't provided) \
      <library:address,library:address,...> <lib_compiler_version(e.g:v5)>
    ```

    Use `#` for an empty `token_id`. The `<library...>` and `<lib_compiler_version>` arguments are
    optional and only needed when the bytecode references libraries.

## Call a contract (state-changing) — `trigger-contract` / `TriggerContract`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile trigger-contract \
      --contract TContract... \
      --method "transfer(address,uint256)" \
      --params "TRecipient...,1000000" \
      --fee-limit 100000000
    ```

    - Required: `--contract`, `--method`, `--fee-limit`.
    - Optional: `--params`, `--value`, `--token-value`, `--token-id`, `--owner`,
      `--permission-id`, `--multi`.

=== "REPL"

    ```
    TriggerContract [OwnerAddress] contractAddress method args isHex \
      fee_limit value token_value token_id(e.g: TRXTOKEN, use # if don't provided)
    ```

    Needs 8 parameters (or 9 with `OwnerAddress`).

To read the execution result of a state-changing call, look it up afterward with
`get-transaction-info-by-id` / `GetTransactionInfoById` (see [Queries](query.md)).

## Call a contract (read-only) — `trigger-constant-contract` / `TriggerConstantContract`

Executes a contract function locally without creating a transaction; returns the result. No gas is
spent.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile trigger-constant-contract \
      --contract TContract... \
      --method "balanceOf(address)" \
      --params "TAccount..."
    ```

    - Required: `--contract`, `--method`. Optional: `--params`, `--owner`.

=== "REPL"

    ```
    TriggerConstantContract ownerAddress(use # if you own) contractAddress method args isHex \
      [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]
    ```

    Needs 5 or 8 parameters. Use `#` for `ownerAddress` to use your own account.

## Estimate energy — `estimate-energy` / `EstimateEnergy`

Estimates the energy a contract call would consume.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile estimate-energy \
      --contract TContract... \
      --method "transfer(address,uint256)" \
      --params "TRecipient...,1000000"
    ```

    - Required: `--contract`, `--method`. Optional: `--params`, `--value`, `--token-value`,
      `--token-id`, `--owner`.

=== "REPL"

    ```
    EstimateEnergy ownerAddress(use # if you own) contractAddress method args isHex \
      [value token_value token_id(e.g: TRXTOKEN, use # if don't provided)]
    ```

    Needs 5 or 8 parameters.

## Predict a CREATE2 address — `Create2` (REPL only)

Computes the deterministic address a contract would deploy to via the CREATE2 opcode.

```
Create2 address code salt
```

- `address` — the deployer address, `code` — the contract bytecode, `salt` — the CREATE2 salt.

## Contract maintenance

### Update resource percent — `update-setting` / `UpdateSetting`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-setting \
      --contract TContract... --consume-user-resource-percent 50
    ```

    - `--contract` (required), `--consume-user-resource-percent` (required, 0–100).
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UpdateSetting [OwnerAddress] contractAddress consume_user_resource_percent
    ```

### Update energy limit — `update-energy-limit` / `UpdateEnergyLimit`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-energy-limit \
      --contract TContract... --origin-energy-limit 10000000
    ```

    - `--contract` (required), `--origin-energy-limit` (required).
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UpdateEnergyLimit [OwnerAddress] contractAddress origin_energy_limit
    ```

### Clear contract ABI — `clear-contract-abi` / `ClearContractABI`

Removes the ABI stored on-chain for a contract.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile clear-contract-abi --contract TContract...
    ```

    - `--contract` (required). `--owner`, `--multi` (optional).

=== "REPL"

    ```
    ClearContractABI [OwnerAddress] contractAddress
    ```

## Contract queries (no auth required)

### Get contract — `get-contract` / `GetContract`

Returns the contract's bytecode and ABI.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-contract --address TContract...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetContract contractAddress
    ```

### Get contract info — `get-contract-info` / `GetContractInfo`

Returns extended contract information (including runtime/code hash details).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-contract-info --address TContract...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetContractInfo contractAddress
    ```
