# Private Network
To build a private chain, it is necessary to deploy at least one fullnode running by SR to produces blocks, and any number of fullnodes to synchronize blocks and broadcast transactions. Only one SR node and one fullnode are set up in this example. Before the deployment, please install the `Oracle JDK 1.8` first, and then you need to prepare at least two TRON network address and save the address and private key. You can use [wallet-cli](https://github.com/tronprotocol/wallet-cli) or [Tronlink](https://www.tronlink.org/) to create address.



# Deployment Guide
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

    In order to be the same as the main network environment, the dynamic parameters of the private chain need to be modified to be consistent with those of the main network. The modification of dynamic parameters can be done through proposals. The SR account can use [wallet-cli](https://github.com/tronprotocol/wallet-cli) or fullnode http API  [`wallet/proposalcreate`](https://developers.tron.network/reference/proposalcreate)to create proposals, [`wallet/proposalapprove`](https://developers.tron.network/reference/proposalapprove) to approve proposals. 
   
    The following are the dynamic parameters and values sorted out according to the proposals passed by the mainnet successively. SR can directly use the following commands to create proposals to complete the modification of all the dynamic parameters of the private chain. Due to the dependencies between some parameters, according to the current parameter values on the main network, the modification of all parameters of the private chain can be divided into two proposals. The first step, SR creates and votes the first proposal according to the following code:

    ```
    var TronWeb = require('tronweb');
    var tronWeb = new TronWeb({
        fullHost: 'http://localhost:16887',
        privateKey: 'c741f5c0224020d7ccaf4617a33cc099ac13240f150cf35f496db5bfc7d220dc'
    })

    // First proposal: "key":30 and "key":70 must be modified first
    var parametersForProposal1 = [{"key":9,"value":1},{"key":10,"value":1},{"key":11,"value":420},{"key":19,"value":90000000000},{"key":15,"value":1},{"key":18,"value":1},{"key":16,"value":1},{"key":20,"value":1},{"key":26,"value":1},{"key":30,"value":1},{"key":5,"value":16000000},{"key":31,"value":160000000},{"key":32,"value":1},{"key":39,"value":1},{"key":41,"value":1},{"key":3,"value":1000},{"key":47,"value":10000000000},{"key":49,"value":1},{"key":13,"value":80},{"key":7,"value":1000000},{"key":61,"value":600},{"key":63,"value":1},{"key":65,"value":1},{"key":66,"value":1},{"key":67,"value":1},{"key":68,"value":1000000},{"key":69,"value":1},{"key":70,"value":14},{"key":71,"value":1},{"key":76,"value":1}];
    var parametersForProposal2 = [{"key":47,"value":15000000000},{"key":59,"value":1},{"key":72,"value":1},{"key":73,"value":3000000000},{"key":74,"value":2000},{"key":75,"value":12000},{"key":77,"value":1},{"key":78,"value":864000}];

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
    After creating the proposal through the above code, you can query the proposal's effective time: "expiration_time" through the http://127.0.0.1:xxxx/wallet/listproposals interface. The timestamp is in milliseconds. After the effective time has passed, if the "state" in the return value of the interface is "APPROVED", it means that the proposal has been passed, and you can continue to the next step and create the second proposal. The sample code is as follows:

    ```
    modifyChainParameters(parametersForProposal2, 2)
    ```
    
    After the proposal takes effect, the dynamic parameters of the private chain will be consistent with the main network. You can query the chain parameters through the /wallet/getchainparameters API.