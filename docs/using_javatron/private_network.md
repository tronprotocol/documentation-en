# Private Network
To build a private chain, it is necessary to deploy at least one fullnode running by SR to produces blocks, and any number of fullnodes to synchronize blocks and broadcast transactions. Only one SR node and one fullnode are set up in this example. Before the deployment, please install the `Oracle JDK 1.8` first, and then you need to prepare at least two TRON network address and save the address and private key. You can use [wallet-cli](https://github.com/tronprotocol/wallet-cli) or [Tronlink](https://www.tronlink.org/) to create address.


## Deployment Guide
The process of building a node on private chain is the same as that on mainnet. The difference is the content of the node configuration file. The most important step to build a private chain is to modify the configuration items in the configuration file, so that the nodes can form a private network for node discovery, block synchronization and broadcast transactions.


1. Create deployment directory

    Create deployment directory, it is recommended to put the two fullnodes in different directories.
      ```
      $ mkdir SR
      $ mkdir FullNode
      ```

2. Obtain [FullNode.jar](https://github.com/tronprotocol/java-tron/releases)

    Obtain FullNode.jar, then put it into the SR and FullNode directories respectively.
     ```
     $ cp FullNode.jar ./SR
     $ cp FullNode.jar ./FullNode
     ```

3. Obtain the node's config file [private_net_config.conf](https://github.com/tronprotocol/tron-deployment/blob/master/private_net_config.conf)

    Obtain the node's config file private_net_config.conf, then put it into the SR and FullNode directories respectively, and modify the file names respectively to supernode.conf, fullnode.conf.
      ```
      $ cp private_net_config.conf ./SR/supernode.conf
      $ cp private_net_config.conf ./FullNode/fullnode.conf
      ```

4. Modify the configuration file of each node

    Please modify each configuration item of the node in turn according to the instructions in the following table:

    | Config Item | SR Fullnode | FullNode | Description |
    | :-------- | :-------- | :-------- | :-------- |
    | localwitness     | The private key of witness address     | Please do not fill in data     | Generating blocks requires signing with a private key    |
    | genesis.block.witnesses	     | Witness address     | The same as SR node's | Genesis block related configuration     |
    | genesis.block.Assets     | Preset TRX for specific accounts. Add the pre-prepared address to the end and specify its TRX balance as needed    | The same as SR node's     | Genesis block related configuration     |
    | p2p.version     | any positive integer except for 11111     | the same as SR node's     | Only nodes of the same p2p version can shake hands successfully    |
    | seed.node     | Please do not fill in data     | Change the seed.node ip.list in the configuration file to the IP address and the port (`listen.port`) of the SR     | Enables fullnode to establish connection with SR node and synchronize data     |
    | needSyncCheck     | false     | true     | Set the first SR’s needSyncCheck to false, other SRs true     |
    | node.discovery.enable     | true     | true     | If it is false, the current node will not be discovered by other nodes    |
    |block.proposalExpireTime|600000 |The same as SR node's |The default proposal effective time is 3 days: 259200000 (ms), if you want to quickly pass the proposal, you can set this item to a smaller value, such as 10 minutes, that is, 600000ms|
    |block.maintenanceTimeInterval|300000| The same as SR node's | The default maintenance time interval is 6 hours: 21600000 (ms), if you want to pass the proposal quickly, you can set this item to a smaller value, such as five minutes, that is, 300000ms.|
    |committee.allowSameTokenName |1|1| Allow same token name|
    |committee.allowTvmTransferTrc10 | 1|1|Allow tvm transfer TRC10|
    

5. Modify the port in the configuration file, and configure the SR and FullNode with different port numbers. **Note**, this step is only required if SR and FullNode are running on the same machine, otherwise, this step can be skipped.

    * `listen.port` ： p2p listen port
    * `http` port： Http listen port
    * `rpc` port： rpc listen port

6. Startup the node

    The fullnode that produces blocks has the different startup command with the fullnodes that do not produce blocks:

    * Fullnode that produces blocks
      ```
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  --witness  -c supernode.conf
      ```
    * Fullnode
      ```
      $ java -Xmx6g -XX:+HeapDumpOnOutOfMemoryError -jar FullNode.jar  -c fullnode.conf
      ```


7. Modify the dynamic parameters of the private chain

    Dynamic parameters can be obtained by [getchainparameters](https://developers.tron.network/reference/wallet-getchainparameters). The main network's current dynamic parameters and committee proposals related to them can be seen [here](https://tronscan.org/#/sr/committee), dynamic parameters are called network parameters here.
    
    If you want all the dynamic parameters of your private network to be the same with the main network, maybe [dbfork](https://github.com/tronprotocol/tron-docker/tree/main/tools/dbfork) which could capture the latest status of Mainnet is what you are interested in.
    
    If you want to modify part of dynamic parameters, there are two ways to choose from:

    * Configure File  
      Some dynamic parameters can be directly set through configure file. These dynamic parameters can be seen [here](https://github.com/tronprotocol/java-tron/blob/develop/common/src/main/java/org/tron/core/Constant.java).
      Below is an example of modifying dynamic parameters through configure file.
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
    
    * Proposal  
      Any witness(SR, SR partner, SR candidate) is entitled to create a proposal, SRs also have the right to vote for the proposal. A witness uses [proposalcreate](https://developers.tron.network/reference/proposalcreate) to create a proposal, and then SRs use [proposalapprove](https://developers.tron.network/reference/proposalapprove) to approve the proposal(Proposals only support voting for yes, super representatives do not vote means they do not agree with the proposal). Below is an code example of modifying two dynamic parameters through a committee proposal. In [proposalcreate](https://developers.tron.network/reference/proposalcreate), dynamic parameters are represented by numbers, the mapping between number and string name of dynamic parameters can be seen [here](https://developers.tron.network/reference/wallet-getchainparameters).
      ```
      var TronWeb = require('tronweb');
      var tronWeb = new TronWeb({
          fullHost: 'http://localhost:16887',
          privateKey: 'c741f5c0224020d7ccaf4617a33cc099ac13240f150cf35f496db5bfc7d220dc'
      })

      var parametersForProposal1 = [{"key":9,"value":1},{"key":10,"value":1}];

      async function modifyChainParameters(parameters,proposalID){
      
          parameters.sort((a, b) => {
                  return a.key.toString() > b.key.toString() ? 1 : a.key.toString() === b.key.toString() ? 0 : -1;
              })
          var unsignedProposal1Txn = await tronWeb.transactionBuilder.createProposal(parameters,"41D0B69631440F0A494BB51F7EEE68FF5C593C00F0")
          var signedProposal1Txn = await tronWeb.trx.sign(unsignedProposal1Txn);
          var receipt1 = await tronWeb.trx.sendRawTransaction(signedProposal1Txn);

          setTimeout(async function() {
              console.log(receipt1)
              console.log("Vote proposal 1 !")
              var unsignedVoteP1Txn = await tronWeb.transactionBuilder.voteProposal(proposalID, true, tronWeb.defaultAddress.hex)
              var signedVoteP1Txn = await tronWeb.trx.sign(unsignedVoteP1Txn);
              var rtn1 = await tronWeb.trx.sendRawTransaction(signedVoteP1Txn);
          }, 1000)

      }

      modifyChainParameters(parametersForProposal1, 1)
      ```
      After creating the proposal through the above code, you can check whether the proposal has been approved through [listproposals](https://developers.tron.network/reference/wallet-listproposals) interface. If the "state" in the return value of the interface is "APPROVED" When expiration time of the proposal has passed, it means that the proposal has been approved.  
      It should be noted that dynamic parameters with interdependent relationships cannot be included in one proposal, the correct approach is to separate them into different proposals and pay attention to order of them.
