# Private Network
This document will guide you through setting up a basic TRON private network. This network will consist of one Super Representative (SR) node responsible for block production and one regular Fullnode used only for syncing block data and broadcasting transactions.

## Prerequisites

Before you begin, please ensure your development environment meets the following requirements:

- **Java Development Kit (JDK)**: You must have Oracle JDK 1.8 installed.
- **TRON Accounts**: You need to create at least two TRON network addresses in advance and securely store the addresses and their corresponding private keys. One address will serve as the initial SR node (Block Production), and the other will be a regular account.
- **Address Creation Tools**: You can use any of the following tools to generate and manage your TRON accounts:
    - [Wallet-cli](https://github.com/tronprotocol/wallet-cli): An official command-line wallet tool, suitable for server environments.
    - [TronLink](https://www.tronlink.org/): A multi-chain wallet that supports the TRON network, featuring a user-friendly graphical interface for easy address creation and management.
    - [TronWeb](https://tronweb.network/docu/docs/intro/): A JavaScript library for developers to interact with the TRON network and build dApps.
    - [Trident](https://github.com/tronprotocol/trident): A lightweight Java SDK designed to help developers easily and efficiently integrate TRON blockchain functionality into Java applications.


## Deployment Guide
The operational steps for deploying a private network node are fundamentally the same as deploying a Mainnet node. The primary difference lies in the node's configuration file. The most crucial part of setting up a private network is modifying the configuration items in this file to allow the nodes to form a private network, enabling network discovery, block synchronization, and transaction broadcasting.

1. Prepare Node Directories

     To keep configurations and data isolated, it is recommended to create separate deployment directories for each node.
     
      ```
      # Create the Super Representative (SR) node directory
      $ mkdir SR
      
      # Create the regular Fullnode directory
      $ mkdir FullNode
      ```

2. Get the `java-tron` Client

     `java-tron` is the official Java implementation of the TRON network.

    - Download the latest `FullNode.jar` from the `java-tron` [GitHub Releases page](https://github.com/tronprotocol/java-tron/releases).
    - Copy the downloaded `JAR` file into each of the two node directories:

         ```
         $ cp FullNode.jar ./SR
         $ cp FullNode.jar ./FullNode
         ```

3. Prepare Configuration Files

     - Download the official configuration file template ([config.conf](https://github.com/tronprotocol/java-tron/blob/develop/framework/src/main/resources/config.conf)) and change the `p2p.version` to any value other than **11111** or **20180622**.
     - Copy it into each node directory and rename the files for distinction.
        ```
        # Configuration file for the SR node
        $ cp private_net_config.conf ./SR/supernode.conf
      
        #  Configuration file for the regular Fullnode
        $ cp private_net_config.conf ./FullNode/fullnode.conf
        ```     

4. Modify Node Configurations

     This is the most critical step in setting up a private network. Please edit the `supernode.conf` and `fullnode.conf` files according to the instructions in the table below.

     | Config Item | SR Node (`supernode.conf`) | Fullnode (`fullnode.conf`) | Description |
      | :-------- | :-------- | :-------- | :-------- |
      | `localwitness`     | The private key| Please do not fill in data     | Generating blocks requires signing with a private key    |
      | `genesis.block.witnesses`	     | SR address     | The same as SR node's | Genesis block related configuration     |
      | `genesis.block.Assets`     | Preset TRX for specific accounts. Add the pre-prepared address to the end and specify its TRX balance as required    | The same as SR node's     | Genesis block related configuration     |
      | `p2p.version`     | any positive integer except for 11111     | the same as SR node's     | Only nodes of the same p2p version can shake hands successfully    |
      | `seed.node`     | Please do not fill in data     | Change the `seed.node` `ip.list` in the configuration file to the IP address and the port (`listen.port`) of the SR     | Enables fullnode to establish connection with SR node and synchronize data     |
      | `needSyncCheck`     | `false`     | `true`     | Set the first SR’s needSyncCheck to `false`, other SRs `true`     |
      | `node.discovery.enable`     | `true`     | `true`     | If it is `false`, the current node will not be discovered by other nodes    |
      |`block.proposalExpireTime`|`600000` |The same as SR node's |The default proposal effective time is 3 days: 259200000 (ms), if you want to quickly pass the proposal, you can set this item to a smaller value, such as 10 minutes, that is, 600000ms|
      |`block.maintenanceTimeInterval`|`300000`| The same as SR node's | The default maintenance time interval is 6 hours: 21600000 (ms), if you want to pass the proposal quickly, you can set this item to a smaller value, such as five minutes, that is, 300000ms.|
      |`committee.allowSameTokenName` |`1`|`1`| Allow same token name|
      |`committee.allowTvmTransferTrc10` | `1`|`1`|Allow tvm transfer TRC-10|
      
5. Adjust Network Ports (If Necessary)

     Modify the port numbers in the configuration files to be different for the SR and the Full Node. This step is only required when running multiple nodes on the same machine to avoid port conflicts. Otherwise, you can skip it.

     * `listen.port`: P2P listening port
     * `http port`: HTTP listening port
     * `rpc port`: RPC listening port
    
6. Start the Nodes

     The startup commands for the Super Representative (block-producing node) and the regular Full Node are slightly different.

     - Start the Super Representative (SR) Node:
     ```
     $ cd SR
     $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c supernode.conf
     ```
    
     - Start the regular Fullnode:
      ```
      $ cd FullNode
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  -c fullnode.conf
      # After starting, monitor the console logs to ensure the Full Node successfully connects to the SR node and begins syncing blocks.
      ```  
      
7. Advanced Operation: Modifying Dynamic Network Parameters

     Dynamic network parameters can be retrieved via the [getchainparameters API](https://developers.tron.network/reference/wallet-getchainparameters). The current Mainnet dynamic parameters and related proposals can be viewed on the TRONSCAN [Parameters & Proposals page](https://tronscan.org/#/sr/committee). If you want your private network's dynamic parameters to match the Mainnet's, you can use the[ dbfork tool](https://github.com/tronprotocol/tron-docker/blob/main/tools/toolkit/DBFork.md), which can capture the latest state of the Mainnet.
   
     After your private network is running, you may need to adjust certain network parameters (e.g., transaction fees, energy price). This can be achieved in two ways:

     - **Method 1: Set via Configuration File (For Initial Deployment)**
    
         Some dynamic parameters can be set directly in the configuration file. You can find a list of these parameters [here](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/core/Constant.java).
      
         Example: Add the following `committee` block to your `.conf` file to enable multi-signature and contract creation.
      
         ```
         committee = {
           allowCreationOfContracts = 1
           allowAdaptiveEnergy = 0
           allowMultiSign = 1
           allowDelegateResource = 1
           allowSameTokenName = 0
           allowTvmTransferTrc10 = 1
          }
         ```

     - **Method 2: Modify via On-Chain Proposals (For a Running Network)**

        This is the standard method for on-chain governance. Any SR, SR partner, or SR candidate has the right to create a proposal, but only Super Representatives (SRs) have the right to vote for its approval.
     
         - Create a Proposal: Any SR, SR partner, or SR candidate uses the [proposalcreate API](https://developers.tron.network/reference/proposalcreate), specifying the parameter to be modified by its ID and the new value. (List of parameter IDs).
         - Approve a Proposal: An SR uses the [proposalapprove API](https://developers.tron.network/reference/proposalapprove) to vote on the proposal. (Only 'approve' votes are supported; if an SR does not vote, it is considered a 'disapprove').
         - Related APIs:
             - Get all proposals: [listproposals](https://developers.tron.network/reference/wallet-listproposals)
             - Get a proposal by ID: [getproposalbyid](https://developers.tron.network/reference/getproposalbyid)

         **Example Code (using TronWeb):**
     
         The following code snippet demonstrates how to create a proposal to modify two network parameters and then vote on it. In [proposalcreate](https://developers.tron.network/reference/proposalcreate), dynamic parameters are represented by their IDs. The mapping between parameter IDs and names can be found [here](https://developers.tron.network/reference/wallet-getchainparameters).
     
      
         ```
         var TronWeb = require('tronweb');
         var tronWeb = new TronWeb({
             fullHost: 'http://localhost:16887',
             privateKey: 'privateKey'
         })

         var parametersForProposal1 = [{"key":9,"value":1},{"key":10,"value":1}];

         async function modifyChainParameters(parameters,proposalID){
      
             parameters.sort((a, b) => {
                     return a.key.toString() > b.key.toString() ? 1 : a.key.toString() === b.key.toString() ? 0 : -1;
                 })
            var unsignedProposal1Txn = await tronWeb.transactionBuilder.createProposal(parameters,"41D0B69631440F0A494BB51F7EEE68FF5C593C00F0");
             var signedProposal1Txn = await tronWeb.trx.sign(unsignedProposal1Txn);
             var receipt1 = await tronWeb.trx.sendRawTransaction(signedProposal1Txn);

             setTimeout(async function() {
                 console.log(receipt1)
                 console.log("Vote proposal 1 !")
                 var unsignedVoteP1Txn = await tronWeb.transactionBuilder.voteProposal(proposalID, true, tronWeb.defaultAddress.hex)
                 var signedVoteP1Txn = await tronWeb.trx.sign(unsignedVoteP1Txn);
                 var rtn1 = await tronWeb.trx.sendRawTransaction(signedVoteP1Txn);
             }, 4000)

         }

         modifyChainParameters(parametersForProposal1, 1) 
         ```

         Once the proposal is approved and the maintenance period has passed, the new network parameters will take effect. You can verify the changes using [listproposals](https://developers.tron.network/reference/wallet-listproposals) or [getchainparameters](https://developers.tron.network/reference/wallet-getchainparameters).
    
         It is important to note that dynamic parameters with interdependencies cannot be included in the same proposal. The correct approach is to separate them into different proposals and pay attention to their order of submission.
