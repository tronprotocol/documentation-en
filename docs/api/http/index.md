# HTTP API

!!! note
    Although TRON has avoided XSS by setting the Content-Type of HTTP APIs to application/json, there are a few APIs that don't have input validation. To better protect user data security, we recommend that you correctly encode any data from APIs before using it in any UI, especially when the parameter visible equals true. It is recommended that you refer to the following resources: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

Most HTTP APIs are accessed via the `wallet` path (default port `8090`). Some APIs also support the `walletsolidity` path (default port `8091`), which provides access to **confirmed on-chain data only**. Each API page indicates which paths it supports.

## API Categories

- [Accounts](accounts/validateaddress.md) - Account creation, query, and permission management
- [Transfers and Transactions](transfers/createtransaction.md) - TRX transfers and transaction broadcasting
- [Resources](resources/getaccountresource.md) - Energy, bandwidth, staking, and delegation
- [Query the Network](network/getnowblock.md) - Blocks, transactions, node info, and chain parameters
- [Smart Contracts](smart-contracts/getcontract.md) - Contract deployment, triggering, and queries
- [TRC-10 Token](trc10-token/getassetissuebyaccount.md) - TRC-10 asset issuance, transfer, and queries
- [Vote and Super Representative](voting/createwitness.md) - Witness management, voting, and rewards
- [Proposals](proposals/proposalcreate.md) - Network proposal creation and management
- [Pending Pool](pending-pool/gettransactionfrompending.md) - Pending transaction queries
