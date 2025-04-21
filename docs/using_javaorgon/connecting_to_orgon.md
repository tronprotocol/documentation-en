# Connect to TRON network

The TRON network is mainly divided into the main network, the Shasta test network, the Nile test network and the private network. Therefore, for the java-tron client software, it can be connected to any TRON network by modifying the configuration items in the configuration file. At present, the Shasta testnet does not support adding a new node, but the Nile testnet supports it.

You need to set the following configuration items to connect java-tron to one of the TRON networks:

* `node.p2p.version` : It is used to set the P2P network id. Only nodes with the same network id can shake hands successfully.
    * TRON mainnet: `node.p2p.version=11111`
    * Nile testnet: `node.p2p.version = 201910292`
    * Private network：set to other values
* `seed.node`: set seed node
* `genesis.block`: Genesis block settings. To join a network, please ensure that the settings of the genesis block are the same as those of other nodes in the network, otherwise you cannot join the network.



## Find peers
java-tron continuously attempts to connect to other nodes on the network until it has enough peers, at the same time, it will also accept connections from other nodes. java-tron finds peers using the discovery protocol. In the discovery protocol, nodes exchange connectivity details and then establish sessions and exchange TRON data. 

If you want java-tron node to do node discovery, you need to enable the node discovery service in the node configuration file first:

```
node.discovery = {
  enable = true
  ...
}
```
Then, for the new node that joins the TRON network, you can configure the `seed node` to make it easier for the current node to connect to the peer node, and then obtain the address information of other nodes through the peer node. Generally, the seed nodes are set as stable online fullnodes. For the TRON main network, community public nodes can be used as seed nodes, for example:

```
seed.node = {
  # List of the seed nodes
  # Seed nodes are stable full nodes

  ip.list = [
    "3.225.171.164:18888",
    "52.53.189.99:18888",
    "18.196.99.16:18888",
    "34.253.187.192:18888",
    "18.133.82.227:18888",
    "35.180.51.163:18888",
    "54.252.224.209:18888",
    "18.231.27.82:18888",
    "52.15.93.92:18888",
    "34.220.77.106:18888",
    "15.207.144.3:18888",
    "13.124.62.58:18888",    
    "54.151.226.240:18888",
    "35.174.93.198:18888",
    "18.210.241.149:18888",
    "54.177.115.127:18888",
    "54.254.131.82:18888",
    "18.167.171.167:18888",
    "54.167.11.177:18888",
    "35.74.7.196:18888",
    "52.196.244.176:18888",
    "54.248.129.19:18888",
    "43.198.142.160:18888",
    "3.0.214.7:18888",
    "54.153.59.116:18888",
    "54.153.94.160:18888",
    "54.82.161.39:18888",
    "54.179.207.68:18888",
    "18.142.82.44:18888",
    "18.163.230.203:18888"
  ]
}

```

There are scenarios where disabling the discovery process is useful, for example for running a local test node or an experimental test network with known, fixed nodes. This can be configured by `node.discovery.enable = false` to close the node discovery process.

## Peers limit
`node.maxActiveNodes` indicates the maximum number of connections between the node and other nodes, the default value is 30. Setting a larger value can enable nodes to establish more connections, join the network more efficiently, and broadcast more efficiently. However, the bandwidth required to maintain the connection is also higher and the performance consumption is higher. Therefore, please set it according to the actual situation.

```
node {
    maxActiveNodes = 30
}

```

## Active and passive connections
java-tron supports setting its actively connected nodes `node.active` as well as passively connected nodes `node.passive`. Configuring `node.active` and `node.passive` can greatly help improve the stability of the network connection of the node.

When java-tron starts, it will actively establish a connection with the peer node in `node.active`.

```
node {
  active = [
    # Active establish connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
 }
```

When a node in `node.passive` actively establishes a connection with the current node, the current node will accept it unconditionally.

```
node {
  passive = [
    # Passive accept connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
 }
```

## Log and network connection verification
The java-tron node log is `/logs/tron.log` in the java-tron installation directory. Under the java-tron installation directory, you can use the following commands to view the latest log of the node and check the block synchronization status of the node:

```
$ tail -f /logs/tron.log/
```

You will see the below block synchronization logs if java-tron is running as expected. 

```
15:41:48.033 INFO  [nioEventLoopGroup-6-2] [DB](Manager.java:1208) pushBlock block number:76, cost/txs:13/0 false
15:41:48.033 INFO  [nioEventLoopGroup-6-2] [net](TronNetDelegate.java:255) Success process block Num:76,ID:000000000000004c9e3899ee9952a7f0d9e4f692c7070a48390e6fea8099432f.
```
For the super representative's fullnode, you will see the following producing blocks log:

```
02:31:33.008 INFO  [DPosMiner] [DB](Manager.java:1383) Generate block 79336 begin
02:31:33.059 INFO  [DPosMiner] [DB](SnapshotManager.java:315) flush cost:51, create checkpoint cost:49, refresh cost:2
02:31:33.060 INFO  [DPosMiner] [DB](Manager.java:1492) Generate block 79336 success, trxs:0, pendingCount: 0, rePushCount: 0, postponedCount: 0
```
If no error messages are reported in the node logs, means everything is fine. You can also send an http request to check whether the node has been started, and to view the status of the node: including the node configuration information, the information about the machine where the node is located, the connection status of the node peers, etc.

```
$ curl http://127.0.0.1:16887/wallet/getnodeinfo
```

Returns：

```
{
    "activeConnectCount": 3,
    "beginSyncNum": 42518346,
    "block": "Num:42518365,ID:000000000288c75d1967232f1efe606ff90b9dd76660d7de8cc091849be6bf10",
    "cheatWitnessInfoMap": {
        ...
    },
    "configNodeInfo": {
        ...
        "codeVersion": "4.5.1",
        "dbVersion": 2,
        "discoverEnable": true,
        "listenPort": 18888,
        ...
    },
    "currentConnectCount": 18,
    "machineInfo": {
        ...
    },
    "passiveConnectCount": 15,
    "peerList": [
        ...
    ],
    "solidityBlock": "Num:42518347,ID:000000000288c74b723398aef104c585bad1c7cbade7793c5551466bd916feee",
    "totalFlow": 8735314
}
```
In order for users to interact with the TRON network, the java-tron node must be running and in a normal state of synchronization. Whether the node is synchronized with other nodes in the network, you can query the current block height in Tronscan and compare it with the result of `/wallet/getnowblock` queried from the local java-tron node. If they are equal, it means that the synchronization status of the local node is normal.

## Connection problems
There are occasions when java-tron simply fails to connect to peers. The common reasons for this are:

* Local time might be incorrect. An accurate clock is required to participate in the TRON network. The local clock can be resynchronized using commands such as `sudo ntpdate -s time.nist.gov`.
* Some firewall configurations can prohibit UDP traffic. But the node discovery service is based on the UDP protocol, so you can make it possible to let the node connect to the network by configuring [`node.active`](#active-and-passive-connections) in the case of node discovery invalid.
* By configuring [`node.passive`](#active-and-passive-connections) to accept active connections from trusted nodes.
* The Shasta testnet does not currently support nodes joining the network. If you need to run nodes to join the public testnet, you can choose the Nile testnet.

## Connect to private network

It is often useful for developers to connect to private test networks rather than public testnets or TRON mainnet. Because the private chain not only has no requirements for machine configuration, but also in the sandbox environment of the private chain network, it is easier to test various functions, and it gives freedom to break things without real-world consequences. 

The private chain network needs to configure the configuration item `node.p2p.version` in the [private chain configuration file](https://github.com/tronprotocol/tron-deployment/blob/master/private_net_config.conf) to a value which is not used by any other existing public network (TRON mainnet, testnet). For detailed instructions on private chain construction, please refer to [Private Chain Network](private_network.md).


