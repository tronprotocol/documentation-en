# Connect to TRON network
The TRON network is mainly divided into the Mainnet, Nile Testnet, Shasta Testnet and Private Network. Therefore, for the java-tron client, you can connect it to any TRON network by modifying the configuration items in the configuration file. Currently, among the testnets, the Shasta Testnet does not support node joining, while the Nile Testnet does.

You need to set the following configuration items to connect java-tron to one of the TRON networks:

* Network ID (`p2p.version`): Indicates the network you want to join. Relevant configuration item:
```
node {
  ...
  p2p {
    version = 11111
  }
  ...
}
```
In particular:
    * Mainnet: `version=11111`
    * Nile Testnet: `version = 201910292`
    * Private Network: Customize and set to other value

* Genesis Block: The settings of the genesis block must be consistent with those of other nodes in the network; otherwise, the connection to other nodes cannot be established. Relevant configuration item:
```
genesis.block = {
  # Reserve balance
  assets = [
    {
      accountName = "Zion"
      accountType = "AssetIssue"
      address = "TLLM21wteSPs4hKjbxgmH1L6poyMjeTbHm"
      balance = "99000000000000000"
    },
    {
      accountName = "Sun"
      accountType = "AssetIssue"
      address = "TXmVpin5vq5gdZsciyyjdZgKRUju4st1wM"
      balance = "0"
    },
    {
      accountName = "Blackhole"
      accountType = "AssetIssue"
      address = "TLsV52sRDL79HXGGm9yzwKibb6BeruhUzy"
      balance = "-9223372036854775808"
    }
  ]

  witnesses = [
    {
      address: THKJYuUmMKKARNf7s2VT51g5uPY6KEqnat,
      url = "http://GR1.com",
      voteCount = 100000026
    },
    {
      address: TVDmPWGYxgi5DNeW8hXrzrhY8Y6zgxPNg4,
      url = "http://GR2.com",
      voteCount = 100000025
    },
    {
      address: TWKZN1JJPFydd5rMgMCV5aZTSiwmoksSZv,
      url = "http://GR3.com",
      voteCount = 100000024
    },
    {
      address: TDarXEG2rAD57oa7JTK785Yb2Et32UzY32,
      url = "http://GR4.com",
      voteCount = 100000023
    },
    {
      address: TAmFfS4Tmm8yKeoqZN8x51ASwdQBdnVizt,
      url = "http://GR5.com",
      voteCount = 100000022
    },
    {
      address: TK6V5Pw2UWQWpySnZyCDZaAvu1y48oRgXN,
      url = "http://GR6.com",
      voteCount = 100000021
    },
    {
      address: TGqFJPFiEqdZx52ZR4QcKHz4Zr3QXA24VL,
      url = "http://GR7.com",
      voteCount = 100000020
    },
    {
      address: TC1ZCj9Ne3j5v3TLx5ZCDLD55MU9g3XqQW,
      url = "http://GR8.com",
      voteCount = 100000019
    },
    {
      address: TWm3id3mrQ42guf7c4oVpYExyTYnEGy3JL,
      url = "http://GR9.com",
      voteCount = 100000018
    },
    {
      address: TCvwc3FV3ssq2rD82rMmjhT4PVXYTsFcKV,
      url = "http://GR10.com",
      voteCount = 100000017
    },
    {
      address: TFuC2Qge4GxA2U9abKxk1pw3YZvGM5XRir,
      url = "http://GR11.com",
      voteCount = 100000016
    },
    {
      address: TNGoca1VHC6Y5Jd2B1VFpFEhizVk92Rz85,
      url = "http://GR12.com",
      voteCount = 100000015
    },
    {
      address: TLCjmH6SqGK8twZ9XrBDWpBbfyvEXihhNS,
      url = "http://GR13.com",
      voteCount = 100000014
    },
    {
      address: TEEzguTtCihbRPfjf1CvW8Euxz1kKuvtR9,
      url = "http://GR14.com",
      voteCount = 100000013
    },
    {
      address: TZHvwiw9cehbMxrtTbmAexm9oPo4eFFvLS,
      url = "http://GR15.com",
      voteCount = 100000012
    },
    {
      address: TGK6iAKgBmHeQyp5hn3imB71EDnFPkXiPR,
      url = "http://GR16.com",
      voteCount = 100000011
    },
    {
      address: TLaqfGrxZ3dykAFps7M2B4gETTX1yixPgN,
      url = "http://GR17.com",
      voteCount = 100000010
    },
    {
      address: TX3ZceVew6yLC5hWTXnjrUFtiFfUDGKGty,
      url = "http://GR18.com",
      voteCount = 100000009
    },
    {
      address: TYednHaV9zXpnPchSywVpnseQxY9Pxw4do,
      url = "http://GR19.com",
      voteCount = 100000008
    },
    {
      address: TCf5cqLffPccEY7hcsabiFnMfdipfyryvr,
      url = "http://GR20.com",
      voteCount = 100000007
    },
    {
      address: TAa14iLEKPAetX49mzaxZmH6saRxcX7dT5,
      url = "http://GR21.com",
      voteCount = 100000006
    },
    {
      address: TBYsHxDmFaRmfCF3jZNmgeJE8sDnTNKHbz,
      url = "http://GR22.com",
      voteCount = 100000005
    },
    {
      address: TEVAq8dmSQyTYK7uP1ZnZpa6MBVR83GsV6,
      url = "http://GR23.com",
      voteCount = 100000004
    },
    {
      address: TRKJzrZxN34YyB8aBqqPDt7g4fv6sieemz,
      url = "http://GR24.com",
      voteCount = 100000003
    },
    {
      address: TRMP6SKeFUt5NtMLzJv8kdpYuHRnEGjGfe,
      url = "http://GR25.com",
      voteCount = 100000002
    },
    {
      address: TDbNE1VajxjpgM5p7FyGNDASt3UVoFbiD3,
      url = "http://GR26.com",
      voteCount = 100000001
    },
    {
      address: TLTDZBcPoJ8tZ6TTEeEqEvwYFk2wgotSfD,
      url = "http://GR27.com",
      voteCount = 100000000
    }
  ]

  timestamp = "0" #2017-8-26 12:00:00

  parentHash = "0xe58f33f9baf9305dc6f82b9f1934ea8f0ade2defb951258d50167028c780351f"
}
```

## Node Discovery

### Enable and Disable
Node discovery is enabled or disabled through the configuration file, and it is usually enabled. The relevant configuration item is as follows:

```
node.discovery = {
  ...
  enable = true
  ...  
}
```

### Boot Nodes
java-tron uses the [Kademlia](https://en.wikipedia.org/wiki/Kademlia) protocol to discover other nodes. Node discovery requires boot nodes, with the help of which other nodes in the TRON network can be discovered. Boot nodes consist of two parts: one part is seed nodes, and the other part is configured active connection nodes. For details, see [Active Connection](#active-connection).

Seed nodes also consist of two parts:

- Configured seed.node:
```
seed.node = {
  # List of the seed nodes
  # Seed nodes are stable full nodes

  ip.list = [
    "3.225.171.164:18888",
    "52.8.46.215:18888",
    "3.79.71.167:18888",
    "108.128.110.16:18888",
    "18.133.82.227:18888",
    "35.180.81.133:18888",
    "13.210.151.5:18888",
    "18.231.27.82:18888",
    "3.12.212.122:18888",
    "52.24.128.7:18888",
    "15.207.144.3:18888",
    "3.39.38.55:18888",    
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
    #"[2a05:d014:1f2f:2600:1b15:921:d60b:4c60]:18888", // use this if support ipv6
    #"[2600:1f18:7260:f400:8947:ebf3:78a0:282b]:18888", // use this if support ipv6
  ]
}
```
If the network card supports IPv6, you can use the seed nodes in the IPv6 address format in the above list by removing the comment symbol `#`.
To obtain the latest seed.node, you can check the official [configuration file](https://github.com/tronprotocol/java-tron/blob/master/framework/src/main/resources/config.conf).

- Persistent nodes read from the database. Persistent nodes require enabling the node persistence service. If this service is enabled, the nodes in the [routing table](https://en.wikipedia.org/wiki/Kademlia#Fixed-size_routing_tables) will be written into the database by a scheduled task. When a node starts based on this database, it will read these nodes from the database and use them as seed nodes. Relevant configuration item:
```
node.discovery = {
  ...
  persist = true
  ... 
}
```

Node discovery is based on the UDP protocol, and the default bound port is 18888 (other ports can also be bound). Relevant configuration item:
```
node {
  ...
  listen.port = 18888
  ...
}
```

In some cases, node discovery does not need to be enabled (e.g., when running a local test node or deploying a test network with fixed nodes). At this time, you can disable node discovery by setting the configuration item to `node.discovery.enable = false`, or by closing the UDP 18888 port through the firewall.


## Node Connection

### Number of Node Connections
`node.maxConnections` indicates the maximum number of connections between the current node and other nodes, with a default value of 30. Setting a larger value allows the node to establish more connections, which improves the efficiency of joining the network and the efficiency of broadcasting. However, it also requires higher bandwidth for maintaining connections and leads to greater performance consumption. Therefore, please set this value according to actual conditions.  
```
node {
  ...
  maxConnections = 30
  ...
}
```

### Active Connection
The target nodes for active connection come from three parts:

- Configured active nodes (high priority): They do not depend on node discovery. Even if node discovery is not enabled, the current node will actively initiate connections to these nodes. Relevant configuration item:
```
node {
  ...
  active = [
    # Active establish connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
  ...
 }
```
- Connectable nodes obtained through node discovery (medium priority)
- DNS nodes (low priority): These are backup nodes obtained from the DNS tree. They require configuring treeUrls and are used only when the first three sources are insufficient (they are generally not used). Relevant configuration item (usually not configured):
```
dns {
  ...
  # dns urls to get nodes, url format tree://{pubkey}@{domain}, default empty
  treeUrls = [
    #"tree://AKMQMNAJJBL73LXWPXDI4I5ZWWIZ4AWO34DWQ636QOBBXNFXH3LQS@main.trondisco.net",
  ]
  ...
}
```
Compared with the traditional static seed node list, the DNS tree mechanism has advantages such as dynamic node update and resistance to attacks in terms of P2P network bootstrapping.

It can be seen that currently, the target nodes for active connection only come from two categories: one is the configured active nodes, and the other is the connectable nodes obtained through node discovery.

### Passive Connection
- Nodes configured in `node.passive`. When these nodes actively initiate a connection to the current node, the current node will accept the connection unconditionally.

```
node {
  ...
  passive = [
    # Passive accept connection in any case
    # Sample entries:
    # "ip:port",
    # "ip:port"
  ]
  ...
 }
```

- Other nodes: While a node is discovering other nodes, it will also be discovered by other nodes, and these nodes may also actively initiate connections to the current node.

Unlike node discovery (which is based on the UDP protocol), node connection is based on the TCP protocol. However, the port number bound for passive connection is the same as that bound for node discovery. If a node does not want to accept passive connections for security reasons, it can close the TCP 18888 port through the firewall. If a node disables passive connections, the entire network topology will be as shown in the figure below:

![image](https://raw.githubusercontent.com/tronprotocol/documentation-en/master/images/network_topology.png)

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


