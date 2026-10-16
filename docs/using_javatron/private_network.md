# Private Network

This document will guide you through setting up a basic TRON private network. This network will consist of one Super Representative (SR) node responsible for block production and one regular FullNode used only for syncing block data and broadcasting transactions.

## Prerequisites

Before you begin, please ensure your development environment meets the following requirements:

- **Java Development Kit (JDK)**: On x86_64 architecture, JDK 8 (latest minor version recommended) must be installed; on arm64 architecture, JDK 17 must be installed.
- **TRON Accounts**: You need to create at least two TRON network addresses in advance and securely store the addresses and their corresponding private keys. One address will serve as the initial SR node (Block Production), and the other will be a regular account.
- **Address Creation Tools**: You can use any of the following tools to generate and manage your TRON accounts:
    - [wallet-cli](../clients/wallet-cli/index.md): The official command-line wallet, suitable for server environments. Available as an interactive Java client and a scriptable TypeScript client.
    - [TronLink](https://www.tronlink.org/): A multi-chain wallet that supports the TRON network, featuring a user-friendly graphical interface for easy address creation and management.
    - [TronWeb](https://tronweb.network/docu/docs/intro/): A JavaScript library for developers to interact with the TRON network and build dApps.
    - [Trident](https://github.com/tronprotocol/trident): A lightweight Java SDK designed to help developers easily and efficiently integrate TRON blockchain functionality into Java applications.


## Deployment Guide

The operational steps for deploying a private network node are fundamentally the same as deploying a Mainnet node. The primary difference lies in the node's configuration file. The most crucial part of setting up a private network is modifying the configuration items in this file to allow the nodes to form a private network, enabling network discovery, block synchronization, and transaction broadcasting.

1. Prepare Node Directories

     To keep configurations and data isolated, it is recommended to create separate deployment directories for each node.
     
      ```bash
      # Create the Super Representative (SR) node directory
      mkdir SR
      
      # Create the regular FullNode directory
      mkdir FullNode
      ```

2. Get the java-tron Client

    - Download the latest FullNode JAR for your system architecture—`FullNode-x64.jar` for x86-64 or `FullNode-aarch64.jar` for ARM64—from the [java-tron GitHub Releases](https://github.com/tronprotocol/java-tron/releases) page, and rename the downloaded file to `FullNode.jar`.
    - Copy the downloaded `JAR` file into each of the two node directories:

         ```bash
         cp FullNode.jar ./SR
         cp FullNode.jar ./FullNode
         ```

3. Prepare Configuration Files

     - Download the current [`framework/src/main/resources/config.conf`](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf).
     - Change `node.p2p.version` to a positive integer that is not used by a public network. The current public IDs are Mainnet `11111`, Nile `201910292`, and Shasta `1`.
     - Copy it into each node directory and rename the files for distinction.

        ```bash
        # Configuration file for the SR node
        cp private_net_config.conf ./SR/supernode.conf
      
        #  Configuration file for the regular Fullnode
        cp private_net_config.conf ./FullNode/fullnode.conf
        ```     

4. Modify Node Configurations

     This is the most critical step in setting up a private network. Please edit the `supernode.conf` and `fullnode.conf` files according to the instructions in the table below.

     | Config Item | SR Node (`supernode.conf`) | Fullnode (`fullnode.conf`) | Description |
      | :-------- | :-------- | :-------- | :-------- |
      | `localwitness`     | The private key of Super Representative (SR) address | Leave empty     | Generating blocks requires signing with a private key   |
      | `genesis.block.witnesses`	     | SR address(es)    | Same as SR configuration	 | Genesis block-related configuration    |
      | `genesis.block.assets`     | Preset TRX for specific accounts. Add the pre-prepared address to the end and specify its balance in SUN (`1 TRX = 1,000,000 SUN`; for example, `100000000` allocates 100 TRX)    | Same as SR configuration	   | Genesis block related configuration     |
      | `node.p2p.version`     | Any positive integer except `11111`, `201910292`, and `1`     | Same as SR configuration   | Only nodes with the same `node.p2p.version` can complete the P2P handshake    |
      | `seed.node.ip.list`     | Leave the list empty    | Add the SR node as `SR_IP:SR_P2P_PORT`, using the port configured by its `node.listen.port` setting   | Enables FullNode to establish a connection with the SR node for data synchronization     |
      | `node.fastForward` | Leave the list empty | Leave the list empty | Remove the fast-forward addresses included in the template. If relay peers are needed, use only relay peers within the private network. |
      | `block.needSyncCheck`     | `false`     | `true`     | Set `block.needSyncCheck` to `false` for the first SR and `true` for other SRs     |
      | `node.discovery.enable`     | `true`     | `true`     | If set to `false`, the current node will not be discovered by other nodes    |
      | `block.proposalExpireTime`|`600000` | Same as SR configuration	 | The default proposal expiration time is 3 days: 259200000 (ms). Because proposals must pass through at least one maintenanceTimeInterval to be approved, you should set both block.proposalExpireTime and block.maintenanceTimeInterval to smaller values if you want to speed up the proposal process in a private network.|
      | `block.maintenanceTimeInterval`|`300000`| Same as SR configuration	 | The default maintenance time interval is 6 hours: 21600000 (ms)|
      | `committee.allowSameTokenName` |`1`|`1`| If set to `1` (true), the creation of tokens with identical names is allowed |
      | `committee.allowTvmTransferTrc10` | `1`|`1`| If set to 1 (true), the TVM is allowed to execute transfers of TRC-10 tokens via smart contracts. |
      
5. Adjust Network Ports (If Necessary)

     Modify the port numbers in the configuration files to be different for the SR and the Full Node. This step is only required when running multiple nodes on the same machine to avoid port conflicts. Otherwise, you can skip it.

     * `node.listen.port`: P2P listening port
     * `node.http.fullNodePort`, `node.http.solidityPort`, and `node.http.PBFTPort`: HTTP listening ports
     * `node.rpc.port`, `node.rpc.solidityPort`, and `node.rpc.PBFTPort`: gRPC listening ports
     * `node.jsonrpc.httpFullNodePort`, `node.jsonrpc.httpSolidityPort`, and `node.jsonrpc.httpPBFTPort`: JSON-RPC listening ports when those services are enabled

     See the [Node Configuration port table](configuration.md#api-services-and-ports) for the corresponding enable switches and defaults.
    
6. Start the Nodes

     The startup commands for the Super Representative (block-producing node) and the regular Full Node are slightly different.

     - Start the Super Representative (SR) Node:

     ```bash
     cd SR
     java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c supernode.conf
     ```
    
     - Start the regular FullNode:

      ```bash
      cd FullNode
      java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  -c fullnode.conf
      # After starting, monitor the console logs to ensure the Full Node successfully connects to the SR node and begins syncing blocks.
      ```  
      
7. Advanced Operation: Modifying Network Parameters

     Network parameters can be retrieved via the [getchainparameters](../api/http/witness-and-governance/getchainparameters.md) API. The current Mainnet network parameters and related proposals can be viewed on the TRONSCAN [Parameters & Proposals page](https://tronscan.org/#/sr/committee).

     To deploy a private network from an existing Mainnet state using your own SR accounts, first obtain a database snapshot or synchronize a node to the desired height. Then use the [DBFork tool](https://github.com/tronprotocol/tron-docker/blob/main/tools/toolkit/DBFork.md) to modify the local database. By default (without `--retain-witnesses`), the tool replaces the witness records in the `witness` database and the active witness list in the `witness_schedule` database according to the `witnesses` settings in `fork.conf`. It also processes accounts in the `account` database according to the `accounts` settings: an account is created if the address does not exist, or the specified fields are updated if it does. Configuring an address under `witnesses` does not automatically create its account, so SR addresses that do not yet exist in the database must also be included under `accounts`. This allows those accounts to participate in block production when the SR nodes are started.
   
     After your private network is running, you may need to adjust certain network parameters (e.g., transaction fees, energy price). This can be achieved in two ways:

     - **Method 1: Set via Configuration File (For Initial Deployment)**
    
         Some network parameters can be set directly in the configuration file. For available configuration options and their defaults, see [`reference.conf`](https://github.com/tronprotocol/java-tron/blob/master/common/src/main/resources/reference.conf).
      
         **Example**: Add the following settings to the existing `committee` block in your `.conf` file to enable multi-signature and contract creation:
      
         ```properties
         committee = {
           allowCreationOfContracts = 1
           allowMultiSign = 1
         }
         ```

     - **Method 2: Modify via On-Chain Proposals (For a Running Network)**

        This is the standard method for on-chain governance. Any Super Representative (SR), SR Partner, or SR Candidate can create or approve a proposal, but only approvals from active SRs count toward the approval threshold.
     
         - Create a Proposal: Use the [proposalcreate](../api/http/witness-and-governance/proposalcreate.md) API, specifying the parameter to be modified by its ID and the new value. See the `ProposalType` mapping linked below for parameter IDs.
         - Approve a Proposal: Use the [proposalapprove](../api/http/witness-and-governance/proposalapprove.md) API to approve a proposal or withdraw an approval. When determining whether the proposal meets the approval threshold, only approvals from active SRs are counted; an SR that has not approved or has withdrawn approval does not increase the approval count.
         - Related APIs:
             - Get all proposals: [listproposals](../api/http/witness-and-governance/listproposals.md)
             - Get a proposal by ID: [getproposalbyid](../api/http/witness-and-governance/getproposalbyid.md)

         **Example Code (using TronWeb):**
     
         The following code snippet demonstrates how to create a proposal to modify two network parameters and then vote on it. In [proposalcreate](../api/http/witness-and-governance/proposalcreate.md), network parameters are represented by their IDs. The mapping between parameter IDs and names is defined in the java-tron source code's [`enum ProposalType`](https://github.com/tronprotocol/java-tron/blob/master/actuator/src/main/java/org/tron/core/utils/ProposalUtil.java) (the number in parentheses for each enum entry is the parameter ID).
     
      
         This example uses [TronWeb v6](https://tronweb.network/docu/docs/intro/#instantiation). Set `SR_PRIVATE_KEY` to the private key of the genesis SR account, which is already registered as a witness, and ensure it has enough balance or bandwidth for the transactions. The example assumes the default account permissions and no concurrent proposal submissions from this account. It waits for successful inclusion on the FullNode, then identifies the new proposal by its proposer and parameters instead of assuming an ID.

         ```javascript
         const { TronWeb } = require('tronweb');
         const tronWeb = new TronWeb({
             fullHost: 'http://localhost:8090',
             privateKey: process.env.SR_PRIVATE_KEY
         });
         const owner = tronWeb.defaultAddress.hex;
         const parameters = [{ key: 9, value: 1 }, { key: 10, value: 1 }];
         // Sort by stringified keys to match Protobuf map serialization.
         parameters.sort((a, b) => {
             const keyA = String(a.key);
             const keyB = String(b.key);
             return keyA < keyB ? -1 : keyA > keyB ? 1 : 0;
         });
         const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

         async function broadcastAndWait(unsignedTransaction) {
             const signed = await tronWeb.trx.sign(unsignedTransaction);
             const result = await tronWeb.trx.sendRawTransaction(signed);
             if (!result.result) {
                 throw new Error(`Broadcast failed: ${JSON.stringify(result)}`);
             }
             const deadline = Date.now() + 120000;
             while (Date.now() < deadline) {
                 const info = await tronWeb.fullNode.request(
                     'wallet/gettransactioninfobyid', { value: signed.txID }, 'post'
                 );
                 if (info.id === signed.txID && info.blockNumber !== undefined) {
                     // SUCESS is the protobuf enum name; the default value may be omitted.
                     const status = info.result ?? 'SUCESS';
                     if (status !== 'SUCESS') {
                         throw new Error(`Transaction ${signed.txID} failed: ${status}`);
                     }
                     return signed.txID;
                 }
                 await sleep(1000);
             }
             throw new Error(`Timed out waiting for ${signed.txID}; check it before retrying.`);
         }

         async function modifyChainParameters() {
             const previousIds = new Set(
                 (await tronWeb.trx.listProposals()).map((p) => p.proposal_id)
             );
             const createTxId = await broadcastAndWait(
                 await tronWeb.transactionBuilder.createProposal(parameters, owner)
             );
             const matches = (await tronWeb.trx.listProposals()).filter((p) =>
                 !previousIds.has(p.proposal_id) &&
                 p.proposer_address.toLowerCase() === owner.toLowerCase() &&
                 p.parameters.length === parameters.length &&
                 parameters.every((expected) => p.parameters.some((actual) =>
                     Number(actual.key) === expected.key && Number(actual.value) === expected.value
                 ))
             );
             if (matches.length !== 1) {
                 throw new Error(`Cannot uniquely identify the proposal from ${createTxId}; inspect listproposals.`);
             }
             const proposalID = matches[0].proposal_id;
             const voteTxId = await broadcastAndWait(
                 await tronWeb.transactionBuilder.voteProposal(proposalID, true, owner)
             );
             console.log({ proposalID, createTxId, voteTxId });
         }

         modifyChainParameters().catch((error) => {
             console.error(error);
             process.exitCode = 1;
         });
         ```

         Approvals do not apply the parameters immediately. At the maintenance boundary when the proposal has expired, java-tron checks approvals from the then-active SRs and applies the parameters only if the proposal passes. You can check the proposal status using [listproposals](../api/http/witness-and-governance/listproposals.md) and verify the current network parameter values using [getchainparameters](../api/http/witness-and-governance/getchainparameters.md).

         **Single-SR private networks:** The current implementation in [`ProposalCapsule.hasMostApprovals`](https://github.com/tronprotocol/java-tron/blob/master/chainbase/src/main/java/org/tron/core/capsule/ProposalCapsule.java) uses integer arithmetic: `approvalCount >= activeWitnessCount * 7 / 10`. With one active SR, the threshold is zero, so a pending proposal can pass at expiration without any approval votes.
    
         It is important to note that network parameters with interdependencies cannot be included in the same proposal. The correct approach is to separate them into different proposals and pay attention to their order of submission. For example, activate `ALLOW_TVM_SHANGHAI` before creating a proposal to enable parameter 95 (`ALLOW_TVM_PRAGUE`).
