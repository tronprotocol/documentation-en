# HTTP API

!!! note
    Although TRON has avoided XSS by setting the Content-Type of HTTP APIs to application/json, there are a few APIs that don't have input validation. To better protect user data security, we recommend that you correctly encode any data from APIs before using it in any UI, especially when the parameter visible equals true. It is recommended that you refer to the following resources: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

Most HTTP APIs are accessed via the `wallet` path (default port `8090`). Some APIs also support the `walletsolidity` path (default port `8091`), which provides access to **confirmed on-chain data only**. Each API page indicates which paths it supports.

## API Categories

- [Account Management](account-management/getaccount.md) - Account query, balance, and multi-signature verification
- [Assets and Tokens](assets-and-tokens/getassetissuebyid.md) - TRC-10 asset issuance, transfer, and queries
- [Block Operations](block-operations/getnowblock.md) - Block query by number, ID, and range
- [Network Information](network-information/getnodeinfo.md) - Node info, chain parameters, and pricing
- [Resource Management](resource-management/getaccountresource.md) - Energy, bandwidth, staking, and delegation
- [Smart Contracts](smart-contracts/getcontract.md) - Contract deployment, triggering, and queries
- [Transaction Operations](transaction-operations/gettransactionbyid.md) - Transaction query and pending pool
- [Wallet Operations](wallet-operations/createtransaction.md) - Account creation, transfers, and broadcasting
- [Witness and Governance](witness-and-governance/listwitnesses.md) - Witness management, voting, proposals, and rewards
